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
                unit.display_name = ""
                continue
            temp_parent_unit = unit.parent_unit_id
            while temp_parent_unit:
                temp_display_name = temp_parent_unit.name + ">" + temp_display_name
                temp_parent_unit = temp_parent_unit.parent_unit_id

            unit.display_name = temp_display_name

    def open_unit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Unit',
            'view_mode': 'form',
            'res_model': 'helpulearn.unit',
            'res_id': self.id,
            'target': 'current',
        }

    def _get_all_child_units(self):
        """Retrieve all descendant units of the current record"""
        all_units = self.env['helpulearn.unit'].browse()
        for unit in self:
            all_units |= unit.child_unit_ids
            all_units |= unit.child_unit_ids._get_all_child_units()  # Recursively add children
        return all_units

    def name_get(self):
        """Override name_get to return (id, display_name)"""
        result = []
        for record in self:
            result.append((record.id, record.display_name or record.name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if name:
            domain = ['|', ('name', operator, name), ('display_name', operator, name)]

            # Find matching parent and child records
            matching_units = self.search(domain + args, limit=limit)

            # Include child units of matched records
            all_units = matching_units
            for unit in matching_units:
                all_units |= unit._get_all_child_units()

            return all_units.name_get()
        return super(HelpULearnUnit, self).name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Extend default search to include sub-units when filtering by name or display_name."""
        name_filter = None
        for arg in args:
            if isinstance(arg, (list, tuple)) and arg[0] in ['name', 'display_name'] and arg[1] in ['ilike', '=like', 'like']:
                name_filter = arg
                break

        if name_filter:
            name_field, operator, value = name_filter
            domain = ['|', (name_field, operator, value), ('display_name', operator, value)]

            # Find all matching units
            matching_units = super().search(domain + args, offset=offset, limit=limit, order=order)

            # Find child units recursively
            all_units = matching_units
            for unit in matching_units:
                all_units |= unit._get_all_child_units()

            return all_units if not count else len(all_units)

        return super().search(args, offset=offset, limit=limit, order=order)

# TODO: Create menus for unit
