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

from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
from osv import osv, fields
import decimal_precision as dp
from tools.translate import _


class sale_order(osv.osv):

    _inherit = 'sale.order'
    
    _columns = {# Impuestos desglosados
                'tax_breakdown_ids':fields.one2many('tax.breakdown','sale_id','Tax Breakdown'),
                }
    
    def _calc_breakdown_taxes(self, cr, uid, ids, context=None):
        if not context:
            context = {}
            
        breakdown_obj = self.pool.get('tax.breakdown')
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
            
        for order in self.browse(cr, uid, ids, context=context):
            cur = order.pricelist_id.currency_id
            self.write(cr, uid, order.id, {'tax_breakdown_ids':[(6,0,[])]})
            
            for line in order.order_line:
                for tax in line.tax_id:
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.order_id.partner_invoice_id.id, line.product_id, line.order_id.partner_id)
                    
                    val = 0.0
                    for c in taxes['taxes']:
                        val += c.get('amount', 0.0)
                        
                    breakdown_ids = breakdown_obj.search(cr, uid,[('sale_id','=', order.id),
                                                                  ('tax_id', '=', tax.id)])                                              
                    if not breakdown_ids:
                        total_amount = val + line.price_subtotal
                        line_vals = {'sale_id': order.id,
                                     'tax_id': tax.id,
                                     'untaxed_amount': line.price_subtotal,
                                     'taxation_amount': val,
                                     'total_amount': total_amount
                                     }
                        breakdown_obj.create(cr, uid, line_vals)     
                    else:
                        breakdown = breakdown_obj.browse(cr, uid, breakdown_ids[0])   
                        untaxed_amount = line.price_subtotal + breakdown.untaxed_amount
                        taxation_amount = val + breakdown.taxation_amount
                        total_amount = untaxed_amount + taxation_amount
                        breakdown_obj.write(cr,uid,[breakdown.id],{'untaxed_amount': untaxed_amount,
                                                                   'taxation_amount': taxation_amount,
                                                                   'total_amount': total_amount})
            
                
        
        return True
    
    def action_wait(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        
        self._calc_breakdown_taxes(cr, uid, ids, context=context)
        
        return super(sale_order, self).action_wait(cr, uid, ids, context)
    
    def button_dummy(self, cr, uid, ids, context=None):
        
        super(sale_order,self).button_dummy(cr, uid, ids, context=context)
        
        if ids:
            self._calc_breakdown_taxes(cr, uid, ids, context=context)

        return True
    
#    def _sale_order_compute_all(self, cr, uid, tax_id, taxes, price_unit, quantity, address_id=None, product=None, partner=None, force_excluded=False):
#        account_tax_obj = self.pool.get('account.tax')
#        """
#        :param force_excluded: boolean used to say that we don't want to consider the value of field price_include of
#            tax. It's used in encoding by line where you don't matter if you encoded a tax with that boolean to True or
#            False
#        RETURN: {
#                'total': 0.0,                # Total without taxes
#                'total_included: 0.0,        # Total with taxes
#                'taxes': []                  # List of taxes, see compute for the format
#            }
#        """
#        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
#        totalin = totalex = round(price_unit * quantity, precision)
#        tin = []
#        tex = []
#        for tax in taxes:
#            if tax.id == tax_id:
#                if not tax.price_include or force_excluded:
#                    tex.append(tax)
#                else:
#                    tin.append(tax)
#        if tin == [] and tex == []:
#            return {
#                'total': 0,
#                'total_included': 0,
#                'taxes': 0
#            }
#        tin = account_tax_obj.compute_inv(cr, uid, tin, price_unit, quantity, address_id=address_id, product=product, partner=partner)
#        for r in tin:
#            totalex -= r.get('amount', 0.0)
#        totlex_qty = 0.0
#        try:
#            totlex_qty = totalex/quantity
#        except:
#            pass
#        tex = account_tax_obj._compute(cr, uid, tex, totlex_qty, quantity, address_id=address_id, product=product, partner=partner)
#        for r in tex:
#            totalin += r.get('amount', 0.0)
#        return {
#            'total': totalex,
#            'total_included': totalin,
#            'taxes': tin + tex
#        }

    
sale_order()