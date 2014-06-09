# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields
from tools.translate import _

class sale_tax_wizard(osv.osv_memory):
    _name = "sale.tax.wizard"
    _description = "Sale Tax Wizard"
    _columns = {
    }
    
    def update_sale_line_taxes(self, cr, uid, ids, context):
        res = {}
        order_line_obj = self.pool['sale.order.line']
        sale_obj = self.pool['sale.order']
        sale_reg = sale_obj.browse(cr, uid, context['active_id'], context)
        partner_id = sale_reg.partner_id.id
        if sale_reg['state'] == 'draft':
            for line in sale_reg.order_line:
                f_p_id=sale_reg.partner_id.property_account_position.id
                date=sale_reg.date_order
                vals = order_line_obj.product_id_change(cr, uid, line.id, 
                                                    sale_reg.pricelist_id.id, 
                                                    line.product_id.id,
                                                    qty=line.product_uom_qty,
                                                    uom=line.product_uom.id,
                                                    uos=line.product_uos.id, 
                                                    partner_id=partner_id,
                                                    fiscal_position=f_p_id,
                                                    date_order=date)
                if vals.get('value',False):
                    if 'tax_id' in vals['value']:
                        tax_id = vals['value']['tax_id']
                        order_line_obj.write(cr, uid, line.id, 
                                    {
                                     'tax_id': [(6,0,tax_id)]
                                     },context=context)
        return res

sale_tax_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: