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

class AccountInvoice(osv.osv):
    _inherit = 'account.invoice'

    def action_number(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        invoice_line_obj = self.pool.get('account.invoice.line')
        result = super(AccountInvoice, self).action_number(cr, uid, ids, context=context)
        for invoice in self.browse(cr, uid, ids, context=context):
            for line in invoice.invoice_line:
                ctx = context.copy()
                ctx['date'] = line.invoice_id.date_invoice
                price_unit = currency_obj.compute(
                    cr, uid, line.company_id.currency_id.id,
                    line.invoice_id.currency_id.id, line.price_unit,
                    context=ctx)
                price_subtotal_eur = currency_obj.compute(
                    cr, uid, line.company_id.currency_id.id,
                    line.invoice_id.currency_id.id, line.price_subtotal,
                    context=ctx)
                vals = {'price_unit_eur': price_unit,
                        'price_subtotal_eur': price_subtotal_eur}
                invoice_line_obj.write(cr, uid, [line.id], vals)
        return result

AccountInvoice()
