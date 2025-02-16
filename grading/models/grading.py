from odoo import fields, models, api


class HelpULearnGrading(models.Model):
    _name = 'helpulearn.grading'
    _description = 'Grading of activities'
    """Attaches a retention and stability to each user and taxonomy
    stores the retention, stability and last activity date"""

    name = fields.Char()
    retention = fields.Float('Retention')
    stability = fields.Float('Stability')
    taxonomy = fields.Many2many('helpulearn.taxonomy')
    learner = fields.Many2one('helpulearn.learner')
    activity_assessment_ids = fields.One2many('helpulearn.activity_assessment')

class HelpULearnActivityAssessment(models.Model):
    _name = 'helpulearn.activity.assessment'
    _description = 'Activity Assessment'
    '''Stores information on the activity as it is executed by the client
     stores:
     start_time - Date and time activity started
     end_time - Date and time the activity ended
     start_retention - Start Retention (Send to the execute)
     start_stability - Start Stability (Send to the stability)
     retention - Retention at end of the activity
     stability - Stability at end of the activity
     grading_id - Link to grading this assessment applies to
     '''