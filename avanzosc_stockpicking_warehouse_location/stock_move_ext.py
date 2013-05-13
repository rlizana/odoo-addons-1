
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from osv import osv
from osv import fields

class stock_move(osv.osv):
    
    _name = 'stock.move'
    _inherit = 'stock.move'
    _order = 'date_expected desc, loc_row, loc_rack, loc_case, id'
    
    def _get_location(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for line in self.browse(cr, uid, ids, context=context):
            literal = ''
            if not line.loc_row:
                literal = literal + ';'
            else:
                literal = literal + line.loc_row + ';'
            if not line.loc_rack:
                literal = literal + ';'
            else:
                literal = literal + line.loc_rack + ';'
            if not line.loc_case:
                literal = literal + ';'
            else:
                literal = literal + line.loc_case            
            
            res[line.id] = literal

        return res

    _columns = {# Fila
                'loc_row':fields.related('product_id', 'loc_row', type='char', string='Row', store=True),
                # Estante
                'loc_rack':fields.related('product_id', 'loc_rack', type='char', string='Rack', store=True),
                # Caja
                'loc_case':fields.related('product_id', 'loc_case', type='char', string='Case', store=True),
                # Localizacion
                'location':fields.function(_get_location, method=True, string='Product Location', type="char", size=50),
                }
      
stock_move()
