# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    06/02/2012
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the  GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
    
from osv import fields, osv
from tools.translate import _
import wizard
import pooler
import time

class alert_eval(osv.osv_memory):

    """Alert Evaluation"""
    _name = 'alert.eval'
    _description = 'Vehicle Alerts'
    _columns = {
                'vehicle': fields.many2one('fleet.vehicles', 'Vehicle'),
                'kmreal' : fields.integer('Real Milleage',help="If the value is 0, the current mileage will be used.",size=10)
                }
    
    def _alert_evaluate(self, cr, uid, data, context):
        res = {}
        odometro = self.browse(cr,uid,data[0]).kmreal  
        vehicle_id = self.browse(cr,uid,data[0]).vehicle.id
        pool = pooler.get_pool(cr.dbname)
        vehicle_prev_op = pool.get('vehicle.prev.op')
        vehicle_obj = pool.get('fleet.vehicles')
        preve_proc_obj = pool.get('preventive.proceed')
        if odometro != 0:
            vehicle_obj.write(cr, uid, vehicle_id, {'actodometer':odometro})
        vehicle_prev_op._alert_create(cr, uid, context)
        prevproc_list = preve_proc_obj.search(cr, uid, [('ivehicle', '=', vehicle_id), ('active', '=', True)])
        res = {
                 'name': False,
                 'view_type': 'form',
                 'view_mode': 'tree,form',
                 'res_model': 'preventive.proceed',
                 'type': 'ir.actions.act_window',
                 'domain': [('ivehicle', '=', vehicle_id),('active','=', True)],
                }  
        return res
    
alert_eval()

class wizard_alert_calc (wizard.interface):
    
    def _alert_check(self, cr, uid, data, context):
        res = {}
        pool = pooler.get_pool(cr.dbname)
        vehicle_prev_op = pool.get('vehicle.prev.op')
        vehicle_prev_op._alert_create(cr, uid,context)
        return res
            
    form1 = '''<?xml version="1.0"?>
    <form string="Alert evaluation wizard">
    <separator string="Calculate Alerts?" colspan="4"/>
    </form>'''
    form1_fields = {}
    
    form2 = '''<?xml version="1.0"?>
    <form string="Alert evaluation wizard">
    <separator string="Alerts evaluated and created!" colspan="4"/>
    </form>'''
    form2_fields = {}
    
    states = {
            'init': {
                     'actions': [_alert_check],
                     'result': {'type': 'form', 'arch':form1, 'fields':form1_fields, 'state': [('end', 'Cancel','gtk-cancel'),('calculate', 'Evaluate','gtk-ok')]}
                        },
            'calculate': {
                       'actions' : [], 
                       'result': {'type': 'form', 'arch':form2, 'fields':form2_fields, 'state': [('end', 'Accept','gtk-ok')]}
                       }
            }
    
wizard_alert_calc('calc.alert.wizard')

