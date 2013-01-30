##############################################################################
#
# Copyright (c) 2008-2009 SIA "KN dati". (http://kndati.lv) All Rights Reserved.
#                    General contacts <info@kndati.lv>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import wizard
import pooler

class agreement_wizard(wizard.interface):
    _create_form = """<?xml version="1.0"?>
    <form string="Run agreement(s)">
        <label string="Do you want set to process selected agreement(s) ?" colspan="4"/>
    </form>"""

    def _set_process(self, cr, uid, data, context):
        pool = pooler.get_pool(cr.dbname)
        agr_obj = pool.get('inv.agreement')
        for r in agr_obj.browse(cr, uid, data['ids'], {}):
            if r.state=='draft':
                agr_obj.set_process(cr, uid, [r.id])
        return {}

    _create_fields = {}

    states = {
        'init' : {
            'actions' : [], 
            'result' : {'type':'form', 'arch':_create_form, 'fields':_create_fields, 'state': [('end','No'),('start','Yes')]},
        },
        'start' : {
            'actions' : [],
            'result' : {'type':'action', 'action':_set_process, 'state':'end'},
        },
    }
agreement_wizard('inv.agreement.wizard')

