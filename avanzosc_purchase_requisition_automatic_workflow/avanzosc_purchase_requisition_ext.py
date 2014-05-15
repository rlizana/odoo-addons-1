
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
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
from osv import osv, fields
from tools.translate import _


class purchase_requisition(osv.osv):

    _name = 'purchase.requisition'
    _inherit = 'purchase.requisition'

    def make_purchase_order_avanzosc(self, cr, uid, ids, context=None):
        res = super(purchase_requisition,self).make_purchase_order_avanzosc(cr, uid, ids, context=context)
        if ids:
            for id in ids:
                self.write(cr,uid,[id],{'state': 'in_progress'})
        
        return res

    def make_purchase_order(self, cr, uid, ids, partner_id, context=None):
        res = super(purchase_requisition,self).make_purchase_order(cr, uid, ids, partner_id, context=context)
        if ids:
            for id in ids:
                self.write(cr,uid,[id],{'state': 'in_progress'})
        
        return res
    
purchase_requisition()