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
#
class crm_lead(osv.osv):

    _inherit = 'crm.lead'
    
    def write(self, cr, uid, ids, vals, context=None):
        crm_phonecall_obj = self.pool.get('crm.phonecall')
        if vals == None:
            vals = {}   
        if vals.has_key('partner_name'):
            partner_name = vals.get('partner_name')  
            for lead in self.browse(cr,uid,ids):
                crm_phonecall_ids = crm_phonecall_obj.search(cr, uid,[('opportunity_id','=',lead.id)])
                if crm_phonecall_ids:
                    for crmphone_call_id in crm_phonecall_ids:
                        crm_phonecall_obj.write(cr,uid,[crmphone_call_id],{'partner_name': partner_name})     
        if vals.has_key('contact_name'):
            contact_name = vals.get('contact_name')  
            for lead in self.browse(cr,uid,ids):
                crm_phonecall_ids = crm_phonecall_obj.search(cr, uid,[('opportunity_id','=',lead.id)])
                if crm_phonecall_ids:
                    for crmphone_call_id in crm_phonecall_ids:
                        crm_phonecall_obj.write(cr,uid,[crmphone_call_id],{'contact_name': contact_name})                        
        if vals.has_key('mobile'):
            mobile = vals.get('mobile')  
            for lead in self.browse(cr,uid,ids):
                crm_phonecall_ids = crm_phonecall_obj.search(cr, uid,[('opportunity_id','=',lead.id)])
                if crm_phonecall_ids:
                    for crmphone_call_id in crm_phonecall_ids:
                        crm_phonecall_obj.write(cr,uid,[crmphone_call_id],{'partner_mobile': mobile})                        
        if vals.has_key('partner_id'):
            partner_id = vals.get('partner_id')  
            for lead in self.browse(cr,uid,ids):
                crm_phonecall_ids = crm_phonecall_obj.search(cr, uid,[('opportunity_id','=',lead.id)])
                if crm_phonecall_ids:
                    for crmphone_call_id in crm_phonecall_ids:
                        crm_phonecall_obj.write(cr,uid,[crmphone_call_id],{'partner_id': partner_id})                       
        if vals.has_key('partner_address_id'):
            partner_address_id = vals.get('partner_address_id')  
            for lead in self.browse(cr,uid,ids):
                crm_phonecall_ids = crm_phonecall_obj.search(cr, uid,[('opportunity_id','=',lead.id)])
                if crm_phonecall_ids:
                    for crmphone_call_id in crm_phonecall_ids:
                        crm_phonecall_obj.write(cr,uid,[crmphone_call_id],{'partner_address_id': partner_address_id})

        return super(crm_lead,self).write(cr, uid, ids, vals, context)

crm_lead()
