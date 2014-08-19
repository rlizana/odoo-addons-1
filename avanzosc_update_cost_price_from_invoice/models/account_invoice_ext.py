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
                if invoice.move_id.line_id:
                    for line in invoice.move_id.line_id:
                        if line.product_id and line.debit > 0:
                            if line.product_id.cost_method == 'average':
                                product = product_obj.browse(
                                    cr, uid, line.product_id.id, context)
                                move_currency_id = line.company_id.currency_id.id
                                context['currency_id'] = move_currency_id
                                qty = uom_obj._compute_qty(
                                    cr, uid, line.product_id.uom_id.id, line.quantity,
                                    line.product_id.uom_id.id)
                                if qty > 0:
                                    product_avail = (product.qty_available -
                                                     line.quantity)
                                    product_currency = move_currency_id
                                    product_price = line.tax_amount / line.quantity
                                    new_price = currency_obj.compute(
                                        cr, uid, product_currency, move_currency_id,
                                        product_price)
                                    new_price = uom_obj._compute_price(
                                        cr, uid, line.product_id.uom_id.id, new_price,
                                        line.product_id.uom_id.id)
                                    if line.product_id.qty_available <= 0:
                                        newstd_price = new_price
                                    else:
                                        # Get the standard price
                                        amount_unit = product.price_get(
                                            'standard_price',
                                            context=context)[product.id]
                                        newstd_price = ((amount_unit * product_avail)\
                                            + (new_price * qty))/(product_avail + qty)
                                    # Write the field according to price type field
                                    nvals = {'standard_price': newstd_price}
                                    context.update({'stprice_from_invoice': True})
                                    product_obj.write(cr, uid, [product.id], nvals,
                                                      context)

        return result
