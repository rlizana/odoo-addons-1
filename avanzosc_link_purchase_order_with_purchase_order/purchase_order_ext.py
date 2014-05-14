# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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

class purchase_order(osv.osv):

    _inherit = 'purchase.order'
    
    _columns = {'purchase_order_ids': fields.many2many('purchase.order','purchase_order_purchase_rel','purchase_order_id','purchase_order_id2','Purchase Orders'),
                'purchase_order_ids2': fields.many2many('purchase.order','purchase_order_purchase_rel','purchase_order_id2','purchase_order_id','Purchase Orders'),
                }
    
purchase_order()