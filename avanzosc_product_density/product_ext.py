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

class product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
     
    _columns = {'density': fields.float('Density'),
                }
    
    def onchange_density(self, cr, uid, ids, density, uom_id, context=None):
        uom_obj = self.pool.get('product.uom')
        res={} 
        
        if density and uom_id:
            if density > 0:
                uom = uom_obj.browse(cr,uid,uom_id)
                # Si es peso
                if uom.category_id.id == 2:
                    volume = 1 / density
                    res = {'weight': 1,
                           'volume': volume,
                           }
                else:
                    # Si es volumen
                    if uom.category_id.id == 5:
                        res = {'weight': density,
                               'volume': 1,
                               }

        return {'value': res}   
        
product()
