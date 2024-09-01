from email.policy import default

from dateutil.utils import today
from datetime import datetime
from odoo import api, fields, models
from odoo.tools.populate import compute



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_note=fields.Text(string='Customer Note')

