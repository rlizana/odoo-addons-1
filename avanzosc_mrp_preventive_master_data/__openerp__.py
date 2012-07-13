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
    "name": "Avanzosc Mrp preventive master data",
    "version": "1.05",
    "depends": ["base","avanzosc_fleet_vehicles_extension"],
    "author": "AvanzOSC",
    "category": "mrp",
    "description": """
    This module allows generating vehicle preventive orders automatically
    """,
    "init_xml": [],
    'update_xml': ["security/avanzosc_preventive_manager_security.xml",
                   "security/ir.model.access.csv",
                   'avanzosc_mrp_preventive_master_data_view.xml',
                   "preventive_sequence.xml",
                   "wizard/create_order_wizard_view.xml",
                   "wizard/create_preventive_wizard_view.xml"
                   ],

#                    ,
#                   
#                   
    
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}