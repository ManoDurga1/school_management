from odoo import api,fields,models

class Invoice(models.Model):
    _inherit = "account.move"

    parent_name = fields.Char(string="Parent Name")
    parent_num = fields.Char(string="Parent Num")

class InvoiceLines(models.Model):
    _inherit = "account.move.line"

    student_fee=fields.Many2one("fee.structure",string="Student Fee")
