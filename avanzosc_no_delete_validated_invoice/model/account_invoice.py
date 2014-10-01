# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2013 Avanzosc <http://www.avanzosc.com>
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
from osv import osv, fields
from tools.translate import _

class AccountInvoice(osv.osv):
    _inherit = 'account.invoice'
    
    def unlink(self, cr, uid, ids, context=None):
        if ids:
            for invoice in self.browse(cr, uid, ids, context=context):
                if invoice.number:
                    raise osv.except_osv(_('Invalid Action !'),
                                         _('The invoice has already been validated and it has number assigned. IT CAN NOT BE REMOVED. To cancel it use the button "REFUND".'))
        return super(AccountInvoice, self).unlink(cr, uid, ids, context=context)
