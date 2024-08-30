from odoo import api,fields,models

class FeeStructure (models.Model):
    _name = "fee.structure"
    name = fields.Char(string= "Name",required= True)
    fee_amount=fields.Float(string="Fee Amount")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    tax_amount = fields.Float(string="Tax Amount")
    student_id = fields.Many2one('school.student',string="Student")