class wizard_vehi_alert_eval (wizard.interface):
    
    def _action_open_window(self, cr, uid, data, context):
        
        vehicle_id = data['form']['vehicles']
        value = {
                 'name': False,
                 'view_type': 'form',
                 'view_mode': 'tree,form',
                 'res_model': 'preventive.proceed',
                 'type': 'ir.actions.act_window',
                 'domain': [('ivehicle', '=', vehicle_id),('active','=', True)],
                }    
        return value
    
    def _alert_evaluate(self, cr, uid, data, context):
        res = {}
        odometro = data['form']['kmreal']
        vehicle_id = data['form']['vehicles']
        pool = pooler.get_pool(cr.dbname)
        vehicle_prev_op = pool.get('vehicle.prev.op')
        vehicle_obj = pool.get('fleet.vehicles')
        preve_proc_obj = pool.get('preventive.proceed') 
        if odometro != 0:
            vehicle_obj.write(cr, uid, vehicle_id, {'actodometer':odometro})
        vehicle_prev_op._alert_create(cr, uid, context)
        prevproc_list = preve_proc_obj.search(cr, uid, [('ivehicle', '=', vehicle_id), ('active', '=', True)])
        return {'vehi_alerts':prevproc_list,'vehicle':vehicle_id}

               
    form1 = '''<?xml version="1.0"?>
    <form string="Vehicle Alerts">
    <separator string="Choose vehicle and its real milleage" colspan="4"/>
    <field name="vehicles" width="150" height="50"/>
    <field name="kmreal" width="150"/>
    </form>'''
    form1_fields = {
    'vehicles': {
        'string': 'Vehicle',
        'type': 'many2one',
        'relation': 'fleet.vehicles',
        'required': True,
        },
     'kmreal': {'string': 'Km Real',
                 'type': 'integer',
                 'help': 'If the value is 0, the current mileage will be used.'
                 },
    }
    
    #
    form2 = '''<?xml version="1.0"?>
    <form string="Vehicle Alerts">
        <label string="Activated alerts for the defines vehicle: " width="200"/>
        <field name="vehicle" nolabel="1" colspan="2" width="150" height="50" />
        <field name="vehi_alerts" nolabel="1" colspan="2" width="700" height="250"  />
     </form > '''
    form2_fields = {
    'vehi_alerts': {
        'string': 'Vehicle Alerts',
        'type': 'one2many',
        'relation': 'preventive.proceed',
        'readonly': True,
        },
    'vehicle' :{
                'string': 'Vehicle',
                'type': 'many2one',
                'relation': 'fleet.vehicles',
                'readonly': True,
                }
    }
    
    states = {
            'init': {
                     'actions': [],
                     'result': {'type': 'form', 'arch':form1, 'fields':form1_fields, 'state': [('end', 'Cancel','gtk-cancel'),('next', 'Accept','gtk-ok')]}
                        },
             'evaluate' : {
                        'actions' : [],
                        'result': {'type': 'action', 'action': _alert_evaluate, 'state': 'next'}
                        },
                        
             'next' : {
                        'actions' : [],
                        'result': {'type': 'action', 'action': _action_open_window, 'state': 'end'}
                         }
              }
    
wizard_vehi_alert_eval('alert.evaluate.wizard')

