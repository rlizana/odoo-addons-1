# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc (Daniel) <http://www.avanzosc.com>
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

from osv import fields,osv
import decimal_precision as dp
from datetime import datetime, timedelta
from tools.translate import _
import netsvc

class mrp_production(osv.osv):
    
    _inherit = 'mrp.production'
    _description = 'Manufacturing Order'
    
    def lot_control (self, cr, uid, ids, context=None):       
        production_id = ids[0]
        mrp_prod_obj = self.pool.get('mrp.production')
        prod_move_ids = self.pool.get('mrp.production')
        product_obj = self.pool.get('product.product')
        stock_move = self.pool.get('stock.move')
        production_reg = mrp_prod_obj.browse(cr,uid,production_id)
        stmove_list = production_reg.move_lines # lineas de movimiento de productos a consumir
        for move in stmove_list :
            product = move.product_id
            track_prod = product.track_production
            move_lot = move.prodlot_id
            if product.track_production and not move.prodlot_id: # Lot control
                 raise osv.except_osv(_('Warning!'), _('Lot not assigned! '))
        wf_service = netsvc.LocalService("workflow") # Load workflow
        wf_service.trg_validate(uid, 'mrp.production',production_id, 'button_produce', cr) # Next workflow step
        return True

mrp_production()
