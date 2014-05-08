
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
    "name": "AvanzOsc - Purchase Requisition extension", 
    "version": "1.0",
    "depends": ["purchase_requisition"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
    Este módulo relaciona la línea de pedido de compra, con la solicitud de compra.
    Además en la solicitud de compra crea una nueva pestaña, en la que muestra
    todas las líneas de compra generadas.
    """,
    "init_xml": [],
    'update_xml': ['avanzosc_purchase_requisition_ext_view.xml',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}