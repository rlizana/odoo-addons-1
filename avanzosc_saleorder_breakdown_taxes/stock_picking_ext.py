# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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

from osv import osv, fields
import decimal_precision as dp
from tools.translate import _


class stock_picking(osv.osv):

    _inherit = 'stock.picking'
    
    _columns = {# Impuestos desglosados
                'tax_breakdown_ids':fields.one2many('tax.breakdown','picking_id','Tax Breakdown'),
                }
    
    def _calc_breakdown_taxes(self, cr, uid, ids, context=None):
        if not context:
            context = {}
            
        breakdown_obj = self.pool.get('tax.breakdown')
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
            
        for picking in self.browse(cr, uid, ids, context=context):
            if picking.type == 'out':
                self.write(cr, uid, picking.id, {'tax_breakdown_ids':[(6,0,[])]})
                taxes_datas = {}
                for line in picking.move_lines:
                    if line.sale_line_id:
                        if line.sale_line_id.tax_id:
                            for tax in line.sale_line_id.tax_id:
                                found = 0
                                for data in taxes_datas:        
                                    datos_array = taxes_datas[data]
                                    tax_id = datos_array['tax_id']
                                    price_subtotal = datos_array['price_subtotal']
                                    if tax_id == tax.id:
                                        found = 1
                                        price_subtotal = price_subtotal + line.sale_line_id.price_subtotal
                                        taxes_datas[data].update({'price_subtotal': price_subtotal,})
                                if found == 0:
                                    taxes_datas[(tax.id)] = {'tax_id': tax.id, 'price_subtotal': line.sale_line_id.price_subtotal} 
                            
                        
                if taxes_datas:
                    for data in taxes_datas:        
                        datos_array = taxes_datas[data]
                        tax_id = datos_array['tax_id']
                        price_subtotal = datos_array['price_subtotal']
                        tax = tax_obj.browse(cr,uid,tax_id)
                        taxation_amount = price_subtotal * tax.amount
                        total_amount = price_subtotal + taxation_amount
                        vals = {'picking_id': picking.id,
                                'tax_id': tax_id,
                                'untaxed_amount': price_subtotal,
                                'taxation_amount': taxation_amount,
                                'total_amount': total_amount
                                }
                        breakdown_obj.create(cr,uid,vals,context=context)         
        
        return True
    
    def write(self, cr, uid, ids, data, context=None):
        if not context:
            context = {}

        data.update({'tax_breakdown_ids':[(6,0,[])]})
        super(stock_picking, self).write(cr, uid, ids, data, context=context)
        self._calc_breakdown_taxes(cr, uid, ids, context=context)

        return True
    
    def refresh_tax_breakdown(self, cr, uid, ids, context=None):
        
        self.write(cr, uid, ids, {'tax_breakdown_ids':[(6,0,[])]})
        
        return True
    
stock_picking()

class stock_move(osv.osv):
    
    _inherit = 'stock.move'
    
    def create(self, cr, uid, data, context=None):
        if not context:
            context = {}

        move_id = super(stock_move, self).create(cr, uid, data, context=context)
            
        if 'picking_id' in data:
            picking_obj = self.pool.get('stock.picking')
            picking_obj.write(cr, uid, [data['picking_id']], {'tax_breakdown_ids':[(6,0,[])]})
        
        return move_id
    
stock_move()
    
