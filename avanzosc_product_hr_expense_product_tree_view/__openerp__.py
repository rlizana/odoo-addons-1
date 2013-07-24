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
    "name": "Avanzosc Product Hr Expense Product Tree View",
    "version": "1.0",
    "depends": ["product","hr_expense"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
        When you install the module hr_expense, creates a view "product.product.tree" with the same priority as normal view product.
        This module puts priority 6 to the view of the product, and priority 16 to the viow of hr_expense

    """,
    "init_xml": [],
    'update_xml': ['product_ext_view.xml',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}