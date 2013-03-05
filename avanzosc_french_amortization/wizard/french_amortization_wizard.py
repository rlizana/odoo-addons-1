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
 
class french_amortization_wizard(osv.osv_memory):

    _name = 'french.amortization.wizard'
    _description = "French Amortization Wizard"
 
    _columns = {# Capital Solicitado
                'requested_capital': fields.float('Requested Capital', digits=(9,2)),
                # Interes
                'interest': fields.float('Interest', digits=(9,2)),
                # Años
                'years':fields.integer('Years'),
         }


    def calculate_french_amortization_wizard(self, cr, uid, ids, context=None):
        wiz = self.browse(cr,uid,ids[0],context)
        cuota = self.pool.get('avanzosc.french.amortization').calculate_french_amortization(cr, uid, wiz.requested_capital, wiz.interest, wiz.years)                        

        res={'requested_capital': wiz.requested_capital,
             'interest': wiz.interest,
             'years': wiz.years,
             'quota': cuota
             }
        
        result_id = self.pool.get('result.french.amortization.wizard').create(cr, uid, res)
        
        return {'type': 'ir.actions.act_window',
                'res_model': 'result.french.amortization.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': context,
                'res_id': result_id,
                }
    
french_amortization_wizard()