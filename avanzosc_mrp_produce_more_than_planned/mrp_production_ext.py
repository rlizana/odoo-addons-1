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
from tools import float_compare

class mrp_production(osv.osv):

    _inherit = 'mrp.production'
    
    def action_produce(self, cr, uid, production_id, production_qty, production_mode, context=None):
        """ To produce final product based on production mode (consume/consume&produce).
        If Production mode is consume, all stock move lines of raw materials will be done/consumed.
        If Production mode is consume & produce, all stock move lines of raw materials will be done/consumed
        and stock move lines of final product will be also done/produced.
        @param production_id: the ID of mrp.production object
        @param production_qty: specify qty to produce
        @param production_mode: specify production mode (consume/consume&produce).
        @return: True
        """
        stock_mov_obj = self.pool.get('stock.move')
        production = self.browse(cr, uid, production_id, context=context)

        produced_qty = 0
        for produced_product in production.move_created_ids2:
            if (produced_product.scrapped) or (produced_product.product_id.id <> production.product_id.id):
                continue
            produced_qty += produced_product.product_qty

        if production_mode in ['consume','consume_produce']:
            consumed_data = {}

            # Calculate already consumed qtys
            for consumed in production.move_lines2:
                if consumed.scrapped:
                    continue
                if not consumed_data.get(consumed.product_id.id, False):
                    consumed_data[consumed.product_id.id] = 0
                consumed_data[consumed.product_id.id] += consumed.product_qty

            # Find product qty to be consumed and consume it
            for scheduled in production.product_lines:

                # total qty of consumed product we need after this consumption
                total_consume = ((production_qty + produced_qty) * scheduled.product_qty / production.product_qty)

                # qty available for consume and produce
                qty_avail = scheduled.product_qty - consumed_data.get(scheduled.product_id.id, 0.0)

                if qty_avail <= 0.0:
                    # there will be nothing to consume for this raw material
                    continue

                raw_product = [move for move in production.move_lines if move.product_id.id==scheduled.product_id.id]
                if raw_product:
                    # qtys we have to consume
                    qty = total_consume - consumed_data.get(scheduled.product_id.id, 0.0)
                    if float_compare(qty, qty_avail, precision_rounding=scheduled.product_id.uom_id.rounding) == 1:
                        # if qtys we have to consume is more than qtys available to consume
                        prod_name = scheduled.product_id.name_get()[0][1]
                        raise osv.except_osv(_('Warning!'), _('You are going to consume total %s quantities of "%s".\nBut you can only consume up to total %s quantities.') % (qty, prod_name, qty_avail))
                    if qty <= 0.0:
                        # we already have more qtys consumed than we need 
                        continue

                    consumed = 0
                    rounding = raw_product[0].product_uom.rounding

                    # sort the list by quantity, to consume smaller quantities first and avoid splitting if possible
                    raw_product.sort(key=attrgetter('product_qty'))

                    # search for exact quantity
                    for consume_line in raw_product:
                        if tools.float_compare(consume_line.product_qty, qty, precision_rounding=rounding) == 0:
                            # consume this line
                            consume_line.action_consume(qty, consume_line.location_id.id, context=context)
                            consumed = qty
                            break

                    index = 0                        
                    # consume the smallest quantity while we have not consumed enough
                    while tools.float_compare(consumed, qty, precision_rounding=rounding) == -1 and index < len(raw_product):
                        consume_line = raw_product[index]
                        to_consume = min(consume_line.product_qty, qty - consumed) 
                        consume_line.action_consume(to_consume, consume_line.location_id.id, context=context)
                        consumed += to_consume
                        index += 1

        if production_mode == 'consume_produce':
            # To produce remaining qty of final product
            #vals = {'state':'confirmed'}
            #final_product_todo = [x.id for x in production.move_created_ids]
            #stock_mov_obj.write(cr, uid, final_product_todo, vals)
            #stock_mov_obj.action_confirm(cr, uid, final_product_todo, context)
            produced_products = {}
            for produced_product in production.move_created_ids2:
                if produced_product.scrapped:
                    continue
                if not produced_products.get(produced_product.product_id.id, False):
                    produced_products[produced_product.product_id.id] = 0
                produced_products[produced_product.product_id.id] += produced_product.product_qty

            for produce_product in production.move_created_ids:
                produced_qty = produced_products.get(produce_product.product_id.id, 0)
                subproduct_factor = self._get_subproduct_factor(cr, uid, production.id, produce_product.id, context=context)
                rest_qty = (subproduct_factor * production.product_qty) - produced_qty

                if rest_qty < production_qty:
                    self.write(cr,uid,[production_id],{'product_qty': production_qty})  
                    move_ids = stock_mov_obj.search(cr, uid,[('production_id','=', production.id)],limit=1,context=context)
                    if move_ids:
                        stock_mov_obj.write(cr,uid,move_ids,{'product_qty': production_qty}) 
                        move_ids = stock_mov_obj.search(cr, uid,[('move_dest_id','=', move_ids[0])],context=context)
                        if move_ids:
                            for move in stock_mov_obj.browse(cr,uid,move_ids,context=context):
                                new_qty = (production_qty * move.product_qty) / rest_qty
                                stock_mov_obj.write(cr,uid,[move.id],{'product_qty': new_qty}) 
                                move2_ids = stock_mov_obj.search(cr, uid,[('move_dest_id','=', move.id)],limit=1,context=context)
                                if move2_ids:
                                    move2 = stock_mov_obj.browse(cr,uid,move2_ids[0],context=context)
                                    new_qty = (production_qty * move2.product_qty) / rest_qty
                                    stock_mov_obj.write(cr,uid,[move2.id],{'product_qty': new_qty}) 

        
        return super(mrp_production, self).action_produce(cr, uid, production_id, production_qty, production_mode, context=context)

mrp_production()