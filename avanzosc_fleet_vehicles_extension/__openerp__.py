# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    09/11/2011
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Fleet vehicles extension",
    "version": "2.04",
    "depends": ["base", "fleet_manager"],
    "author": "AvanzOSC",
    "category": "category",
    "website": 'http://www.avanzosc.com',
    "description": """This module add new fields for sharoons fleet manager module.
    Adds a relation between vehicles <=> Products.
    Adds a wizard for automatic refueling data load from a csv file. Disabled Account unlink.
    Adds a preventive management repair creator for the vehicles using defined frecuency or milleage created alarms """,
    "init_xml": [],
    "update_xml": [
                   "avanzosc_fleet_vehicles_extension_view.xml",
                   "wizard/import_refuellog_view.xml"
                   
    ],
    "demo_xml": [],
    "installable": True,
    "active": False,
#    'certificate': 'certificate',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
