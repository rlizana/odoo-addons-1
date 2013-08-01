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

class product_supplierinfo(osv.osv):

    _name = 'product.supplierinfo'
    _inherit = 'product.supplierinfo'   
    
    _columns = {# Modifico este campo porque ahora puede ser un Proveedor o un Cliente
                'name' : fields.many2one('res.partner', 'Supplier/Customer', required=True, ondelete='cascade', help="Supplier/Customer of this product"),
                # Campo para saber si es un proveedor
                'is_customer':fields.boolean('Is Customer'),
                }
    _defaults = {
                 'is_customer': lambda self, cr, uid, c: c.get('is_customer', False),
                 }
    
    def create(self, cr, uid, data, context=None):
        return super(product_supplierinfo, self).create(cr,uid,data,context)

product_supplierinfo()