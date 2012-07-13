# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc  
#    Copyright (C) 2011-2012 Avanzosc  (http://www.avanzosc.com). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields


class fleet_vehicles (osv.osv):
    
    _inherit = 'fleet.vehicles'
    
    _columns = {
                'preop':fields.one2many('vehicle.prev.op','vehicle','Next Revisions'),
                'alert_list':fields.one2many('preventive.proceed','ivehicle','Alerts'),
                'vehicles_ids':fields.many2many('preventive_master', 'vehicles_maint_rel', 'fleet_vehicles_id','preventive_master_id'),
    }
    
fleet_vehicles()

class vehicle_prev_op(osv.osv):
    
    _inherit = 'vehicle.prev.op'
    
    _columns = {
            'opname':fields.many2one('operation.vehicle.materials', 'Preventive operation', readonly=True),
            }
        
vehicle_prev_op()


    