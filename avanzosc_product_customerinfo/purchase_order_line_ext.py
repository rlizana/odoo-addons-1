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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from osv import osv, fields
import netsvc
import pooler
from tools.translate import _
import decimal_precision as dp
from osv.orm import browse_record, browse_null
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class purchase_order_line(osv.osv):
    
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line' 

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, notes=False, context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}
        
        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'notes': notes or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_supplierinfo = self.pool.get('product.supplierinfo')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        if not pricelist_id:
            raise osv.except_osv(_('No Pricelist !'), _('You have to select a pricelist or a supplier in the purchase form !\nPlease set one before choosing a product.'))
        if not partner_id:
            raise osv.except_osv(_('No Partner!'), _('You have to select a partner in the purchase form !\nPlease set one partner before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        lang = res_partner.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        res['value'].update({'name': product.name, 'notes': notes or product.description_purchase})
        
        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id
        
        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            res['warning'] = {'title': _('Warning'), 'message': _('Selected UOM does not belong to the same category as the product UOM')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.date.context_today(cr,uid,context=context)

        qty = qty or 1.0
        supplierinfo = False
        supplierinfo_ids = product_supplierinfo.search(cr, uid, [('name','=',partner_id),('product_id','=',product.id),('is_customer','=',False)])
        if supplierinfo_ids:
            supplierinfo = product_supplierinfo.browse(cr, uid, supplierinfo_ids[0], context=context)
            if supplierinfo.product_uom.id != uom_id:
                res['warning'] = {'title': _('Warning'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
            min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
            if qty < min_qty: # If the supplier quantity is greater than entered from user, set minimal.
                res['warning'] = {'title': _('Warning'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                qty = min_qty

        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        res['value'].update({'date_planned': date_planned or dt, 'product_qty': qty})

        # - determine price_unit and taxes_id
        price = product_pricelist.price_get(cr, uid, [pricelist_id],
                    product.id, qty or 1.0, partner_id, {'uom': uom_id, 'date': date_order})[pricelist_id]
        
        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})

        return res

purchase_order_line()