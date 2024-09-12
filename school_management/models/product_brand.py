from odoo import api, models, fields
from odoo.addons.test_convert.tests.test_env import field


class Product(models.Model):
    _name = 'product.brand'
    _description = "Product Brand"

    brand_name = fields.Char(string="Brand Name")


class ProductUpgrade(models.Model):
    _inherit = 'product.template'


    brand_id = fields.Many2one("product.brand", string="Brand Name")
