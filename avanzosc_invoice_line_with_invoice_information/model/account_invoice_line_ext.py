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

class AccountInvoiceLine(osv.osv):
    _inherit = 'account.invoice.line'

    _columns = {
        'number': fields.related('invoice_id','number', type='char', readonly=True, size=64, relation='account.invoice', store=True, string='Number'),
        'date_invoice':fields.related('invoice_id', 'date_invoice', type="date", string="Invoice Date", store=True),
        'standard_price': fields.float('Cost Price', readonly=True, digits_compute=dp.get_precision('Purchase Price')),
        'currency_id': fields.many2one('res.currency', "Currency", readonly=True),
        'price_unit_eur': fields.float('Unit Price EUR', readonly=True, digits_compute= dp.get_precision('Account')),
        'price_subtotal_eur': fields.float('Subtotal EUR', readonly=True, digits_compute= dp.get_precision('Account')),
        'invoice_type': fields.related('invoice_id', 'type', type="selection", selection=[('out_invoice','Customer Invoice'),('in_invoice','Supplier Invoice'),('out_refund','Customer Refund'),('in_refund','Supplier Refund')], string="Invoice type", store=True),
    }

    def create(self, cr, uid, data, context=None):
        product_obj = self.pool.get('product.product')
        invoice_obj = self.pool.get('account.invoice')
        if 'product_id' in data:
            product_id =  data.get('product_id')
            if product_id:
                product = product_obj.browse(cr, uid, product_id, context=context)
                data.update({'standard_price': product.standard_price})
        if 'invoice_id' in data:
            invoice_id =  data.get('invoice_id')
            if invoice_id:
                invoice = invoice_obj.browse(cr, uid, invoice_id, context=context)
                data.update({'currency_id': invoice.currency_id.id})
            
        return super(AccountInvoiceLine, self).create(cr,uid,data,context)

    def write(self, cr, uid, ids, vals, context=None):
        product_obj = self.pool.get('product.product')
        invoice_obj = self.pool.get('account.invoice')
        if 'product_id' in vals:
            product_id =  vals.get('product_id')
            if product_id:
                product = product_obj.browse(cr, uid, product_id, context=context)
                vals.update({'standard_price': product.standar_price})
        if 'invoice_id' in vals:
            invoice_id =  vals.get('invoice_id')
            if invoice_id:
                invoice = invoice_obj.browse(cr, uid, invoice_id, context=context)
                vals.update({'currency_id': invoice.currency_id.id})
        result = super(osv.osv, self).write(cr, uid, ids, vals, context=context)
        return result

AccountInvoiceLine()
