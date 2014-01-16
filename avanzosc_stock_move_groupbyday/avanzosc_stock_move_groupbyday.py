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

from osv import fields, osv

class stock_move(osv.osv):

    _inherit = 'stock.move'

    def _calculate_day(self, cr, uid, ids, field_name, arg, context=None):
        res = {}

        for id in ids:
            date = self.browse(cr, uid, id, context).date.split(" ")
            day_date = date[0]
            res[id] = day_date
        return res

    _columns = {

        'day':fields.function(_calculate_day, method=True, type="char", size=64, store=True, string="Date Planned by day"),

    }

stock_move()


