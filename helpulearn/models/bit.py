from odoo import fields, models, api
from datetime import timedelta
import math


class HelpULearnBit(models.Model):
    _name = 'helpulearn.bit'
    _description = 'Bit of information'
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
    next_review = fields.Date('Next Review Date', compute="_calculate_review_agg", store=True, readonly=False,
                              recursive=True)
    manual_review = fields.Date(
        'Manual Review Date')  # TODO: The manual review date that the student want to review overriding normal review.
    current_state = fields.Float('Current State',
                                 compute="_calculate_current_state",
                                 store=True, recursive=True)  # TODO: formula to calculate estimated retention
    last_review = fields.Date('Last Review Date',
                              compute='_last_review',
                              store=True)  # TODO: Returns the last date this work has been reviewed
    current_decay_rate = fields.Float('Decay Rate', default=0.223,
                                      compute="_calculate_current_decay_rate")  # TODO: The Decay rate adjusted on each revision
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

    @api.depends('review_ids', 'review_ids.retention_after', 'review_ids.review_date', 'current_decay_rate')
    def _calculate_current_state(self):
        """Estimate current retention based on the last review's retention and decay."""
        for bit in self:
            review_ids = bit.review_ids.filtered(lambda r: r.state == 'reviewing')

            if not review_ids:
                bit.current_state = 0
                continue

            # Find the most recent review
            latest_review = review_ids.sorted(key=lambda r: r.review_date)[-1]

            days_since_review = (fields.Date.today() - latest_review.review_date).days
            if days_since_review < 0:
                days_since_review = 0  # Safety for future-dated reviews

            decay_rate = bit.current_decay_rate or 0.223  # Fallback decay rate if missing

            # Starting point is retention_after immediately after review
            starting_retention = latest_review.retention_after

            # Apply forgetting curve decay
            retention_now = starting_retention * math.exp(-decay_rate * days_since_review)

            # Convert back to percentage scale and clamp between 0–100%
            bit.current_state = max(0.0, min(1.0, retention_now))

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

    @api.depends('review_ids', 'state', 'manual_review', 'review_ids.state', 'review_ids.review_date')
    def _calculate_review_agg(self):
        for bit in self:

            if bit.manual_review and (not bit.last_review or bit.manual_review > bit.last_review):
                bit.next_review = bit.manual_review
            elif bit.state == 'new' and not bit.next_review:
                bit.next_review = fields.Date.today()
            elif bit.state == 'archived':
                bit.next_review = False
            elif bit.state == 'learning' and bit.last_review:
                bit.next_review = bit.last_review + timedelta(days=1)
            elif (bit.state == 'reviewing' or bit.state == 'mastered') and bit.last_review:
                decay_rate = bit.current_decay_rate or 0.035
                target_state = bit.target_state or 0.8

                if decay_rate <= 0:
                    decay_rate = 0.035
                if target_state <= 0 or target_state >= 1:
                    target_state = 0.8

                # Get the latest review
                reviews = \
                bit.review_ids.filtered(lambda r: r.state == 'reviewing' or r.state == 'mastered').sorted(key=lambda r: r.review_date)
                if reviews:
                    last_review = reviews[-1]
                else:
                    continue

                start_retention = last_review and last_review.retention_after or 1.0  # retention right after last review

                if start_retention <= 0 or start_retention > 1:
                    start_retention = 1.0  # fallback safety

                try:
                    ratio = target_state / start_retention
                    if ratio > 1:
                        days_to_target = 1  # Already below target, review tomorrow
                    else:
                        days_to_target = -math.log(ratio) / decay_rate
                        days_to_target = max(1, round(days_to_target))
                except (ValueError, ZeroDivisionError):
                    days_to_target = 1

                bit.next_review = last_review.review_date + timedelta(days=days_to_target)

    @api.depends('review_ids', 'review_ids.retention_after', 'review_ids.review_date')
    def _calculate_current_decay_rate(self):
        """Estimate the decay rate based on sequential review prediction, adjusting decay rate after each review."""
        DEFAULT_DECAY_RATE = 0.223  # Start fast forgetting for new bits

        for bit in self:
            review_ids = bit.review_ids.filtered(lambda r: r.state == 'reviewing' or r.state == 'mastered')

            if not review_ids:
                bit.current_decay_rate = DEFAULT_DECAY_RATE
                continue

            review_ids = review_ids.sorted(key=lambda r: r.review_date)

            decay_rate = DEFAULT_DECAY_RATE  # Start fresh for this Bit
            previous_review = None

            for review in review_ids:
                if previous_review:
                    days_between = (review.review_date - previous_review.review_date).days
                    if days_between <= 0:
                        days_between = 1  # avoid divide by zero

                    previous_retention = previous_review.retention_after
                    current_retention = review.retention_after

                    if previous_retention <= 0 or previous_retention > 1 or current_retention <= 0 or current_retention > 1:
                        previous_review = review
                        continue

                    # Predict expected retention using current decay_rate (before adjustment)
                    expected_retention = previous_retention * math.exp(-decay_rate * days_between)

                    if current_retention >= expected_retention:
                        decay_rate = decay_rate * 0.5
                    else:
                        # Weaker memory than expected → increase decay rate
                        decay_rate = decay_rate * 1.1

                    # Update decay rate immediately after each review
                    decay_rate = min(max(decay_rate, 0.00012), 0.4)

                previous_review = review

            # After all reviews processed, set final decay rate
            bit.current_decay_rate = decay_rate

# TODO: Add a method to specify question and manage questions to be asked or tasks to be accomplished in each review
# calculate based on target date and reviews to target date
# TODO: Move bits to units same concept. Bits rollup into units anyway.
# TODO: Set multiple targets with Units/bits that need to be completed by that target
