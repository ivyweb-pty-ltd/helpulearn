from odoo import fields, models, api
from datetime import timedelta
import math


class HelpULearnBit(models.Model):
    _name = 'helpulearn.bit'
    _description = 'Describes a bit of information that can be used to create a learning objective'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'next_review,sequence'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char('Name')
    description = fields.Text('Description')
    content = fields.Html('Content')
    unit_id = fields.Many2one('helpulearn.unit', 'Unit', search="_search_unit_id")
    unit_type_id = fields.Many2one('helpulearn.unit_type', 'Unit Type', related='unit_id.unit_type_id')
    review_ids = fields.One2many('helpulearn.review', 'bit_id', 'Reviews', recursive=True)
    state = fields.Selection(
        [('new', 'New'), ('learning', 'Learning'), ('reviewing', 'Reviewing'), ('mastered', 'Mastered'),
         ('archived', 'Archived')], 'State', default='new', tracking=True
    )
    next_review = fields.Date('Next Review Date', compute="_calculate_review_agg", store=True, readonly=False)
    manual_review = fields.Date(
        'Manual Review Date')  # TODO: The manual review date that the student want to review overriding normal review.
    current_state = fields.Float('Current State',
                                 compute="_calculate_current_state",
                                 store=True, recursive=True)  # TODO: formula to calculate estimated retention
    last_review = fields.Date('Last Review Date',
                              compute='_last_review',
                              store=True)  # TODO: Returns the last date this work has been reviewed
    current_decay_rate = fields.Float('Decay Rate',default=0.035)  # TODO: The Decay rate adjusted on each revision
    current_alpha = fields.Float('Alpha',
                                 default=0.5)  # TODO: How much the decay rate will be adjusted on each revision
    target_date = fields.Date('Target Date')  # TODO: The date the student wants to have this information mastered
    target_state = fields.Float('Target State',
                                default=0.8)  # TODO: The state the student wants to have this information mastered

    number_of_reviews = fields.Integer('Number of Reviews', compute='_calculate_number_of_reviews', store=True)

    @api.model
    def cron_update_current_state(self):
        bits = self.search([])
        for bit in bits:
            bit._last_review()
            bit._calculate_number_of_reviews()
            bit._calculate_state()
            bit._calculate_current_decay_rate()
            bit._calculate_current_state()
            bit._calculate_review_agg()

    def _search_subunit_ids(self, unit_name):
        print('Unit Name to search', unit_name)
        return ('unit_id', '=', unit_name)

    def _search_unit_id(self, operator, value):
        # Search recursively including all the children of the unit
        """Search for unit_id based on the name of the unit"""
        unit_ids = self.env['helpulearn.unit'].search([('name', operator, value)])
        all_unit_ids = unit_ids._get_all_child_unit_ids()
        return [('unit_id', 'in', all_unit_ids)]

    @api.depends('review_ids')
    def _calculate_state(self):
        """Calculate the state of the bit based on the reviews."""
        for bit in self:
            if len(bit.review_ids) == 0:
                bit.state = 'new'
                continue
            elif bit.state == 'archived':
                continue
            else:
                last_review = bit.review_ids.search([('bit_id', '=', bit.id)], order='review_date desc', limit=1)
                bit.state = last_review.state

    @api.depends('review_ids', 'review_ids.retention_after', 'review_ids.review_date')
    def _calculate_current_state(self):
        """Calculate the weighted average of the retention after."""
        # TODO: Calculate the estimated retention rather than the weighted average based on the current date.
        for bit in self:
            if len(bit.review_ids) == 0:
                bit.current_state = 0
                continue
            total_weight = 0
            total_retention = 0
            review_ids = bit.review_ids.search([('bit_id', '=', bit._origin.id), ('state', '=', 'reviewing')],
                                               order='review_date asc')
            # Weight is the length between the reviews
            if review_ids and len(review_ids) > 1:
                # Calculate the weighted retention based on percentage after review and the time to review.
                for i in range(1, len(review_ids)):
                    weight = (review_ids[i].review_date - review_ids[i - 1].review_date).days
                    total_weight += weight
                    total_retention += review_ids[i].retention_after * weight
            elif len(review_ids) == 1:
                total_retention = review_ids[0].retention_after
                total_weight = 1
            else:
                total_retention = 0
                total_weight = 1
            if total_weight == 0:
                total_weight = 1
            bit.current_state = total_retention / total_weight

    @api.depends('review_ids')
    def _calculate_number_of_reviews(self):
        """Calculate the number of reviews."""
        for bit in self:
            bit.number_of_reviews = bit.review_ids.search_count(
                [('bit_id', '=', bit._origin.id), ('state', '=', 'reviewing')])

    @api.depends('review_ids')
    def _last_review(self):
        """Calculate the last review date."""
        for bit in self:
            if len(bit.review_ids) == 0:
                bit.last_review = False
                continue
            last_review = bit.review_ids[0].review_date
            for review in bit.review_ids:
                if last_review < review.review_date:
                    last_review = review.review_date
            bit.last_review = last_review

    def _set_manual_review(self):
        """Set the manual review date."""
        for bit in self:
            bit.manual_review = bit.next_review

    @api.depends('review_ids', 'state', 'manual_review', 'review_ids.state')
    def _calculate_review_agg(self):
        for bit in self:

            if bit.manual_review and (not bit.last_review or bit.manual_review >= bit.last_review):
                bit.next_review = bit.manual_review
            elif bit.state == 'new' and not bit.next_review:
                bit.next_review = fields.Date.today()
            elif bit.state == 'archived':
                bit.next_review = False
            elif bit.state == 'learning' and bit.last_review:
                bit.next_review = bit.last_review + timedelta(days=1)
            elif (bit.state == 'reviewing' or bit.state == 'mastered') and bit.last_review:
                current_percent = bit.current_state
                if current_percent <= bit.target_state:
                    factor = current_percent / bit.target_state
                else:
                    factor = 2 - (1 - current_percent) / (1 - bit.target_state)
                bit.next_review = bit.last_review + max(timedelta(days=1),
                                                        timedelta(days=2 ** (bit.number_of_reviews - 1)) * factor)

    @api.depends('review_ids', 'review_ids.retention_after', 'review_ids.review_date')
    def _calculate_current_decay_rate(self):
        """Estimate the current decay rate based on past reviews and forgetting curve fitting."""
        for bit in self:
            review_ids = bit.review_ids.filtered(lambda r: r.state == 'reviewing')

            if not review_ids:
                bit.current_decay_rate = 0.035  # Default starting decay rate if no reviews
                continue

            total_decay = 0
            decay_count = 0

            for review in review_ids:
                days_since_review = (fields.Datetime.now() - review.review_date).days
                if days_since_review <= 0:
                    continue  # Skip future reviews or reviews today

                retention = review.retention_after  # Convert to 0–1 scale

                if retention <= 0 or retention >= 1:
                    continue  # Skip impossible values

                k_estimated = -math.log(retention) / days_since_review

                total_decay += k_estimated
                decay_count += 1

            if decay_count == 0:
                bit.current_decay_rate = 0.035  # Safe fallback
            else:
                estimated_decay = total_decay / decay_count
                # Clamp decay rate between 0.00012 and 0.1
                bit.current_decay_rate = min(max(estimated_decay, 0.00012), 0.1)

# TODO: Add a method to specify question and manage questions to be asked or tasks to be accomplished in each review
# calculate based on target date and reviews to target date
# TODO: Move bits to units same concept. Bits rollup into units anyway.
# TODO: Set multiple targets with Units/bits that need to be completed by that target