class wizard_vehi_repair_create (wizard.interface):
    

    form1 = '''<?xml version="1.0"?>
    <form string="Repair Create">
        <label string="Create repair for the selected alerts?" width="100"/>
     </form > '''
    form1_fields = {}
    
    form2 = '''<?xml version="1.0"?>
    <form string="Error at repair creation">
    <separator string="The preventive repair must be on same vehicle! " colspan="4"/>
    </form>'''
    form2_fields = {}
    
    form3 = '''<?xml version="1.0"?>
    <form string="Repair Create">
    <separator string="Preventive repair created!" colspan="4"/>
    </form>'''
    form3_fields = {}
    
     
    def _action_open_window(self, cr, uid, data, context):
        
        alert_id= data['id']
        pool = pooler.get_pool(cr.dbname)
        vehicle_id = pool.get('preventive.proceed').browse(cr,uid,alert_id).ivehicle.id
        value = {
                 'name': False,
                 'view_type': 'form',
                 'view_mode': 'tree,form',
                 'res_model': 'mrp.repair',
                 'type': 'ir.actions.act_window',
                 'domain': [('idvehicle', '=', vehicle_id),('preventive','=', True)],
                }    
        return value
    
    def _repair_order_create(self, cr, uid, data, context):
        
        res={}
        pool = pooler.get_pool(cr.dbname)
        prev_proc = pool.get('preventive.proceed')
        alert_list = []
        if data['ids'] !=[]:
            alert_list = prev_proc.browse(cr,uid,data['ids'])
        vehicle_id = 0
        for alert in alert_list: # comprobar que todas las alertas pertenecen al mismo vehiculo
            if vehicle_id == 0:
                vehicle_id = alert.ivehicle.id
            if alert.ivehicle.id == vehicle_id:
                equals = True
            else :
                equals = False
        if not equals:
            return 'error'
        # crear reparación
        vehicle= pool.get('fleet.vehicles').browse(cr, uid,vehicle_id)
        product_id = vehicle.product_id.id
        product_obj= pool.get('product.product').browse(cr,uid,product_id)
        location_from = vehicle.location
        location_to = pool.get ('stock.location').search(cr,uid,[('name', 'like', 'Taller')])
        pool.get('fleet.vehicles').write(cr, uid, [vehicle_id],{ 'location': location_to[0]})
        move_id = pool.get('stock.move').create(cr,uid,{ 
                                                      'product_id' : vehicle.product_id.id, 
                                                      'name' : _('Orden Preventiva') + time.strftime('%Y-%m-%d %H:%M:%S'),
                                                      'location_id' : location_from.id,
                                                      'location_dest_id': location_to[0],
                                                      'product_uom': product_obj.product_tmpl_id.uom_id.id,
                                                      })
        ref= pool.get('mrp.repair').create(cr,uid,{'name':  pool.get('ir.sequence').get(cr, uid, 'mrp.repair'), 
                                                   'location_id' : location_from.id, 
                                                   'location_dest_id' :  location_to[0], 
                                                   'move_id' : move_id, 
                                                   'product_id': product_id,
                                                   'preventive': True,
                                                   'idvehicle': vehicle_id})
        mrp_repair_obj = pool.get('mrp.repair').browse(cr,uid,ref)
        for alert in alert_list: # crear lineas de producto + descripción
            descrip= alert.opdescription 
            if res =={}:
                if alert.opdescription:
                    res = {'internal_notes' : alert.opdescription }
                else : 
                    res = {'internal_notes' : '' }
            else:
                if alert.opdescription:
                    total= res['internal_notes'] + "\n" + alert.opdescription
                    res['internal_notes'] = total
            ope_vehi_mat = pool.get('operation.vehicle.materials').browse(cr,uid,alert.opr.id)
            mat_list = pool.get('operation.material').search(cr,uid,[('op_vehi_mat', '=', ope_vehi_mat.id)])
            for material in mat_list:
                mat_obj = pool.get('operation.material').browse(cr,uid,material)
                product= mat_obj.product_id
                prod_tmpl = product.product_tmpl_id
                loc_from = pool.get('stock.location').search(cr,uid,[('name','=','Stock')])
                loc_dest =  pool.get('stock.location').search(cr,uid,[('name','=','Production')])
                tax_list = prod_tmpl.taxes_id
                tax_list_ids=[]
                for tax in tax_list:
                    tax_list_ids.append(tax.id)
                move_id = pool.get('stock.move').create(cr,uid,{ 
                                                      'product_id' : product.id, 
                                                      'name' : prod_tmpl.name,
                                                      'location_id' : loc_from[0],
                                                      'location_dest_id': loc_dest[0],
                                                      'product_uom': mat_obj.product_uom.id,
                                                      })
                ref_line= pool.get('mrp.repair.line').create(cr,uid,{'name': '[' + product.default_code + '] ' + prod_tmpl.name,
                                                                     'product_uom' : mat_obj.product_uom.id,
                                                                     'repair_id': ref,
                                                                     'type' : 'add',
                                                                     'price_unit' : prod_tmpl.standard_price,
                                                                     'product_uom_qty' : mat_obj.product_uom_qty,
                                                                     'state' : 'draft',
                                                                     'product_id' : product.id,
                                                                     'location_dest_id' : loc_dest[0],
                                                                     'to_invoice' : True,
                                                                     'invoiced' : False,
                                                                     'location_id': loc_from[0],
                                                                     'move_id' : move_id,
                                                                     'tax_id' : [(6,0,tax_list_ids)],
                                                                     'user_id' : uid
                                                                     })
        pool.get('mrp.repair').write(cr,uid,ref,res)
        for alert in alert_list:
            prev_proc.write(cr,uid,alert.id,{'order' : ref})
        return 'final'

     
    states = {
            'init': {
                     'actions': [],
                     'result': {'type': 'form', 'arch':form1, 'fields':form1_fields, 'state': [('end', 'Cancel','gtk-cancel'),('create', 'Accept','gtk-ok')]}
                        },
            'create' : {
                      'actions' : [],
                      'result': {'type': 'choice', 'next_state' : _repair_order_create}
                         },
            'error':{
                     'actions': [],
                     'result': {'type': 'form', 'arch':form2, 'fields':form2_fields, 'state': [('end', 'Accept','gtk-ok')]}
                        },
            'next' :{
                     'actions': [],
                     'result': {'type': 'form', 'arch':form3, 'fields':form3_fields, 'state': [('final', 'Accept','gtk-ok')]}
                        },
            'final' :{
                     'actions': [],
                     'result': {'type': 'action', 'action': _action_open_window, 'state': 'end'}
                        }
            }
     
wizard_vehi_repair_create ('repair.create.wizard')
