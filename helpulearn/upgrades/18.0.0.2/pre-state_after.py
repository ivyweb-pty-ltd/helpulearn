"""
Created by jacobus on 2025/03/15

This upgrade scripts renames the field state_before and state_after to retention_before and retention_after respectively
"""

from odoo import api, fields, models, _

def migrate(cr, version):
    if not version:
        return

    #Check old version before proceeding

    if version != '18.0.0.1':
        return

    cr.execute("""
     DO $$
     BEGIN
        IF EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'helpulearn_review' 
            AND column_name = 'state_before'
            ) THEN
        ALTER TABLE helpulearn_review RENAME COLUMN state_before TO retention_before;
        END IF;
     END $$
    """)

    cr.execute("""
    DO $$
    BEGIN
       IF EXISTS(
         SELECT 1 FROM information_schema.columns
         WHERE table_name = 'helpulearn_review'
            AND column_name = 'state_after'
        ) THEN
          ALTER TABLE helpulearn_review RENAME COLUMN state_after TO retention_after;
        END IF;
    END $$
    """)

