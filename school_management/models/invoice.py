from odoo import api,fields,models

class Invoice(models.Model):
    _inherit = "account.move"

    parent_name = fields.Char(string="Parent Name")
    parent_num = fields.Char(string="Parent Num")

    bank = fields.Char(string="Bank Name")
    account_no = fields.Char(string="Account No")
    branch = fields.Char(string="Branch Name")
    ifsc_code = fields.Char(string="IFSC Code")

class InvoiceLines(models.Model):
    _inherit = "account.move.line"

    student_fee=fields.Many2one("fee.structure",string="Student Fee")
