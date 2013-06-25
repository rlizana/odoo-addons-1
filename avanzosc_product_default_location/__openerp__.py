# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2013 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    "name": "Avanzosc Product Default Location",
    "version": "1.0",
    "depends": ["base","product","stock"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
        This module displays the default location field in the product tree, and also installs a wizard for entering the default location field in all the products that do not have.
    """,
    "init_xml": [],
    'update_xml': ['wizard/wiz_product_default_location_view.xml',
                   'wizard/wiz_product_default_location_line_view.xml',
                   'product_product_ext_view.xml'
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}