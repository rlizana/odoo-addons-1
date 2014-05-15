
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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
from osv import osv, fields
from tools.translate import _

class purchase_requisition_line(osv.osv):

    _inherit = 'purchase.requisition.line'

    _columns = {# Proveedor por defecto
                'default_supplier': fields.many2one('res.partner', 'Default Supplier'),
                # Proveedor última compra
                'last_supplier_id':fields.related('product_id','last_supplier_id', type="many2one" ,relation='res.partner', string='Last Supplier', store=True, readonly=True),
                # Precio ultima compra
                'last_purchase_price': fields.related('product_id','last_purchase_price', type='float', string='Last purchase price', store=True, readonly=True),
                # Fecha ultima compra
                'last_purchase_date':fields.related('product_id', 'last_purchase_date', type="date", string="Last purchase date", store=True, readonly=True),
                }
    
    def create(self, cr, uid, data, context=None):
        product_obj = self.pool.get('product.product')
        line_id = super(purchase_requisition_line, self).create(cr, uid, data, context=context)
            
        line = self.browse(cr,uid,line_id,context=context)
        product = product_obj.browse(cr,uid,line.product_id.id,context=context)
        if product.seller_ids:
            sequence = 0
            default_supplier = 0
            for seller in product.seller_ids:
                if sequence == 0:
                    sequence = seller.sequence
                    default_supplier = seller.name.id
                else:
                    if seller.sequence < sequence:
                        sequence = seller.sequence
                        default_supplier = seller.name.id
            if default_supplier > 0:
                self.write(cr,uid,[line_id],{'default_supplier': default_supplier})

        return line_id

purchase_requisition_line()