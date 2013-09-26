
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 25/09/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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
from tools.translate import _


class wiz_assign_pdl (osv.osv_memory):
    
    def _seleclocat_func (self,cr,uid,context):
        
        #get all locations for selection
        obj = self.pool.get('stock.location')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['name', 'id'], context)
        res = [(r['id'], r['name']) for r in res]
        return res
    
    _name = 'wiz.assign.pdl'
    _description = 'Wizard to Assign Product Default Location'
    
    _columns = {
                'def_location': fields.many2one('stock.location','Default Location', selection=_seleclocat_func, size=300, help=_('Only Products with an empty location will be updated')), 
        }

    
    def action_pdl_assign (self, cr, uid, ids, context):
        
        if context is None:
            context = {}
        def_loc = self.browse(cr,uid,ids[0]).def_location
        active_ids=[]
        if context['active_ids']:
            active_ids = context['active_ids']
        if active_ids != []:
            product_obj= self.pool.get('product.product')
            for product_id in active_ids:
                product_reg = product_obj.browse(cr, uid, product_id)
                if not product_reg.default_location:
                    product_obj.write(cr, uid, product_id, {'default_location' : def_loc.id})
        value = {
                 'type': 'ir.actions.close_window',
                }   
        return value
    
wiz_assign_pdl ()