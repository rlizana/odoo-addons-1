# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from osv import fields,osv
import netsvc
import mx.DateTime
from mx.DateTime import RelativeDateTime, today, DateTime, localtime
from tools import config
from tools.translate import _


class mrp_repair(osv.osv):
    _inherit = 'mrp.repair'

    _columns = {
        'operations' : fields.one2many('mrp.repair.line', 'repair_id', 'Material Lines', readonly=True, states={'draft':[('readonly',False)],'confirmed':[('readonly',False)],'under_repair':[('readonly',False)]}),
        'fees_lines' : fields.one2many('mrp.repair.fee', 'repair_id', 'Operation Lines', readonly=True, states={'draft':[('readonly',False)],'confirmed':[('readonly',False)],'under_repair':[('readonly',False)]}),
        'state': fields.selection([
            ('draft','Borrador'),
            ('confirmed','Abierto'),
            ('ready','Ready to Repair'),
            ('under_repair','Pre-cierre'),
            ('2binvoiced','To be Invoiced'),
            ('invoice_except','Invoice Exception'),
            ('done','Cerrado'),
            ('cancel','Cancelado')
            ], 'Repair State', readonly=True, help="Gives the state of the Repair Order"),
    }

    _defaults = {
        'state': lambda *a: 'draft',
    }

    def action_repair_end_wizard(self, cr, uid, ids, context=None):
        res = self.action_repair_end(cr,uid,ids,context)
        for order in self.browse(cr, uid, ids): 
            if order.invoice_method=='b4repair' or order.invoice_method=='none':
                res = self.wkf_repair_done(cr,uid,ids,context)
        return res

    def action_repair_start_wizard(self, cr, uid, ids, context=None):
        res = True
        for order in self.browse(cr, uid, ids): 
            if order.invoice_method=='after_repair' or order.invoice_method=='none':
                res = self.action_repair_start(cr,uid,ids,context) 
        return res

    def action_reopen(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'confirmed'})
        return True

mrp_repair()

class mrp_repair_line(osv.osv):
    _inherit = 'mrp.repair.line'

    _columns = {
            'user_id': fields.many2one('res.users', 'User',required=True),
    }

    def product_id_change(self, cr, uid, ids, pricelist, product, uom=False, product_uom_qty=0, partner_id=False, guarantee_limit=False):
        result = super(mrp_repair_line, self).product_id_change(cr, uid, ids, pricelist, product, uom, product_uom_qty, partner_id, guarantee_limit)
        if product:
            product =  self.pool.get('product.product').browse(cr, uid, product)
            if not 'value' in result:
                result['value'] = {}
            if not 'tax_id' in result['value']:
                result['value']['tax_id'] = [x.id for x in product.taxes_id]
        return result

    def onchange_operation_type(self, cr, uid, ids, type, guarantee_limit):
        if not type:
            return {'value': {
                        'location_id': False,
                        'location_dest_id': False
                    }
            }
        produc_id = self.pool.get('stock.location').search(cr, uid, [('name','=','Production')])[0]
        stock_id = self.pool.get('stock.location').search(cr, uid, [('name','=','Stock')])[0]

        if type == 'add':
            to_invoice=False
            if guarantee_limit and today() > mx.DateTime.strptime(guarantee_limit, '%Y-%m-%d'):
                to_invoice=True
            return {'value': {
                        'to_invoice': to_invoice,
                        'location_id': stock_id,
                        'location_dest_id' : produc_id
                    }
            }
        return {'value': {
                'to_invoice': False,
                'location_id': produc_id,
                'location_dest_id': stock_id
            }
        }

mrp_repair_line()


class mrp_repair_fee(osv.osv):
    _inherit = 'mrp.repair.fee'

    _columns = {
        'name': fields.char('Description', size=64, select=True,required=False),
        'product_uom_qty': fields.float('Quantity', digits=(16,2), required=False),
        'price_unit': fields.float('Unit Price', required=False),
        'product_uom': fields.many2one('product.uom', 'Product UoM', required=False),
        'user_id': fields.many2one('res.users', string='Usuario', required=False, states={'close':[('readonly',True)]}),
        'hours_qty': fields.float('Quantity Hours', digits=(16,2), required=False, states={'close':[('readonly',True)]}),
        'comments' : fields.text('Comments', states={'close':[('readonly',True)]}),
    }
    def onchange_hours(self, cr, uid, ids, hours_qty):

        values = {'product_uom_qty': hours_qty,}
        return {'value' : values}
        
    def onchange_comment (self, cr, uid, ids, comments):
        values = {}
        if ids == []:
            values = {'name': comments,}
        else:
            fee_line = self.browse(cr,uid,ids[0])
            self.write (cr,uid,fee_line.id, {'name': comments,})
        return {'value' : values}
    
    def onchange_user_id(self, cr, uid, ids, user_id):
        
        values ={}
        emp_obj = self.pool.get('hr.employee')
        product_obj = self.pool.get('product.product')
        emp_lst = emp_obj.search(cr,uid,[('user_id', '=', user_id)])
        
        if emp_lst !=[]:
            employ= emp_obj.browse(cr,uid,emp_lst[0])
            if employ.product_id.id != False:
                prod = employ.product_id.id
                product = product_obj.browse(cr,uid,prod)
                price = product.standard_price
                uom = product.uom_id.id
                values = {'price_unit': price, 'product_uom':uom, 'product_id':prod,}
                
        return {'value' : values}
    
mrp_repair_fee()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
