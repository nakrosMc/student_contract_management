{
    'name': 'Gestión de Contratos Estudiantiles',
    'description': """
        this module in made for student contract management
    """,
    'author': "Leon Chacon",
    'category': 'Education',
    "contributors": "nakrosnc@gmail.com",
    "maintainer": "nakrosnc@gmail.com",
    'version': '17.0',
    'depends': ['base', 'contacts', 'account', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_contract_views.xml',
        'views/student_subject_views.xml',
        'views/res_partner_views.xml',
        'views/student_contract_dashboard_view.xml',
        'views/student_menu.xml',
        'report/student_contract_report_template.xml',
        'report/student_contract_report.xml',
        ],
    'assets': {
        'web.assets_backend': [
            'student_contract_management/static/src/js/dashborad.js',
            'student_contract_management/static/src/js/widget.js'
            ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
