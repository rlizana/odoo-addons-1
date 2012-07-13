
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    28/03/2012
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
import Image
import time

class wizard_tire_mount (wizard.interface):
    
    form1 = '''<?xml version="1.0"?>
    <form string="Tire Change">
    <field name="tire" width="250" height="50"/>
    <separator string="Move Tire" colspan="4"/>
    <field name="origin" width="250" height="50"/>
    <field name="destination" width="250" height="50"/>
    <group string="Bus Location" colspan="4" >
        <field name="locat" width="150" height="50" domain="[('location_id','=',destination)]" />
        <field name="odometer" />
    </group>
    </form>'''
    #attrs="{'invisible':[('destination','ilike','bus')]}"
    form1_fields = {
        'tire': {
                             'string': 'Tire',
                             'type': 'many2one',
                             'relation': 'stock.production.lot',
                             'required': True,
                             'readonly': True
        },
        'origin': {
                             'string': 'Origin',
                             'type': 'many2one',
                             'relation': 'stock.location',
                             'required': True,
                             'readonly': True
        },
        'destination': {
                             'string': 'Destination',
                             'type': 'many2one',
                             'relation': 'stock.location',
                             'required': True
        },
        'locat': {
                             'string': 'Tire Location',
                             'type': 'many2one',
                             'relation': 'stock.location',
                             
        },
        'odometer': {
                             'string': 'Odometer',
                             'type': 'integer',
                             
        },
                    
                    }
    
    form2 = '''<?xml version="1.0"?>
    <form string="Tire move">
    <label string="Location occupied! The chosen location already has a tire assigned, move it before assigning new one." colspan="4"/>
    </form>''' 
    form2_fields = {}
        
    form3 = '''<?xml version="1.0"?>
    <form string="Tire mount">
    <separator string="Origin location cannot be a Vehicle!" colspan="4"/>
    </form>''' 
    form3_fields = {}
    
    form4 = '''<?xml version="1.0"?>
    <form string="Tire move">
    <separator string="Tire correctly moved! " colspan="4"/>
    </form>''' 
    form4_fields = {}
    
    form5 = '''<?xml version="1.0"?>
    <form string="Tire mount">
    <separator string="Destination location must be a Vehicle!" colspan="4"/>
    </form>''' 
    form5_fields = {}
        
    def tire_init (self,cr,uid, data,context):

        move_data = {}
        pool = pooler.get_pool(cr.dbname)
        tire_obj = pool.get('stock.production.lot')
        move_obj = pool.get('stock.move')
        loc_obj = pool.get('stock.location')
        company_obj = pool.get('res.company')
        company_list = company_obj.search(cr,uid,[])
        tire = tire_obj.browse(cr,uid,data['id'])
        company=tire.company_id
        move_list = move_obj.search(cr,uid,[('prodlot_id','=',tire.id)])
        locat_default = company.tire_stock
        destini = False
        if move_list == []:
            origin = locat_default.id
        else:
            loc_id = max(move_list)
            move= move_obj.browse(cr,uid, loc_id)
            origin = move.location_dest_id.id
        move_data={'tire':tire.id, 'origin': origin, 'destination': destini} 
        return move_data
    
    def tire_move (self,cr,uid, data,context):
        
        pool = pooler.get_pool(cr.dbname)
        tire_obj = pool.get('stock.production.lot')
        move_obj = pool.get('stock.move')
        vehic_obj = pool.get('fleet.vehicles')
        loc_obj = pool.get('stock.location')
        data_obj = pool.get('tire.stock.lot')
        company_obj = pool.get('res.company')
        tire_data_obj = pool.get('tire.stock.lot')
        tire = tire_obj.browse(cr,uid,data['form']['tire'])
        company = tire.company_id
        move_list = move_obj.search(cr,uid,[('prodlot_id','=',tire.id)])
            
        destination = loc_obj.browse (cr,uid,data['form']['destination'])
        destination_name = destination.name
        origin = loc_obj.browse (cr,uid,data['form']['origin'])
        origin_name = origin.name
        
        #Comprobar si el origen es un vehiculo
        loc_parent_ori = origin.location_id.id
        if loc_parent_ori:
            vehic_list = vehic_obj.search(cr,uid,[('buslocat','=',loc_parent_ori)])
        else : vehic_list = []
        if vehic_list ==[]:
            ori_vehicle = False
            res = 'moved'
        else:
            ori_vehicle = True
            res = 'ori_vehic'
            vehicle =  vehic_obj.browse(cr,uid,vehic_list[0]) # vehiculo origen
        # Termina comprobación origen    
        
        #Comprobar destino es vehiculo
        if data['form']['locat'] :
            location = loc_obj.browse (cr,uid,data['form']['locat'])
            dest_vehi = True
        else: 
            dest_vehi = False
            res= 'dest_vehic'
        #Termina comprobación destino
        
        # actualizar odometro rueda
        odometer = data['form']['odometer']
        if move_list == []:
            odometer_text = str(data['form']['odometer'])
            tire_odometer = tire.tire_km
            if odometer_text == '0' and dest_vehi == True : #first move and destination vehicle odometer = 1
                odometer = 1
        else:
            loc_id = max(move_list)
            move= move_obj.browse(cr,uid, loc_id)
            tire_odometer =  tire.tire_km
            if tire.odometers:
                odometer_text = tire.odometers + "\n" + str(data['form']['odometer'])
            else: odometer_text = str(data['form']['odometer'])
        # Termina actualización odometro rueda
        
        if dest_vehi and not ori_vehicle : # Destination = Vehicle / Origen = No Vehicle
            
            #Datos movimiento
            product_id = tire.product_id
            move_data = {'product_id' : tire.product_id.id, 
                          'name' : origin.name + ' | ' + tire.name  + ' => ' + destination.name,
                          'location_id' : origin.id,
                          'product_uom': tire.product_id.product_tmpl_id.uom_id.id,
                          'prodlot_id' : tire.id,
                          'location_dest_id': location.id,
                          'odometer': odometer
                          }
            
            tire_data_val={
                        'name': origin.name + ' | ' + tire.name  + ' => ' + destination.name,
                        'lot_id': tire.id,
                        'origin' : origin.id,
                        'destination': location.id,
                       # 'data':time.strftime('%Y-%m-%d %H:%M:%S'),
                        'odomold' : 0,
                        'odomnew' :  odometer,
                        'tire_km' : 0,
                        'tire_km_total':tire.tire_km
                       }
            
            vehicle_id = vehic_obj.search(cr,uid,[('buslocat','=',destination.id)]) 
            vehicle = vehic_obj.browse(cr,uid,vehicle_id[0])
            loc_name = data['form']['locat']
            occupied = False
            if location.name.endswith("-1"): # Tire to right
                mount = {'f_l_tire' : tire.id} 
                if vehicle.f_l_tire.id: # Tire occupied
                    occupied = vehicle.f_l_tire
            elif location.name.endswith("-2"):
                mount = {'f_r_tire' : tire.id}
                if vehicle.f_r_tire.id: # Tire occupied
                    occupied = vehicle.f_r_tire
            if vehicle.tires == 6:
                if location.name.endswith("-3"):
                    mount = {'r_l_tire1' : tire.id}
                    if vehicle.r_l_tire1.id:
                        occupied = vehicle.r_l_tire1
                elif location.name.endswith("-4"):
                    mount = {'r_l_tire2' : tire.id}
                    if vehicle.r_l_tire2.id:
                        occupied = vehicle.r_l_tire2
                elif location.name.endswith("-5"):
                    mount = {'r_r_tire2' : tire.id}
                    if vehicle.r_r_tire2.id:
                        occupied = vehicle.r_r_tire2
                elif location.name.endswith("-6"):
                    mount = {'r_r_tire1' : tire.id}
                    if vehicle.r_r_tire1.id:
                        occupied = vehicle.r_r_tire1
            if vehicle.tires > 6:
                if location.name.endswith("-3"):
                    mount = {'m_l_tire1' : tire.id}
                    if vehicle.m_l_tire1.id:
                        occupied = vehicle.m_l_tire1
                elif location.name.endswith("-4"):
                    mount = {'m_l_tire2' : tire.id}
                    if vehicle.m_l_tire2.id:
                        occupied = vehicle.m_l_tire2
                elif location.name.endswith("-5"):
                    mount = {'m_r_tire2' : tire.id}
                    if vehicle.m_r_tire2.id:
                        occupied = vehicle.m_r_tire2
                elif location.name.endswith("-6"):
                    mount = {'m_r_tire1' : tire.id}
                    if vehicle.m_r_tire1.id:
                        occupied = vehicle.m_r_tire1
                elif location.name.endswith("-7"):
                    mount = {'r_l_tire1' : tire.id}
                    if vehicle.r_l_tire1.id:
                        occupied = vehicle.r_l_tire1
                elif location.name.endswith("-8"):
                    mount = {'r_r_tire1' : tire.id}
                    if vehicle.r_r_tire1.id:
                        occupied = vehicle.r_r_tire1
            if not occupied:
                #Actualiza rueda
                tire_obj.write(cr,uid, tire.id,{'tire_km' : tire_odometer, 'odometers' : odometer_text})
                #actualiza vehiculo
                vehic_obj.write(cr,uid, vehicle_id, mount)
                #actualiza movimiento
                move_id = move_obj.create(cr,uid,move_data)
                #crear datos neumático
                move_data_reg = move_obj.browse(cr,uid,move_id)
                tire_data_val['data']= move_data_reg.date
                data_id= data_obj.create(cr,uid,tire_data_val)
            elif occupied:
                res = 'full'
        elif not dest_vehi: # Destination = Warehouse 
            tire_data_val={}
            product_id = tire.product_id
            if ori_vehicle : # Origen = Vehicle
                if origin.name.endswith("-1"): # Tire to right
                    unmount = {'f_l_tire' : False} 
                elif origin.name.endswith("-2"):
                    unmount = {'f_r_tire' : False}
                if vehicle.tires == 6:
                    if origin.name.endswith("-3"):
                        unmount = {'r_l_tire1' : False}
                    elif origin.name.endswith("-4"):
                        unmount = {'r_l_tire2' : False}
                    elif origin.name.endswith("-5"):
                        unmount = {'r_r_tire2' : False}
                    elif origin.name.endswith("-6"):
                        unmount = {'r_r_tire1' : False}

                elif vehicle.tires > 6:
                    if origin.name.endswith("-3"):
                        unmount = {'m_l_tire1' : False}
                    elif origin.name.endswith("-4"):
                        unmount = {'m_l_tire2' : False}
                    elif origin.name.endswith("-5"):
                        unmount = {'m_r_tire2' : False}
                    elif origin.name.endswith("-6"):
                        unmount = {'m_r_tire1' : False}
                    elif origin.name.endswith("-7"):
                        unmount = {'r_l_tire1' : False}
                    elif origin.name.endswith("-8"):
                        unmount = {'r_r_tire1' : False}
                            #actualiza vehiculo
                vehic_obj.write(cr,uid, vehicle.id, unmount)
                
            #Datos rueda
            tire_data_list = tire_data_obj.search(cr,uid,[('lot_id','=',tire.id)])
            if tire_data_list== []:
                tire_data_val={
                        'name': origin.name + ' | ' + tire.name  + ' => ' + destination.name,
                        'lot_id': tire.id,
                        'origin' : origin.id,
                        'destination': destination.id,
                       # 'data':time.strftime('%Y-%m-%d %H:%M:%S'),
                        'odomold' : 0,
                        'odomnew' : 0,
                        'tire_km' : 0,
                        'tire_km_total': tire.tire_km
                       }
            else :
                tire_data_id = max(tire_data_list)
                tire_data = tire_data_obj.browse(cr,uid,tire_data_id)
                tire_data_val={
                        'name': origin.name + ' | ' + tire.name  + ' => ' + destination.name,
                        'lot_id': tire.id,
                        'origin' : origin.id,
                        'destination': destination.id,
                       # 'data':time.strftime('%Y-%m-%d %H:%M:%S'),
                       }
                if ori_vehicle: # Update odometer from vehicle
                    tire_data_val['odomold'] = tire_data.odomnew
                    tire_data_val['odomnew'] = odometer
                    tire_data_val['tire_km'] = odometer - tire_data.odomnew
                    tire_data_val['tire_km_total'] = tire_data.tire_km_total + odometer - tire_data.odomnew
                else:
                    tire_data_val['odomold'] = tire_data.odomnew
                    tire_data_val['odomnew'] = odometer 
                    tire_data_val['tire_km'] = 0
                    tire_data_val['tire_km_total'] = tire.tire_km
            #Fin datos rueda
            
            #Datos movimiento    
            move_data = {'product_id' : tire.product_id.id, 
                          'name' : origin.name + ' | ' + tire.name  + ' => ' + destination.name,
                          'location_id' : origin.id,
                          'product_uom': tire.product_id.product_tmpl_id.uom_id.id,
                          'prodlot_id' : tire.id,
                          'location_dest_id': destination.id,
                          'odometer': odometer
                          }
            #Fin datos movimiento
            
            #Actualiza rueda
            tire_obj.write(cr,uid, tire.id,{'tire_km' : tire_data_val['tire_km_total'], 'odometers' : odometer_text})
            #actualiza movimiento
            move_id = move_obj.create(cr,uid,move_data)
            #crear datos neumático
            move_data_reg = move_obj.browse(cr,uid,move_id)
            tire_data_val['data']= move_data_reg.date
            data_id= data_obj.create(cr,uid,tire_data_val)
            res = 'moved'
        
        return res
    
        
    states = {
            'init': {
                     'actions': [tire_init],
                     'result': {'type': 'form', 'arch':form1, 'fields':form1_fields, 'state': [('end', 'Cancel','gtk-cancel'),('mount', 'Accept','gtk-ok')]}
                    },
            'mount': {
                       'actions' : [],
                       'result': {'type': 'choice', 'next_state': tire_move}
                     },
            'full' : {
                      'actions' : [],
                      'result': {'type': 'form', 'arch':form2, 'fields':form2_fields,'state': [('end', 'Accept','gtk-cancel')]}
                         },
            'ori_vehic': {
                       'actions' : [],
                       'result': {'type': 'form', 'arch':form3, 'fields':form3_fields,'state': [('end', 'Accept','gtk-cancel')]}

              },

            'moved': {
                       'actions' : [],
                       'result': {'type': 'form', 'arch':form4, 'fields':form4_fields,'state': [('end', 'Accept','gtk-ok')]}

              },
            'dest_vehic': {
                       'actions' : [],
                       'result': {'type': 'form', 'arch':form5, 'fields':form5_fields,'state': [('end', 'Accept','gtk-cancel')]}

              },
            
            }

wizard_tire_mount('tire.mount')