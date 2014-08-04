# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
import time
from tools.translate import _

class account_invoice(osv.osv):
    _inherit="account.invoice"
    
    
    def write(self, cr, uid, ids, vals, context=None):
        product_obj = self.pool['product.product']
        user_obj = self.pool.get('res.users')
        found = False
        if 'move_id' in vals:
            found = True
        result = super(account_invoice, self).write(cr, uid, ids, vals,
                                                    context)
        if found:
            invoice = self.browse(cr, uid, ids[0], context)
            if invoice.type == 'in_invoice' and invoice.move_id.id:
                if invoice.move_id.line_id:
                    for line in invoice.move_id.line_id:
                        if line.product_id and line.debit > 0:
                            if line.product_id.cost_method == 'average':
                                product = product_obj.browse(
                                    cr, uid, line.product_id.id, context)
                                cond = [('name', '=', 'Administrator'),
                                        ('active', '=', True),]
                                administrator_ids = user_obj.search(cr, uid, cond)
                                administrator = user_obj.browse(
                                    cr, uid, administrator_ids[0])
                                cond = [('name', 'ilike','Admin'),
                                        ('active', '=', True),
                                        ('company_id', '!=',
                                         administrator.company_id.id)]
                                child_user_ids = user_obj.search(
                                    cr, administrator.id, cond)
                                standard_price = 0
                                for child_user in user_obj.browse(
                                        cr,administrator.id,child_user_ids):
                                    product = product_obj.browse(
                                        cr, child_user.id, line.product_id.id)
                                    if product.standard_price:
                                        standard_price = (standard_price +
                                                          product.standard_price)
                                if standard_price > 0:
                                    standard_price = standard_price / 3
                                    nvals = {'parent_company_standard_price':
                                             standard_price}
                                    product_obj.write(
                                        cr, administrator.id, [line.product_id.id],
                                        nvals)

        return result

account_invoice()