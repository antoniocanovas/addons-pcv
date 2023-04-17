# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo      = fields.Selection(['time','Time'], store=True, string='Tipo cálculo')

    horas_minimo      = fields.float('Horas mínimas')
    inicio_extra      = fields.float('Hora incio extra')
    inicio_ordinario  = fields.float('Hora incio ordinaria')
    final_ordinario   = fields.float('Hora final ordinaria')
    final_extra       = fields.float('Hora final extra')
    hextra_factor     = fields.float('Factor extra')
#    hfestivo_factor   = fields.float('Factor festivo')
