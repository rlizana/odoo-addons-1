
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2014 AvanzOSC (Daniel). All Rights Reserved
#    Date: 27/03/2014
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

from osv import osv,fields
from tools.translate import _
import netsvc
import pooler

class wizard_analytic_run(osv.osv_memory):
    
    """
    This wizard will generate the analytic lines
    """
    
    _name = "wizard.analytic.run"
    _description = "Generate analytic entry lines for selected agreements"
    
    _columns = {
                'date': fields.date('Invoicing Date', size=64, 
                    help='If no date is selected current date will be assigned'),
                 }
    
    
    def analytic_run(self, cr, uid, ids, context):
        
        if context is None:
            context = {}
        res = {}
        #wf_service = netsvc.LocalService('workflow')
        #pool_obj = pooler.get_pool(cr.dbname)
        agreement_obj = self.pool.get('inv.agreement')
        wiz = self.browse(cr,uid,ids[0])
        if wiz.date:
            context['current_date'] = wiz.date
        method_obj = self.pool.get('inv.method')
        if context['active_ids']:
            for agree_id in context['active_ids']:
                agrement = agreement_obj.browse(cr,uid,agree_id)
                if agrement.state != 'running':
                    raise osv.except_osv(_('Warning'), _("Selected Agreement is not in 'Running' state!"))
                methods = agrement.service.method_ids
                if methods:
                    context['wizard'] = True
                    for m in methods:
                        method_obj._run_filters(cr,uid,[m.id],agree_id,context)
        return res
        
wizard_analytic_run()