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
from tools.translate import _


class ir_attachment(osv.osv):

    _inherit = 'ir.attachment'
    
    _columns = {# Productos
                'product_ids': fields.many2many('product.product','product_attachment_rel','attachment_id','product_id','Products'),
                # Plantillas test
                'test_template_ids': fields.many2many('qc.test.template','qc_test_template_attachment_rel','attachment_id','qc_test_template_id','Test Templates'),
                # Tests
                'test_ids': fields.many2many('qc.test','qc_test_attachment_rel','attachment_id','qc_test_id','Tests'),
                }
                
    def create(self, cr, uid, data, context=None):
        qc_test_id = super(qc_test, self).create(cr, uid, data, context=context)
        test = self.browse(cr,uid,qc_test_id,context=context)
        if test.attachment_ids:
            self.write(cr,uid,[qc_test_id],{'has_attachments': True},context=context)            
        return qc_test_id
    
ir_attachment()