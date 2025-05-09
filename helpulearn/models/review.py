from reportlab.platypus.tableofcontents import defaultTableStyle

from odoo import fields, models, api


class HelpULearnReview(models.Model):
    """This records each time a unit is reviewed. Should record state (how well you do before session) and after session"""
    _name = 'helpulearn.review'
    _description = 'Records review actions'

    unit_id = fields.Many2one('helpulearn.unit', 'Unit', related='bit_id.unit_id')
    bit_id = fields.Many2one('helpulearn.bit', 'Bit')
    review_date = fields.Date('Date', default=fields.Date.today, required=True)
    review_duration = fields.Float('Review Duration', default=1)
    retention_before = fields.Float('Retantion Before')
    retention_after = fields.Float('Retention After')
    state = fields.Selection([('new', 'New'), ('learning', 'Learning'), ('reviewing', 'Reviewing'), ('mastered', 'Mastered'), ('archived', 'Archived')], 'Status', default='new', tracking=True)

    @api.model
    def default_get(self, fields_list):
        defaults = super(HelpULearnReview, self).default_get(fields_list)

        bit_id = self.env.context.get('default_bit_id')
        if bit_id:
            bit = self.env['helpulearn.bit'].browse(bit_id)
            if bit.exists() and bit.state:
                defaults['state']=bit.state

        return defaults

#TODO: Write code to calculate retention before

