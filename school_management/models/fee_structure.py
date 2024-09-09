from email.policy import default

from odoo import api, fields, models
from odoo.tools.populate import compute


class FeeStructure(models.Model):
    _name = "fee.structure"
    _rec_name = "student_id"
    _inherit = [
        'mail.thread'
    ]

    student_id = fields.Many2one('school.student', string="Student")
    name = fields.Selection([('tution fee', 'Tution Fee'), ('sports fee', 'Sports Fee'),
                             ('lab fee', 'Lab Fee'), ('exam fee', 'Exam Fee'), ('bus fee', 'Bus Fee')],
                            string="Fee Name")

    fee_amount = fields.Float(string="Fee Amount")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    tax_amount = fields.Float(string="Tax Amount", compute="_compute_tax_amount")
    state = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')],
                             default="unpaid")
    tax = fields.Many2many('account.tax', string='Tax')

    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount')

    def action_confirm(self):
        for rec in self:
            rec.state = "paid"

    @api.depends('fee_amount', 'tax')
    def _compute_tax_amount(self):
        for rec in self:
            total_tax_amount = 0.0
            if rec.tax:
                for tax in rec.tax:
                    # Assuming 'amount' field in account.tax represents the tax rate
                    # and it is a percentage (e.g., 15 for 15%)
                    total_tax_amount += (rec.fee_amount * tax.amount / 100)
                rec.tax_amount = total_tax_amount

    # another method to calculate the tax....using compute_all() we calculate the tax
    #  it is built-in function in odoo
    #  @api.depends('fee_amount', 'tax')
    #  def _compute_tax_amount(self):
    #      for record in self:
    #          tax_amount = 0.0
    #          if record.tax:
    #              # Compute tax using Odoo's tax API
    #              taxes = record.tax.compute_all(record.fee_amount)
    #              tax_amount = taxes['total_included'] - taxes['total_excluded']
    #          record.tax_amount = tax_amount

    # compute the total amount based on the fee amount and total tax amount
    @api.depends('total_amount', 'tax_amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.fee_amount + rec.tax_amount
