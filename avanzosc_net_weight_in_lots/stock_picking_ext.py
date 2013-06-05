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
import decimal_precision as dp
from tools.translate import _
#
class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    def action_process(self, cr, uid, ids, context=None):
        prodlot_obj = self.pool.get('stock.production.lot')
        move_obj = self.pool.get('stock.move')
        if context is None: context = {}
        if ids:
            for picking in self.browse(cr,uid,ids):
                if picking.type == 'in':
                    for move in picking.move_lines:
                        if not move.prodlot_id:        
                            name = picking.name[3:8] + '-' + move.product_id.default_code   
                            prodlot_id = prodlot_obj.create(cr, uid, {'name': name,
                                                                      'product_id': move.product_id.id,
                                                                      'active': True})
                            move_obj.write(cr, uid, [move.id], {'prodlot_id': prodlot_id})
 
        return super(stock_picking,self).action_process(cr,uid,ids,context)
        
stock_picking()
