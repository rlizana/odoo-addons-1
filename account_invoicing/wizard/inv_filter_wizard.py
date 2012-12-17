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

import time
import wizard
import osv
import pooler


section_form_stage1 = '''<?xml version="1.0"?>
<form string="Record filter">
    <field name="method_id" readonly="1"/>
    <field name="field_id"/>
    <field name="cond_type"/>
</form>'''

section_form_stage2 = '''<?xml version="1.0"?>
<form string="Record filter condition">
    <field name="rec_filter_id"/>
    <field name="cond_value" colspan="4" nolabel="1"/>
</form>'''

def _field_type_get(self, cr, uid, context={}):
    #pool = pooler.get_pool(cr.dbname)
    #obj = pool.get('inv.rec_filter')
    #ids = obj.search(cr, uid, [])
    #rec = obj.browse(cr, uid, ids, context)
    if data['form']['domain']:
        return [('eq','equal to'), ('nq','not equal to'), ('rxp', 'regexp')]
    return []

section_fields_stage1 = {
    'method_id': {'string':'Methodology', 'type':'many2one', 'relation':'inv.method', 'required':True},
    'field_id': {'string':'Fields', 'type':'many2one', 'relation':'ir.model.fields', 'required':True, 'domain':"[('model_id','=',domain)]"},
    'cond_type': {'string':'Condition type', 'type':'selection', 'selection':[], 'required':True},
    'domain': {'string':'Domain field', 'type':'many2one', 'relation':'ir.model'},
    #'condition_id': {'string':'Condition', 'type':'one2many', 'relation':'inv.rec_filter_cond', 'required':True},
}

section_fields_stage2 = {
    'rec_filter_id': {'string':'Filter', 'type':'many2one', 'relation':'inv.rec_filter', 'required':True},
    'cond_value': {'string':'Condition value', 'type':'one2many', 'relation':'inv.cond_value', 'required':True},
}

def load_data1(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)
    obj = pool.get('inv.method')
    method = obj.browse(cr, uid, data['id'], context)
    data['form']['domain'] = method.model_id.id
    data['form']['method_id'] = method.id
    form = data['form']
    return data['form']

def load_data2(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)
    obj = pool.get('inv.rec_filter')

    #recfilter = obj.browse(cr, uid, data['id'], context)
    #data['form']['rec_filter_id'] = recfilter.id
    #ids = obj.search(cr, uid, [])
    #new_id = ",".join(map(str,ids))
    #recfilter = obj.read(cr, uid, ids, ['id'], context)
    #data['form']['rec_filter_id'] = recfilter[0]['id']
    return data['form']

def save_data(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)
    rec_filter = pool.get('inv.rec_filter')
    rec_filter_cond = pool.get('inv.rec_filter_cond')
    #rec = rec_filter.browse(cr, uid, data['id'], context)
    #ids = rec_filter.search(cr, uid, [])

    #cr.execute("select nextval('"+rec_filter._sequence+"')")
    #id_new = cr.fetchone()[0]
    #rec_filter.write(cr, uid, ids, {'method_id':data['form']['method_id'], 'field_id':data['form']['field_id']})
    field_id = rec_filter.browse(cr, uid, data['form']['field_id'])

    rec_filter.create(cr, uid, {'method_id': data['form']['method_id'],'field_id': field_id.id})

    return {}

class wizard_rec_filter(wizard.interface):
    states = {
        'init': {
            'actions': [load_data1], 
            'result': {'type':'form', 'arch':section_form_stage1, 'fields':section_fields_stage1, 'state':[('end','Cancel'),('next','Next')]}
        },
        'next': {
            'actions': [load_data2], 
            'result': {'type':'form', 'arch':section_form_stage2, 'fields':section_fields_stage2, 'state':[('end','Cancel'),('init','Back'),('save','Save')]}
        },
        'save': {
            'actions': [save_data],
            'result': {'type':'state', 'state':'end'}
        }
    }

wizard_rec_filter('inv.rec_filter.menu')

