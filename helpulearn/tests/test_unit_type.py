"""
Created by jacobus on 2025/02/02 
"""
from odoo.tests import TransactionCase


class test_unit_type(TransactionCase):
    def setUp(self):
        super(test_unit_type, self).setUp()
        self.unit_type = self.env['helpulearn.unit_type'].create({
            'name': 'Course',
            'description': 'This is a course',
        })

    def test_create_unit(self):
        self.assertEqual(self.unit_type.name, 'Course')
        self.assertEqual(self.unit_type.description, 'This is a course')
        self.assertEqual(self.unit_type.display_name, '/Course')

    def test_with_one_parent(self):
        parent_unit_type = self.env['helpulearn.unit_type'].create({
            'name': 'Parent Course',
            'description': 'This is a parent course',
        })
        self.unit_type.parent_unit_type_id = parent_unit_type
        self.assertEqual(self.unit_type.parent_unit_type_id, parent_unit_type)
        self.assertEqual(parent_unit_type.child_unit_types_ids, self.unit_type)
        self.assertEqual(self.unit_type.display_name,"/Parent Course/Course")

    def test_with_many_parents(self):
        current_unit_type = self.unit_type
        for i in range(2):
            parent_unit_type = self.env['helpulearn.unit_type'].create({
                'name': 'Parent Course %s' % i,
                'description': 'This is a parent course',
            })
            current_unit_type.parent_unit_type_id = parent_unit_type
            current_unit_type = parent_unit_type
        self.assertEqual(self.unit_type.display_name, "/Parent Course 1/Parent Course 0/Course")

    def test_with_more_than_two_parents(self):
        current_unit_type = self.unit_type
        for i in range(4):
            parent_unit_type = self.env['helpulearn.unit_type'].create({
                'name': 'Parent Course %s' % i,
                'description': 'This is a parent course',
            })
            current_unit_type.parent_unit_type_id = parent_unit_type
            current_unit_type = parent_unit_type
        self.assertEqual(self.unit_type.display_name, "../Parent Course 1/Parent Course 0/Course")
