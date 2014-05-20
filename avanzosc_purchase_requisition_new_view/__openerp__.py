
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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
    "name": "Avanzosc Purchase Requisition New View", 
    "version": "1.0",
    "depends": ["purchase_requisition","avanzosc_purchase_requisition_ext","avanzosc_product_extended_multicompany"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
    Modificaciones en Vistas de árbol de las Purchase Requisition:
    
    1.- Ficha "Productos", para cada línea, campos a incluir y orden:

            1.1. Producto
            1.2. Cantidad
            1.3. Proveedor por defecto
            1.4. Proveedor última compra
            1.5. Precio última compra
            1.6. Fecha última compra
            
    2.- Ficha "Presupuestos", para cada línea, campos a incluir y orden:

            2.1. Referencia (Pedido de Compras)
            2.2. Fecha Pedido
            2.3. Proveedor
            2.4. Fecha Prevista
            2.6. Estado
            
    3.- Ficha "Purchase Lines Info", para cada línea, campos a incluir y orden:

            3.1. Referencia del pedido (de compras)
            3.2. Descripción
            3.3. Proveedor
            3.4. Fecha planificada
            3.5. Precio
            3.6. Cantidad
            3.7. Subtotal
    """,
    "init_xml": [],
    'update_xml': ['purchase_requisition_line_ext_view.xml',],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}