
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2014 AvanzOSC (Daniel). All Rights Reserved
#    Date: 20/03/2014
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

import wizard
from osv import osv
from tools.translate import _
import netsvc

class wizard_saleorder_wf(osv.osv_memory):
    
    _name = 'wizard.saleorder.wf'
    _description = 'Wizard Sale Order Workflow'
    
    def saleorder_process_wf(self, cr, uid, ids, context=None):
        
        res = {}
        if context is None:
           context = {}
        wf_service = netsvc.LocalService('workflow')
        sale_obj = self.pool.get('sale.order')
        procurement_obj = self.pool.get('procurement.order')
        if 'active_ids' in context:
            for sale_id in context['active_ids']:
                sale = sale_obj.browse(cr,uid,sale_id)
                if sale.state != 'progress':
                    raise osv.except_osv(_('Warning'), _("Selected Sale Order cannot be processed as they are already in 'Done' state!"))
                else:
                    procurement_id_lst = procurement_obj.search(cr,uid,[('origin','=',sale.name),('state','=','confirmed')])
                    for procurement_id in procurement_id_lst:
                        wf_service.trg_validate(uid, 'procurement.order', procurement_id, 'button_check', cr)
        return res

wizard_saleorder_wf()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
