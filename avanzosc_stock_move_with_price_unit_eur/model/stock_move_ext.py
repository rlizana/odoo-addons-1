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
from tools.translate import _
import decimal_precision as dp

class StockMove(osv.osv):
    _inherit = 'stock.move'

    _columns = {
        'price_unit_eur': fields.float('Unit Price EUR', readonly=True, digits_compute= dp.get_precision('Account')),
    }

    def create(self, cr, uid, data, context=None):
        currency_obj = self.pool.get('res.currency')
        new_id = super(StockMove, self).create(cr, uid, data, context)
        if context is None:
            context = {}
        move = self.browse(cr, uid, new_id, context=context)
        if move.price_unit:
            if move.price_unit > 0 and move.purchase_line_id:
                ctx = context.copy()
                ctx['date'] = move.purchase_line_id.order_id.date_order
                price_unit_eur = currency_obj.compute(
                    cr, uid, move.company_id.currency_id.id,
                    move.purchase_line_id.order_id.pricelist_id.currency_id.id,
                    move.price_unit, context=ctx)
                vals = {'price_unit_eur': price_unit_eur}
                self.write(cr,uid, [move.id], vals, context=context)
        return new_id

    def write(self, cr, uid, ids, vals, context=None):
        purchase_line_obj = self.pool.get('purchase.order.line')
        if 'price_unit' in vals:
            price_unit =  vals.get('price_unit')
            if price_unit:
                if price_unit > 0:
                    purchase_line = False
                    move = self.browse(cr, uid, ids[0], context=context)
                    if 'purchase_line_id' in vals:
                        purchase_line_id = vals.get('purchase_line_id')
                        if purchase_line_id:
                            purchase_line = purchase_line_obj.browse(cr, uid, purchase_line_id, context=context)
                    if not purchase_line:
                        if move.purchase_line.id:
                            purchase_line = move.purchase_line_id
                    if purchase_line:
                        ctx = context.copy()
                        ctx['date'] = purchase_line.order_id.date_order
                        price_unit_eur = currency_obj.compute(
                            cr, uid, move.company_id.currency_id.id,
                            purchase_line.order_id.pricelist_id.currency_id.id,
                            price_unit, context=ctx)
                        vals.update({'price_unit_eur': price_unit_eur})
        return super(StockMove, self).write(cr, uid, ids, vals, context=context)

StockMove()
