
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2012 Daniel (AvanzOSC). All Rights Reserved
#    
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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

from osv import fields,osv
from tools.translate import _

class mrp_repair(osv.osv): 

    _inherit = 'mrp.repair'
    
    def onchange_move_id(self, cr, uid, ids, prod_id=False, move_id=False, context=None):
        data = super(mrp_repair, self).onchange_move_id(cr, uid, ids, prod_id, move_id)
        if 'location_dest_id' in data ['value']:
            move = self.pool.get('stock.move').browse(cr, uid, move_id)
            data ['value']['location_dest_id'] = move.location_id.id
        return data
    
    def onchange_lot_id(self, cr, uid, ids, lot, product_id):
        data = super(mrp_repair, self).onchange_lot_id(cr, uid, ids, lot, product_id)
        if 'location_dest_id' in data ['value']:
            #move = self.pool.get('stock.move').browse(cr, uid, move_id)
            data ['value']['location_dest_id'] = data ['value']['location_id']
        return data
    
mrp_repair()

