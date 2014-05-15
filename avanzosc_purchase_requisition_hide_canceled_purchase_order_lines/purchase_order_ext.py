
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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
from osv import osv, fields
from tools.translate import _


class purchase_order(osv.osv):

    _inherit = 'purchase.order'
    
    def write(self, cr, uid, ids, vals, context=None):  
        purchase_line_obj = self.pool.get('purchase.order.line')
        found_draft = False
        found_cancel = False
        if vals.has_key('state'):
            my_state = vals.get('state')
            if my_state == 'draft':
                found_draft = True
            else:
                if my_state == 'cancel':
                    found_cancel = True
                    
        result = super(purchase_order,self).write(cr, uid, ids, vals, context=context)
        
        if ids:
            if found_draft or found_cancel:
                for purchase in self.browse(cr,uid,ids,context=context):
                    if purchase.order_line:
                        for line in purchase.order_line:
                            if found_draft:
                                purchase_line_obj.write(cr,uid,[line.id],{'purchase_canceled': False})
                            else:
                                purchase_line_obj.write(cr,uid,[line.id],{'purchase_canceled': True})
                                
        
        return result


purchase_order()