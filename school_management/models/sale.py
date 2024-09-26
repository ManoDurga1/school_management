from email.policy import default

from dateutil.utils import today
from datetime import datetime
from odoo import api, fields, models
from odoo.tools.populate import compute



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_note=fields.Text(string='Customer Note')
    parent_name = fields.Char(string="Parent Name")
    parent_num =  fields.Char(string="Parent Num")

    # bank_name = fields.Char(string="Bank Name")
    # branch = fields.Char(string="Branch")
    # account_no = fields.Char(string="Account Number")
    # ifsc_code = fields.Char(string="IFSC Code")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    brand_id = fields.Many2one('product.brand',string="Product Brand")




