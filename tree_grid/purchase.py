# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
#    Date: 05/06/2013
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

from osv import osv
from osv import fields

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import decimal_precision as dp

class purchase_order_line(osv.osv):
    _inherit="purchase.order.line"
    
#    def product_id_change(self, cr, uid, ids, pricelist, product, qty, uom,
#            partner_id, date_order=False, fiscal_position=False, date_planned=False,
#            name=False, price_unit=False, notes=False):
##        if not pricelist:
##            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist or a supplier in the purchase form !\nPlease set one before choosing a product.'))
##        if not  partner_id:
##            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))
#        if not product:
#            return {'value': {'price_unit': price_unit or 0.0, 'name': name or '',
#                'notes': notes or'', 'product_uom' : uom or False}, 'domain':{'product_uom':[]}}
#        res = {}
#        # prod= self.pool.get('product.product').browse(cr, uid, product)
#
#        product_uom_pool = self.pool.get('product.uom')
#        lang=False
#        if partner_id:
#            lang=self.pool.get('res.partner').read(cr, uid, partner_id, ['lang'])['lang']
#        context={'lang':lang}
#        context['partner_id'] = partner_id
#
#        prod = self.pool.get('product.product').browse(cr, uid, product, context=context)
#        prod_uom_po = prod.uom_po_id.id
#        if uom <> prod_uom_po:
#            uom = prod_uom_po
#        if not date_order:
#            date_order = time.strftime('%Y-%m-%d')
#        qty = qty or 1.0
#        seller_delay = 0
#
#        prod_name = self.pool.get('product.product').name_get(cr, uid, [prod.id], context=context)[0][1]
#        res = {}
#        for s in prod.seller_ids:
#            if s.name.id == partner_id:
#                seller_delay = s.delay
#                if s.product_uom:
#                    temp_qty = product_uom_pool._compute_qty(cr, uid, s.product_uom.id, s.min_qty, to_uom_id=prod.uom_id.id)
#                    uom = s.product_uom.id #prod_uom_po
#                temp_qty = s.min_qty # supplier _qty assigned to temp
#                if qty < temp_qty: # If the supplier quantity is greater than entered from user, set minimal.
#                    qty = temp_qty
#                    res.update({'warning': {'title': _('Warning'), 'message': _('The selected supplier has a minimal quantity set to %s, you cannot purchase less.') % qty}})
#        qty_in_product_uom = product_uom_pool._compute_qty(cr, uid, uom, qty, to_uom_id=prod.uom_id.id)
#        price = self.pool.get('product.pricelist').price_get(cr,uid,[pricelist],
#                    product, qty_in_product_uom or 1.0, partner_id, {
#                        'uom': uom,
#                        'date': date_order,
#                        })[pricelist]
#        dt = (datetime.now() + relativedelta(days=int(seller_delay) or 0.0)).strftime('%Y-%m-%d %H:%M:%S')
#
#
#        res.update({'value': {'price_unit': price, 'name': prod_name,
#            'taxes_id':map(lambda x: x.id, prod.supplier_taxes_id),
#            'date_planned': date_planned or dt,'notes': notes or prod.description_purchase,
#            'product_qty': qty,
#            'product_uom': uom}})
#        domain = {}
#
#        taxes = self.pool.get('account.tax').browse(cr, uid,map(lambda x: x.id, prod.supplier_taxes_id))
#        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
#        res['value']['taxes_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)
#
#        res2 = self.pool.get('product.uom').read(cr, uid, [uom], ['category_id'])
#        res3 = prod.uom_id.category_id.id
#        domain = {'product_uom':[('category_id','=',res2[0]['category_id'][0])]}
#        if res2[0]['category_id'][0] != res3:
#            raise osv.except_osv(_('Wrong Product UOM !'), _('You have to select a product UOM in the same category than the purchase UOM of the product'))
#        
#        res['domain'] = domain       
#
#        return res

    _columns = {'pricelist_id': fields.related('order_id', 'pricelist_id', type='many2one', relation='product.pricelist', string='Pricelist'),
                'partner_id': fields.related('order_id', 'partner_id', type='many2one', relation='res.partner', string='Customer'),
                'date_order':fields.related('order_id', 'date_order', type="date", string="Date"),
                'fiscal_position': fields.related('order_id', 'fiscal_position', type='many2one', relation='account.fiscal.position', string='Fiscal Position'),
                }
    _defaults = {'pricelist_id': lambda self, cr, uid, c: c.get('pricelist_id', False),
                 'partner_id': lambda self, cr, uid, c: c.get('partner_id', False),
                 'date_order': lambda self, cr, uid, c: c.get('date_order', False),
                 'fiscal_position': lambda self, cr, uid, c: c.get('fiscal_position', False),
                 }
    
    
purchase_order_line()