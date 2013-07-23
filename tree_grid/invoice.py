##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

class account_invoice_line(osv.osv):
    
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
        
    _columns = {'type':fields.related('invoice_id', 'type', type="selection", selection=[('out_invoice','Customer Invoice'),
                                                                                         ('in_invoice','Supplier Invoice'),
                                                                                         ('out_refund','Customer Refund'),
                                                                                         ('in_refund','Supplier Refund'),
                                                                                         ], string="Type"),
                'fiscal_position': fields.related('invoice_id', 'fiscal_position', type='many2one', relation='account.fiscal.position', string='Fiscal Position'),
                'address_invoice_id': fields.related('invoice_id', 'address_invoice_id', type='many2one', relation='res.partner.address', string='Invoice Address'),
                'currency_id': fields.related('invoice_id', 'currency_id', type='many2one', relation='res.currency', string='Currency'),
                'journal_id': fields.related('invoice_id', 'journal_id', type='many2one', relation='account.journal', string='Journal'),
                'company_id': fields.related('invoice_id','company_id',type='many2one',relation='res.company',string='Company', store=True, readonly=True),
                'partner_id': fields.related('invoice_id','partner_id',type='many2one',relation='res.partner',string='Partner',store=True)
                }
    _defaults = {'type': lambda self, cr, uid, c: c.get('type', False),
                 'fiscal_position': lambda self, cr, uid, c: c.get('fiscal_position', False),
                 'address_invoice_id': lambda self, cr, uid, c: c.get('address_invoice_id', False),
                 'currency_id': lambda self, cr, uid, c: c.get('currency_id', False),
                 'journal_id': lambda self, cr, uid, c: c.get('journal_id', False),
                 'company_id': lambda self, cr, uid, c: c.get('company_id', False),
                 'partner_id': lambda self, cr, uid, c: c.get('partner_id', False),
                 }
    
account_invoice_line()