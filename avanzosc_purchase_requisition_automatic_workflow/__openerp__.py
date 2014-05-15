
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
    "name": "Avanzosc Purchase Requisition Automatic Workflow", 
    "version": "1.0",
    "depends": ["purchase_requisition","avanzosc_purchase_requisition_ext"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
    Este módulo automatiza el workflow de solicitudes de compra, de la siguiente manera:
    
         1.- Que pase a "En proceso" cuando se creen presupuestos/pedidos para los materiales incluidos. 
         2.- Que pase a "Realizado" cuando se aprueben mediante 1 ó varios pedidos TODAS las líneas que incluye la solicitud.    
    """,
    "init_xml": [],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}