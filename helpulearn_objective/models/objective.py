from odoo import fields, models, api


class HULObjective(models.Model):
    """Objective
    This object maps different element to the objective that are trying to be achieved.

    By defining the objectives it will be possible to customise the learning experience for each student the following
    elements will likely be mapped to this object.

    The taxonomy is not strictly necessary to build an effective curriculum but it helps in defining and choosing
    possible assessment and activities necessary to teach the objective.

    Objective Types: Global Objectives, Educational, Instructional
    Taxonomy : Taxonomies necessary to fulfill this objective
    Objective requirements: The objectives that need to be achieved to achieve this objective
    Objective potential: The objectives that can potentially follow this objective

    Expected to be added in separate module:
    content - Reference to media that is relevant to the specific topic.
    activities - Activities that can be performed to achieve this objective eg. Read, Build
    assessment - Assessment that can be used to prove that objective have been achieved (should be related to
                 cognitive and knowledge dimension)
    grading - Grading of the specific objective, mapping to different grading systems Eg. US school, college course level
    curriculum - Matching curriculum to objectives, combining objectives to create a course, degree.
    """
    _name = 'helpulearn.objective'

    name = fields.Char("Name")  # A short name for the objective
    description = fields.Text("Description")  # Longer name for the objective
    objective_type_id = fields.Many2one('helpulearn.objective.type', 'Objective Type')
    taxonomy_ids = fields.Many2many('helpulearn.taxonomy')
    # Objectives target
    target_objective_ids = fields.Many2many('helpulearn.objective', relation='related_objectives',
                                            string='Target Objectives',
                                            column1='required_objective_id', column2='target_objective_id')
    # Objectives required
    required_objective_ids = fields.Many2many('helpulearn.objective', relation='related_objectives',
                                              string='Required Objectives',
                                              column1='target_objective_id', column2='required_objective_id')
    # Objectives that can be linked from here, related but not part of
    potential_objective_ids = fields.Many2many('helpulearn.objective', relation='potential_objectives',
                                               column1='related_objective_id', column2='potential_objective_id',
                                               string='Potential Objectives')


class HULObjectiveType(models.Model):
    """Objective Type - Global, Educational, Instructional"""
    _name = 'helpulearn.objective.type'
    _description = 'Objective types'

    name = fields.Char('Objective Type')
    description = fields.Text('Description of objective type')
    scope = fields.Char('Objective Scope')
    time_required = fields.Char('Time required')
    purpose = fields.Char('Purpose')
    examples = fields.Text('Examples')
