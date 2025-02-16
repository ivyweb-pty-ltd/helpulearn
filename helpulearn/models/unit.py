from odoo import fields, models, api


class HelpULearnUnit(models.Model):
    _name = 'helpulearn.unit'
    _description = (
        'Unit is just a hierarchical structure used to group several learning objectives, it could refer to '
        'course, unit inside a course or any other way that learning objectives are grouped together')

    name = fields.Char(required=True)
    unit_type_id = fields.Many2one('helpulearn.unit_type', 'Unit Type')
    parent_unit_id = fields.Many2one('helpulearn.unit', 'Parent Unit')
    child_unit_ids = fields.One2many('helpulearn.unit', 'parent_unit_id', 'Child Units')
    bit_ids = fields.One2many('helpulearn.bit', 'unit_id', 'Bits')
    review_ids = fields.One2many('helpulearn.review', 'unit_id', 'Reviews')

    def _compute_display_name(self):
        # Runs through the hierarchy and combines them using a / in between
        for unit in self:
            temp_display_name = unit.name
            if not unit.name:
                unit.display_name=""
                continue
            count = 1
            temp_parent_unit = unit.parent_unit_id
            while temp_parent_unit and count < 3:
                temp_display_name = temp_parent_unit.name + "/" + temp_display_name
                count = count + 1
                temp_parent_unit = temp_parent_unit.parent_unit_id

            if not temp_parent_unit.parent_unit_id:
                temp_display_name = "/" + temp_display_name
            else:
                temp_display_name = "../" + temp_display_name

            unit.display_name = temp_display_name

# TODO: Create menus for unit
