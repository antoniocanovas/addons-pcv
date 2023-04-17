# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo      = fields.Selection([('no','None'),('time','Time')], store=True, string='Tipo cálculo', default='no')

    horas_minimo      = fields.Float('Horas mínimas')
    inicio_extra      = fields.Float('Hora incio extra')
    inicio_ordinario  = fields.Float('Hora incio ordinaria')
    final_ordinario   = fields.Float('Hora final ordinaria')
    final_extra       = fields.Float('Hora final extra')
    pt_hora_ordinaria = fields.Many2one('product.template', string='Hora ordinaria')
    pt_hora_extra     = fields.Many2one('product.template', string='Hora extra')
