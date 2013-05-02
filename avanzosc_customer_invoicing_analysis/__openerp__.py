# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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

{
    "name": "Avanzosc Customer Invoicing Analysis",
    "version": "1.0",
    "depends": ["account","avanzosc_sector_area_incustumers"],
    "author": "Avanzosc",
    "category": "Custom Modules",
    "description": """
    
    """,
    "init_xml": [],
    'update_xml': ["account_invoice_line_ext_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}