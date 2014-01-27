# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields

class product_product(osv.osv):
    
    _inherit = 'product.product'
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        response = super(product_product, self).search(cr, uid, args, offset, limit, order, context, count)
        search_term = False
        product_supplierinfo = self.pool.get('product.supplierinfo')
        
        for arg in args:
            if arg[0] == 'name':
                search_term = arg[2]
        if search_term and (type(response)==type([])):
            product_ids = []
            supinfo_ids = product_supplierinfo.search(cr, uid,['|',('product_name','ilike', search_term),('product_code','ilike', search_term)])
            products = product_supplierinfo.read(cr, uid, supinfo_ids, ['product_id'])
            for product_id in products:
                if product_id['product_id']:
                    product_ids.append(product_id['product_id'][0])
            response.extend([element for element in product_ids if element not in response])
        
        return response
    
product_product()