# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    30/12/2011
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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import wizard
import pooler
import time   

class wizard_create_preventive (osv.osv_memory):
    """Create Vehicle Preventive operations """
    _name = 'wizard.create.preventive'
    _description = 'Create Vehicle Preventive operations'
    
    def create_preventive(self, cr, uid, data, context):
        if context is None:
            context = {}
        value = {}
        pool = pooler.get_pool(cr.dbname)
        preventive_list=[]
        count_op = 0
        vehicle_operations = pool.get('vehicle.prev.op')
        master_operations = pool.get('preventive.master')
        templ_operations = pool.get('optype')
        operations = pool.get('operation.vehicle.materials')
        prev_master = master_operations.browse(cr,uid, context['active_id'])
        operation_list = prev_master.ope_material
        for operation in operation_list: # The preventive master operation list from operation vehicle materials
            optype_id = operation.optype_id.id
            op_name = templ_operations.browse(cr,uid,optype_id).name
            op_compose_name = prev_master.name + ' - ' + op_name
            if operation.name != op_compose_name : # Preventive master operation name update
                operations.write(cr,uid, operation.id, {'name': op_compose_name})
            vehicle_list = prev_master.vehicles_ids
            for vehicle in vehicle_list:  # Loop Preventive master vehicle list
                vehicle_op_list = vehicle_operations.search(cr,uid,[('vehicle','=',vehicle.id)]) # Lista de Operaciones preventivas de vehiculo (vehicle.prev.opv) para el vehiculo seleccionado
                exist = False
                if vehicle_op_list != [] : 
                    for vehicle_op in vehicle_op_list : 
                        vehi_pre_op = vehicle_operations.browse(cr,uid,vehicle_op)
                        info1id = vehi_pre_op.opname.id
                        info2 = vehi_pre_op.opname
                        if vehi_pre_op.opname.id == operation.id :
                            exist = True
                            break
                if not exist : # El vehiculo no tiene vehicle.prev.op
                    result = operation.material
                    nombre_operacion = op_compose_name + '/' + vehicle.name
                    id_opname = operation.id
                    descripcion = operation.op_description
                    vehiculo = vehicle.id
                    res = {'name': op_compose_name + '/' + vehicle.name,
                           'opname': operation.id,
                           'opdescription':operation.op_description,
                           'vehicle': vehicle.id,
                           'margin_km1':operation.op_margin_km1,
                           'margin_km2': operation.op_margin_km2,
                           'frequency': operation.op_frequency,
                           'measUnit':operation.op_measUnit,
                           'margin_fre1':operation.op_margin_fre1,
                           'measUnit1':operation.op_measUnit1,
                           'margin_fre2':operation.op_margin_fre2,
                           'measUnit2':operation.op_measUnit2,
                           'nexttime': operation.op_nexttime,
                           'lasttime': operation.op_nexttime,
                         }
                    
                    if operation.kms > 0 : # Operation by Km
                        res['nextkm'] = operation.kms + vehicle.actodometer
                        res['mileage'] = operation.kms
                    if operation.op_frequency > 0: # Operation by date
                        op_freq = operation.op_frequency
                        op_meas = operation.op_measUnit
                        time_now = datetime.now()
                        if op_meas == 'day':
                            calc_date = time_now + relativedelta(days=op_freq)
                        elif op_meas == 'week':
                            calc_date = time_now + relativedelta(weeks=op_freq)
                        elif op_meas == 'mon':
                            calc_date = time_now + relativedelta(months=op_freq)
                        else:
                            calc_date = datetime.strptime(last_op_date,"%Y-%m-%d") + relativedelta(years=op_freq)
                        alc_date = datetime.strftime(calc_date,"%Y-%m-%d")
                        last_date = datetime.strftime(time_now,"%Y-%m-%d")
                        res['nextdate'] = calc_date
                        res['lastdate'] = last_date      
                    if operation.kms > 0 or operation.op_frequency > 0 : # Alarm check activation
                        res['check_al1'] = True
                        if operation.op_margin_km2 != 0 or operation.op_margin_fre2 != 0:
                            res['check_al2'] = True
                    prevent_oper = vehicle_operations.create(cr,uid, res) # Create preventive order
                    count_op = count_op+1
                    preventive_list.append(prevent_oper)
        context = {'op_count':count_op,'vehi_prevs':preventive_list}
             
        values = {'context': context}
        wizard = {
            'type': 'ir.actions.act_window',
            'name' : 'View Preventives',
            'res_model': 'wizard.preventive.list',
            'view_mode': 'form',
#            'res_id': context['vehi_prevs'],
            'target': 'new',
            'context' : context,
            #'domain': "[('vehi_prevs', 'in', %s)]" % preventive_list,
            }
        return wizard
    
wizard_create_preventive()

class wizard_preventive_list (osv.osv_memory):
    

    def _prev_list(self, cr, uid, context=None):
        
        """This function checks for precondition before wizard executes
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values
        """
        data = []
        pool = pooler.get_pool(cr.dbname)
        vehicle_operations = pool.get('vehicle.prev.op')
        for prev_id in context['vehi_prevs'] :
            vehi_pre = vehicle_operations.browse(cr,uid,prev_id)
            res = {'name': vehi_pre.name,
                #'opname': vehi_pre.opname,
                'opdescription':vehi_pre.opdescription,
                'vehicle': vehi_pre.vehicle.id,
                'margin_km1':vehi_pre.margin_km1,
                'margin_km2': vehi_pre.margin_km2,
                'frequency': vehi_pre.frequency,
                'measUnit': vehi_pre.measUnit,
                'margin_fre1':vehi_pre.margin_fre1,
                'measUnit1':vehi_pre.measUnit1,
                'margin_fre2':vehi_pre.margin_fre2,
                'measUnit2':vehi_pre.measUnit2,
                'nexttime': vehi_pre.nexttime,
                'lasttime': vehi_pre.lasttime,
                         }
            data.append(res)
        return  data
    
    def _op_count (self, cr, uid, context=None):
        
        cont= len(context['vehi_prevs'])
        return cont
    
    """Create Vehicle Preventive operations """
    _name = 'wizard.preventive.list'
    _description = 'Preventive list'
    _columns = {
        'vehi_prevs': fields.one2many ('vehicle.prev.op','vehicle','Vehicle Preventive Operations',readonly=True),
        'op_count': fields.integer('Counter',readonly=True)
    }
    
    _defaults = {
                 'vehi_prevs': _prev_list,
                 'op_count': _op_count 
    }
     
wizard_preventive_list()
