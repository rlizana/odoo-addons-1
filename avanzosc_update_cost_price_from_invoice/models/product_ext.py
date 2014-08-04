# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp.osv import orm, fields


class ProductProduct(orm.Model):
    _inherit = 'product.product'

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        print '*** estoy en mi write, vals: ' + str(vals) + ', context: ' + str(context)
        if 'standard_price' in vals:
            if not 'stprice_from_invoice' in context:
                print '*** borro standard_price de vals'
                vals.pop('standard_price')

        return super(ProductProduct, self).write(cr, uid, ids, vals, context)
