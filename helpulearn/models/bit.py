from odoo import fields, models, api
from datetime import timedelta


class HelpULearnBit(models.Model):
    _name = 'helpulearn.bit'
    _description = 'Describes a bit of information that can be used to create a learning objective'

    name = fields.Char('Name')
    description = fields.Text('Description')
    content = fields.Html('Content')
    unit_id = fields.Many2one('helpulearn.unit','Unit')
    unit_type_id = fields.Many2one('helpulearn.unit_type','Unit Type', related='unit_id.unit_type_id')
    review_ids = fields.One2many('helpulearn.review', 'bit_id', 'Reviews')

    next_review = fields.Date('Next Review Date')
    current_state = fields.Float('Current State') #TODO: formula to calculat eestimated retention
    last_review = fields.Date('Last Review Date',compute='_calculate_review_agg') #TODO: Returns the last date this work has been reviewed
    current_decay_rate = fields.Float('Decay Rate') #TODO: The Decay rate adjusted on each revision
    current_alpha = fields.Float('Alpha',default=0.5) #TODO: How much the decay rate will be adjusted on each revision
    target_date = fields.Date('Target Date') #TODO: The date the student wants to have this information mastered
    target_state = fields.Float('Target State', default=0.8) #TODO: The state the student wants to have this information mastered

    number_of_reviews = fields.Integer('Number of Reviews', compute='_calculate_review_agg')

    @api.depends('review_ids')
    def _calculate_review_agg(self):
        for bit in self:
            bit.number_of_reviews = len(bit.review_ids)
            if bit.number_of_reviews == 0:
                bit.last_review = False
                bit.next_review = False
                continue
            bit.last_review = max(bit.review_ids.mapped('review_date'))
            bit.next_review = bit.last_review + timedelta(days=2 ** (bit.number_of_reviews - 1))



