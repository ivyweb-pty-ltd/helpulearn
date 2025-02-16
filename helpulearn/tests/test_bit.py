"""
Created by jacobus on 2025/02/15 
"""
from odoo.tests import TransactionCase
from datetime import datetime, timedelta,date

class TestBit(TransactionCase):
    def setUp(self):
        super(TestBit, self).setUp()
        self.bit = self.env['helpulearn.bit'].create({
            'name': 'Bit',
            'description': 'This is a bit of information',
            'content': 'This is the content of the bit',
        })

    def test_bit_number_of_reviews(self):
        self.assertEqual(self.bit.number_of_reviews, 0)

        self.bit.review_ids = self.env['helpulearn.review'].create({
            'bit_id': self.bit.id,
            'state_before': 0.5,
            'state_after': 0.8,
        })

        self.assertEqual(self.bit.number_of_reviews, 1)

    def test_bit_next_review(self):
        self.bit.review_ids = self.env['helpulearn.review'].create({
            'bit_id': self.bit.id,
            'state_before': 0.5,
            'state_after': 0.8,
            'review_date': date(2025,2,1)
        })

        last_review = self.bit.last_review
        number_of_reviews = self.bit.number_of_reviews
        days_to_next_review = 2 ** (number_of_reviews-1)
        next_review = last_review+timedelta(days=days_to_next_review)

        self.assertEqual(self.bit.next_review, next_review)

