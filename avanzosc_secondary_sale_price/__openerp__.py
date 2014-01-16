# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2014 AvanzOSC S.L. (Oihane) All Rights Reserved
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "AvanzOsc - Secondary unit price extension",
    "version": "1.0",
    "depends": ["avanzosc_calculate_coeficient_udv_automatically"],
    "author": "AvanzOSC",
    "category": "Custom Module",
    "website": "http://www.avanzosc.es",
    "complexity": "easy",
    "description": """
    This module adds secondary price to be calculated by coef_amount
    """,
    "init_xml": [],
    "update_xml": ["product_view.xml"],
    "demo_xml": [],
    "installable": True,
    "active": False,
#    "certificate": 'certificate',
}