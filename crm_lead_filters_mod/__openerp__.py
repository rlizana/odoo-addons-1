
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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

{
    "name" : "Avanzosc crm lead filters modification",
    "version" : "1.0",
    "description": """ 
                This module adds custom filters in crm Leads.
                - Contact/Address
                Group by...
                    - Last action date
                    - Update date
                    """,
    "author" : "AvanzOSC",
    "website" : "www.avanzosc.com",
    "depends" : ["crm"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["crm_lead_filters.xml",
                    ],
    "active" : False,
    "installable" : True
    
}

