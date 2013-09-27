
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 Daniel (AvanzOSC). All Rights Reserved
#    Date: 18/02/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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
    "name" : "Avanzosc Human Resources Task Control",
    "version" : "1.2",
    "description": """ 
                This module adds:
                - Presence task time control by user task list 
                    """,
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "depends" : ["base","hr_attendance","project_timesheet"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["hr_task_control_view.xml",
                    ],
    "active" : False,
    "installable" : True
    
}
