from odoo import api, fields, models


class school_management(models.Model):
    _name = 'school.teacher'
    _description = 'teacher of the school'
    _rec_name = "teacher_name"

    teacher_name = fields.Char(string='Name', required=True)
    dateofbirth = fields.Date(string="DOB")
    address = fields.Char(string="Address")
    mobile_number = fields.Char(string="Mobile Number")
    dateofjoining = fields.Date(string="Joining Date")
    classteacher = fields.Boolean(string="Class Teacher")
    state = fields.Selection([('draft','Draft'),('permanent','Permanent')
                              ],default='draft',string="State")
    email = fields.Char(string="Email")
    login_id = fields.Many2one('res.users', string='User Id')


    def action_confirm(self):
        self.state='permanent'
        self.env['res.users'].create({
            'name': self.teacher_name,
            'login': self.email,
            'email': self.email,
            'password': 'teacher',
            'groups_id':[(6, 0, [self.env.ref('school_management.group_school_teacher').id])]
        })




