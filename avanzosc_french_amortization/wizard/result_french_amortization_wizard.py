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
 
class result_french_amortization_wizard(osv.osv_memory):

    _name = 'result.french.amortization.wizard'
    _description = "Result French Amortization Wizard"
 
    _columns = {# Capital Solicitado
                'requested_capital': fields.float('Requested Capital', digits=(9,2), readonly=True),
                # Interes
                'interest': fields.float('Interest', digits=(9,2), readonly=True),
                # Años
                'years':fields.integer('Years', readonly=True),
                # Cuota
                'quota': fields.float('Quota', digits=(9,2), readonly=True),
         }
    
    def result_french_amortization_wizard(self, cr, uid, ids, context=None):
                
        return {'type': 'ir.actions.act_window_close'}

    
result_french_amortization_wizard()