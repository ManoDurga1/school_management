from email.policy import default

from dateutil.utils import today
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError

from odoo.tools.populate import compute



class SchoolManagement(models.Model):
    _name = 'school.student'
    _description = 'school life is memorible'
    _rec_name = "student_name"

    student_name = fields.Char(string='Name', required=True)
    dateofbirth = fields.Date(string="DOB")
    age= fields.Integer(string="Student Age",compute='_age_student',store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string='Gender')
    gaurdian_name = fields.Char(string='Guardian Name', required=True)
    address = fields.Char(string="Address")
    phone_number = fields.Char(string="Phone NUmber")
    joining_date = fields.Date(string="Joining Date")
    standard = fields.Char(string="Class")
    department = fields.Char(string="Department")
    teacher = fields.Many2one(comodel_name="school.teacher")
    teacher_no = fields.Char(string="Teacher No")
    extra_staff= fields.Many2many("school.teacher",string="other subject teachers",
                                 help= "mention the teachers who teach other subjects as well")
    fee_structure = fields.One2many('fee.structure', inverse_name='student_id', string="Fee Structure")
    state =fields.Selection([('not selected','Not selected'),('selected','Selected')],
                            default="not selected",string="State")

    def create(self, vals):
        print('Entered in create', vals)
        if vals['phone_number']:
            student_id=self.env["school.student"].search([('phone_number','=',vals['phone_number'])])
            if student_id:
                raise ValidationError("there is a student with same phone number")
        return super(SchoolManagement,self).create(vals)
    
    
    @api.onchange('teacher')
    def _onchange_teacher(self):
       if self.teacher:
        self.teacher_no = self.teacher.mobile_number
    def action_select(self):
        self.state= "selected"

    @api.depends('dateofbirth')
    def _age_student(self):
        for rec in self:
            if rec.dateofbirth:
                today=datetime.today().date()
                dob=fields.Date.from_string(rec.dateofbirth)
                age=today.year-dob.year
                rec.age=age
            else:
                rec.age=0