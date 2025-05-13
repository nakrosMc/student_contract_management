from odoo import _, api, fields, models, tools

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="¿Es estudiante?", default=False)
    is_teacher = fields.Boolean(string="¿Es profesor?", default=False)
    subject_ids = fields.Many2one('school.subject', string="Materias (para estudiantes)", domain="[('teacher_ids', '!=', False)]")

    school_type = fields.Selection([
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
    ], string="Tipo de usuario")

    # Filtra los estudiantes disponibles en función de las materias asociadas al profesor del contrato
    @api.onchange('school_type')
    def _onchange_school_type(self):
        if self.school_type == 'student':
            self.is_student = True
            self.is_teacher = False
        elif self.school_type == 'teacher':
            self.is_teacher = True
            self.is_student = False
