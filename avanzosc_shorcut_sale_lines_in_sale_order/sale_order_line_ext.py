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

from osv import osv
from osv import fields
from tools.translate import _
import decimal_precision as dp
import netsvc
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import time
import netsvc

class sale_order_line(osv.osv):
    
    _inherit = 'sale.order.line'
     
    _columns = {# Pedido de venta
                'order_id': fields.many2one('sale.order', 'Order Reference', required=True, ondelete='cascade', select=True, readonly=True, states={'draft':[('readonly',False)]}), 
                'partner_id': fields.related('order_id', 'partner_id', type='many2one', relation='res.partner', store=True),
                'pricelist_id': fields.related('order_id', 'pricelist_id', type='many2one', relation='product.pricelist', store=True),
                'shop_id': fields.related('order_id', 'shop_id', type='many2one', relation='sale.shop', store=True),
                }

    _defaults = {'order_id': lambda self,cr,uid,context:context.get('sale_order_id', False),
                 'partner_id': lambda self,cr,uid,context:context.get('partner_id', False),
                 'pricelist_id': lambda self,cr,uid,context:context.get('pricelist_id', False),
                 'shop_id': lambda self,cr,uid,context:context.get('shop_id', False),
                 }
    
    def product_id_change_shortcutsaleline(self, cr, uid, ids, order_id, product, qty=0, uom=False, qty_uos=0, uos=False, name='',  lang=False, update_tax=True, packaging=False, flag=False, context=None):
        sale_order_obj = self.pool.get('sale.order')
        if context is None:
            context = {}   
        if not order_id:
            raise osv.except_osv(_('Error'), _('You must save the sale order before.'))
        
        sale_order = sale_order_obj.browse(cr,uid,order_id)
        
        return super(sale_order_line,self).product_id_change(cr, uid, ids, sale_order.pricelist_id.id, product, qty, uom, qty_uos, uos, name, sale_order.partner_id.id, lang, update_tax, sale_order.date_order, packaging, sale_order.fiscal_position.id, flag, context)
            

    def product_uom_change_shortcutsaleline(self, cursor, user, ids, order_id, product, qty=0,uom=False, qty_uos=0, uos=False, name='',lang=False, update_tax=True, context=None):  
        sale_order_obj = self.pool.get('sale.order')
        if context is None:
            context = {}   
        if not order_id:
            raise osv.except_osv(_('Error'), _('You must save the sale order before.'))
        
        sale_order = sale_order_obj.browse(cursor,user,order_id)
        
        return super(sale_order_line,self).product_uom_change(cursor, user, ids, sale_order.pricelist_id.id,product,qty,uom,qty_uos,uos,name, sale_order.partner_id.id,lang, update_tax, sale_order.date_order,context)
    
    def product_packaging_change_shortcutsaleline(self, cr, uid, ids, order_id, product, qty=0, uom=False, packaging=False, flag=False, context=None):
        sale_order_obj = self.pool.get('sale.order')
        if context is None:
            context = {}   
        if not order_id:
            raise osv.except_osv(_('Error'), _('You must save the sale order before.'))
        
        sale_order = sale_order_obj.browse(cr,uid,order_id)
        
        return super(sale_order_line,self).product_packaging_change(cr, uid, ids, sale_order.pricelist_id.id, product, qty, uom, sale_order.partner_id.id, packaging, flag, context)

            
sale_order_line()