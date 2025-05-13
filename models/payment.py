from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    student_contract_id = fields.Many2one('student.contract', string='Contrato Estudiantil')
    payment_date = fields.Date(string='Fecha de Pago', default=fields.Date.today)
    journal_id = fields.Many2one('account.journal', string='Diario')
    currency_id = fields.Many2one('res.currency', string="Moneda", related='student_contract_id.currency_id',store=True, readonly=False)
    amount = fields.Monetary(string="Monto", currency_field='currency_id')

