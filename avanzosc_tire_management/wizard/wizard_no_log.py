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

class wizard_tirenolog (osv.osv_memory):
    
    def _get_faults(self, cr, uid, data, context={}):
        
        values = {}
        bus_id = data['active_id']
        bus = self.pool.get('fleet.vehicles').browse(cr,uid,bus_id)
        res = bus.buslocat.id
        return res
    
    def _get_defaults(self, cr, uid, data, context={}):
        
        bus_id = data['active_id']    
        return bus_id
    
    """Tire mount no log"""
    _name = 'wizard.tirenolog'
    _description = 'Tire mount no log'
    
    _columns = {
                'bus': fields.many2one ('fleet.vehicles','Bus',readonly=True), # cambiar a tipo bus
                'bus_locat': fields.many2one ('stock.location','Bus',readonly=True),    
                'tire_locat': fields.many2one ('stock.location','Tire Location',required=True ),
                'tire' : fields.many2one ('stock.production.lot','Tire')
                }
    
    _defaults = {
      'bus': _get_defaults,
      'bus_locat': _get_faults,
      }

    def tire_mount (self, cr, uid, data, context):
        
        bus = self.browse(cr,uid,data[0]).bus
        tire_locat = self.browse(cr,uid,data[0]).tire_locat # aqui necesito saber el nombre -1 / -2 y tal
        tire= self.browse(cr,uid,data[0]).tire
        bus_obj = self.pool.get('fleet.vehicles')
        update={}
        if tire:
            if tire_locat.name.endswith("-1"):
                update ={ 'f_l_tire' : tire.id}
            elif tire_locat.name.endswith("-2"):
                update ={ 'f_r_tire' : tire.id}
            if bus.tires == 6:
                if tire_locat.name.endswith("-3"):
                    update ={ 'r_l_tire1' : tire.id}
                elif tire_locat.name.endswith("-4"):
                    update ={ 'r_l_tire2' : tire.id}
                elif tire_locat.name.endswith("-5"):  
                    update ={ 'r_r_tire2' : tire.id}                
                elif tire_locat.name.endswith("-6"):
                    update ={ 'r_r_tire1' : tire.id}
            elif bus.tires > 6:
                if tire_locat.name.endswith("-3"):
                    update ={ 'm_l_tire1' : tire.id}
                elif tire_locat.name.endswith("-4"):
                    update ={ 'm_l_tire2' : tire.id}
                elif tire_locat.name.endswith("-5"):  
                    update ={ 'm_r_tire2' : tire.id}                
                elif tire_locat.name.endswith("-6"):
                    update ={ 'm_r_tire1' : tire.id}
                elif tire_locat.name.endswith("-7"):
                    update ={ 'r_l_tire1' : tire.id}
                elif tire_locat.name.endswith("-8"):
                    update ={ 'r_r_tire1' : tire.id}
            bus_obj.write(cr,uid,bus.id,update)
        else:
            if tire_locat.name.endswith("-1"):
                update ={ 'f_l_tire' : False}
            elif tire_locat.name.endswith("-2"):
                update ={ 'f_r_tire' : False}
            if bus.tires == 6:
                if tire_locat.name.endswith("-3"):
                    update ={ 'r_l_tire1' : False}
                elif tire_locat.name.endswith("-4"):
                    update ={ 'r_l_tire2' : False}
                elif tire_locat.name.endswith("-5"):  
                    update ={ 'r_r_tire2' : False}                
                elif tire_locat.name.endswith("-6"):
                    update ={ 'r_r_tire1' : False}
            elif bus.tires > 6:
                if tire_locat.name.endswith("-3"):
                    update ={ 'm_l_tire1' : False}
                elif tire_locat.name.endswith("-4"):
                    update ={ 'm_l_tire2' : False}
                elif tire_locat.name.endswith("-5"):  
                    update ={ 'm_r_tire2' : False}                
                elif tire_locat.name.endswith("-6"):
                    update ={ 'm_r_tire1' : False}
                elif tire_locat.name.endswith("-7"):
                    update ={ 'r_l_tire1' : False}
                elif tire_locat.name.endswith("-8"):
                    update ={ 'r_r_tire1' : False}
            bus_obj.write(cr,uid,bus.id,update)
        res = {}
         
        return res
        
    
wizard_tirenolog()
    