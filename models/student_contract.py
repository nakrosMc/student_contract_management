from odoo import models, fields, api
from odoo.exceptions import UserError

class StudentContract(models.Model):
    _name = 'student.contract'
    _description = 'Contrato Estudiantil'

    dashboard_id = fields.Many2one('powerbi.dashboard', string='Dashboard Power BI')
    payment_ids = fields.One2many('account.payment', 'student_contract_id', string='Pagos')
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id)
    name = fields.Char(string="Nombre del Contrato", required=True, default="Nuevo")
    student_id = fields.Many2one('res.partner', string="Estudiante", domain="[('is_student', '=', True)]")
    contract_line_ids = fields.One2many('student.contract.line', 'contract_id', string="Materias")
    amount_total = fields.Float(string="Total a pagar", compute="_compute_total", store=True)
    total_paid = fields.Float(string='Total Pagado', compute='_compute_total_paid', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('paid', 'Pagado'),
        ('partial', 'Parcial'),
        ('unpaid', 'No Pagado'),
    ], string='Estado', default='draft', compute='_compute_state', store=True)

    # Calcula el total a pagar basado en los precios de las líneas del contrato
    @api.depends('contract_line_ids.price')
    def _compute_total(self):
        for record in self:
            record.amount_total = sum(line.price for line in record.contract_line_ids)

    # Calcula el estado del contrato basado en los pagos realizados y el total a pagar
    @api.depends('payment_ids.amount', 'contract_line_ids.price')
    def _compute_state(self):
        for contract in self:
            # Filtra los pagos que están en estado 'posted'
            pagos_posteados = contract.payment_ids.filtered(lambda p: p.state == 'posted')
            pagos_sin_duplicar = {}

            # Evita duplicados en los pagos basándose en el monto y la moneda
            for pago in pagos_posteados:
                key = (pago.amount, pago.currency_id.id)
                if key not in pagos_sin_duplicar:
                    pagos_sin_duplicar[key] = pago

            # Calcula el total pagado
            total_paid = sum(pago.amount for pago in pagos_sin_duplicar.values())
            contract.total_paid = total_paid

            # Determina el estado del contrato según el total pagado
            if total_paid == 0:
                contract.state = 'unpaid'
            elif total_paid < contract.amount_total:
                contract.state = 'partial'
            elif total_paid >= contract.amount_total:
                contract.state = 'paid'
            else:
                contract.state = 'draft'

    # Calcula el total pagado basado en los pagos en estado 'posted'
    @api.depends('payment_ids.amount', 'payment_ids.state')
    def _compute_total_paid(self):
        for record in self:
            pagos_posteados = record.payment_ids.filtered(lambda p: p.state == 'posted')
            record.total_paid = sum(pago.amount for pago in pagos_posteados)

    # Acción para mostrar las materias y montos asociados al contrato
    def action_show_total(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Materias y Montos',
            'res_model': 'student.contract.line',
            'view_mode': 'tree',
            'target': 'new',
            'domain': [('contract_id', '=', self.id)],
        }

    # Acción para mostrar el total pagado
    def action_show_paid(self):
        for record in self:
            total_paid = sum(p.amount for p in record.payment_ids if p.state == 'posted')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'student.contract',
                'views': [[False, 'form']],
                'target': 'new',
                'context': {
                    'default_total_paid': total_paid,
                }
            }

    # Acción para mostrar el estado actual del contrato
    def action_show_state(self):
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'student.contract',
                'views': [[False, 'form']],
                'target': 'new',
                'context': {
                    'default_state': record.state,
                }
            }

    # Acción para registrar un nuevo pago
    def action_register_payment(self):
        self.ensure_one()

        # Verifica si el contrato ya está completamente pagado
        if self.total_paid >= self.amount_total and self.state == 'paid':
            raise UserError("Este contrato ya está completamente pagado.")

        # Calcula el monto pendiente por pagar
        monto_pendiente = self.amount_total - self.total_paid

        # Verifica si ya existe un pago registrado o pendiente por el monto restante
        existing_payment = self.payment_ids.filtered(
            lambda p: p.amount == monto_pendiente and p.state in ['draft', 'posted'] and self.state == 'paid'
        )

        if existing_payment:
            raise UserError("Ya existe un pago registrado o pendiente por el monto restante.")

        # Retorna la acción para registrar un nuevo pago
        return {
            'name': 'Registrar Pago',
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_contract_id': self.id,
                'default_partner_id': self.student_id.id,
                'default_amount': monto_pendiente,
                'default_currency_id': self.currency_id.id,
                'default_payment_type': 'inbound',
                'default_payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                'default_journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
                'default_company_id': self.env.user.company_id.id,
            }
        }

    # Fuerza el recálculo del estado del contrato
    def force_recompute_state(self):
        for record in self:
            record._compute_state()

    # Acción para realizar un pago y actualizar el estado del contrato
    def action_pay(self):
        self.ensure_one()

        # Obtiene el monto pagado
        monto_pagado = self.payment_ids.amount

        # Verifica que el monto a pagar sea mayor que 0
        if monto_pagado <= 0:
            raise UserError("El monto a pagar debe ser mayor que 0.")

        # Actualiza el total pagado
        self.total_paid += monto_pagado
        print(f"total_pagado después de actualizar: {self.total_paid}")

        # Actualiza el estado del contrato según el total pagado
        if self.total_paid >= self.amount_total:
            self.state = 'paid'
        elif self.total_paid > 0:
            self.state = 'partial'
        else:
            self.state = 'unpaid'

        return True