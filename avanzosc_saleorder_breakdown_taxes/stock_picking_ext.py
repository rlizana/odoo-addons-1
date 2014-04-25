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
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            val = 0.0
            
            for line in picking.move_lines:
                if line.sale_line_id:
                    cur = line.sale_line_id.order_id.pricelist_id.currency_id
                    price = line.sale_line_id.price_unit * (1 - (line.sale_line_id.discount or 0.0) / 100.0)
                    
                    taxes = tax_obj.compute_all(cr, uid, line.sale_line_id.tax_id, price, line.product_qty, line.sale_line_id.order_id.partner_invoice_id.id, line.product_id, line.sale_line_id.order_id.partner_id)
                    
                    val += cur_obj.round(cr, uid, cur, taxes['total_included'])
                    
            res[picking.id] = {'amount_total': val}
        return res
    
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for move in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[move.picking_id.id] = True
        return result.keys()
    
    _columns = {
                'amount_total': fields.function(_amount_all, digits_compute = dp.get_precision('Sale Price'), string='Total',
                                store = {
                                         'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['move_lines'], 10),
                                         'stock.move': (_get_order, ['product_qty', 'product_uos_qty'], 10),
                                }, help="The total amount."),
                # Impuestos desglosados
                'tax_breakdown_ids':fields.one2many('tax.breakdown', 'picking_id', 'Tax Breakdown'),
                }
    
    def _calc_breakdown_taxes(self, cr, uid, ids, context=None):
        if not context:
            context = {}
            
        breakdown_obj = self.pool.get('tax.breakdown')
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
            
        for picking in self.browse(cr, uid, ids, context=context):
            if picking.type == 'out':
                
                for line in picking.move_lines:
                    if line.sale_line_id:
                        cur = line.sale_line_id.order_id.pricelist_id.currency_id
                        for tax in line.sale_line_id.tax_id:
                            price = line.sale_line_id.price_unit * (1 - (line.sale_line_id.discount or 0.0) / 100.0)
                            taxes = tax_obj.compute_all(cr, uid, line.sale_line_id.tax_id, price, line.product_qty, line.sale_line_id.order_id.partner_invoice_id.id, line.product_id, line.sale_line_id.order_id.partner_id)
                                
                            breakdown_ids = breakdown_obj.search(cr, uid,[('picking_id','=', picking.id),
                                                                          ('tax_id', '=', tax.id)])
                            subtotal = cur_obj.round(cr, uid, cur, taxes['total'])
                                                                        
                            if not breakdown_ids:
                                line_vals = {'picking_id': picking.id,
                                             'tax_id': tax.id,
                                             'untaxed_amount': subtotal,
                                             'taxation_amount': cur_obj.round(cr, uid, cur, (subtotal * tax.amount)),
                                             'total_amount': cur_obj.round(cr, uid, cur, (subtotal * (1 + tax.amount)))
                                             }
                                breakdown_obj.create(cr, uid, line_vals)     
                            else:
                                breakdown = breakdown_obj.browse(cr, uid, breakdown_ids[0])   
                                untaxed_amount = subtotal + breakdown.untaxed_amount
                                taxation_amount = cur_obj.round(cr, uid, cur, (untaxed_amount * tax.amount))
                                total_amount = untaxed_amount + taxation_amount
                                breakdown_obj.write(cr, uid, [breakdown.id], {'untaxed_amount': untaxed_amount,
                                                                              'taxation_amount': taxation_amount,
                                                                              'total_amount': total_amount})
        
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
    
