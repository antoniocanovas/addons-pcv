# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo      = fields.Selection([('no','None'),('time','Time')], store=True, string='Tipo cálculo', default='no')

    horas_minimo      = fields.Float('Horas mínimas')
    inicio_ordinaria  = fields.Float('Hora incio ordinaria')
    final_ordinaria   = fields.Float('Hora final ordinaria')
    pt_hora_ordinaria = fields.Many2one('product.template', string='Hora ordinaria')
    pt_hora_extra     = fields.Many2one('product.template', string='Hora extra')
    atributo_hinicio  = fields.Many2one('product.attribute', string='Atributo hora inicio')
    atributo_hfin     = fields.Many2one('product.attribute', string='Atributo hora fin')

    def compute_special_variant_price(self):
        for record in self:
            if (record.tipo_calculo == 'time'):
                # Inicialización:
                inicio_ordinaria = record.inicio_ordinaria
                final_ordinaria = record.final_ordinaria
                horas_minimo = record.horas_minimo

                for va in record.product_variant_ids:
                    hextras, hordinarias = 0, 0

                    inicio = env['product.template.attribute.value'].search(
                        [('attribute_id', '=', record.atributo_hinicio.id),
                         ('id', 'in', va.product_template_variant_value_ids.ids)]).name
                    hinicio = inicio.split(":", 2)
                    empezar = int(hinicio[0]) + int(hinicio[1]) / 100
                    fin = env['product.template.attribute.value'].search([('attribute_id', '=', record.atributo_hfin.id), (
                        'id', 'in', va.product_template_variant_value_ids.ids)]).name
                    hfin = fin.split(":", 2)
                    terminar = int(hfin[0]) + int(hfin[1]) / 100

                    if (terminar - empezar <= 0): raise UserError(
                        'Configura bien las variantes, hay horas de finalización similares o anteriores a las de inicio.')

                    if (inicio_ordinaria - empezar > 0): hextras += (inicio_ordinaria - empezar)
                    if (terminar - final_ordinaria > 0): hextras += (terminar - final_ordinaria)

                    if (empezar < inicio_ordinaria) and (terminar > final_ordinaria):
                        hordinarias = final_ordinaria - inicio_ordinaria
                    elif (empezar < inicio_ordinaria) and (terminar <= final_ordinaria):
                        hordinarias = terminar - inicio_ordinaria
                    elif (empezar >= inicio_ordinaria) and (terminar > final_ordinaria):
                        hordinarias = final_ordinaria - empezar
                    else:
                        hordinarias = terminar - empezar

                    if (hordinarias + hextras < horas_minimo): hordinarias = horas_minimo - hextras

                    # Cálculo coste y venta por variante:
                    pvp = (hordinarias * record.pt_hora_ordinaria.list_price) + (hextras * record.pt_hora_extra.list_price)
                    coste = (hordinarias * record.pt_hora_ordinaria.standard_price) + (
                            hextras * record.pt_hora_extra.standard_price)
                    if (va.lst_price != pvp) or (va.standard_price != coste):
                        va.write({'lst_price': pvp, 'standard_price': coste})
