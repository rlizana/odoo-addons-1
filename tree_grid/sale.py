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

class sale_order_line(osv.osv):
    
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
            
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context={}):
#        if not pricelist:
#            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist or a supplier in the purchase form !\nPlease set one before choosing a product.'))
#        if not  partner_id:
#            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))
        if not product:
            return {'value': {'th_weight': 0, 'product_packaging': False,
                'product_uos_qty': qty, 'tax_id':[]}, 'domain': {'product_uom': [],
                   'product_uos': []}, 'domain':{'product_uom':[]}}           
            
        res = {}
        #prod= self.pool.get('product.product').browse(cr, uid, product)

        product_uom_pool = self.pool.get('product.uom')
        lang=False
        if partner_id:
            lang=self.pool.get('res.partner').read(cr, uid, partner_id, ['lang'])['lang']
        context={'lang':lang}
        context['partner_id'] = partner_id

        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
        prod_uom_po = prod.uom_po_id.id
        if uom <> prod_uom_po:
            uom = prod_uom_po
            
        prod_uos = prod.uos_id.id
        if not uos:
            uos = prod_uos
        if not date_order:
            date_order = time.strftime('%Y-%m-%d')
        qty = qty or 1.0
        seller_delay = 0
        prod_name = self.pool.get('product.product').name_get(cr, uid, [prod.id], context=context)[0][1]
        res = {}
        for s in prod.seller_ids:
            if s.name.id == partner_id:
                seller_delay = s.delay
                if s.product_uom:
                    temp_qty = product_uom_pool._compute_qty(cr, uid, s.product_uom.id, s.min_qty, to_uom_id=prod.uom_id.id)
                    uom = s.product_uom.id #prod_uom_po
                temp_qty = s.min_qty # supplier _qty assigned to temp
                if qty < temp_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    qty = temp_qty
                    res.update({'warning': {'title': _('Warning'), 'message': _('The selected supplier has a minimal quantity set to %s, you cannot purchase less.') % qty}})
        qty_in_product_uom = product_uom_pool._compute_qty(cr, uid, uom, qty, to_uom_id=prod.uom_id.id)
        price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
                    product, qty_in_product_uom or 1.0, partner_id, {
                        'uom': uom,
                        'date': date_order,
                        })[pricelist]
        dt = (datetime.now() + relativedelta(days=int(seller_delay) or 0.0)).strftime('%Y-%m-%d %H:%M:%S')


        res.update({'value': {'price_unit': price, 'name': prod_name,
            'tax_id':map(lambda x: x.id, prod.supplier_taxes_id),
             # 'date_planned': date_planned or dt,'notes': notes or prod.description_purchase,
            'product_uom_qty': qty,
            'product_uom': uom,
            'product_uos': uos}})
        
        
        domain = {}

        taxes = self.pool.get('account.tax').browse(cr, uid,map(lambda x: x.id, prod.supplier_taxes_id))
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        res['value']['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)

        res2 = self.pool.get('product.uom').read(cr, uid, [uom], ['category_id'])
        res3 = prod.uom_id.category_id.id
        domain = {'product_uom':[('category_id','=',res2[0]['category_id'][0])]}
        if res2[0]['category_id'][0] != res3:
            raise osv.except_osv(_('Wrong Product UOM !'), _('You have to select a product UOM in the same category than the purchase UOM of the product'))
        
        res['domain'] = domain       

        return res

    def _get_virtual_stock(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids):
            res[obj.id] = obj.product_id.virtual_available            
        return res
    
    def _get_real_stock(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for obj in self.browse(cr, uid, ids):
            res[obj.id] = obj.product_id.qty_available            
        return res

#    def uom_change(self, cr, uid, ids, product_uom, product_uom_qty=0, product_id=None):
#        product_obj = self.pool.get('product.product')
#        if not product_id:
#            return {'value': {'product_uos': product_uom,
#                'product_uos_qty': product_uom_qty}, 'domain': {}}
#
#        product = product_obj.browse(cr, uid, product_id)
#        value = {
#            'product_uos': product.uos_id.id,
#        }
#        
#        try:
#            value.update({
#                'product_uos_qty': product_uom_qty * product.uos_coeff,
#            })
#        except ZeroDivisionError:
#            pass
#        return {'value': value}

    def uos_change(self, cr, uid, ids, product_uos, product_uos_qty=0, product_id=None):
        product_obj = self.pool.get('product.product')
        if not product_id:
            return {'value': {'product_uom': product_uos,
                'product_uom_qty': product_uos_qty}, 'domain': {}}

        product = product_obj.browse(cr, uid, product_id)
        
        value = super(sale_order_line, self).uos_change(cr, uid, ids, product_uos, product_uos_qty, product_id)['value']
        
        value.update({
                'product_uos': product.uos_id.id
            })
        
        return {'value': value}

    def calculate_secondary_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for so_line in self.browse(cr, uid, ids, context=context):
            price = 0
            prod = self.pool.get('product.product').browse(cr, uid, so_line.product_id.id, context=context)
            try:
                price = prod.list_price / prod.uos_coeff
            except ZeroDivisionError:
                pass

            res[so_line.id] = price
        return res
        
    _columns = {
        'virtual_avl': fields.function(_get_virtual_stock, method=True, string='Virtual Stock'),
        'qty_avl': fields.function(_get_real_stock, method=True, string='Real Stock'),
        'secondary_price': fields.function(calculate_secondary_price,
                                        method=True,
                                        string='Price',
                                        type="float",
                                        store=False),
    }
    
    _defaults = {
        'product_uom_qty': 0,
        'product_uos_qty': 0,
    }
    
sale_order_line()