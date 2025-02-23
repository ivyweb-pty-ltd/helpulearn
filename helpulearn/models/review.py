from odoo import fields, models, api


class HelpULearnReview(models.Model):
    """This records each time a unit is reviewed. Should record state (how well you do before session) and after session"""
    _name = 'helpulearn.review'
    _description = 'Records review actions'

    unit_id = fields.Many2one('helpulearn.unit', 'Unit', related='bit_id.unit_id')
    bit_id = fields.Many2one('helpulearn.bit', 'Bit')
    review_date = fields.Date('Date', default=fields.Date.today, required=True)
    review_duration = fields.Float('Review Duration', default=1)
    state_before = fields.Float('State Before')
    state_after = fields.Float('State After')
