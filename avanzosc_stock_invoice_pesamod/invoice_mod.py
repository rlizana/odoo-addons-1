
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    02/02/2012
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the  GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

'''
Created on 01/02/2012

@author: daniel
'''

from osv import fields, osv
from tools.translate import _
import pooler

class account_invoice (osv.osv):
    _inherit = 'account.invoice'
    _columns = {
                'name': fields.char('Description', size=256, select=True,readonly=True, states={'draft':[('readonly',False)]}),
                'origin': fields.char('Origin', size=256, help="Reference of the document that produced this invoice."),
                }
    
account_invoice()

