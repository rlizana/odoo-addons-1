# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields
from datetime import datetime
#
class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    def write(self, cr, uid, ids, vals, context={}):
        entra = False
        if context.has_key('__last_update'):
            if context.get('__last_update').keys() != []:
                entra=True
        account_invoice_line_obj = self.pool.get('account.invoice.line')
        context2 = context
        res = super(account_invoice, self).write(cr, uid, ids, vals, context=context)
        if entra:     
            for invoice in self.browse(cr,uid,ids):
                if invoice.invoice_line:
                    if invoice.date_invoice:
                        
                        my_date = datetime.strptime(str(invoice.date_invoice),'%Y-%m-%d')
                        my_year = my_date.year
                        my_month = my_date.month
                        if my_month == 1:
                            my_month2 = 'january'
                        if my_month == 2:
                            my_month2 = 'february'
                        if my_month == 3:
                            my_month2 = 'march'      
                        if my_month == 4:
                            my_month2 = 'april'               
                        if my_month == 5:
                            my_month2 = 'may'
                        if my_month == 6:
                            my_month2 = 'june'
                        if my_month == 7:
                            my_month2 = 'july'
                        if my_month == 8:
                            my_month2 = 'august'
                        if my_month == 9:
                            my_month2 = 'september'
                        if my_month == 10:
                            my_month2 = 'october'
                        if my_month == 11:
                            my_month2 = 'november'
                        if my_month == 12:
                            my_month2 = 'december'
                        for invoice_line in invoice.invoice_line:
                            account_invoice_line_obj.write(cr, uid, [invoice_line.id], {'date_invoice': invoice.date_invoice,
                                                                                        'year': my_year,
                                                                                        'month': my_month2}, context=context)
                    else:
                        for invoice_line in invoice.invoice_line:
                            account_invoice_line_obj.write(cr, uid, [invoice_line.id], {'date_invoice': False,
                                                                                        'year': False,
                                                                                        'month': False}, context=context)
        return res

account_invoice()
