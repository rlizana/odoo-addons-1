# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
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
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from tools.translate import _
from osv import osv, fields

class product_template(osv.osv):
    
    _inherit = 'product.template'
    
    def write(self, cr, uid, ids, vals, context=None):
        move_obj = self.pool.get('stock.move')
        product_obj = self.pool.get('product.product')
        
        if 'uom_po_id' in vals:
            new_uom = self.pool.get('product.uom').browse(cr, uid, vals['uom_po_id'], context=context)
            for product in self.browse(cr, uid, ids, context=context):
                old_uom = product.uom_po_id
                if old_uom.category_id.id != new_uom.category_id.id:
                    product_id = product_obj.search(cr, uid, [('product_tmpl_id','=',product.id)])
                    moves = move_obj.search(cr, uid, [('product_id','in',product_id)])
                    if len(moves) <> 0:
                        raise osv.except_osv(_('UoM categories Mismatch!'), _("New UoM '%s' must belong to same UoM category '%s' as of old UoM '%s'. If you need to change the unit of measure, you may desactivate this product from the 'Procurement & Locations' tab and create a new one.") % (new_uom.name, old_uom.category_id.name, old_uom.name,))
        return super(osv.osv, self).write(cr, uid, ids, vals, context=context)

product_template()