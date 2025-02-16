from odoo import fields, models, api


class HelpULearnUnitType(models.Model):
    _name = 'helpulearn.unit_type'
    _description = ('Unnt Type is the type of unit that is used, eg course might be a type for a university and it is '
                    'group in units, which are grouped into lessons. Each one of these are unit types.')

    name = fields.Char()
    description = fields.Text()
    parent_unit_type_id = fields.Many2one('helpulearn.unit_type', 'Parent Unit Type')
    child_unit_types_ids = fields.One2many('helpulearn.unit_type', 'parent_unit_type_id', 'Child Unit Types')
    unit_ids = fields.One2many('helpulearn.unit', 'unit_type_id', 'Units')

    def _compute_display_name(self):
        # Runs through the hierarchy and combines them using a / in between
        for unit_type in self:
            if not unit_type.name:
                unit_type.display_name = ""
                return

            temp_display_name = unit_type.name
            count = 1
            temp_parent_unit_type = unit_type.parent_unit_type_id
            while temp_parent_unit_type and count < 3:
                temp_display_name = temp_parent_unit_type.name + "/" + temp_display_name
                count = count + 1
                temp_parent_unit_type = temp_parent_unit_type.parent_unit_type_id

            if not temp_parent_unit_type.parent_unit_type_id:
                temp_display_name = "/" + temp_display_name
            else:
                temp_display_name = "../" + temp_display_name

            unit_type.display_name = temp_display_name

#TODO: Creat menus for unit type