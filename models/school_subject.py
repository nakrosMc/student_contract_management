from odoo import _, api, fields, models, tools

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Materia Escolar'

    name = fields.Char(string="Nombre de la materia", required=True)
    code = fields.Char(string="Código")
    
    teacher_ids = fields.Many2many('res.partner', 
        'subject_teacher_rel',
        'subject_id',           
        'teacher_id',         
        string="Profesores asignados", 
        domain="[('is_teacher', '=', True)]"
    )
    

    contract_line_ids = fields.One2many(
        'student.contract.line', 
        'subject_id', 
        string="Líneas de Contrato"
    )