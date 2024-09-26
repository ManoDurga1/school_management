from odoo import api, fields, models

class SaleOrderPy(models.Model):
    _inherit = 'sale.order'

    # bank_name = fields.Char(string="Bank")
    # branch = fields.Char(string="Account Name")
    # account_no = fields.Char(string="Account No")
    # ifsc_code = fields.Char(string="IBAN NO")

    # CREATE DUE DATE AND SHIPPING TERMS FOR XLSX REPORT
    due_date = fields.Date(string='Due Date')
    shipping_terms = fields.Char(string='Shipping Terms')




