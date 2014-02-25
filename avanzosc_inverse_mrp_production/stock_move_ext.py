# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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

from datetime import datetime
from osv import osv, fields
import decimal_precision as dp
from tools import float_compare
from tools.translate import _
import netsvc
import time
import tools


class stock_move(osv.osv):
    
    _inherit = 'stock.move'
    

    def onchange_quantity(self, cr, uid, ids, product_id, product_qty, product_uom, product_uos):
        """ On change of product quantity finds UoM and UoS quantities
        @param product_id: Product id
        @param product_qty: Changed Quantity of product
        @param product_uom: Unit of measure of product
        @param product_uos: Unit of sale of product
        @return: Dictionary of values
        """
        result = {
                  'product_uos_qty': 0.00
          }

        if (not product_id) or (product_qty <=0.0):
            return {'value': result}

        product_obj = self.pool.get('product.product')
        uos_coeff = product_obj.read(cr, uid, product_id, ['coef_amount'])

        if product_uos and product_uom and (product_uom != product_uos):
            result['product_uos_qty'] = product_qty / uos_coeff['coef_amount']
        else:
            result['product_uos_qty'] = product_qty

        return {'value': result}

    def onchange_uos_quantity(self, cr, uid, ids, product_id, product_uos_qty, product_uos, product_uom):
        """ On change of product quantity finds UoM and UoS quantities
        @param product_id: Product id
        @param product_uos_qty: Changed UoS Quantity of product
        @param product_uom: Unit of measure of product
        @param product_uos: Unit of sale of product
        @return: Dictionary of values
        """
        result = {
                  'product_qty': 0.00
          }

        if (not product_id) or (product_uos_qty <=0.0):
            return {'value': result}

        product_obj = self.pool.get('product.product')
        uos_coeff = product_obj.read(cr, uid, product_id, ['coef_amount'])

        if product_uos and product_uom and (product_uom != product_uos):
            result['product_qty'] = product_uos_qty * uos_coeff['coef_amount']
        else:
            result['product_qty'] = product_uos_qty

        return {'value': result}
        
stock_move()