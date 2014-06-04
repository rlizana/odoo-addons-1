
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2014 AvanzOSC (Daniel). All Rights Reserved
#    Date: 03/06/2014
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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

from osv import osv
from osv import fields

#update sql to existing registries
#update account_move_line asl
#set user_id = ai.user_id
#from account_invoice as ai
#where ai.move_id = asl.move_id

class account_move_line(osv.osv):
        
    _inherit = 'account.move.line'
    
    def _get_salesman (self, cr, uid, ids, field_name, arg, context):
        res = {}
        if not context:
            context ={}
        for reg_id in ids:
            invoice_obj = self.pool['account.invoice']
            aml_reg = self.browse(cr,uid,reg_id)
            res[reg_id] = False
            if aml_reg.invoice:
                invo = aml_reg.invoice
                res[reg_id] = invo.user_id.id
        return res
    
    _columns = {
                'user_id': fields.function(_get_salesman, type="many2one", 
                    method=True, store=True, obj="res.users", string="salesman"),
                }
        
account_move_line()
