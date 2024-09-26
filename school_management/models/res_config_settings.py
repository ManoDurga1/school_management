from odoo import api, fields, models

  # create bank details in the configuration menu under the settings
class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bank_name = fields.Char(string="Bank")
    branch = fields.Char(string="Account Name")
    account_no = fields.Char(string="Account No")
    ifsc_code = fields.Char(string="IBAN NO")

    def set_values(self):
        res=super(ConfigSettings, self).set_values()
        result = self.env['ir.config_parameter'].sudo()  # result is a variable name
        result.set_param('res.config.settings.bank_name', self.bank_name)   # call the objects using result(variable) name
        result.set_param('res.config.settings.branch', self.branch)
        result.set_param('res.config.settings.account_no', self.account_no)
        result.set_param('res.config.settings.ifsc_code', self.ifsc_code)
        return res

    @api.model
    def get_values(self):
        res = super(ConfigSettings, self).get_values()
        result = self.env['ir.config_parameter'].sudo()
        res.update(
            bank_name=result.get_param('res.config.settings.bank_name', default=''),
            branch=result.get_param('res.config.settings.branch', default=''),
            account_no=result.get_param('res.config.settings.account_no', default=''),
            ifsc_code=result.get_param('res.config.settings.ifsc_code', default=''),
        )
        return res

    # res.config.settings model is a transient model used only for configuration purposes and does not store persistent data like normal models.
    #nstead, data is saved in ir.config_parameter. But, if you have bank details in another model, such as a custom configuration model or sale.order,
    # you can access it in the report using the model name.
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bank_name = fields.Char(string="Bank Name", compute='_compute_bank_details')
    branch = fields.Char(string="Branch", compute='_compute_bank_details')
    account_no = fields.Char(string="Account No", compute='_compute_bank_details')
    ifsc_code = fields.Char(string="IFSC Code", compute='_compute_bank_details')

    @api.depends()
    def _compute_bank_details(self):
        config = self.env['ir.config_parameter'].sudo()
        self.bank_name = config.get_param('res.config.settings.bank_name', default='')
        self.branch = config.get_param('res.config.settings.branch', default='')
        self.account_no = config.get_param('res.config.settings.account_no', default='')
        self.ifsc_code = config.get_param('res.config.settings.ifsc_code', default='')


