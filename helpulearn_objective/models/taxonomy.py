from odoo import api, fields, models


class HelpULearn_Taxonomy(models.Model):
    _name = 'helpulearn.taxonomy'
    _description = 'Blooms Revised Taxonomy'


    name = fields.Char('Name')

    component_ids = fields.One2many('helpulearn.taxonomy.component', 'taxonomy_id', 'Components')
    knowledge_dimension_id = fields.Many2one('helpulearn.knowledge.dimension', 'Knowledge Dimension')
    knowledge_type_id = fields.Many2one('helpulearn.knowledge.subtype', 'Knowledge type', domain="[('knowledge_dimension_id', '=', knowledge_dimension_id)]")
    cognitive_dimension_id = fields.Many2one('helpulearn.cognitive.dimension', 'Cognitive Dimension')
    cognitive_type_id = fields.Many2one('helpulearn.cognitive.subtype', 'Cognitive type', domain="[('cognitive_dimension_id', '=', cognitive_dimension_id)]")


class KnowledgeDimension(models.Model):
    _name = "helpulearn.knowledge.dimension"

    name = fields.Char('Name')


class KnowledgeSubtype(models.Model):
    _name = "helpulearn.knowledge.subtype"

    name = fields.Char('Name')
    knowledge_dimension_id = fields.Many2one('helpulearn.knowledge.dimension')


class CognitiveDimension(models.Model):
    _name = "helpulearn.cognitive.dimension"

    name = fields.Char("Name")


class CognitiveSubtype(models.Model):
    _name = 'helpulearn.cognitive.subtype'

    name = fields.Char('Name')
    cognitive_dimension_id = fields.Many2one('helpulearn.cognitive.dimension')
