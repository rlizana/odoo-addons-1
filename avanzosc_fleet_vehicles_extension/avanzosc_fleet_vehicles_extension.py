# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    09/11/2011
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
import pooler

from osv import osv, fields
from tools.translate import _


class fleet_vehicles(osv.osv):
    _description = 'fleet vehicles Inheritance'
    _inherit = 'fleet.vehicles'
    
    def _get_name(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('product_id')

    #def calc_seat(self, cr, uid, ids, fields, arg, context=None):
    def calc_seat(self,cr,uid,ids,field,unknown,context={}):
#        result = []
#        data= self.browse(cr, uid, ids, context=None)[0]
#        total = data.places + data.places2 + data.places3 + data.places4
#        result.append((data['id'],total))
#        return dict(result)
        res={}
        for data in self.browse(cr,uid,ids):
            res[data.id] = data.places + data.places2 + data.places3 + data.places4
        return res
    
    def calc_years(self,cr,uid,ids,field,unknown,context={}):
        res={}
        date = time.strftime('%Y')
        for data in self.browse(cr,uid,ids):
            enrol= data.enrolldate.split('-')
            res[data.id] = result= int(date)-int(enrol[0])
        return res
    
    def _check_product(self, cr, uid, ids): 
    #TODO : check condition and return boolean accordingly
        user = self.pool.get('res.users').browse (cr,uid, uid)
        user_lang = user.context_lang
        context = {'lang' : user_lang}
        for vehicle in self.browse(cr,uid,ids, context=context):
            prod_name = vehicle.product_id.name
            if vehicle.product_id:
                if vehicle.name == prod_name:
                    return True
            else:
                return False
        return False
    
    _columns = {
        'name':fields.char('Vehicle Name',size=50,required=True, translate=True),
        'product_id': fields.many2one('product.product', 'Product Associated', required=True),
        'depot': fields.many2one('stock.location','Depot Location',required=True),
        'tires':fields.integer('Tires',size=2),
        'enrolldate':fields.date('Enrollment date', required=True ),
        'card':fields.char('Card',size=20),
        'cardexp':fields.date('Card Expiration'),
        'frame':fields.char('Frame Number',size=24),
        'places':fields.integer('Number of seat places',size=10),
        'places2':fields.integer('Number of standing places ',size=10),
        'places3':fields.integer('Number of DP places',size=10),  
        'places4':fields.integer('Extra Driver Seat',size=10),  
        'totalplaces':fields.function(calc_seat, method=True, type='integer', string='Total places',digits=(10,0),store=True),
        'ambit':fields.selection([
                ('local','Local'),
                ('provincial','Provincial'),
                ('national','National'),
                ('international','International')],'Ambit',required=True),         
        'service':fields.selection([
                ('lines','Lines'),
                ('urban','Urban'),
                ('discretionary','Discretionary'),],'Service',required=True),  
        'viat':fields.char('VIA-T',size=24),
        #'itv':fields.date('ITV revision'),
        #'serv_time': fields.integer('Years in Service', size=8),
        'serv_time': fields.function(calc_years, method=True, type='integer', string='Years in Service',digits=(4,0),store=True),
        'lowboy':fields.boolean('Lowboy'),
        'pmr':fields.integer('Number of PMR doors',size=10),
        'ramp':fields.boolean('Ramp'),
        'lphone':fields.char('Long phone number',size=12),
        'sphone':fields.char('Short phone number',size=12),
        'wifi': fields.char('Wifi number',size=24),
        'insurance':fields.char('Insurance Name',size=10),
        'policy':fields.char('Vehicle policy',size=20),
        'schedname':fields.many2one('fleet.service.templ','PM Schedule',help="Preventive maintenance schedule for this vehicle"),
        'startodometer':fields.integer('Start Odometer'),
        'actodometer':fields.integer('Actual Odometer'),
        'assetacc':fields.many2one('account.account',string='Asset Account',required=True),
        }
    
    _defaults= {
          'ambit': lambda *a: 'provincial',  
          'service': lambda *a: 'lines',   
    }   
    
    _constraints = [(_check_product, _('Error: El nombre del producto y del vehículo deben ser iguales!'), ['product_id']),]
    _sql_constraints = [('name_uniq','unique(name)', _('El Vehículo ya existe!'))]

      
fleet_vehicles()

class fleet_fuellog(osv.osv):
    _description = 'fleet fuellog Inheritance'
    _inherit = 'fleet.fuellog'
    
    _columns = {
                'log_no':fields.char('Log Entry#',size=24),
                'vendor':fields.many2one('res.partner','Fuel Station',size=10),
                'supplier':fields.many2one('stock.location','Supplier Station'),
                'engine': fields.float('Engine Hours',digits=(16,2)),
                'emp_resp':fields.many2one('hr.employee','Employee Responsible',help="Employee reporting fuelling details"),
                'driver':fields.many2one('hr.employee','Driver',help="Driver who has driven the vehice before this fuelling"),
                'd_number': fields.char('Driver Number', size=20),
                'invoiceno':fields.many2one('account.invoice','Invoice no',size=10),
                'invno':fields.char('Invoice no',size=20),
                'journal_id':fields.many2one('account.journal', 'Journal'),
                'move_id':fields.many2one('account.move', 'Account Entry'),
                'period_id': fields.many2one('account.period', 'Period'),
                'date':fields.date('Transaction Date', required=True),
                'time':fields.time('Transaction Time', required=True),
                'cost':fields.float('Cost Per Ltr',digits=(16,2),required=True),
           }
    
fleet_fuellog()


    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
