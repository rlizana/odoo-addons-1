
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
    
product_uom()



