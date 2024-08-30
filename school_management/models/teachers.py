from odoo import  api,fields,models
class school_management(models.Model):
    _name='school.teacher'
    _description='teacher of the school'
    _rec_name = "teacher_name"

    teacher_name=fields.Char(string='Name',required=True)
    dateofbirth=fields.Date(string="DOB")
    address=fields.Char(string="Address")
    mobile_number=fields.Char(string="Mobile Number")
    dateofjoining=fields.Date(string="Joining Date")
    classteacher=fields.Boolean(string="Class Teacher")

