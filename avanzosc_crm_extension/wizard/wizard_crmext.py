# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
from tools.translate import _
import wizard
import pooler
import time        
class wizard_mrp_repair (wizard.interface):    
    
    def _action_open_window(self, cr, uid, data, context):

            value = {
                     'name': False,
                     'view_type': 'form',
                     'view_mode': 'tree,form',
                     'res_model': 'mrp.repair',
                     'type': 'ir.actions.act_window',
                     'domain': "[]",
                     }    
            return value
        
    def check_state(self, cr, uid, data, context):
            pool = pooler.get_pool(cr.dbname)
            crm_case_objs = pool.get('crm.case')
            cases = crm_case_objs.browse(cr, uid, data['ids'])
            crm_case_obj = crm_case_objs.browse(cr, uid, data['id'])
            user = pool.get('res.users').browse (cr,uid, uid)
            u_name = user.name
            driver = pool.get('res.users').browse (cr,uid,crm_case_obj.crm_user_id.id)
            d_name = driver.name
            vehicle = crm_case_obj.idvehicle
            vehi_id = crm_case_obj.idvehicle.id
            if crm_case_obj.description == False:
                crm_case_obj.description = ' '
            notes = crm_case_obj.idvehicle.name + ': ' +  crm_case_obj.name + "\n" + crm_case_obj.description
            if vehi_id >0: 
                vehicle= pool.get('fleet.vehicles').browse(cr, uid,vehi_id)
                product_id = vehicle.product_id.id
                if product_id != False: 
                    product_obj= pool.get('product.product').browse(cr,uid,product_id)
                    location_from = vehicle.location
                    location_to = pool.get ('stock.location').search(cr,uid,[('name', 'like', 'Taller')])
                    pool.get('fleet.vehicles').write(cr, uid, [vehi_id],{ 'location': location_to[0]})
                    
                    #añadir a history
                    for case in cases:
                        data = {    
                                'name': _('Open'),
                                'som': case.som.id,
                                'canal_id': case.canal_id.id,
                                'user_id': uid,
                                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'case_id': case.id,
                                'section_id': case.section_id.id,
                                }
                        
                        #añadir a communication history
                        obj = pool.get('crm.case.log')
                        if case.description:
                            crm_case_objs.write(cr, uid, case.id, {'description': d_name + ': ' + case.description ,
                    }, context=context)
                            #context ={'date' : case.create_date}
                            crm_case_objs.case_log(cr, uid, [case.id], email=False)
                            obj = pool.get('crm.case.history')
                            data['description'] =_('Accepted: Waiting for Vehicle')
                        obj.create(cr, uid, data, context)
                    
                    move_id = pool.get('stock.move').create(cr,uid,{ 
                                                      'product_id' : vehicle.product_id.id, 
                                                      'name' : crm_case_obj.name,
                                                      'location_id' : location_from.id,
                                                      'location_dest_id': location_to[0],
                                                      'product_uom': product_obj.product_tmpl_id.uom_id.id,
                                                      })
                    ref= pool.get('mrp.repair').create(cr,uid,{'name':  pool.get('ir.sequence').get(cr, uid, 'mrp.repair'), 'location_id' : location_from.id, 'location_dest_id' :  location_to[0], 'move_id' : move_id, 'product_id': product_id, 'case': crm_case_obj.id, 'internal_notes': notes })
                    crm_case_objs.write(cr,uid,[crm_case_obj.id],{'ref3': ref, 'state': 'pending'}) 
                    return 'next'
                else:
                    return 'display2'
            else:
                return 'display'

    form1 = '''<?xml version="1.0"?>
    <form string="Repair Case">
    <separator string="Create repair case with the defined vehicle?" colspan="4"/>
    </form>'''
    form1_fields = {}
    
    form2 = '''<?xml version="1.0"?>
    <form string="Repair Case">
    <separator string="Not vehicle defined!" colspan="4"/>
    </form>'''
    form2_fields = {}
    
    form3 = '''<?xml version="1.0"?>
    <form string="Repair Case">
    <separator string="Repair Order Created!" colspan="4"/>
    </form>'''
    form3_fields = {}
    
    form4 = '''<?xml version="1.0"?>
    <form string="Repair Case">
    <separator string="Vehicle has no product defined! The repair needs a product defined for it. " colspan="4"/>
    </form>'''
    form4_fields = {}
    
    states = {
            'init': {
                     'actions': [],
                     'result': {'type': 'form', 'arch':form1, 'fields':form1_fields, 'state': [('end', 'Cancel','gtk-cancel'),('create', 'Accept','gtk-ok')]}
                        },
            'create': {
                       'actions' : [],
                       'result' : {'type' : 'choice', 'next_state' : check_state}
                     },
            'display': {
                       'actions' : [], 
                       'result': {'type': 'form', 'arch':form2, 'fields':form2_fields, 'state': [('end', 'Accept','gtk-ok')]}
                       },
            'display2': {
                       'actions' : [], 
                       'result': {'type': 'form', 'arch':form4, 'fields':form4_fields, 'state': [('end', 'Accept','gtk-ok')]}
                       },                       
            'next' : {
                      'actions' : [], 
                      'result': {'type': 'form', 'arch':form3, 'fields':form3_fields, 'state': [('open', 'Accept','gtk-ok')]}
                      },
            'open' : {
                      'actions' : [], 
                      'result': {'type': 'action', 'action': _action_open_window, 'state':'end'}
                      }
            }
    
wizard_mrp_repair('wizard.crmext')
