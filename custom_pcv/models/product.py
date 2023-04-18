# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo      = fields.Selection([('no','None'),('time','Jornada laboral establecida, con horas extras')], store=True, string='Recálculo variantes', default='no')

    horas_minimo      = fields.Float('Horas mínimas')
    inicio_ordinaria  = fields.Float('Hora incio ordinaria')
    final_ordinaria   = fields.Float('Hora final ordinaria')
    nocturnidad_ok    = fields.Boolean('Permitir nocturnidad')
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

                    inicio = self.env['product.template.attribute.value'].search(
                        [('attribute_id', '=', record.atributo_hinicio.id),
                         ('id', 'in', va.product_template_variant_value_ids.ids)]).name
                    hinicio = inicio.split(":", 2)
                    empezar = int(hinicio[0]) + int(hinicio[1]) / 100
                    fin = self.env['product.template.attribute.value'].search([('attribute_id', '=', record.atributo_hfin.id), (
                        'id', 'in', va.product_template_variant_value_ids.ids)]).name
                    hfin = fin.split(":", 2)
                    terminar = int(hfin[0]) + int(hfin[1]) / 100

                    # Servicios normales, con y sin nocturnidad, en el mismo día:
                    if (terminar - empezar > 0):
                        # Horas extras:
                        if (inicio_ordinaria - empezar > 0): hextras += (inicio_ordinaria - empezar)
                        if (terminar - final_ordinaria > 0): hextras += (terminar - final_ordinaria)
                        # Horas jornada ordinaria:
                        if (empezar < inicio_ordinaria) and (terminar > final_ordinaria):
                            hordinarias = final_ordinaria - inicio_ordinaria
                        elif (empezar < inicio_ordinaria) and (terminar <= final_ordinaria):
                            hordinarias = terminar - inicio_ordinaria
                        elif (empezar >= inicio_ordinaria) and (terminar > final_ordinaria):
                            hordinarias = final_ordinaria - empezar
                        else:
                            hordinarias = terminar - empezar
                        if (hordinarias + hextras < horas_minimo): hordinarias = horas_minimo - hextras

                    # Servicios con nocturnidad días distintos (24h):
                    elif (terminar - empezar == 0) and  (record.nocturnidad_ok == True):
                        hordinarias = (24 - inicio_ordinaria) + (24 - final_ordinaria)
                        hextras = 24 - hordinarias

                    # Servicios con nocturnidad días distintos (menos de 24h):
                    elif (terminar - empezar < 0) and (record.nocturnidad_ok == True):
                        # DÍA 1.- Horas extras de mañana y Horas extras nocturnidad:
                        if (inicio_ordinaria - empezar > 0):
                            hextras += (inicio_ordinaria - empezar)
                            hextras += (24 - final_ordinaria)
                        # DÍA 2.- Extras de mañana y nocturnidad:
                        if (inicio_ordinaria - terminar <= 0):
                            hextras += terminar
                        if (inicio_ordinaria - terminar > 0):
                            hextras += inicio_ordinaria
                        if (terminar - final_ordinaria > 0):
                            hextras += (terminar - final_ordinaria)
                        hordinarias = (24 + terminar - empezar - hextras)

                    # Archivar variantes que no permiten nocturnidad y hora salida anterior o igual a entrada:
                    # (terminar - empezar <= 0) and (record.nocturnidad_ok == False)
                    else: archivar = True


                    # Archivar o escribir valores del Cálculo coste y venta por variante:
                    if archivar == True:
                        va.write({'active':False})
                    else:
                        pvp = (hordinarias * record.pt_hora_ordinaria.list_price) + (hextras * record.pt_hora_extra.list_price)
                        coste = (hordinarias * record.pt_hora_ordinaria.standard_price) + (
                                hextras * record.pt_hora_extra.standard_price)
                        if (va.lst_price != pvp) or (va.standard_price != coste):
                            va.write({'lst_price': pvp, 'standard_price': coste})
