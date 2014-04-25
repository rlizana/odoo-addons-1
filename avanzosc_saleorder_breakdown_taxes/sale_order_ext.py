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
            
        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id, {'tax_breakdown_ids':[(6,0,[])]})
            
            for line in order.order_line:
                for tax in line.tax_id:
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                        
                    breakdown_ids = breakdown_obj.search(cr, uid,[('sale_id','=', order.id),
                                                                  ('tax_id', '=', tax.id)])                                              
                    if not breakdown_ids:
                        line_vals = {'sale_id': order.id,
                                     'tax_id': tax.id,
                                     'untaxed_amount': line.price_subtotal,
                                     'taxation_amount': line.price_subtotal * tax.amount,
                                     'total_amount': line.price_subtotal * (1 + tax.amount)
                                     }
                        breakdown_obj.create(cr, uid, line_vals)     
                    else:
                        breakdown = breakdown_obj.browse(cr, uid, breakdown_ids[0])   
                        untaxed_amount = line.price_subtotal + breakdown.untaxed_amount
                        taxation_amount = untaxed_amount * tax.amount #val + breakdown.taxation_amount
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

sale_order()