# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    Revision: --- nhomar.hernandez@netquatro.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from osv import osv
from osv import fields
from tools.translate import _
import time
import netsvc
import ir
from mx import DateTime
import pooler

class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"

    def _amount_line(self, cr, uid, ids, prop, unknow_none,unknow_dict):
        res = {}
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, line.price_unit * line.product_qty )
        return res

    _columns = {
        'discount': fields.float('Discount (%)', digits=(16,2), help="If you chose apply a discount for this way you will overide the option of calculate based on Price Lists, you will need to change again the product to update based on pricelists, this value must be between 0-100"),
        'price_unit': fields.float('Real Unit Price', required=True, digits=(16, 4), help="Price that will be used in the rest of accounting cycle"),
        'price_base': fields.float('Base Unit Price', required=True, digits=(16, 4), help="Price base taken to calc the discount, is an informative price to use it in the rest of the purchase cycle like reference for users"),
    }
    _defaults = {
        'discount': lambda *a: 0.0,
    }

    def discount_change(self, cr, uid, ids, product, discount, price_unit, product_qty, partner_id, price_base):
        if not product:
            return {'value': {'price_unit': 0.0,}}
        prod= self.pool.get('product.product').browse(cr, uid,product)
        lang=False
        res=[]
        #TODO Improve pending to offer discounts based in price lists selected on order.
        if res==[]:
            res = {'value': {'price_unit': price_base*(1-discount/100),'price_base': price_base}}
            return res

    def rpu_change(self, cr, uid, ids, rpu, discount):
        res = {'value': {'price_base': rpu*(1+discount/100)}}
        return res

    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position=False):
        """Copied from purchase/purchase.py and modified to take discount"""
        if not pricelist:
            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist in the purchase form !\nPlease set one before choosing a product.'))
        if not  partner_id:
            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))
        if not product:
            return {'value': {'price_unit': 0.0, 'name':'','notes':'', 'product_uom' : False}, 'domain':{'product_uom':[]}}
        prod= self.pool.get('product.product').browse(cr, uid,product)
        lang=False
        if partner_id:
            lang=self.pool.get('res.partner').read(cr, uid, partner_id)['lang']
        context={'lang':lang}
        context['partner_id'] = partner_id

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
        if not date_order:
            date_order = time.strftime('%Y-%m-%d')

        qty = qty or 1.0
        seller_delay = 0
        for s in prod.seller_ids:
            if s.name.id == partner_id:
                seller_delay = s.delay
                temp_qty = s.qty # supplier _qty assigned to temp
                if qty < temp_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    qty = temp_qty

        price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
                product, qty or 1.0, partner_id, {
                    'uom': uom,
                    'date': date_order,
                    })[pricelist]
        dt = (DateTime.now() + DateTime.RelativeDateTime(days=int(seller_delay) or 0.0)).strftime('%Y-%m-%d %H:%M:%S')
        prod_name = prod.partner_ref


        res = {'value': {'price_unit': price, 'price_base': price, 'name':prod_name, 'taxes_id':map(lambda x: x.id, prod.supplier_taxes_id),
            'date_planned': dt,'notes':prod.description_purchase,
            'product_qty': qty,
            'product_uom': uom}}
        domain = {}

        partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
        taxes = self.pool.get('account.tax').browse(cr, uid,map(lambda x: x.id, prod.supplier_taxes_id))
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        res['value']['taxes_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)

        res2 = self.pool.get('product.uom').read(cr, uid, [uom], ['category_id'])
        res3 = prod.uom_id.category_id.id
        domain = {'product_uom':[('category_id','=',res2[0]['category_id'][0])]}
        if res2[0]['category_id'][0] != res3:
            raise osv.except_osv(_('Wrong Product UOM !'), _('You have to select a product UOM in the same category than the purchase UOM of the product'))

        res['domain'] = domain
        return res

purchase_order_line()

class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"

    def _get_order(self, cr, uid, ids, context={}):
        """Copied from purchase/purchase.py"""
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    def inv_line_create(self, cr, uid, a, ol):
        res = super(purchase_order,self).inv_line_create(cr, uid, a, ol)
        res[2].update({'discount': ol.discount, 'price_unit': ol.price_base or 0.0,})
        return res

purchase_order()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    def _get_discount_invoice(self, cursor, user, move_line):
        '''Return the discount for the move line'''
        discount = 0.00
        if move_line and move_line.purchase_line_id:
            discount = move_line.purchase_line_id.discount
        return discount
    
    def action_invoice_create(self, cursor, user, ids, journal_id=False,
            group=False, type='out_invoice', context=None):
        '''Return ids of created invoices for the pickings'''
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        invoices_group = {}
        res = {}

        for picking in self.browse(cursor, user, ids, context=context):
            if picking.invoice_state != '2binvoiced':
                continue
            payment_term_id = False
            partner = picking.address_id and picking.address_id.partner_id
            if not partner:
                raise osv.except_osv(_('Error, no partner !'),
                    _('Please put a partner on the picking list if you want to generate invoice.'))

            if type in ('out_invoice', 'out_refund'):
                account_id = partner.property_account_receivable.id
                payment_term_id = self._get_payment_term(cursor, user, picking)
            else:
                account_id = partner.property_account_payable.id

            address_contact_id, address_invoice_id = \
                    self._get_address_invoice(cursor, user, picking).values()

            comment = self._get_comment_invoice(cursor, user, picking)
            if group and partner.id in invoices_group:
                invoice_id = invoices_group[partner.id]
                invoice = invoice_obj.browse(cursor, user, invoice_id)
                invoice_vals = {
                    'name': (invoice.name or '') + ', ' + (picking.name or ''),
                    'origin': (invoice.origin or '') + ', ' + (picking.name or '') + (picking.origin and (':' + picking.origin) or ''),
                    'comment': (comment and (invoice.comment and invoice.comment+"\n"+comment or comment)) or (invoice.comment and invoice.comment or ''),
                }
                invoice_obj.write(cursor, user, [invoice_id], invoice_vals, context=context)
            else:
                invoice_vals = {
                    'name': picking.name,
                    'origin': (picking.name or '') + (picking.origin and (':' + picking.origin) or ''),
                    'type': type,
                    'account_id': account_id,
                    'partner_id': partner.id,
                    'address_invoice_id': address_invoice_id,
                    'address_contact_id': address_contact_id,
                    'comment': comment,
                    'payment_term': payment_term_id,
                    'fiscal_position': partner.property_account_position.id
                    }
                cur_id = self.get_currency_id(cursor, user, picking)
                if cur_id:
                    invoice_vals['currency_id'] = cur_id
                if journal_id:
                    invoice_vals['journal_id'] = journal_id
                invoice_id = invoice_obj.create(cursor, user, invoice_vals,
                        context=context)
                invoices_group[partner.id] = invoice_id
            res[picking.id] = invoice_id
            for move_line in picking.move_lines:
                if move_line.state == 'cancel':
                    continue
                origin = move_line.picking_id.name
                if move_line.picking_id.origin:
                    origin += ':' + move_line.picking_id.origin
                if group:
                    name = (picking.name or '') + '-' + move_line.name
                else:
                    name = move_line.name

                if type in ('out_invoice', 'out_refund'):
                    account_id = move_line.product_id.product_tmpl_id.\
                            property_account_income.id
                    if not account_id:
                        account_id = move_line.product_id.categ_id.\
                                property_account_income_categ.id
                else:
                    account_id = move_line.product_id.product_tmpl_id.\
                            property_account_expense.id
                    if not account_id:
                        account_id = move_line.product_id.categ_id.\
                                property_account_expense_categ.id
                price_unit = self._get_price_unit_invoice(cursor, user,
                        move_line, type)
                discount = self._get_discount_invoice(cursor, user, move_line)
                # mod Dani
                if discount > 0:
                    if discount == 100 :
                        price_unit = move_line.purchase_line_id.price_base
                    else:
                        price_unit = price_unit / (1-discount/100) 
                tax_ids = self._get_taxes_invoice(cursor, user, move_line, type)
                account_analytic_id = self._get_account_analytic_invoice(cursor,
                        user, picking, move_line)

                #set UoS if it's a sale and the picking doesn't have one
                uos_id = move_line.product_uos and move_line.product_uos.id or False
                if not uos_id and type in ('out_invoice', 'out_refund'):
                    uos_id = move_line.product_uom.id

                account_id = self.pool.get('account.fiscal.position').map_account(cursor, user, partner.property_account_position, account_id)
                invoice_line_id = invoice_line_obj.create(cursor, user, {
                    'name': name,
                    'origin': origin,
                    'invoice_id': invoice_id,
                    'uos_id': uos_id,
                    'product_id': move_line.product_id.id,
                    'account_id': account_id,
                    'price_unit': price_unit,
                    'discount': discount,
                    'quantity': move_line.product_uos_qty or move_line.product_qty,
                    'invoice_line_tax_id': [(6, 0, tax_ids)],
                    'account_analytic_id': account_analytic_id,
                    }, context=context)
                self._invoice_line_hook(cursor, user, move_line, invoice_line_id)

            invoice_obj.button_compute(cursor, user, [invoice_id], context=context,
                    set_total=(type in ('in_invoice', 'in_refund')))
            self.write(cursor, user, [picking.id], {
                'invoice_state': 'invoiced',
                }, context=context)
            self._invoice_hook(cursor, user, picking, invoice_id)
        self.write(cursor, user, res.keys(), {
            'invoice_state': 'invoiced',
            }, context=context)
        return res

stock_picking()

class account_invoice_line(osv.osv):
    _inherit='account.invoice.line'

    def _get_price_wd(self, cr, uid, ids, prop, unknow_none,unknow_dict):
        res = {}
        cur_obj=self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            if line.invoice_id:
                res[line.id] = line.price_unit * (1-(line.discount or 0.0)/100.0)
                cur = line.invoice_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
            else:
                res[line.id] = line.price_unit * (1-(line.discount or 0.0)/100.0)
        return res

    _columns={
    'price_wd': fields.function(_get_price_wd, method=True, string='Price With Discount',store=True, type="float", digits=(16, 4)),
    }
account_invoice_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
