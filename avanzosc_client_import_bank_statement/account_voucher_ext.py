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
from osv import osv
from osv import fields
import decimal_precision as dp

class account_voucher(osv.osv):
    
    _inherit = 'account.voucher'
    
    def action_move_line_create(self, cr, uid, ids, context=None):
        
        super(account_voucher,self).action_move_line_create(cr, uid, ids, context)
        
        account_bank_statement_line_obj = self.pool.get('account.bank.statement.line')
        account_voucher_obj = self.pool.get('account.voucher')
        account_move_line_obj = self.pool.get('account.move.line')
        for voucher in self.browse(cr, uid, ids, context=context):
            account_bank_statement_line_ids = account_bank_statement_line_obj.search(cr, uid, [('voucher_id', '=', voucher.id)])
            if account_bank_statement_line_ids:
                account_bank_statement_line = account_bank_statement_line_obj.browse(cr,uid, account_bank_statement_line_ids[0])
                if account_bank_statement_line.type == 'customer':
                    account_voucher2 = account_voucher_obj.browse(cr,uid, voucher.id)
                    if account_voucher2.move_ids:
                        for line in account_voucher2.move_ids:
                            if line.credit > 0:
                                w_imp = line.credit
                                account_move_line_obj.write(cr, uid, [line.id], {'credit': 0,
                                                                                 'debit': w_imp})
                            else:
                                w_imp = line.debit
                                account_move_line_obj.write(cr, uid, [line.id], {'debit': 0,
                                                                                 'credit': w_imp,
                                                                                 'account_id': account_bank_statement_line.account_id.id})
        return True

account_voucher()
