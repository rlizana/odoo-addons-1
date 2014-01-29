# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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

from osv import osv, fields

class product_template(osv.osv):

    _inherit = 'product.template'
     
    _columns = {# Cantidad para el calculo del coeficiente
                'coef_amount': fields.float('Coef Amount',  digits=(16,2)),        
                }
    
    _default = {
                'coef_amount' : lambda *a: 1.0,
                }
    
    def onchange_coef_amount(self, cr, uid, ids, coef_amount, context=None):
        res={}
        
        if coef_amount:
            uos_coeff = 1 / coef_amount              
            res.update({'uos_coeff': uos_coeff})      
 
        return {'value': res} 

product_template()

class product_product(osv.osv):
    
    _inherit = 'product.product'
    
    def onchange_coef_amount(self, cr, uid, ids, coef_amount, context=None):
        res={}
        
        if coef_amount:
            uos_coeff = 1 / coef_amount              
            res.update({'uos_coeff': uos_coeff})      
 
        return {'value': res} 
    
product_product()
