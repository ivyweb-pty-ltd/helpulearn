from odoo import fields, models, api


class TaxonomyComponent(models.Model):
    _name = 'helpulearn.taxonomy.component'
    _description = 'Component of a taxonomy'

    taxonomy_id = fields.Many2one('helpulearn.taxonomy', 'Taxonomy') # The Parent taxonomy
    contribution = fields.Float('Contribution') # The percentage that the taxonomy contributes
    contributing_taxonomy_id = fields.Many2one('helpulearn.taxonomy', 'Contributing Taxonomy') # The child taxonomy.