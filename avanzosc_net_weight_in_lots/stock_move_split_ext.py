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
#
class stock_move_split(osv.osv):
    _name = 'stock.move.split'
    _inherit = 'stock.move.split'
     
    def split(self, cr, uid, ids, move_ids, context=None):
        stock_move_obj = self.pool.get('stock.move')
        stock_production_lot_obj = self.pool.get('stock.production.lot')
        new_move = super(stock_move_split,self).split(cr,uid,ids,move_ids,context)
        if move_ids:
            for stock_move in stock_move_obj.browse(cr,uid,move_ids):
                if stock_move.prodlot_id:
                    stock_production_lot_obj.write(cr,uid,[stock_move.prodlot_id.id],{'weight_net': stock_move.weight_net2})
                    
        if new_move:
            for stock_move in stock_move_obj.browse(cr,uid,new_move):
                if stock_move.prodlot_id:
                    stock_production_lot_obj.write(cr,uid,[stock_move.prodlot_id.id],{'weight_net': stock_move.weight_net2})
                    
        return new_move
        
stock_move_split()
