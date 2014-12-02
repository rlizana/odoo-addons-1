# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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
from openerp.osv import orm


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def write(self, cr, uid, ids, vals, context=None):
        uom_obj = self.pool['product.uom']
        product_obj = self.pool['product.product']
        currency_obj = self.pool['res.currency']
        purchase_line_obj = self.pool['purchase.order.line']
        move_obj = self.pool['account.move']
        found = False
        if 'move_id' in vals:
            found = True
        if not ids[0]:
            return False
        result = super(AccountInvoice, self).write(cr, uid, ids, vals,
                                                   context=context)
        if found:
            invoice = self.browse(cr, uid, ids[0], context=context)
            if invoice.type == 'in_invoice' and invoice.move_id.id:
#                if invoice.move_id.line_id:
                for line in invoice.invoice_line:
                    product = line.product_id
                    if product and line.price_unit > 0:
                        if product.cost_method == 'average':
                            processed_qty = 0
                            purchase_lines = purchase_line_obj.search(
                                cr, uid, [('invoice_lines', '=', line.id)],
                                context=context)
                            for purchase_line in purchase_line_obj.browse(
                                    cr, uid, purchase_lines, context=context):
                                for move in purchase_line.move_ids:
                                    if move.state == 'done':
                                        processed_qty += move.product_qty
                            company_cur_id = invoice.company_id.currency_id.id
                            invoice_cur_id = invoice.currency_id.id
                            move_currency_id = line.company_id.currency_id.id
                            context['currency_id'] = move_currency_id
                            qty = uom_obj._compute_qty(
                                cr, uid, product.uom_id.id, line.quantity,
                                product.uom_id.id)
                            if qty > 0:
                                product_avail = (product.qty_available -
                                                 processed_qty)
                                product_price = line.price_unit
                                new_price = currency_obj.compute(
                                    cr, uid, invoice_cur_id, company_cur_id,
                                    product_price)
                                new_price = uom_obj._compute_price(
                                    cr, uid, product.uom_id.id, new_price,
                                    product.uom_id.id)
                                if product.qty_available <= 0:
                                    newstd_price = new_price
                                else:
                                    # Get the standard price
                                    amount_unit = product.price_get(
                                        'standard_price',
                                        context=context)[product.id]
                                    newstd_price = ((amount_unit *
                                                     product_avail) + \
                                                    (new_price * qty))/ \
                                                    (product_avail + qty)
                                # Write the field according to price type field
                                nvals = {'standard_price': newstd_price}
                                context.update({'stprice_from_invoice': True})
                                product_obj.write(cr, uid, [product.id], nvals,
                                                  context)

        return result
