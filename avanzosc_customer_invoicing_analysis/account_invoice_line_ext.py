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
class account_invoice_line(osv.osv):
    
    _inherit = 'account.invoice.line'
    
    def _get_year(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            if line.invoice_id.date_invoice:
                my_date = datetime.strptime(str(line.invoice_id.date_invoice),'%Y-%m-%d')
                my_year = my_date.year
                res[line.id] = str(my_year)
        return res
    
    def _get_month(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            if line.invoice_id.date_invoice:
                my_date = datetime.strptime(str(line.invoice_id.date_invoice),'%Y-%m-%d')
                my_month = my_date.month
                if my_month == 1:
                    res[line.id] = 'january'
                if my_month == 2:
                    res[line.id] = 'february'
                if my_month == 3:
                    res[line.id] = 'march'      
                if my_month == 4:
                    res[line.id] = 'april'               
                if my_month == 5:
                    res[line.id] = 'may'
                if my_month == 6:
                    res[line.id] = 'june'
                if my_month == 7:
                    res[line.id] = 'july'
                if my_month == 8:
                    res[line.id] = 'august'
                if my_month == 9:
                    res[line.id] = 'september'
                if my_month == 10:
                    res[line.id] = 'october'
                if my_month == 11:
                    res[line.id] = 'november'
                if my_month == 12:
                    res[line.id] = 'december'
                    
        return res
    
    
    _columns = {# Tipo factura
                'type': fields.related('invoice_id','type', type="selection", selection=[('out_invoice','Customer Invoice'),('in_invoice','Supplier Invoice'),('out_refund','Customer Refund'),('in_refund','Supplier Refund')], string='Type', store=True, readonly=True),
                # Fecha Factura
                'date_invoice': fields.related('invoice_id','date_invoice', type='date', relation='account.invoice', string='Date Invoice', store=True, readonly=True),
                # Area
                'area_id':fields.related('partner_id','area_id', type="many2one" ,relation='res.partner.area', string='Area', store=True, readonly=True),
                # Sector
                'sector_id':fields.related('partner_id','sector_id', type="many2one" ,relation='res.partner.sector', string='Sector', store=True, readonly=True),
                # Comercial
                'salesman_id':fields.related('invoice_id','user_id', type="many2one" ,relation='res.users', string='Salesman', store=True, readonly=True),      
                # Categoria del producto
                'categ_id':fields.related('product_id','categ_id', type="many2one" ,relation='product.category', string='Category', store=True, readonly=True),      
                # Año
                'year': fields.function(_get_year, string='year', store=True, type='char', size=4),
                # Mes
                'month': fields.function(_get_month, type='selection', selection=[('january','January'),('february','February'),('march','March'),('april','April'),('may','May'),('june','June'),('july','July'),('august','August'),('september','September'),('october','October'),('november','November'),('december','December')], string='Month',store=True),
                }

    def write(self, cr, uid, ids, vals, context={}): 
        context.update({'vengo_de_linea': True})
        res = super(account_invoice_line, self).write(cr, uid, ids, vals, context=context)

        return res
    
account_invoice_line()
