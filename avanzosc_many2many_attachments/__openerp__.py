# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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
    "name": "Avanzosc many2many Attachments",
    "version": "1.0",
    "depends": ["base","product","nan_quality_control","document"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
        Avanzosc Custom Modules. This module creates a Many2Many in the following tables:
        
        product with ir.attachment
        qc_test_template with ir.attachment
        qc_test with ir.attachment
        
    """,
    "init_xml": [],
    'update_xml': ['product_product_ext_view.xml',
                   'qc_test_template_ext_view.xml',
                   'qc_test_ext_view.xml',
                   'ir_attachment_ext_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}