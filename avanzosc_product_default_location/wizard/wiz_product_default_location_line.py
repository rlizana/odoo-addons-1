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
from tools.translate import _
import netsvc
 
class wiz_product_default_location_line(osv.osv_memory):
    
    _name="wiz.product.default.location.line"
    _description = "Wiz Product Default Location line"
    
    _columns = {'wiz_product_default_location_id':fields.many2one('wiz.product.default.location', 'wizard'),
                'product_id':fields.many2one('product.product', 'Product'),
                'default_location_id':fields.many2one('stock.location', 'Default Location'),    
                }
    
wiz_product_default_location_line()