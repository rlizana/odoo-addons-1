# -*- encoding: latin-1 -*-
##############################################################################
#
# Copyright(c)2010 NaN Projectes de Programari Lliure,S.L. All Rights Reserved.
#                    http://www.NaN-tic.com
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
import netsvc
import pooler
from osv import osv
from osv import fields
from tools.translate import _

class wizard_invoice_draft(osv.osv_memory):
    
    _name = 'wizard.invoice.draft'
    
    def invoice_draft(self, cr, uid, ids, context=None):
        invoice_obj = self.pool['account.invoice']
        
        if not context:
            context = {}
        
        has_error = False
        
        inv_ids = False
        if 'active_ids' in context:
            inv_ids = context['active_ids']
        
        ids = invoice_obj.search(cr,uid,[('id','in',inv_ids),
                                         ('state','=','open')])
        ids.sort()
        inv_ids.sort()
        
        if ids != inv_ids:
            has_error = True
            
        draft_ids = ids[:]
        cancel_ids = ids[:]
        
        for cancel_id in cancel_ids:
            try:
                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_validate(uid, 'account.invoice', cancel_id,
                                        'invoice_cancel',cr)
            except:
                draft_ids.remove(cancel_id)
                has_error = True            
                continue
        cr.commit()
        
        for draft_id in draft_ids:
            try:
                invoice_obj.write(cr,uid,[draft_id], {'state':'draft'})
                wf_service2 = netsvc.LocalService("workflow")
                wf_service2.trg_create(uid, 'account.invoice', draft_id, cr)
            except:
                has_error = True
                continue
        cr.commit()
        
        if has_error:
            raise osv.except_osv(_('Error!'),_('Some invoices can not be set '
                                               'to draft state.'))
        return {'type': 'ir.actions.act_window_close'}