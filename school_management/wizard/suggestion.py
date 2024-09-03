from odoo import api, fields, models


class StudentSuggest(models.TransientModel):
    _name = "suggestion.student"
    _description = "Student Complaint"


    student_id = fields.Many2one('school.student', string='Student Name')
    student_class1 = fields.Char(string="Class")
    message = fields.Text(string="Message")


    @api.onchange('student_id')  # onchange is decorator to triger the value with out changeing the actual code..
    def manu(self):# _onchange_manu_id is the method name
        if self.student_id:
            self.student_class1 = self.student_id.standard


    def action_save(self):
        self.env['suggestion.student12'].create({
            "student_name":self.student_id.student_name,
            "student_class1":self.student_class1,
            "message":self.message
        })


