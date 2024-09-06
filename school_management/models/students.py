from email.policy import default

from dateutil.utils import today
from datetime import datetime
from odoo import api, fields, models, _
from odoo.cli.scaffold import template
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
    email = fields.Char(string="Email")
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

    login_id = fields.Many2one('res.users', string='User Id')

    suggestion_count = fields.Integer(string="Suggestion",
                                      compute="_suggestion_count")

    def _suggestion_count(self):
        self.suggestion_count=self.env['suggestion.student12'].search_count(
            domain=[('student_name','=',self.student_name)]
        )


    def create(self, vals):
        print('Entered in create', vals)
        if vals['phone_number']:
            student_id=self.env["school.student"].search([('phone_number','=',vals['phone_number'])])
            if student_id:
                raise ValidationError("there is a student with same phone number")
        return super(SchoolManagement,self).create(vals)


    def action_suggestion(self):
        return {
            'name': _('Suggestion'),
            'type': 'ir.actions.act_window',
            'res_model': 'suggestion.student',
            'view_mode': 'form',
            'target':'new',
            'context': "{'default_student_id':active_id}"
        }


    @api.onchange('teacher')
    def _onchange_teacher(self):
       if self.teacher:
        self.teacher_no = self.teacher.mobile_number

    #  select button and automate fetch and creation of users and login creadintials
    def action_select(self):
        self.state= "selected"
        user_vals={
            'name':self.student_name,
            'login':self.email,
            'email':self.email,
            'password':'student',
            'groups_id': [(6, 0, [self.env.ref('school_management.group_school_student').id])]
        }
        stu_user=self.env['res.users'].create(user_vals)
        for rec in self:
            rec.login_id=stu_user.id
        # Anotherway for understanding purpose
        # stu_user = self.env['res.users'].create({
        #     'name':self.student_name,
        #     'login':self.email,
        #     'email':self.email,
        #     'password':'student',
        #     'groups_id': [(6, 0, [self.env.ref('school_management.group_school_student').id])]
        # })
        # for rec in self:
        #     rec.login_id=stu_user.id

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


    def action_view_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Related Records',
            'view_mode': 'tree,form',
            'res_model': 'suggestion.student12',  #  your related model
            'domain':[('student_name', '=', self.student_name)]

        }

    # Email button
    def action_email(self):
        template = self.env.ref('school_management.student_email')
        template.send_mail(self.login_id, force_send=True)
