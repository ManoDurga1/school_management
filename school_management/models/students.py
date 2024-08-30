from odoo import  api,fields,models
class school_management(models.Model):
    _name='school.student'
    _description='school life is memorible'
    _rec_name = "student_name"
    student_name=fields.Char(string='Name',required=True)
    dateofbirth=fields.Date(string="DOB")
    gender=fields.Selection([('male','Male'),('female','Female'),('others','Others')],string='Gender')
    gaurdian_name =fields.Char(string='Guardian Name',required=True)
    address=fields.Char(string="Address")
    phone_number=fields.Char(string="Phone NUmber")
    joining_date=fields.Date(string="Joining Date")
    standard=fields.Char(string="Class")
    department=fields.Char(string="Department")
    teacher=fields.Many2one(comodel_name="school.teacher")
    fee_structure=fields.One2many('fee.structure',inverse_name='student_id',string="Fee Structure")
