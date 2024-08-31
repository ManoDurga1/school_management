from odoo import api,models,fields

class Enquire(models.Model):
    _name = "scl.enquire"
    _description = "Admissions Open"
    parent_name = fields.Char(string="Parent Name")
    parent_job = fields.Char(string="Parent Job")
    parent_no= fields.Char(string="Parent No")
    student_name= fields.Char(string="Student Name")
    student_age= fields.Integer(string="Student Age")
    standard=fields.Char(string="Class")
    status=fields.Selection([('draft','Draft'),('admit','Admit')],
                            default="draft",string="Status")

    def action_join(self):
        self.status='admit'
        var=self.env["school.student"]
        for rec in self:
            var.create({
                'student_name':rec.student_name,
                'gaurdian_name':rec.parent_name,
                'phone_number':rec.parent_no,
                'age':rec.student_age,
                'standard':rec.standard

            })



