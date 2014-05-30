# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
    "name": "Avanzosc Product Extended Multicompany",
    "version": "1.0",
    "depends": ["product", "sale","stock"],
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "category": "category",
    "description": """
    This module adds new calculate fields in product:
        'last_purchase_price'
        'last_purchase_date'
        'last_sale_price'
        'last_sale_date'
        'standard_code'
        
    Si es una compra o venta entre compañías del grupo, no se actulizan estos datos
    en la ficha del producto.
    """,
    "init_xml": [],
    'update_xml': ['security/avanzosc_product_extended_multicompany.xml',
                   'product_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}