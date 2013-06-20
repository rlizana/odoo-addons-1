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
import decimal_precision as dp
from tools.translate import _
#
class stock_picking(osv.osv):

    _inherit = 'stock.picking'
    
    _columns = {# Taxas desglosadas
                'stock_picking_tax_breakdown_ids':fields.one2many('sale.order.tax.breakdown','stock_picking_id','Tax Breakdown'),
                }
    
    def create(self, cr, uid, data, context=None):
        breakdown_obj = self.pool.get('sale.order.tax.breakdown')
        sale_order_obj = self.pool.get('sale.order')
        sale_order_id = 0
        if data['type'] == 'out':
            if data.get('sale_id'):
                sale_order_id = data['sale_id']
          
        stock_picking_id = super(stock_picking, self).create(cr,uid,data,context)
        
        if sale_order_id > 0:
            sale_order = sale_order_obj.browse(cr,uid,sale_order_id)
            for breakdown in sale_order.sale_order_tax_breakdown_ids:
                breakdown_obj.write(cr,uid,[breakdown.id],{'stock_picking_id': stock_picking_id}) 
        
        return stock_picking_id    
        
    
stock_picking()