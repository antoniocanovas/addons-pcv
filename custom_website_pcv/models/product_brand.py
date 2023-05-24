# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

MONTHS = [('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),
          ('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12')]


class ProductBrand(models.Model):
    _inherit = "product.brand"


    name = fields.Char(translate=True)
