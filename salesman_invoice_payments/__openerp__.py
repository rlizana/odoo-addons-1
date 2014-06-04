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
    "name": "Avanzosc Salesman Saleorder Payments",
    "version": "1.0",
    "depends": ["account_payment_extension"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
        This module adds a relation field between saleorder payment and the
        salesman defined in the invoice of the payment. 
    """,
    "init_xml": [],
    'update_xml': [
                   'salesman_invoice_payment_view.xml'
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}