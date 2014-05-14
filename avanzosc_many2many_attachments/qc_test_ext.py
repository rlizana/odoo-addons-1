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

class qc_test(osv.osv):

    _inherit = 'qc.test'
    
    _columns = {# Tiene adjuntos
                'has_attachments':fields.boolean('Has Attachmets', readonly=True),
                # Adjuntos
                'attachment_ids': fields.many2many('ir.attachment','qc_test_attachment_rel','qc_test_id','attachment_id','Attachments'),
                }
    
    def create(self, cr, uid, data, context=None):
        qc_test_id = super(qc_test, self).create(cr, uid, data, context=context)
        test = self.browse(cr,uid,qc_test_id,context=context)
        if test.attachment_ids:
            self.write(cr,uid,[qc_test_id],{'has_attachments': True},context=context)            
        return qc_test_id
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals.has_key('attachment_ids'):
            attachment_ids = vals['attachment_ids']
            if attachment_ids:
                if attachment_ids[0][2]:
                    vals.update({'has_attachments': True})
                else:
                    vals.update({'has_attachments': False})
            else:
                vals.update({'has_attachments': False})

        result = super(qc_test, self).write(cr, uid, ids, vals, context=context)
        return result
    
qc_test()