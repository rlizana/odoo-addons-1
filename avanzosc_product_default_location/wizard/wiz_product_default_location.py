# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2013 Avanzosc <http://www.avanzosc.com>
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
from osv import osv
from osv import fields
from tools.translate import _
import netsvc
 
class wiz_product_default_location(osv.osv_memory):
    
    _name="wiz.product.default.location"
    _description = "Wiz Product Default Location"
    
    _columns = {'name':fields.char('Name', size=64, readonly=True),
                'data_ids':fields.one2many('wiz.product.default.location.line', 'wiz_product_default_location_id', 'Products'),
                }
    
    def default_get(self, cr, uid, fields, context=None):
        res={}
        vals = []
        if context is None:
            context = {}  
        product_obj = self.pool.get('product.product')
        product_ids = product_obj.search(cr, uid,[('default_code','=', False)])
        if not product_ids:
            raise osv.except_osv(_('Wizard Warning'), _('No products found without default location'))
        else:
            for product in product_obj.browse(cr,uid,product_ids):
                line_vals = {'product_id': product.id
                             }
                vals.append(line_vals)
                        
        res = {'name': 'Default Location',
               'data_ids': vals
               }
        return res
    
    def do_assign_default_location(self, cr, uid, ids, context = None):  
        product_obj = self.pool.get('product.product')
        if ids:
            for line in self.browse(cr,uid,ids):
                if line.data_ids:
                    for data in line.data_ids:
                        if data.default_location_id:
                            product_obj.write(cr,uid,[data.product_id.id],{'default_location': data.default_location_id.id})

                             
        return {'type': 'ir.actions.act_window_close'}
  

wiz_product_default_location()