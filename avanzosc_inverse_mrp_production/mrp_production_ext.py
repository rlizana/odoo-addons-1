# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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

from datetime import datetime
from osv import osv, fields
import decimal_precision as dp
from tools import float_compare
from tools.translate import _
import netsvc
import time
import tools
from operator import attrgetter

class mrp_production(osv.osv):
    
    _inherit = 'mrp.production'
    
    _columns = {# Inverse Production
                'inverse_production':fields.boolean('Inverse Production'), 
                # Lote de Producción
                'prodlot_id': fields.many2one('stock.production.lot','Lot'),
                }
    

    def write(self, cr, uid, ids, vals, context=None):
        stock_move_obj = self.pool.get('stock.move')
        if context is None:
            context = {}
         
        found = False   
        if vals.has_key('move_created_ids'):
            move_created_ids = vals['move_created_ids']
            if move_created_ids:
                found = True
            
        result = super(mrp_production, self).write(cr, uid, ids, vals, context=context)
        
        if ids:
            for production in self.browse(cr,uid,ids,context=context):
                if production.inverse_production and found == True:
                    for move in production.move_created_ids:
                        # Busco el producto a consumir de la OF
                        stock_move_obj.write(cr,uid,[move.id],{'prodlot_id': production.prodlot_id.id})
                        move_ids = stock_move_obj.search(cr, uid, [('move_dest_id','=',move.id)],limit=1)
                        if move_ids:
                            move2 = stock_move_obj.browse(cr,uid,move_ids[0])
                            stock_move_obj.write(cr,uid,[move2.id],{'product_qty': move.product_qty,
                                                                    'prodlot_id': production.prodlot_id.id})
                            # Busco el producto en albaran interno
                            move_ids = stock_move_obj.search(cr, uid, [('move_dest_id','=',move2.id)],limit=1)
                            if move_ids:
                                move3 = stock_move_obj.browse(cr,uid,move_ids[0])
                                stock_move_obj.write(cr,uid,[move3.id],{'product_qty': move.product_qty,
                                                                        'prodlot_id': production.prodlot_id.id})

        return result
    
    def action_compute(self, cr, uid, ids, properties=[], context=None):
        """ Computes bills of material of a product.
        @param properties: List containing dictionaries of properties.
        @return: No. of products.
        """
        if not context:
            context={}
        results = []
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        prod_line_obj = self.pool.get('mrp.production.product.line')
        workcenter_line_obj = self.pool.get('mrp.production.workcenter.line')
        
        if ids:
            production = self.browse(cr,uid,ids[0])
            if not production.inverse_production:
                results = super(mrp_production,self).action_compute(cr, uid, ids, properties=properties, context=context)
            else:
                cr.execute('delete from mrp_production_product_line where production_id=%s', (production.id,))
                cr.execute('delete from mrp_production_workcenter_line where production_id=%s', (production.id,))
                bom_point = production.bom_id
                bom_id = production.bom_id.id
                if not bom_point:
                    bom_id = bom_obj._bom_find(cr, uid, production.product_id.id, production.product_uom.id, properties)
                    if bom_id:
                        bom_point = bom_obj.browse(cr, uid, bom_id)
                        routing_id = bom_point.routing_id.id or False
                        self.write(cr, uid, [production.id], {'bom_id': bom_id, 'routing_id': routing_id})
    
                if not bom_id:
                    raise osv.except_osv(_('Error'), _("Couldn't find a bill of material for this product."))
                factor = uom_obj._compute_qty(cr, uid, production.product_uom.id, production.product_qty, bom_point.product_uom.id)
                res = bom_obj._bom_explode2(cr, uid, bom_point, factor / bom_point.product_qty, properties, routing_id=production.routing_id.id)
                results = res[0]
                results2 = res[1]
                for line in results:
                    line['production_id'] = production.id
                    prod_line_obj.create(cr, uid, line)
                for line in results2:
                    line['production_id'] = production.id
                    workcenter_line_obj.create(cr, uid, line)
                    
                results =  len(results)
                

        return results

    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms production order.
        @return: Newly generated Shipment Id.
        """
        if not context:
            context={}
        shipment_id = False
        wf_service = netsvc.LocalService("workflow")
        uncompute_ids = filter(lambda x:x, [not x.product_lines and x.id or False for x in self.browse(cr, uid, ids, context=context)])
        self.action_compute(cr, uid, uncompute_ids, context=context)
        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        
        
        for production in self.browse(cr, uid, ids, context=context):
            if not production.inverse_production:
                shipment_id = super(mrp_production,self).action_confirm(cr, uid, ids, context=context)
            else:
                if not production.prodlot_id:
                    raise osv.except_osv(_('Inverse Production Error'), _("You must define one lot"))  
                shipment_id = self._make_production_internal_shipment(cr, uid, production, context=context)
                
                for bom2 in production.bom_id.bom_lines:
    
                    produce_move_id = self._make_production_produce_line2(cr, uid, production, bom2.product_id,context=context)
                    move = move_obj.browse(cr,uid,produce_move_id,context=context)
                    if move.product_id.uos_id.id <> move.product_id.uom_id.id:
                        move_obj.write(cr,uid,[move.id],{'product_uos': move.product_id.uos_id.id,
                                                         'product_uos_qty': 1})
                    
                    # Take routing location as a Source Location.
                    source_location_id = production.location_src_id.id
                    if production.bom_id.routing_id and production.bom_id.routing_id.location_id:
                        source_location_id = production.bom_id.routing_id.location_id.id
        
                    for line in production.product_lines:
                        consume_move_id = self._make_production_consume_line(cr, uid, line, produce_move_id, source_location_id=source_location_id, context=context)
                        shipment_move_id = self._make_production_internal_shipment_line(cr, uid, line, shipment_id, consume_move_id,\
                                         destination_location_id=source_location_id, context=context)
                        self._make_production_line_procurement(cr, uid, line, shipment_move_id, context=context)
                        
                picking = picking_obj.browse(cr,uid,shipment_id)
                count = 0
                if picking.move_lines:
                    for move in picking.move_lines:
                        count = count + 1
                        
                res = production.product_qty % count
                qty = production.product_qty / count
                if res == 0:
                    for move in picking.move_lines:
                        move_obj.write(cr,uid,[move.id],{'product_qty': qty})
                        if move.move_dest_id:
                            move_obj.write(cr,uid,[move.move_dest_id.id],{'product_qty': qty})
                            
                else:
                    count2 = 0
                    assigned = 0
                    for move in picking.move_lines:
                        count2 = count2 + 1
                        if count == count2:
                            new_qty = production.product_qty - assigned
                            move_obj.write(cr,uid,[move.id],{'product_qty': new_qty})
                            if move.move_dest_id:
                                move_obj.write(cr,uid,[move.move_dest_id.id],{'product_qty': qty})
                        else:
                            assigned = assigned + qty
                            move_obj.write(cr,uid,[move.id],{'product_qty': qty})
                            if move.move_dest_id:
                                move_obj.write(cr,uid,[move.move_dest_id.id],{'product_qty': qty})

                 
                wf_service.trg_validate(uid, 'stock.picking', shipment_id, 'button_confirm', cr)
                production.write({'state':'confirmed'}, context=context)
                message = _("Manufacturing order '%s' is scheduled for the %s.") % (
                    production.name,
                    datetime.strptime(production.date_planned,'%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'),
                )
                self.log(cr, uid, production.id, message)
                
        #raise osv.except_osv(_('ERROR ALFREDO'), _("Mirar Displays"))
        
        return shipment_id
    
    def _make_production_produce_line2(self, cr, uid, production, product_id, context=None):
        stock_move = self.pool.get('stock.move')
        source_location_id = product_id.product_tmpl_id.property_stock_production.id
        destination_location_id = production.location_dest_id.id
        move_name = _('PROD: %s') + production.name 
        data = {
            'name': move_name,
            'date': production.date_planned,
            'product_id': product_id.id,
            'product_qty': 1,
            'product_uom': product_id.uom_id.id,
            'product_uos_qty': product_id.coef_amount or False,
            'product_uos': product_id.uos_id.id or False,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'move_dest_id': production.move_prod_id.id,
            'state': 'waiting',
            'company_id': production.company_id.id,
            'production_id': production.id
        }
        move_id = stock_move.create(cr, uid, data, context=context)
        
        return move_id
    
    def button_inverse_production(self, cr, uid, ids, *args):
        context={}
        wf_service = netsvc.LocalService("workflow")
        move_obj = self.pool.get('stock.move')
        lot_obj = self.pool.get('stock.production.lot')
        if ids:
            production = self.browse(cr,uid,ids[0])
            if not production.inverse_production:
                context.update({'active_ids':ids, 'active_id':ids[0], 'active_model':'mrp.production'})
                res = {'type': 'ir.actions.act_window',
                       'res_model': 'mrp.product.produce',
                       'view_type': 'form',
                       'view_mode': 'form',
                       'target': 'new',
                       'nodestroy': True,
                       'context':context
                       }
                return res 
            else:
                # Proceso movimientos de productos a consumir
                for move in production.move_lines:
                    move_obj.action_done(cr, uid, [move.id], context={})
                    
                # Creo lotes para movimientos a producir
                for move in production.move_created_ids:
                    line_vals = {'name': move.prodlot_id.name,
                                 'product_id': move.product_id.id,
                                 'date': datetime.now()
                                 }
                    lot_id = lot_obj.create(cr,uid,line_vals)
                    move_obj.write(cr,uid,[move.id],{'prodlot_id': lot_id})

                # Proceso movimientos de productos a producir   
                for move in production.move_created_ids:
                    move_obj.action_done(cr, uid, [move.id], context={})

                wf_service.trg_validate(uid, 'mrp.production', production.id, 'button_produce_done', cr)

        return True 
        
mrp_production()