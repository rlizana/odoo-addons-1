# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price1 = fields.Float(
        string='First price', digits=dp.get_precision('Product Price'))
    price2 = fields.Float(
        string='Second price', digits=dp.get_precision('Product Price'))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    price1 = fields.Float(
        string='First price', digits=dp.get_precision('Product Price'))
    price2 = fields.Float(
        string='Second price', digits=dp.get_precision('Product Price'))
