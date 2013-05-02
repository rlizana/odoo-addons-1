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
from osv import osv
from osv import fields
from datetime import datetime
#
class crm_phonecall(osv.osv):
    
    _inherit = 'crm.phonecall'
    
    _columns = {'contact_name': fields.char('Contact Name', size=64),
                'partner_name': fields.char("Customer Name", size=64,help='The name of the future partner that will be created while converting the lead into opportunity', select=1),
                'partner_mobile': fields.char('Mobile', size=32),
                'partner_id': fields.many2one('res.partner', 'Partner'),
                'partner_address_id': fields.many2one('res.partner.address', 'Partner Contact', \
                                 domain="[('partner_id','=',partner_id)]"),
                }
    
    _defaults = {'contact_name': lambda self,cr,uid,context:context.get('contact_name', False),
                 'partner_name': lambda self,cr,uid,context:context.get('partner_name', False),
                 'partner_mobile': lambda self,cr,uid,context:context.get('partner_mobile', False),
                 'partner_id': lambda self,cr,uid,context:context.get('partner_id', False),
                 'partner_address_id': lambda self,cr,uid,context:context.get('partner_address_id', False)
                 }

crm_phonecall()
