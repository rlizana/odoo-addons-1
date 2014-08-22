# -*- encoding: utf-8 -*-
##############################################################################
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


class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        res = {}
        for po in self.browse(cr, uid, ids, context=context):
            if not po.order_line:
                res = super(purchase_order, self).wkf_confirm_order(
                    cr, uid, ids=ids, context=context)
                return res
            for line in po.order_line:
                # Search for supplierinfo lines
                supplierinfo_obj = self.pool.get('product.supplierinfo')
                supplierinfo_ids = supplierinfo_obj.search(
                    cr, uid,
                    [('product_id', '=', line.product_id.product_tmpl_id.id)],
                    order='sequence', context=context)
                w_found = False
                w_sequence = 0
                if supplierinfo_ids:
                    for supplierinfo in supplierinfo_ids:
                        supplierinfo_id = supplierinfo_obj.browse(
                            cr, uid, supplierinfo, context)
                        w_sequence = supplierinfo_id.sequence
                        if supplierinfo_id.name.id == po.partner_id.id:
                            # Provideer already asigned to product
                            w_found = True
                if not w_found:
                    # Create new product-provideer relation
                    w_sequence = w_sequence + 1
                    values = {'name': po.partner_id.id,
                              'sequence': w_sequence,
                              'product_uom': line.product_uom.id,
                              'min_qty': 1,
                              'product_code': line.product_id.default_code,
                              'product_id': line.product_id.product_tmpl_id.id,
                              }
                    supplierinfo_obj.create(cr, uid, values, context)
        res = super(purchase_order, self).wkf_confirm_order(cr, uid, ids=ids,
                                                            context=context)
        return res

purchase_order()
