"""
Created by jacobus on 2025/02/02 
"""
from odoo.tests import TransactionCase


class test_unit(TransactionCase):
    def setUp(self):
        super(test_unit, self).setUp()
        self.unit = self.env['helpulearn.unit'].create({
            'name': 'Course',
        })


    def test_create_unit_no_name(self):
        with self.assertRaises(Exception):
            self.env['helpulearn.unit'].create({})


    def test_create_unit(self):
        self.assertEqual(self.unit.name, 'Course')
        self.assertEqual(self.unit.display_name, 'Course')

    def test_with_one_parent(self):
        parent_unit = self.env['helpulearn.unit'].create({
            'name': 'Parent Course',
        })
        self.unit.parent_unit_id = parent_unit
        self.assertEqual(self.unit.parent_unit_id, parent_unit)
        self.assertEqual(parent_unit.child_unit_ids, self.unit)
        self.assertEqual(self.unit.display_name, "Parent Course>Course")

    def test_with_many_parents(self):
        current_unit = self.unit
        for i in range(2):
            parent_unit = self.env['helpulearn.unit'].create({
                'name': 'Parent Course %s' % i,
            })
            current_unit.parent_unit_id = parent_unit
            current_unit = parent_unit
        self.assertEqual(self.unit.display_name, "Parent Course 1>Parent Course 0>Course")

    def test_with_more_than_two_parents(self):
        current_unit = self.unit
        for i in range(4):
            parent_unit = self.env['helpulearn.unit'].create({
                'name': 'Parent Course %s' % i,
            })
            current_unit.parent_unit_id = parent_unit
            current_unit = parent_unit
        self.assertEqual(self.unit.display_name, "Parent Course 3>Parent Course 2>Parent Course 1>Parent Course 0>Course")
