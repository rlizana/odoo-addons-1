
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 23/09/2013
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

from osv import osv
from osv import fields
import math
from _common import rounding
from tools.translate import _
import datetime
#
class product_template(osv.osv):
    
    _inherit = 'product.template'

    def write(self, cr, uid, ids, vals, context=None):
        return super(osv.osv, self).write(cr, uid, ids, vals, context=context)
    
product_template()

class product_uom(osv.osv):
    
    _inherit = 'product.uom'
        
    def write(self, cr, uid, ids, vals, context=None):
#        if 'category_id' in vals:
#            for uom in self.browse(cr, uid, ids, context=context):
#                if uom.category_id.id != vals['category_id']:
                    #raise osv.except_osv(_('Warning'),_("Cannot change the category of existing UoM '%s'.") % (uom.name,))
        return super(osv.osv, self).write(cr, uid, ids, vals, context=context)
    
    def _compute_qty_obj(self, cr, uid, from_unit, qty, to_unit, context=None):
        if context is None:
            context = {}
#        if from_unit.category_id.id <> to_unit.category_id.id:
#            if context.get('raise-exception', True):
#                raise osv.except_osv(_('Error !'), _('Conversion from Product UoM %s to Default UoM %s is not possible as they both belong to different Category!.') % (from_unit.name,to_unit.name,))
#            else:
#                return qty
        amount = qty / from_unit.factor
        if to_unit:
            amount = rounding(amount * to_unit.factor, to_unit.rounding)
        return amount
    
product_uom()



