from . import ModelName


class HelpULearn_Taxonomy(models.Model):
    _name = 'helpulearn.taxonomy'
    _description = 'Blooms Revised Taxonomy'

    name = fields.Char('name')
    knowledge_dimension_id = fields.Many2one('Knowledge Dimension', 'helpulearn.knowledge.dimension',
                                             related='knowledge_id.knowledge_dimension_id')
    knowledge_type_id = fields.Many2one('Knowledge type', 'helpulearn.knowledge.subtype')
    cognitive_dimension_id = fields.Many2one('Cognitive Dimension', 'helpulearn.cognitive.dimension',
                                             related='cognitive_id.cognitive_dimension_id')
    cognitive_type_id = fields.Many2one('Cognitive type', 'helpulearn.cognitive.subtype')
