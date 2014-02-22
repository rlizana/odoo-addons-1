# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2013 Avanzosc <http://www.avanzosc.com>
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields
from tools.translate import _
import time
import netsvc

class split_in_production_lot(osv.osv_memory):
    
    _inherit = 'stock.move.split'
    
    _columns = {
        'name': fields.char('Wizard Stock Move Split', size=64),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        lot_obj = self.pool.get('stock.production.lot')
        if context is None:
            context = {}
        vals = []
        
        res = super(split_in_production_lot, self).default_get(cr, uid, fields, context=context)
        location_id = res.get('location_id')
        qty = res.get('qty')
              
        
        if context.get('active_id'):
            move = self.pool.get('stock.move').browse(cr, uid, context['active_id'], context=context)
            if 'use_exist' in fields:
                context.update({'location_id':location_id})
                lot_ids = lot_obj.search(cr, uid,[('product_id','=', move.product_id.id),
                                                  ('stock_available', '>', 0)])
                if lot_ids:
                    context.update({'location_id':move.location_id.id})
                    for lot in lot_obj.browse(cr,uid,lot_ids,context=context):
                        
                        w_virtual_stock = 0
                        if lot.move_ids:
                            for m in lot.move_ids:
                                if m.location_id.name == 'Stock':
                                    if m.state not in ('cancel','done'):
                                        w_virtual_stock = w_virtual_stock + m.product_qty
                                        
                        w_stock_available = lot.stock_available - w_virtual_stock
                        
                        if w_stock_available >= qty and w_stock_available > 0:                                   
                            line_vals = {'prodlot_id': lot.id,
                                         'quantity_available': lot.stock_available
                                        }
                            vals.append(line_vals)
                    res.update({'line_exist_ids': vals})

                if context.get('lot_type'):
                    if context['lot_type'] == 'in':
                        res.update({'use_exist': False})
                    else:
                        res.update({'use_exist': True})
                else:
                    res.update({'use_exist': True})
        return res

    def split(self, cr, uid, ids, move_ids, context=None):
        """ To split stock moves into production lot

        :param move_ids: the ID or list of IDs of stock move we want to split
        """
        if context is None:
            context = {}
        assert context.get('active_model') == 'stock.move',\
             'Incorrect use of the stock move split wizard'
        inventory_id = context.get('inventory_id', False)
        prodlot_obj = self.pool.get('stock.production.lot')
        inventory_obj = self.pool.get('stock.inventory')
        move_obj = self.pool.get('stock.move')
        new_move = []
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                if data.use_exist:
                    lines = [l for l in data.line_exist_ids if l]
                    if move.picking_id:
                        if move.picking_id.type == 'out' or move.picking_id.type == 'internal':
                            quantity = 0
                            for line in lines:
                                if line.quantity > 0:
                                    if line.quantity > line.quantity_available:
                                        raise osv.except_osv(_('Error'), _('Introduced quantity greater than quantity available, for lot: %s') % (line.prodlot_id.name))
                                    else:
                                        quantity = quantity + line.quantity
                            if quantity > data.qty:
                                raise osv.except_osv(_('Error'), _('Sum amounts greater than quantity of the product'))
                    else:
                        quantity = 0
                        for line in lines:
                            if line.quantity > 0:
                                if line.quantity > line.quantity_available:
                                    raise osv.except_osv(_('Error'), _('Introduced quantity greater than quantity available, for lot: %s') % (line.prodlot_id.name))
                                else:
                                    quantity = quantity + line.quantity
                        if quantity > data.qty:
                            raise osv.except_osv(_('Error'), _('Sum amounts greater than quantity of the product'))               
                                
        return super(split_in_production_lot, self).split(cr, uid, ids, move_ids, context=context)


split_in_production_lot()