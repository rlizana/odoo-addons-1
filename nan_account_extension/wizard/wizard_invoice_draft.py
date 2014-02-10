# -*- encoding: latin-1 -*-
##############################################################################
#
# Copyright (c) 2010 NaN Projectes de Programari Lliure, S.L. All Rights Reserved.
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
from osv import osv
from tools.translate import _
import netsvc
import pooler

class wizard_invoice_draft(osv.osv_memory):
    """
    This wizard will cancel the all the selected invoices and them set as draft state
    If in the journal, the option allow cancelling entry is not selected then it will give warning message.
    """
    
    _name = "wizard.invoice.draft"
    _description = "SCancel the Selected Invoices and set to draft State"
    


    def invoice_draft(self, cr, uid, data, context):
        
        if context is None:
           context = {}
        wf_service = netsvc.LocalService('workflow')
        pool_obj = pooler.get_pool(cr.dbname)
        invoice_obj = pool_obj.get('account.invoice')
        if context['active_ids']:
            for id in context['active_ids']:
                invoice = invoice_obj.read(cr, uid, id, ['state'], context=context)
                if invoice['state'] in ('cancel', 'paid'):
                    raise osv.except_osv(_('Warning'), _("Selected Invoice(s) cannot be cancelled as they are already in 'Cancelled' or 'Done' state!"))
                wf_service.trg_validate(uid, 'account.invoice', id, 'invoice_cancel', cr) # cancelar factura
                invoice_obj.write(cr, uid, id, {'state':'draft'}) # estado draft
        return {}

wizard_invoice_draft()
#class wizard_invoice_draft(wizard.interface):
#    states = {
#        'init': {
#            'actions': [_invoice_draft],
#            'result': {'type':'state', 'state':'end'}
#        }
##    }
#wizard_invoice_draft('account.invoice.state.draft')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

