
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Daniel (Avanzosc) <danielcampos@avanzosc>
#    03/11/2011
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    "name" : "Avanzosc Inventory Calculation", 
    "version" : "1.0",
    "description": """ 
                This module adds:
                 - Wizard button to calculate inventory by product agrupation and its location (lot omitted)
                    """,
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "depends" : ["base","stock"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["inventory_calc_view.xml"
                    ],
    "active" : False,
    "installable" : True
    
}
