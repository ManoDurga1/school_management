from email.policy import default

from odoo import api, fields, models


class FeeStructure(models.Model):
    _name = "fee.structure"

    student_id = fields.Many2one('school.student', string="Student")
    name = fields.Selection([('tution fee','Tution Fee'),('sports fee','Sports Fee'),
                             ('lab fee','Lab Fee'),('exam fee','Exam Fee'),('bus fee','Bus Fee')],
                            string="Fee Name")

    fee_amount = fields.Float(string="Fee Amount")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    tax_amount = fields.Float(string="Tax Amount")
    state= fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')],
                         default="unpaid")


    def action_confirm(self):
       for rec in self:
              rec.state="paid"

