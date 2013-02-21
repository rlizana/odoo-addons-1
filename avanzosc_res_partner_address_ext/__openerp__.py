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
        "name" : "Avanzosc Partner Address Extension",
        "version" : "6.0.3",
        "author" : "Avanzosc",
        "website" : "http://www.openerp.com",
        "category" : "Vertical Modules/Parametrization",
        "description": """
            If I go to an address, both from a purchase order, and from a sales order, I change the ZIP code of the address,
            and not saved the changes of direction. This module solves this error.
            """,
        "depends" : ["base",
		             "l10n_es_toponyms",
					 "l10n_es_toponyms_region"
                     ],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : [],
        "installable": True
} 
