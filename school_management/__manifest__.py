{
    "name": "school management",
    "author": "mr.manu",
    "version": "18.0",
    "depends": ['sale',
           'account','mail'],

    "data": [
        "security/ir.model.access.csv",
        "security/school_groups.xml",
        "security/school_security.xml",
        "data/student_mail_template.xml",
        "data/cron.xml",
        "data/student_due_reminder_template.xml",
        "views/enquire_views.xml",
        "views/student_views.xml",
        "views/teacher_views.xml",
        "views/fee_structure_views.xml",
        "views/sale.xml",
        "views/product_brand.xml",
        "views/invoice_views.xml",
        "views/suggestion_stu_views.xml",
        "wizard/suggestion_views.xml",
        "views/menu.xml",
        "report/report.xml",
        "report/report_template.xml",
        "report/sale_report.xml",
        "report/sale_order_report_template.xml",
        "report/invoice_report_inherit.xml"
    ]

}
