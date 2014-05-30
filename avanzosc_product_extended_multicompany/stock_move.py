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
from osv import osv, fields
#import decimal_precision as dp
import time

from tools.translate import _

class stock_move(osv.osv):
    _inherit="stock.move"
    
    def write(self, cr, uid, ids, vals, context=None):
        print '*** ESTOY EN MI WRITE'
        user_obj = self.pool.get('res.users')
        product_obj = self.pool.get('product.product')
        found = False   
        if vals.has_key('state'):
            if vals['state']:
                if vals['state'] == 'done':
                    found = True
                    
        result = super(stock_move, self).write(cr, uid, ids, vals)
        
        if ids and found:
            print '*** ids: ' + str(ids)
            for move in self.browse(cr,uid,ids,context=context):
                print '*** move id: ' + str(move.id)
                print '*** product_id: ' + str(move.product_id)
                if move.product_id:
                    print '*** realizo mi tratamiento'
                    administrator_ids = user_obj.search(cr, uid, [('name','=','Administrator'),
                                                                  ('active','=', True),])
                    administrator = user_obj.browse(cr,uid,administrator_ids[0])
                    child_user_ids = user_obj.search(cr, administrator.id, [('name','ilike','Admin'),
                                                                            ('active','=', True),
                                                                            ('company_id','!=',administrator.company_id.id)
                                                                           ])   
                    standard_price = 0
                    for child_user in user_obj.browse(cr,administrator.id,child_user_ids):
                        product = product_obj.browse(cr,child_user.id,move.product_id.id)
                        if product.standard_price:
                            standard_price = standard_price + product.standard_price
                    if standard_price > 0:
                        standard_price = standard_price / 3      
                        product_obj.write(cr,administrator.id,[move.product_id.id],{'parent_company_standard_price': standard_price})
                
        return result
    
stock_move()