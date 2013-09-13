
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 13/09/2013
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

class proc_agreement_wizard (osv.osv_memory):
    
    _name = 'proc.agreement.wizard'
    _description = 'Process Agreement Wizard'
    
    def action_process_agree(self, cr, uid, ids, *args):
        
        active_ids=[]
        if args[0]['active_ids']:
            active_ids = args[0]['active_ids']
        if active_ids != []:
            agreement_obj= self.pool.get('inv.agreement')
            wf_service = netsvc.LocalService("workflow")
            for agree_id in active_ids:
                agree_reg = agreement_obj.browse(cr, uid, agree_id)
                if agree_reg.state == 'draft':
                    agreement_obj.set_process(cr, uid, [agree_id])
                    #wf_service.trg_create(uid, 'inv.agreement', agree_id, cr)
        value = {
                 'type': 'ir.actions.close_window',
                }   
        return value
    
    def action_stop_agree(self, cr, uid, ids, *args):
        
        active_ids=[]
        if args[0]['active_ids']:
            active_ids = args[0]['active_ids']
        if active_ids != []:
            agreement_obj= self.pool.get('inv.agreement')
            wf_service = netsvc.LocalService("workflow")
            for agree_id in active_ids:
                agree_reg = agreement_obj.browse(cr, uid, agree_id)
                if agree_reg.state == 'running':
                    agreement_obj.set_done(cr, uid, [agree_id])
                    #wf_service.trg_create(uid, 'inv.agreement', agree_id, cr)
        value = {
                 'type': 'ir.actions.close_window',
                }   
        return value
    
    def action_draft_agree(self, cr, uid, ids, *args):
        
        active_ids=[]
        if args[0]['active_ids']:
            active_ids = args[0]['active_ids']
        if active_ids != []:
            agreement_obj= self.pool.get('inv.agreement')
            wf_service = netsvc.LocalService("workflow")
            for agree_id in active_ids:
                agree_reg = agreement_obj.browse(cr, uid, agree_id)
                if agree_reg.state == 'done':
                    agreement_obj.set_draft(cr, uid, [agree_id])
                    #wf_service.trg_create(uid, 'inv.agreement', agree_id, cr)
        value = {
                 'type': 'ir.actions.close_window',
                }   
        return value
    
proc_agreement_wizard()