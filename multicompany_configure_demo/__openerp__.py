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
        "name" : "multicompany_configure",
        "version" : "6.0.3",
        "author" : "Avanzosc",
        "website" : "http://www.openerp.com",
        "category" : "Vertical Modules/Parametrization",
        "description": """Module to create multicompany objects: Basic sequences, shop, warehouse, location and so on""",
        "depends" : ["account",
		            "product",
					"analytic",
					"base",
					"account_balance_reporting",
					"sale",
					"purchase",
					"stock"],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : ["multicompany_configure_demo1.xml",
					"multicompany_configure_demo2.xml",
						],
        "installable": True
} 
