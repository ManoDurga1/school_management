from odoo import api,models,fields

class Enquire(models.Model):
    _name = "scl.enquire"
    _description = "enquire about school management"
    parent_name = fields.Char(string="Parent Name")
    parent_job = fields.Char(string="Parent Job")
    parent_no= fields.Char(string="Parent No")
    student_name= fields.Char(string="Student Name")
    student_age= fields.Integer(string="Student Age")
    standard=fields.Char(string="Class")


