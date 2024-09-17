from email.policy import default

from odoo import api, fields, models
from odoo.tools.populate import compute
from odoo.exceptions import UserError


class FeeStructure(models.Model):
    _name = "fee.structure"
    _rec_name = "student_id"
    _inherit = [
        'mail.thread'
    ]

    student_id = fields.Many2one('school.student', string="Student", tracking=True)
    name = fields.Selection([('tuition fee', 'Tuition Fee'), ('sports fee', 'Sports Fee'),
                             ('lab fee', 'Lab Fee'), ('exam fee', 'Exam Fee'), ('bus fee', 'Bus Fee')],
                            string="Fee Name")

    fee_amount = fields.Float(string="Fee Amount", default=0.0)
    from_date = fields.Date(string="From Date")
    due_date = fields.Date(string="Due Date")
    tax_amount = fields.Float(string="Tax Amount", default=0.0, compute="_compute_tax_amount")
    state = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')],
                             default="unpaid", compute="_compute_status_based_on_invoice")
    tax = fields.Many2many('account.tax', string='Tax')

    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount')

    product_id = fields.Many2one('product.product', string="Product")

    invoice_id = fields.Many2one('account.move')

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
            else:
                rec.tax_amount = 0.0

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
    # this code is belong's to make payment button
    def action_payment(self):
        print("button")
        if self.state == 'paid':
            raise UserError("this payment is already done!!!!")
        if self.invoice_id:
            return {
                'name': 'Customer Invoice',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_id.id,
                'target': 'current',
            }
        else:
            invoice = self.env['account.move'].create(
                {
                    'move_type': 'out_invoice',  # Customer Invoice
                    'partner_id': self.student_id.login_id.partner_id.id,  # Linked partner (customer)
                    'parent_name': self.student_id.gaurdian_name,
                    'parent_num': self.student_id.phone_number,
                    'invoice_line_ids': [(0, 0, {
                        'name': self.name,  # Description of the fee
                        'product_id': self.product_id.id,
                        'quantity': 1,
                        'price_unit': self.fee_amount,  # The fee amount
                        'tax_ids': [(6, 0, self.tax.ids)],  # Taxes if applicable
                    })],
                }
            )
            self.invoice_id = invoice.id
            return {
                'name': 'Customer Invoice',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
                'target': 'current',
            }

    def _compute_status_based_on_invoice(self):
        """ Compute the fee status based on invoice payment state """
        for rec in self:
            if rec.invoice_id:
                if rec.invoice_id.payment_state == 'paid':
                    rec.state = 'paid'
                else:
                    rec.state='unpaid'
            else:
                rec.state = 'unpaid'
