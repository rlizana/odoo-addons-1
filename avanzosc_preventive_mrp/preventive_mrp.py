# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    21/02/2012
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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import wizard
import pooler

from osv import osv, fields
from tools.translate import _


class vehicle_prev_op(osv.osv):
    _inherit = "vehicle.prev.op"
     
    def _alert_create(self, cr, uid, context={}):        
        res={'alert':False, 'extra_alert':False}
        ids = self.search(cr, uid, [])
        operations_vehi_mat = self.pool.get('operation.vehicle.materials')
        for ope in self.pool.get('vehicle.prev.op').browse(cr,uid,ids): # Loop para todas las alarmas de operaciones de vehiculo definidas
            vh=ope.vehicle
            vehicle_name = vh.name
            #fuellog = self.pool.get('fleet.fuellog').browse(cr,uid,vh)  
            odometer = vh.actodometer
            nextmileage = ope.lastkm + ope.mileage # último Kmetraje + margen de km
            mileage1 = nextmileage + ope.margin_km1
            mileage2 = nextmileage + ope.margin_km2
            if ope.nextkm is not False:
                kmmarg1 = ope.nextkm + ope.margin_km1
                kmmarg2 = ope.nextkm + ope.margin_km2
            if ope.nextdate is not False:
                freq_list = self._get_freq_date(cr, uid, ope.id, context)
                date = time.strftime('%Y-%m-%d')
                freq1 = freq_list[0]
                freq2 = freq_list[1]
            
            exists = self.pool.get('preventive.proceed').search(cr,uid,[('prevname','=', ope.id)])
            operavm = operations_vehi_mat.browse(cr,uid,ope.opname.id)
            if ope.frequency == 0: # Sin margen de frequencia 
                if not exists: # No existe alarma de operación preventiva
                    res = {'nextkm':nextmileage}
                    if (odometer >= kmmarg1 and ope.check_al1 == True):
                        poto= operavm.opmaster.id
                        value = {'prevname': ope.id, 'ivehicle':vh.id, 'opdescription':ope.opdescription, 'opr':ope.opname.id, 'active': True}
                        alert = self.pool.get('preventive.proceed').create(cr, uid, value)
                        if ( odometer >= kmmarg2 and ope.check_al2 == True):
                            self.pool.get('preventive.proceed').write(cr,uid,[alert], {'date2':time.strftime('%Y-%m-%d')})
                            res = {'alert':True,'extra_alert':True}
                        else:
                            res = {'alert':True,'extra_alert':False}
                    else:
                        res = {'alert':False, 'extra_alert':False}
                else:
                    alert = exists[0]
                    if (odometer >= kmmarg1 and ope.check_al1 == True):
                        if (odometer >= kmmarg2 and ope.check_al2 == True):
                            res = {'alert':True,'extra_alert':True}
                            if not self.pool.get('preventive.proceed').browse(cr,uid,exists[0]).date2:
                                self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'date2':time.strftime('%Y-%m-%d')})
                        else:
                            self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'date2':False})
                            res = {'alert':True,'extra_alert':False}
                    else: 
                        res = {'alert':False,'extra_alert':False}
                        self.pool.get('preventive.proceed').unlink(cr,uid,exists[0])
            elif ope.mileage == 0: # Sin margen de kilometraje
                if not exists:
                    if (date >= freq1 and ope.check_al1 == True):
                        poto= operavm.opmaster.id
                        value = {'prevname': ope.id, 'ivehicle':vh.id, 'opdescription':ope.opdescription, 'opr':ope.opname.id, 'active': True}
                        alert = self.pool.get('preventive.proceed').create(cr, uid, value)
                        if (date >= freq2 and ope.check_al2 == True):
                            self.pool.get('preventive.proceed').write(cr,uid,[alert], {'date2':time.strftime('%Y-%m-%d'),'dateorder':ope.nextdate})
                            res = {'alert':True,'extra_alert':True}
                        else:
                            res = {'alert':True,'extra_alert':False}
                            self.pool.get('preventive.proceed').write(cr,uid,[alert], {'dateorder':ope.nextdate})
                    else:
                        res = {'alert':False, 'extra_alert':False}
                else:
                    alert = exists[0]
                    if (date >= freq1 and ope.check_al1 == True):
                        if (date >= freq2 and ope.check_al2 == True):
                            res = {'alert':True,'extra_alert':True}
                            if not self.pool.get('preventive.proceed').browse(cr,uid,exists[0]).date2:
                                self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'date2':time.strftime('%Y-%m-%d'),'dateorder':ope.nextdate})
                        else:
                            self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'date2':False,'dateorder':ope.nextdate})
                            res = {'alert':True,'extra_alert':False}
                    else: 
                        res = {'alert':False,'extra_alert':False}
                        self.pool.get('preventive.proceed').unlink(cr,uid,exists[0])
            else:
                if not exists:
                    res = {'nextkm':nextmileage}
                    if ((odometer >= kmmarg1) or (date >= freq1) and ope.check_al1 == True):
                        value = {'prevname': ope.id, 'ivehicle':vh.id, 'opr':operavm.opmaster.id}
                        alert = self.pool.get('preventive.proceed').create(cr, uid, value)
                        if ((odometer >= kmmarg2) or (date >= freq2) and ope.check_al2 == True):
                            self.pool.get('preventive.proceed').write(cr,uid,[alert], {'date2':time.strftime('%Y-%m-%d')})
                            res = {'alert':True,'extra_alert':True}
                        else:
                            res = {'alert':True,'extra_alert':False}
                    else:
                        res = {'alert':False, 'extra_alert':False}
                else:
                    alert = exists[0]
                    if ((odometer >= kmmarg1) or (date >= freq1) and ope.check_al1 == True):
                        if ((odometer >= kmmarg2) or (date >= freq2) and ope.check_al2 == True):
                            res = {'alert':True,'extra_alert':True}
                            if not self.pool.get('preventive.proceed').browse(cr,uid,exists[0]).date2:
                                self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'date2':time.strftime('%Y-%m-%d')})
                                if ope.frequency != 0:
                                    self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'dateorder':ope.nextdate})
                                else:
                                     self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'dateorder':time.strftime('%Y-%m-%d')})           
                        else:
                            self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'date2':False})
                            if ope.frequency != 0:
                                    self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'dateorder':ope.nextdate})
                            else:
                                     self.pool.get('preventive.proceed').write(cr,uid,[exists[0]], {'dateorder':time.strftime('%Y-%m-%d')})
                            res = {'alert':True,'extra_alert':False}
                    else: 
                        res = {'alert':False,'extra_alert':False}
                        self.pool.get('preventive.proceed').unlink(cr,uid,exists[0])
            
            # Crear reparación segun orden preventiva
            #if res['extra_alert']:
            #   order = self._create_repair_order(cr, uid, ope.id, context)
            self.pool.get('vehicle.prev.op').write(cr,uid,[ope.id],res)                          
        
        return res
    
    
    def _get_freq_date(self, cr, uid, op_id, context=None):
        freq_list = []
        
        ope = self.pool.get('vehicle.prev.op').browse(cr,uid,op_id)
        
        last_op_date = ope.lastdate
        if not last_op_date:
            last_op_date = ope.vehicle.enrolldate
            
        op_meas = ope.measUnit
        op_freq = ope.frequency     
        op_freq1 = ope.margin_fre1
        op_meas1 = ope.measUnit1 
        op_freq2 = ope.margin_fre2
        op_meas2 = ope.measUnit2
        
        #calc_date = datetime.strftime(ope.nextdate,"%Y-%m-%d")
        calc_date = ope.nextdate
        
        # Calculo primera alarma
        if op_meas1 == 'day':
            freq1 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(days=op_freq1)
        elif op_meas1 == 'week':
            freq1 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(weeks=op_freq1)
        elif op_meas1 == 'mon':
            freq1 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(months=op_freq1)
        else:
            freq1 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(years=op_freq1)
        
        # Calculo segunda alarma
        if op_meas2 == 'day':
            freq2 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(days=op_freq2)
        elif op_meas2 == 'week':
            freq2 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(weeks=op_freq2)
        elif op_meas2 == 'mon':
            freq2 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(months=op_freq2)
        else:
            freq2 = datetime.strptime(calc_date,"%Y-%m-%d") + relativedelta(years=op_freq2)
        
        freq1 = datetime.strftime(freq1,"%Y-%m-%d")
        freq2 = datetime.strftime(freq2,"%Y-%m-%d")
        
        freq_list.append(freq1)
        freq_list.append(freq2)
        
        return freq_list

