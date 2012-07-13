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

class wizard_tire_scratch (wizard.interface):
    
    form1 = '''<?xml version="1.0"?>
    <form string="Tire Change">
    <field name="tire" width="250" height="50"/>
    <separator string="Move Tire" colspan="6"/>
    <field name="origin" width="250" height="50"/>
    <field name="destination" width="250" height="50"/>
    <field name="odometer" />
    </form>'''
    
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
                             'required': True,
                             'readonly': True
        },
        'odometer': {
                             'string': 'Odometer',
                             'type': 'integer',
                             
        },
                    
                    }
    
    form2 = '''<?xml version="1.0"?>
    <form string="Tire move">
    <separator string="Tire correctly moved! " colspan="4"/>
    </form>''' 
    form2_fields = {}
        
    def tire_init (self,cr,uid, data,context):

        move_data = {}
        pool = pooler.get_pool(cr.dbname)
        tire_obj = pool.get('stock.production.lot')
        move_obj = pool.get('stock.move')
        loc_obj = pool.get('stock.location')
        company_obj = pool.get('res.company')
        data_obj = pool.get('tire.stock.lot')
        tire_data_obj = data_obj
        tire = tire_obj.browse(cr,uid,data['id'])
        company=tire.company_id
        move_list = move_obj.search(cr,uid,[('prodlot_id','=',tire.id)])
        locat_default = company.tire_stock
        destini = company.scratch.id
        if move_list == []:
            origin = locat_default.id
        else:
            loc_id = max(move_list)
            move= move_obj.browse(cr,uid, loc_id)
            origin = move.location_dest_id.id
        move_data={'tire':tire.id, 'origin': origin, 'destination': destini}
        return move_data
    
    def tire_scratch (self,cr,uid, data,context):
        
        pool = pooler.get_pool(cr.dbname)
        tire_obj = pool.get('stock.production.lot')
        move_obj = pool.get('stock.move')
        vehic_obj = pool.get('fleet.vehicles')
        loc_obj = pool.get('stock.location')
        company_obj = pool.get('res.company')
        tire_data_obj = pool.get('tire.stock.lot')
        tire = tire_obj.browse(cr,uid,data['form']['tire'])
        company=tire.company_id
        move_list = move_obj.search(cr,uid,[('prodlot_id','=',tire.id)])
        destination = loc_obj.browse (cr,uid,data['form']['destination'])
        destination_name = destination.name
        origin = loc_obj.browse (cr,uid,data['form']['origin'])
        origin_name = origin.name
        
        #Comprobar si el origen es un vehiculo
        if origin.location_id:
            loc_parent_ori = origin.location_id.id
            if loc_parent_ori:
                vehic_list = vehic_obj.search(cr,uid,[('buslocat','=',loc_parent_ori)])
            else : vehic_list = []            
            if vehic_list ==[]:
                ori_vehicle = False
                res = 'error'
            else:
                vehicle = vehic_obj.browse(cr,uid,vehic_list[0])
                ori_vehicle = True
                res = 'moved'
        else: 
            ori_vehicle = False
            res = 'moved'
        # Termina comprobación origen    

        if ori_vehicle : # Origin = Vehicle
            if origin_name.endswith("-1"):
                update ={ 'f_l_tire' : False}
            elif origin_name.endswith("-2"):
                update ={ 'f_r_tire' : False}
            if vehicle.tires == 6:
                if origin_name.endswith("-3"):
                    update ={ 'r_l_tire1' : False}
                elif origin_name.endswith("-4"):
                    update ={ 'r_l_tire2' : False}
                elif origin_name.endswith("-5"):  
                    update ={ 'r_r_tire2' : False}                
                elif origin_name.endswith("-6"):
                    update ={ 'r_r_tire1' : False}
            elif vehicle.tires > 6:
                if origin_name.endswith("-3"):
                    update ={ 'm_l_tire1' : False}
                elif origin_name.endswith("-4"):
                    update ={ 'm_l_tire2' : False}
                elif origin_name.endswith("-5"):  
                    update ={ 'm_r_tire2' : False}                
                elif origin_name.endswith("-6"):
                    update ={ 'm_r_tire1' : False}
                elif origin_name.endswith("-7"):
                    update ={ 'r_l_tire1' : False}
                elif origin_name.endswith("-8"):
                    update ={ 'r_r_tire1' : False}
            vehic_obj.write(cr,uid,vehicle.id,update)
                    #Datos movimiento
        product_id = tire.product_id
        
        # actualizar odometro rueda
        odometer = data['form']['odometer']
        if move_list == []:
            odometer_text = str(data['form']['odometer'])
            tire_odometer = 1
            if odometer_text == '0':
                odometer = 1
            tire_val= {'tire_km' : tire_odometer,'odometers' : odometer_text}
        else:
            if ori_vehicle :
                loc_id = max(move_list)
                move= move_obj.browse(cr,uid, loc_id)
                result = int(odometer) - move.odometer
                tire_odometer =  tire.tire_km + result
                if tire.odometers:
                    odometer_text = tire.odometers + "\n" + str(data['form']['odometer'])
                else: odometer_text = str(data['form']['odometer'])
                tire_val= {'tire_km' : tire_odometer, 'odometers' : odometer_text}                
            else:
                if tire.odometers:
                    odometer_text = tire.odometers + "\n" + str(data['form']['odometer'])
                else: odometer_text = str(data['form']['odometer'])
                tire_val= {'odometers' : odometer_text}
        tire_obj.write(cr,uid, tire.id,tire_val)
        # Termina actualización odometro rueda
        
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
        #actualiza movimiento
        move_id = move_obj.create(cr,uid,move_data)
        #Fin datos movimiento
            
        #Actualiza rueda
        tire_obj.write(cr,uid, tire.id,{'tire_km' : tire_data_val['tire_km_total'], 'odometers' : odometer_text})
        
        #crear datos neumático
        move_data_reg = move_obj.browse(cr,uid,move_id)
        tire_data_val['data']= move_data_reg.date
        data_id= tire_data_obj.create(cr,uid,tire_data_val)
        #Fin datos rueda
        res = 'moved'
        
        return res
    
        
    states = {
            'init': {
                     'actions': [tire_init],
                     'result': {'type': 'form', 'arch':form1, 'fields':form1_fields, 'state': [('end', 'Cancel','gtk-cancel'),('waste', 'Accept','gtk-ok')]}
                    },
            'waste': {
                       'actions' : [],
                       'result': {'type': 'choice', 'next_state': tire_scratch}
                     },
            'moved': {
                       'actions' : [],
                       'result': {'type': 'form', 'arch':form2, 'fields':form2_fields,'state': [('end', 'Accept','gtk-ok')]}
              }
            
            }

wizard_tire_scratch('tire.scratch')
 