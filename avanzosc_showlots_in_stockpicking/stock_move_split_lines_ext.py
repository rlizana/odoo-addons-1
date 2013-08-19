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
import decimal_precision as dp

class stock_move_split_lines_exist(osv.osv_memory):
    
    _inherit = "stock.move.split.lines"

    _columns = {'quantity_available': fields.float('Quantity Available', digits_compute=dp.get_precision('Product UoM')),
                'quantity': fields.float('Quantity', digits_compute=dp.get_precision('Product UoM')),
                }
    
    _defaults = {'quantity': lambda self, cr, uid, c: c.get('quantity', False),
                 }
    
    def onchange_showlot_quantity_available(self, cr, uid, ids, prodlot_id, quantity_available, context=None):
        lot_obj = self.pool.get('stock.production.lot')
        res={} 
        if prodlot_id:
            lot = lot_obj.browse(cr,uid,prodlot_id)
            res = {'quantity_available': lot.stock_available}

        return {'value': res}   

stock_move_split_lines_exist()