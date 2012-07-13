# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
	"name" : "Pesa MRP Repair",
	"version" : "0.9",
	"description" : """Modifies the original mrp_repair module to simplify repair form.""",
	"author" : "NaN Projectes de Programari LLiure, S.L. - Mod (Daniel)",
	"website" : "http://www.NaN-tic.com",
	"depends" : [ 
		'mrp_repair', 
	], 
	"category" : "Custom Modules",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : [ 
		'mrp_repair_wizard.xml', 
		'actions_mrp_repair_data.xml',
#		'security.xml',
        ],
	"active": False,
	"installable": True
}
