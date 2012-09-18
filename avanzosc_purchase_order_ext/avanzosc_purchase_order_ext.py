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

from osv import osv, fields
from tools.translate import _

#
### Heredo esta clase para que cuando confirme el pedido de compra, si 
### hay algun producto que no tiene como proveedor al del pedido de
### compra, le asigna dicho proveedor al producto
class purchase_order(osv.osv):

    _name = 'purchase.order'
    _inherit = 'purchase.order'
 
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        todo = []
        for po in self.browse(cr, uid, ids, context=context):
            if not po.order_line:
                raise osv.except_osv(_('Error !'),_('You cannot confirm a purchase order without any lines.'))
            for line in po.order_line:
                #
                ### MODIFICACION ALFREDO
                #
                # Cojo los proveedores asignados al producto
                supplierinfo_obj = self.pool.get('product.supplierinfo')
                supplierinfo_ids = supplierinfo_obj.search(cr, uid,[('product_id','=', line.product_id.id)],                                                                 
                                                                    order='sequence')
                w_found = 0
                w_sequence = 0
                # Trato todos los proveedores asignados al producto         
                if supplierinfo_ids:
                    for supplierinfo in supplierinfo_ids:
                        supplierinfo_id = supplierinfo_obj.browse(cr, uid, supplierinfo) 
                        w_sequence = supplierinfo_id.sequence                
                        if supplierinfo_id.name.id == po.partner_id.id:
                            # Si el proveedor asignado al producto, es el mismo proveedor
                            # que el del pedido de compra, lo he encontrado
                            w_found = 1
                # Si no he encontrado el proveedor, doy de alta al producto que estoy tratando
                # el proveedor del pedido de compra
                if w_found == 0:
                    w_sequence = w_sequence + 1
                    values = {'name' : po.partner_id.id,
                              'sequence': w_sequence,
                              'product_uom': line.product_uom.id,
                              'min_qty': 1,
                              'product_id': line.product_id.id,
                              }
                    new_supplierinfo_id = supplierinfo_obj.create(cr, uid, values)
                #
                ### FIN MODIFICACION ALFREDO
                #
                if line.state=='draft':
                    todo.append(line.id)
            message = _("Purchase order '%s' is confirmed.") % (po.name,)
            self.log(cr, uid, po.id, message)
#        current_name = self.name_get(cr, uid, ids)[0][1]
        self.pool.get('purchase.order.line').action_confirm(cr, uid, todo, context)
        for id in ids:
            self.write(cr, uid, [id], {'state' : 'confirmed', 'validator' : uid})
        return True

purchase_order()