vehicle_prev_op()

class preventive_proceed(osv.osv):
    _inherit = "preventive.proceed"
    _columns = {
                'order':fields.many2one('mrp.repair', 'Repair Order', readonly=True),
                'dateorder':fields.date('Order expected date'),
                'active':fields.boolean('Active'), 
                }
    
preventive_proceed()  


class mrp_repair (osv.osv):
 
    _inherit= 'mrp.repair'
    _columns = {
        'prevproc':fields.one2many('preventive.proceed', 'order', 'Preventive Orders'),
        }
    
    def action_repair_done(self, cr, uid, ids, context=None):
        vehi_prev_objets = self.pool.get('vehicle.prev.op')
        vehic_objets = self.pool.get('fleet.vehicles')
        for order in self.browse(cr, uid, ids):
            val = {}
            if order.preventive == True:
                prevent_objets = self.pool.get('preventive.proceed')
                prev_list = prevent_objets.search(cr,uid,[('order', '=', order.id),('active','=',True)])
                for preventive_id in prev_list: # Lista de alertas, actualizar vehicle.pre.op 
                    prev_obj = prevent_objets.browse(cr,uid,preventive_id)
                    prevent_objets.write(cr,uid,prev_obj.id,{'active' : False}) # Desactivar alerta
                    vehi_prev_obj = vehi_prev_objets.browse(cr,uid,prev_obj.prevname.id)
                    vehicle_id = vehi_prev_obj.vehicle.id
                    vehicle = vehic_objets.browse(cr,uid,vehi_prev_obj.vehicle.id)
                    val= {'alert' : False, 
                        'extra_alert': False 
                        } # Desactivar alertas vehicle.pre.op
                    freq = vehi_prev_obj.frequency
                    if vehi_prev_obj.mileage != 0:
                        val['lastkm'] = vehi_prev_obj.acdometer
                        val['nextkm'] = vehi_prev_obj.acdometer + vehi_prev_obj.mileage
                    if freq != 0:
                        date = time.strftime('%Y-%m-%d')
                        val['lastdate'] = date
                        freq_list = vehi_prev_objets._get_freq_date(cr, uid, vehi_prev_obj.id, context)
                        me_unit = vehi_prev_obj.measUnit
                        if me_unit == 'day':
                            next_date = datetime.strptime(date,"%Y-%m-%d") + relativedelta(days=freq)
                        elif me_unit == 'week':
                            next_date = datetime.strptime(date,"%Y-%m-%d") + relativedelta(weeks=freq)
                        elif me_unit == 'mon':
                            next_date = datetime.strptime(date,"%Y-%m-%d") + relativedelta(months=freq)
                        else:
                            next_date = datetime.strptime(date,"%Y-%m-%d") + relativedelta(years=freq)
                        val['nextdate'] = next_date
                    vehi_prev_objets.write(cr,uid,vehi_prev_obj.id,val)
        super(mrp_repair, self).action_repair_done(cr, uid, ids)
        return True      
        
mrp_repair()

#class fleet_vehicles(osv.osv):
#    _inherit = 'fleet.vehicles'
#    
#    _columns = {
#                'order_list':fields.one2many('mrp.repair','idvehicle','Preventive Orders'),
#              
#                }
#fleet_vehicles()
   
