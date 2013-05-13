# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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
        "name" : "Avanzosc StockPicking Warehouse Location",
        "version" : "6.0.3",
        "author" : "Avanzosc",
        "website" : "http://www.openerp.com",
        "category" : "Custom",
        "description": """
            This module shows the location of the product (row, shelf, box) in the stock pickings
            """,
        "depends" : ["product","stock"],
        "init_xml": ['stock_move_ext_view.xml'],
        "demo_xml" : [ ],
        "update_xml" : [],
        "installable": True
} 
