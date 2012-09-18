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


{
    "name" : "Preventive MRP & Fleet Manager Extension",
    "version" : "2.05",
    "description" : """ 
        This module ables to create repair orders using alarms.
        Create new repair orders for the vehicles, using the preventive alarms defined in the module avanzosc_mrp_preventive_master_data.
    """,
    "author" : "AvanzOSC",
    "website" : "www.avanzosc.com",
    "depends" : ["mrp_repair","avanzosc_mrp_preventive_master_data"],
    "category" : "Generic Modules",
    "init_xml" : ["preventive_mrp_data.xml"],
    "demo_xml" : [],
    "update_xml" : [
                    "preventive_mrp_view.xml",
                    "wizard/wizard_prev_op_view.xml"
                   ],
                    
    "active" : False,
    "installable" : True
    
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
