
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



{
    "name" : "Tire Management",
    "version" : "1.4",
    "description" : """This module allows to manage tires traceability from a vehicle.
                        - Defines a location for each vehicle
                        - Defines Numeric locations for each tire
                        """,
    "author" : "AvanzOSC",
    "website" : "www.avanzosc.com",
    "depends" : ["base","avanzosc_fleet_vehicles_extension"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    "security/avanzosc_tire_manager_security.xml",
                    "security/ir.model.access.csv",
                    "wizard/create_vehicle_loc_view.xml",
                    "avanzosc_mng_tires_view.xml",
                    ],
                    
    "active" : False,
    "installable" : True
    
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
