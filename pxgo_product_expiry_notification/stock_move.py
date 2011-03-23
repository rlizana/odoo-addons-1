# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""inherits fromk stock_move for checks expired prodlots"""

from osv import osv
from tools.translate import _

class stock_move(osv.osv):
    """inherits fromk stock_move for checks expired prodlots"""
    _inherit = "stock.move"

    def _check_prodlot_expiration(self, cr, uid, ids):
        """checks if prodlot is expired and is trying move it to internal or customer location"""
        for move in self.browse(cr, uid, ids):
            if move.prodlot_id and move.location_dest_id:
                if move.prodlot_id.expired and move.location_dest_id.usage in ['internal', 'customer']:
                    return False
        return True

    _constraints = [
    (_check_prodlot_expiration, 'Cannot move an expired production lot to internal or customer location', ['expired']),
    ]

    def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False, loc_id=False, context={}):
        """overwrites this event for shows a warning if the production lot selected is expired"""
        if not prodlot_id or not loc_id:
            return {}
        res = super(stock_move, self).onchange_lot_id(cr, uid, ids, prodlot_id = prodlot_id, product_qty = product_qty, loc_id = loc_id, context = context)
        if 'warning' in res and len(res['warning']) > 0:
            return res
        else:
            obj_prodlot_id = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id)
            if obj_prodlot_id.expired:
                res['warning'] = {
                    'title': _('Production Lot Expired!'),
                    'message': _('This production lot is expired'),
                        }
                return {'warning': res['warning']}
        return res

stock_move()
