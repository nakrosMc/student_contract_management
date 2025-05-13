from odoo import models, fields, api

class StudentContractLine(models.Model):
    _name = 'student.contract.line'
    _description = 'Línea de Contrato Estudiantil'


    contract_id = fields.Many2one('student.contract', string="Contrato")
    subject_id = fields.Many2one('school.subject', string="Materia")
    teacher_id = fields.Many2one('res.partner', string="Profesor")
    price = fields.Monetary(string="Monto",currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Moneda", related='contract_id.currency_id', store=True, readonly=False)

    # Filtra las materias disponibles en función de las materias asociadas al estudiante del contrato
    @api.onchange('contract_id')
    def _onchange_subject_domain(self):
        if self.contract_id and self.contract_id.student_id:
            return {
                'domain': {
                    'subject_id': [('id', 'in', self.contract_id.student_id.subject_ids.ids)]
                }
            }

    # Filtra las materias disponibles para el campo 'subject_id' según las materias asociadas al estudiante del contrato.
    @api.onchange('subject_id')
    def _onchange_teacher_domain(self):
        if self.subject_id:
            teacher_ids = self.subject_id.teacher_ids
            domain = [('id', 'in', teacher_ids.ids)]
            value = {}
            if teacher_ids:
                value['teacher_id'] = teacher_ids[0].id
            return {
                'domain': {'teacher_id': domain},
                'value': value
            }
