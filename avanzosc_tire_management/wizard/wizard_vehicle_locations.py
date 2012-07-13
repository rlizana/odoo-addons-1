
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

 
class wizard_create_locations (osv.osv_memory):
    
    """create locations"""
    _name = 'wizard.create.locations'
    _description = 'Vehicle location'
    
    _columns = {
                'company': fields.many2one ('res.company','Company', required=True),
                'tire_stock': fields.many2one ('stock.location','Tire Stock'),
                'retread': fields.many2one ('stock.location','Retread'),
                'scratch': fields.many2one ('stock.location','Scratch'),
                'waste': fields.many2one ('stock.location','Waste'),
                'flatire': fields.many2one ('stock.location','Flat Tire'),
                'schema4' : fields.binary('4 Tire Schema'),
                'schema6' : fields.binary('6 Tire Schema'),
                'schema8' : fields.binary('8 Tire Schema'),
                }
    
    def onchange_company (self, cr, uid, ids, company_id, context=None):
        
        
        pool = pooler.get_pool(cr.dbname)
        company_obj = pool.get('res.company')
        company = company_obj.browse (cr,uid,company_id)
        context = {'company' : company.id}
        values ={}
        if company.tire_stock:
            values['tire_stock'] = company.tire_stock.id
        if company.retread: 
            values['retread'] = company.retread.id
        if company.scratch:
            values['scratch'] = company.scratch.id
        if company.waste:
            values['waste'] = company.waste.id
        if company.flatire:
            values['flatire'] = company.flatire.id
        if company.schema4:
            values['schema4'] = company.schema4
        if company.schema6:
            values['schema6'] = company.schema6
        if company.schema8:
            values['schema8'] = company.schema8
        values ['context'] = context
        return {'value' : values}
    
    def save_config (self,cr,uid,ids,data,context=None):
        
        values ={}
        pool = pooler.get_pool(cr.dbname)
        company_obj = pool.get('res.company')
        company= self.browse(cr,uid,ids[0]).company
        values ['tire_stock'] = self.browse(cr,uid,ids[0]).tire_stock.id
        values ['retread'] = self.browse(cr,uid,ids[0]).retread.id
        values ['scratch'] = self.browse(cr,uid,ids[0]).scratch.id
        values ['waste'] = self.browse(cr,uid,ids[0]).waste.id
        values ['flatire'] = self.browse(cr,uid,ids[0]).flatire.id
        
        if self.browse(cr,uid,ids[0]).schema4:
            values ['schema4'] = self.browse(cr,uid,ids[0]).schema4.id
        else: 
            values ['schema4'] = ''
        if self.browse(cr,uid,ids[0]).schema6:
            values ['schema6'] = self.browse(cr,uid,ids[0]).schema6.id
        else: 
            values ['schema6'] = ''
        if self.browse(cr,uid,ids[0]).schema8:
            values ['schema8'] = self.browse(cr,uid,ids[0]).schema8
        else: 
            values ['schema8'] = ''
        company = company_obj.browse(cr,uid,company.id)
        company_obj.write(cr,uid,company.id,values)
        
        value = {
                 'type': 'ir.actions.close_window',
                }   
        
        return value
    
    def create_locations(self, cr, uid, data, context):
        
        res = {}
        pool = pooler.get_pool(cr.dbname)
        company_obj = pool.get('res.company')
        company_list = company_obj.search(cr,uid,[])
        company= company_obj.browse(cr,uid,company_list[0])
        vehicle_obj = pool.get('fleet.vehicles')
        stloc_obj = pool.get('stock.location')
        vehicle_list = vehicle_obj.search(cr, uid, [('buslocat','=', None)])
        for vehicle in vehicle_list:
            vehi = vehicle_obj.browse(cr, uid, vehicle)      
            buslo_val={'name': vehi.name,'active':True ,'usage':'internal', 'chained_location_type':'none','chained_auto_packing' :'manual', 'chained_delay':'0'}
            bus_location = stloc_obj.create(cr,uid,buslo_val)
            if vehi.tires:
                if vehi.tires > 6:
                    vehi_vals = {'axles' : '3axle', 'buslocat':bus_location, 'schema':''}
                    if company.schema8 :
                        vehi_vals ['schema'] = company.schema8
                elif vehi.tires ==4:
                    vehi_vals = {'axles' : '2axle', 'buslocat':bus_location, 'schema':''}
                    if company.schema4 :
                        vehi_vals ['schema'] = company.schema4
                else: 
                    vehi_vals = {'axles' : '2axle', 'buslocat':bus_location, 'schema':''}
                    if company.schema6 :
                        vehi_vals ['schema'] = company.schema6
                for i in range (1,vehi.tires+1): # middle axle creation and its tires
                    tire_name= vehi.name.strip('bus ') + '-' + str(i)          
                    tire = {'name': tire_name,'active':True,'usage':'internal','location_id': bus_location, 'chained_location_type':'none','chained_auto_packing' :'manual', 'chained_delay':'0'}
                    tires = stloc_obj.create(cr,uid,tire)   
                vehicle_obj.write(cr,uid,vehi.id,vehi_vals)       
        return res
        
wizard_create_locations()
    