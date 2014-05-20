
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    23/02/2012
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

from osv import osv
from osv import fields
from tools.translate import _

class vehicle_prev_op(osv.osv):
     
    _name = "vehicle.prev.op"
    _description="Preventive operations of a vehicle."
    _columns={
              'name':fields.char('REF', size=80, required=True),
              'opdescription': fields.text('Description'),
              'vehicle':fields.many2one('fleet.vehicles', 'Vehicle',required=True, readonly=True),
              'frequency':fields.integer('Frequency', help="Estimated time for the next operation."),
              'measUnit':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.', ),
              'mileage':fields.integer('Op. Mileage Increment',help="Mileage increment for the next operation. Measured in kilometers."),
              'lastdate':fields.date('Date', help="Last date on which the operation was done."),
              'lastkm':fields.integer('Mileage', help="Mileage of the vehicle in the last operation. Measured in kilometers."),
              'lasttime':fields.time('Time', help="Time it takes to make the operation. hh:mm:ss"),
              'nextkm':fields.integer('Mileage', help="Mileage of the vehicle for the next operation. Measured in kilometers."),
              'nextdate':fields.date('Date', help="Expected date for the next operation."),
              'nexttime':fields.time('Time', size=10, help="Expected time for the execution of the operation. hh:mm:ss"),
              'alert':fields.boolean('1st alert', readonly=True),
              'extra_alert':fields.boolean('2nd alert', readonly=True),
              'check_al1':fields.boolean('1st alert check', help="If checked the alarm will be test at the specified parameters."),
              'check_al2':fields.boolean('2nd alert check', help="If checked the alarm will be test at the specified parameters."),
              'margin_km1': fields.integer('Km. Margin', size=20),
              'margin_km2':fields.integer('Km. Margin', size=20),
              'margin_fre1':fields.integer('Frequency Margin'),
              'measUnit1':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
              'margin_fre2':fields.integer('Frequency Margin'),
              'measUnit2':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
              'acdometer': fields.related ('vehicle', 'actodometer', type ='integer', relation="fleet.vehicles",string="Actual Odometer" ),
              }
    _defaults = {
#                'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'vehicle.prev.op'),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(vehicle_prev_op, self).default_get(cr, uid, fields, context)
        if 'name' in context:
            if context['name']:
                opt = self.pool.get('fleet.vehicles').search(cr, uid, [('name', '=', context['name'])])[0]
                res.update({'vehicle': opt})
        return res
        
vehicle_prev_op()

class vehiclemodel(osv.osv):
 
    _name = 'vehiclemodel'
    _description = 'vehiclemodel'
 
    _columns = {
            'name':fields.char('Name', size=24),
            
        }
vehiclemodel()

class optype(osv.osv):
 
    _name = 'optype'
    _description = 'optype'
 
    _columns = {
            'name':fields.char('Name', size=24),
            'km':fields.integer('Km', size=24),
            'basedonkm': fields.boolean('Based on Km'),
            'margin_km1': fields.integer('Km. Margin 1'),
            'margin_km2': fields.integer('Km. Margin 2'),
            'frequency': fields.integer('Frequency', help="Estimated time for the next operation."),
            'measUnit':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
            'margin_fre1':fields.integer('Frequency Margin 1'),
            'measUnit1':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
            'margin_fre2':fields.integer('Frequency Margin 2'),
            'measUnit2':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
            'description':fields.text('Description'),
            'nexttime':fields.float('Operation Time', size=10, help="Expected time for the execution of the operation. hh:mm:ss"),
        }
    
    def onchange_measUnit(self, cr, uid, fields, measUnit, context=None):
        res = {}
        if measUnit:
            res = {
                'measUnit1':measUnit,
                'measUnit2':measUnit,
            }
        return {'value': res}
    
optype()

class preventive_master(osv.osv):
 
    _name = 'preventive.master'
    _description = 'preventive.master'
    
    def name_assig (self, cr, uid, ids, field, arg, context={}):
        
        values = {} 
        for data in self.browse(cr,uid,ids):
            values[data.id] = _('Operation Type ') + data.type.capitalize() + ' - ' + data.vehiclemodel.name
        context = {'name' : values[data.id]}
        return values
 
    _columns = {
            'name':fields.function(name_assig , method=True, type='char', string='Operation Ref. Name',store=True, size = 64),
            'type':fields.selection([('a','A'),('b','B'),('c','C'),('d','D'),('e','E'),('f','F'),('g','G')], 'Maintenance type', required=True, size = 14),
            'vehiclemodel':fields.many2one('vehiclemodel','Vehicle Model', required=True, size=24),
            'vehicles_ids':fields.many2many('fleet.vehicles', 'vehicles_maint_rel', 'preventive_master_id', 'fleet_vehicles_id'),
            'ope_material':fields.one2many('operation.vehicle.materials','opmaster','Material'),
            'opdescription':fields.text('Description'),
                        
        }
        
preventive_master()


class operation_vehicle_materials(osv.osv):
 
    _name = 'operation.vehicle.materials'
    _description = 'Operation - Material Relation'
 
    _columns = {
            'name' : fields.char('Name', size=64),
            'optype_id' : fields.many2one('optype', 'Operations'),
            'material':fields.one2many('operation.material','op_vehi_mat','Material'),
            'kms': fields.integer('Kms'),
            'op_margin_km1': fields.integer('Km. Margin 1'),
            'op_margin_km2': fields.integer('Km. Margin 2'),
            'op_frequency': fields.integer('Frequency', help="Estimated time for the next operation."),
            'op_measUnit':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
            'op_margin_fre1':fields.integer('Frequency Margin 1'),
            'op_measUnit1':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
            'op_margin_fre2':fields.integer('Frequency Margin 2'),
            'op_measUnit2':fields.selection([('day', 'Days'),('week', 'Weeks'),('mon','Months'),('year', 'Years')],'Meas.'),
            'op_description': fields.text('Description'),
            'opmaster' :  fields.many2one('preventive.master', 'Operations'),
            'op_nexttime': fields.time('Operation Time'),
        }
    
    def onchange_opmeasUnit(self, cr, uid, fields, op_measUnit, context={}):
        res = {}
        if op_measUnit:
            res = {
                'op_measUnit1':op_measUnit,
                'op_measUnit2':op_measUnit,
            }
        return {'value': res}


    def onchange_optype_id(self, cr, uid, ids, optype_id, context={}):
            
        values = {}
        optype_obj = self.pool.get('optype')
        
        if optype_id != False :
            optype_aux = optype_obj.browse(cr, uid, optype_id)
            values = {'kms' : optype_aux.km,
                      'op_margin_km1': optype_aux.margin_km1,
                      'op_margin_km2': optype_aux.margin_km2,
                      'op_frequency': optype_aux.frequency,
                      'op_measUnit': optype_aux.measUnit,
                      'op_margin_fre1': optype_aux.margin_fre1,
                      'op_measUnit1': optype_aux.measUnit1,
                      'op_margin_fre2': optype_aux.margin_fre2,
                      'op_measUnit2': optype_aux.measUnit2,
                      'op_description':  optype_aux.description,
                      'name': optype_aux.name,
                      'op_nexttime': optype_aux.nexttime,
                        }
                
        return {'value' : values}

        
operation_vehicle_materials()

class operation_material(osv.osv):
    _name = "operation.material"
    _description="New material line."
    _columns={ 
              'op_vehi_mat':fields.many2one('operation.vehicle.materials', 'Operation'),
              'product_id':fields.many2one('product.product', 'Product', required=True),
              'product_uom_qty':fields.float('Quantity', digits=(16, 2)),
              'product_uom':fields.many2one('product.uom', 'Unit of Measure', required=True),
              } 
    _defaults={
               'product_uom_qty':1,
               }         
    
    def onchange_product(self, cr, uid, fields, product_id, context=None):
        res = {}
        if product_id:
            product = self.pool.get('product.product').browse(cr,uid,product_id)
            res = {
                'product_uom': product.uom_id.id,            
                }
        return {'value': res}
  
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = {}
        if 'name' in context:
            if context['name']:
                opt = self.pool.get('optype').search(cr, uid, [('name', '=', context['name'])])[0]
                res.update({'op_temp_mat': opt})
        return res
          
operation_material()

class preventive_proceed(osv.osv):
    _name = "preventive.proceed"
    _description = "All preventive operations scheduled to be done."
    _columns = {
                'prevname':fields.many2one('vehicle.prev.op', 'Op.', required=True),
                'opdescription':fields.text('Description'),
                'ivehicle':fields.many2one('fleet.vehicles', 'Vehicle'),
                'date1':fields.date('1st alert date'),
                'opr':fields.many2one('operation.vehicle.materials', 'Preventive operation', readonly=True),
                'date2':fields.date('2nd alert date'),      
                } 
    _defaults = {
                 'date1':lambda *a:time.strftime('%Y-%m-%d'),
                 }
    
preventive_proceed()



