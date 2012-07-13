# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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

'''
Created on 23/09/2011

@author: daniel
'''

from osv import fields, osv
from tools.translate import _
import pooler

class stock_move(osv.osv):
    _inherit = 'stock.move'
    _columns = {
        'product_tmpl_id': fields.related ('product_id', 'product_tmpl_id', type ='many2one', relation="product.template",string="Bridge" ),
        'rack': fields.related ('product_tmpl_id', 'loc_rack', type='char',relation="product.template",string="Rack"),
#        'stan2': fields.char (string="Rack", size=64),
    }
    _defaults = {
        'product_tmpl_id': lambda *a:False,
        'rack': lambda *a:False
    }
    
stock_move()