# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
