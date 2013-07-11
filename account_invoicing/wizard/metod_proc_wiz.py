
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 09/07/2013
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

import wizard
from osv import fields, osv
import pooler
import netsvc

class inv_method_wizard (osv.osv_memory):
    
    _name = 'inv.method.wizard'
    _description = 'Invoice Methodologies Wizard'
    
    def action_create_meth(self, cr, uid, ids, *args):
        
        active_ids=[]
        if args[0]['active_ids']:
            active_ids = args[0]['active_ids']
        if active_ids != []:
            method_obj= self.pool.get('inv.method')
            wf_service = netsvc.LocalService("workflow")
            for inv_id in active_ids:
                met_reg = method_obj.browse(cr, uid, inv_id)
                if met_reg.state != 'close':
                    method_obj.write(cr, uid, inv_id, {'state':'close'})
                    wf_service.trg_create(uid, 'inv.metod', inv_id, cr)
        value = {
                 'type': 'ir.actions.close_window',
                }   
        return value
    
inv_method_wizard()