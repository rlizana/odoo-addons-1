
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


class purchase_order_line(osv.osv):

    _inherit = 'purchase.order.line'

    def write(self, cr, uid, ids, vals, context=None): 
        requisition_obj = self.pool.get('purchase.requisition') 
        found = False
        if vals.has_key('state'):
            my_state = vals.get('state')
            if my_state in ('approved','confirmed'):
                found = True
                    
        result = super(purchase_order_line,self).write(cr, uid, ids, vals, context=context)
        
        if ids and found:
            for line in self.browse(cr,uid,ids,context=context):
                if line.order_id:
                    if line.order_id.requisition_id:
                        end = True
                        for purchase_line in line.order_id.requisition_id.purchase_order_line_ids:
                            if purchase_line.state not in ('approved','confirmed'):
                                if line.order_id.state != 'cancel':
                                    end = False
                        if end:
                            requisition_obj.write(cr,uid,[line.order_id.requisition_id.id],{'state': 'done'})
                            
        return result

purchase_order_line()