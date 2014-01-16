# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2014 AvanzOSC S.L. (Oihane) All Rights Reserved
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv, fields
import decimal_precision as dp

class product_template(osv.osv):
    
    _inherit = 'product.template'
    
    _columns = {
            'uos_list_price': fields.float('Sale Price', digits_compute=dp.get_precision('Sale Price')),
        }
    
    _defaults = {
            'uos_list_price': lambda *a: 1,
        }
    
    def onchange_uos_list_price(self, cr, uid, ids, uos_list_price, coef_amount, context=None):
        
        if uos_list_price:
            list_price = uos_list_price / coef_amount 
            return {'value':{'list_price': list_price}}

        return {}

product_template()

class product_product(osv.osv):
    
    _inherit = 'product.product'
    
    def onchange_uos_list_price(self, cr, uid, ids, uos_list_price, coef_amount, context=None):
        
        if uos_list_price:
            list_price = uos_list_price / coef_amount 
            return {'value':{'list_price': list_price}}

        return {}
product_product()