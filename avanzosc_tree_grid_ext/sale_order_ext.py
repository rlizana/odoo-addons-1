# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
#    Date: 08/07/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv, fields

class sale_order_line(osv.osv):
    
    _inherit = 'sale.order.line'
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context={}):

        if not product:
            return {'value': {'th_weight': 0, 'product_packaging': False,
                'product_uos_qty': qty, 'tax_id':[]}, 'domain': {'product_uom': [],
                   'product_uos': []}, 'domain':{'product_uom':[]}}  
        
        res={}
        
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag)
        
        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        qty = qty or 0.0
        prod_uos = prod.uos_id.id
        if not uos:
            uos = prod_uos
            
        price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist], product, qty or 1.0, partner_id, dict(context, uom=uom,date=date_order, ))[pricelist]
        try:
            price = price / prod.uos_coeff
        except ZeroDivisionError:
            pass

        res['value']['product_uom_qty'] = qty
        res['value']['product_uos'] = uos
        res['value']['secondary_price'] = price
        res['value']['product_uos_qty'] = qty / prod.coef_amount
        
        value = res['value'] 
        value.update({'tax_id': value.get('taxes_id')}) 
        res.update({'value':value})

        return res

    
    def uos_change(self, cr, uid, ids, product_uos, product_uos_qty=0, product_id=None):
        product_obj = self.pool.get('product.product')
        if not product_id:
            return {'value': {'product_uom': product_uos,
                'product_uom_qty': product_uos_qty}, 'domain': {}}

        product = product_obj.browse(cr, uid, product_id)
        
        value = super(sale_order_line, self).uos_change(cr, uid, ids, product_uos, product_uos_qty, product_id)['value']
        
        product_uom_qty = product_uos_qty * product.coef_amount
        
        value.update({
                'product_uos': product.uos_id.id,
                'product_uom_qty': product_uom_qty, 
            })
        
        return {'value': value}

    def calculate_secondary_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for so_line in self.browse(cr, uid, ids, context=context):
            price = so_line.price_unit
            prod = self.pool.get('product.product').browse(cr, uid, so_line.product_id.id, context=context)
            try:
                price = price / prod.uos_coeff
            except ZeroDivisionError:
                pass

            res[so_line.id] = price
        return res
        
        
    _columns = {'secondary_price': fields.function(calculate_secondary_price, method=True, string='Price', type="float", store=False),
                }
    
    _defaults = {'product_uom_qty': 0,
                 'product_uos_qty': 0,
                 }
    
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        res = {}
        
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id, context)
        res['sec_qty'] = line.product_uom_qty
        res['sec_uom_id'] = line.product_uom.id
        
        return res
    
sale_order_line()