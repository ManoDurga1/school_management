from odoo import api,models,fields
from odoo.exceptions import ValidationError
from datetime import datetime


class Enquire(models.Model):
    _name = "scl.enquire"
    _description = "Admissions Open"
    _rec_name = "student_name"

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
        today=datetime.today()
        student_id=self.env["school.student"].search([('phone_number','=',self.parent_no)])
        print("Student Ids are :",student_id)
        for stu in student_id:
            print("Student Name is:",stu.student_name)
        if student_id:
            raise ValidationError("there is a student with same phone number")
        var=self.env["school.student"]
        for rec in self:
            var.create({
                'student_name':rec.student_name,
                'gaurdian_name':rec.parent_name,
                'phone_number':rec.parent_no,
                'age':rec.student_age,
                'standard':rec.standard,
                'joining_date':today

            })



