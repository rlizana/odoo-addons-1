# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProductAttribute(models.Model):

    _inherit = 'product.attribute'

    attribute_code = fields.Char(string='Code')