from odoo import api, fields, models


class StudentSuggestion(models.Model):
    _name = "suggestion.student12"
    _description = "Student Complaint"


    student_name=fields.Char(string="Student Name")
    student_class1 = fields.Char(string="Class")
    message = fields.Text(string="Message")


