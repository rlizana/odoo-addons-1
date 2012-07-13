
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    22/03/2012
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

from osv import osv
from osv import fields
import base64, urllib
from tools.translate import _


class fleet_vehicles (osv.osv):
    
    _inherit = 'fleet.vehicles'
    
    _columns = {
                'axles':fields.selection([
                ('2axle','2 Axles'),
                ('3axle','3 Axles')],'Axles'),
                'buslocat': fields.many2one ('stock.location','Bus Location',readonly=True),
                'schema' : fields.binary('Schema'),
                'f_r_tire' : fields.many2one ('stock.production.lot','Right Tire', readonly=True),
                'f_l_tire' : fields.many2one ('stock.production.lot','Left Tire', readonly=True),
                'r_r_tire1': fields.many2one ('stock.production.lot','Right Tire', readonly=True),
                'r_l_tire1': fields.many2one ('stock.production.lot','Left Tire', readonly=True),
                'r_r_tire2': fields.many2one ('stock.production.lot','Right Tire (Internal)', readonly=True), 
                'r_l_tire2': fields.many2one ('stock.production.lot','Left Tire (Internal)', readonly=True), 
                'm_r_tire1': fields.many2one ('stock.production.lot','Right Tire', readonly=True),
                'm_l_tire1': fields.many2one ('stock.production.lot','Left Tire', readonly=True),
                'm_r_tire2': fields.many2one ('stock.production.lot','Right Tire (Internal)', readonly=True),
                'm_l_tire2': fields.many2one ('stock.production.lot','Left Tire (Internal)', readonly=True)
    }
    
    def tire_mount(self, cr, uid, ids, *args):
        form_view_id = self.pool.get('ir.model.data').search(cr, uid, [('name', '=', 'mount_button_view')])[0]
        res = {
                 'name': False,
                 'view_type': 'form',
                 'view_id': False,
                 'view_mode': 'form',
                 'res_model': 'fleet.vehicles',
                 'views': [(form_view_id , 'form')],
                 'type': 'ir.actions.act_window'
        
#                 'views': [(form_view_id, 'form'), (False,'calendar'), (False, 'graph')],
#                 'view_id': form_view_id
                } 
        
        return res
    
fleet_vehicles()


class tire_stock_lot(osv.osv):
    
    _name = 'tire.stock.lot'
    _description = 'Tire Stock Lot'
    _columns = {
                'name': fields.char('Move', size=64),
                'lot_id': fields.many2one('stock.production.lot', 'Tire'),
                'origin' : fields.many2one ('stock.location','Origin'),
                'destination': fields.many2one ('stock.location','Destination'),
                'data':fields.datetime('Created Date'),
                'odomold' : fields.integer('Old Odometer km.',size=10),
                'odomnew' : fields.integer('New Odometer km.',size=10),
                'tire_km' :fields.integer('Tire Km.',size=10),
                'tire_km_total':fields.integer('Tire Total Km.',size=10)
                }
tire_stock_lot()

class stock_production_lot(osv.osv):
    
    _inherit = 'stock.production.lot'
    
    _columns = {
                'prod_move':fields.one2many('stock.move','prodlot_id','Product moves'),
                'tire_km':fields.integer('Tire Km.',size=10),
                'odometers':fields.text('Odometers'),
                'tire_lot_data': fields.one2many('tire.stock.lot', 'lot_id', 'Tire Data', readonly=True)
                }

stock_production_lot()


class res_company (osv.osv):
    
    _inherit = 'res.company'
    
    _columns = {
                'tire_stock': fields.many2one ('stock.location','Tire Stock'),
                'retread': fields.many2one ('stock.location','Retread'),
                'scratch': fields.many2one ('stock.location','Scratch'),
                'waste': fields.many2one ('stock.location','Waste'),
                'flatire': fields.many2one ('stock.location','Flat Tire'),
                'schema4' : fields.binary('4 Tire Schema'),
                'schema6' : fields.binary('6 Tire Schema'),
                'schema8' : fields.binary('8 Tire Schema')
                }
res_company()

class stock_move(osv.osv):
    
    _inherit = 'stock.move'
    
    _columns = {
                'odometer':fields.integer('Odometer km.',size=10),
                }
    
    def unlink( self, cr, uid, ids, context=None ):
        
        stock_movement = self.browse(cr,uid,ids[0])
        tire_data = self.pool.get('tire.stock.lot')
        odometer= stock_movement.odometer
        tire_list=tire_data.search(cr,uid,[('lot_id','=',stock_movement.prodlot_id.id),('data','=',stock_movement.date)])
        #Borrar datos rueda
        if tire_list != []:
            tire_data.unlink(cr, uid, tire_list[0])
        #Final borrado datos rueda
        
        if odometer >0:
            #tire_list=tire_data.search(cr,uid,[('lot_id','=',stock_movement.prodlot_id.id),('data','=',stock_movement.date)])
            loc_obj = self.pool.get('stock.location')
            vehic_obj = self.pool.get('fleet.vehicles')
            if stock_movement.location_dest_id.location_id:
                loc_parent_id = stock_movement.location_dest_id.location_id.id #movement location from parent id
                loc_name = stock_movement.location_dest_id.name
                vehic_list = vehic_obj.search(cr,uid,[('buslocat','=',loc_parent_id)])
                vehicle = vehic_obj.browse(cr,uid,vehic_list[0])
                if loc_name.endswith("-1"):
                    update ={ 'f_l_tire' : False}
                elif loc_name.endswith("-2"):
                    update ={ 'f_r_tire' : False}
                if vehicle.tires == 6:
                    if loc_name.endswith("-3"):
                        update ={ 'r_l_tire1' : False}
                    elif loc_name.endswith("-4"):
                        update ={ 'r_l_tire2' : False}
                    elif loc_name.endswith("-5"):  
                        update ={ 'r_r_tire2' : False}                
                    elif loc_name.endswith("-6"):
                        update ={ 'r_r_tire1' : False}
                elif vehicle.tires > 6:
                    if loc_name.endswith("-3"):
                        update ={ 'm_l_tire1' : False}
                    elif loc_name.endswith("-4"):
                        update ={ 'm_l_tire2' : False}
                    elif loc_name.endswith("-5"):  
                        update ={ 'm_r_tire2' : False}                
                    elif loc_name.endswith("-6"):
                        update ={ 'm_r_tire1' : False}
                    elif loc_name.endswith("-7"):
                        update ={ 'r_l_tire1' : False}
                    elif loc_name.endswith("-8"):
                        update ={ 'r_r_tire1' : False}
                vehic_obj.write(cr,uid,vehicle.id,update)
        result = super(stock_move, self).unlink(cr, uid, ids, context)
        return result

    
stock_move()
    


