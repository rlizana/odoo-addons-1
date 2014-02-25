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
        
        if ids and found == True:
            production = self.browse(cr,uid,ids[0],context=context)
            for move in production.move_created_ids:
                # Busco el producto a consumir de la OF
                move_ids = stock_move_obj.search(cr, uid, [('move_dest_id','=',move.id)])
                if move_ids:
                    move2 = stock_move_obj.browse(cr,uid,move_ids[0])
                    stock_move_obj.write(cr,uid,move2.id,{'product_qty': move.product_qty})
                    # Busco el producto en albaran interno
                    move_ids = stock_move_obj.search(cr, uid, [('move_dest_id','=',move2.id)])
                    if move_ids:
                        move3 = stock_move_obj.browse(cr,uid,move_ids[0])
                        stock_move_obj.write(cr,uid,move3.id,{'product_qty': move.product_qty})

        return result
    
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirms production order.
        @return: Newly generated Shipment Id.
        """
        shipment_id = False
        wf_service = netsvc.LocalService("workflow")
        uncompute_ids = filter(lambda x:x, [not x.product_lines and x.id or False for x in self.browse(cr, uid, ids, context=context)])
        self.action_compute(cr, uid, uncompute_ids, context=context)
        move_obj = self.pool.get('stock.move')
        for production in self.browse(cr, uid, ids, context=context):
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
                    
            wf_service.trg_validate(uid, 'stock.picking', shipment_id, 'button_confirm', cr)
            production.write({'state':'confirmed'}, context=context)
            message = _("Manufacturing order '%s' is scheduled for the %s.") % (
                production.name,
                datetime.strptime(production.date_planned,'%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'),
            )
            self.log(cr, uid, production.id, message)
        
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
    

        
mrp_production()