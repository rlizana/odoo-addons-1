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

class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        sale_obj = self.pool.get('sale.order')
        stock_obj = self.pool.get('stock.picking')
        
        for sale_id in sale_obj.search(cr, uid, [('invoice_ids','in',ids)], context=context):
            for stock_id in stock_obj.search(cr, uid, [('sale_id','=',sale_id)], context=context):
                stock_obj.write(cr, uid, stock_id, {'invoice_state':'2binvoiced'}, context=context)
            
        return super(account_invoice, self).unlink(cr, uid, ids, context=context)
    
account_invoice()