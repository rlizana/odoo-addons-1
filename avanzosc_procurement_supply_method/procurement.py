# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2008-2014 AvanzOSC S.L. (Oihane) All Rights Reserved
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
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import orm, fields

class procurement_order(orm.Model):
    
    _inherit = 'procurement.order'
    
    _columns = {
            'supply_method': fields.selection([('produce','Produce'),('buy','Buy')],
                                              'Supply method', required=True),
    }
    
    _defaults = {
            'supply_method': lambda *a: 'buy',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
            
        if 'product_id' in vals:
            product_obj = self.pool['product.product']
            prod_tmpl_obj = self.pool['product.template']
            
            product = product_obj.browse(cr, uid, vals['product_id'], context=context)
            template = prod_tmpl_obj.browse(cr, uid, product.product_tmpl_id.id, context=context)
            
            vals.update({'supply_method': template.supply_method})
            
        return super(procurement_order, self).create(cr, uid, vals, context=context)
    
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        """ Finds Supply Method of changed product.
        @param product_id: Changed id of product.
        @return: Dictionary of values.
        """        
        if product_id:
            result = super(procurement_order, self).onchange_product_id(cr, uid, ids, product_id, context=context)
            
            product_obj = self.pool['product.product']
            prod_tmpl_obj = self.pool['product.template']
            
            product = product_obj.browse(cr, uid, product_id, context=context)
            template = prod_tmpl_obj.browse(cr, uid, product.product_tmpl_id.id, context=context)
            
            if 'value' in result:
                result['value'].update({'supply_method': template.supply_method})

            return result
        return {}