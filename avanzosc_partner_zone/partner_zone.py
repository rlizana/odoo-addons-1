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

from osv import osv, fields
from tools.translate import _

class partner_zone(osv.osv):    
    _name = 'partner.zone'
    _description = 'Zone Master for the partner'
    
    _columns = {
        'code': fields.char('Code', size=64, required=True),
        'name': fields.char('Name', size=64, required=True),
        'analytic_acc': fields.many2one('account.analytic.account', 'Analytic account', required=True),
        
    }
partner_zone()

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address' 
    
    _columns = {
        'zone_id': fields.many2one('partner.zone', 'Zone'),
        'installer_id' : fields.many2one('res.partner', 'Installer'),
        'analytic': fields.many2one('account.analytic.account', 'Analytic account'),
    }
    
    def _get_default_invoice_type(self, cr, uid, context=None):
        factor = self.pool.get('hr_timesheet_invoice.factor')
        return factor.search(cr, uid, [])[0]

    def change_zone(self, cr, uid, ids, context=None):
        account_obj = self.pool.get('account.analytic.account')
        partner_obj = self.pool.get('res.partner')
        zone_obj = self.pool.get('partner.zone')
        for address in self.browse(cr, uid, ids):
            if not address.zip:
                raise osv.except_osv(_('Error!'),_('Zip does not exist!!\nPlease, fill the zip first.'))
#            if not address.zone_id:
#                raise osv.except_osv(_('Error!'),_('You must choose a Project!'))
            if not address.installer_id:
                raise osv.except_osv(_('Error!'),_('You must choose a Installer!'))
            if not address.partner_id.property_product_pricelist:
                raise osv.except_osv(_('Error!'),_('Partner has no sale pricelist set!'))
            if not address.partner_id.ref:
                raise osv.except_osv(_('Error!'),_('Partner has no reference set!'))
            
            installer = partner_obj.browse(cr, uid, address.installer_id.id)
            zone = zone_obj.browse(cr, uid, address.zone_id.id)
            address_obj = self.pool.get('res.partner.address')
            inst_add_lst = address_obj.search(cr,uid,[('partner_id','=',installer.id)])
            zona = False
            if inst_add_lst == []:
               raise osv.except_osv(_('Error!'),_('Installer address info not configured!')) 
            else:
                for add_id in inst_add_lst:
                    inst_addr_reg = address_obj.browse(cr, uid, add_id)
                    zona_instalador = inst_addr_reg.zone_id
                    lazona = zone.id
                    if inst_addr_reg.zone_id.id == zone.id:
                        zona = True
                        if  inst_addr_reg.analytic:
                            parent_analy = inst_addr_reg.analytic
                        else:
                            raise osv.except_osv(_('Error!'),_('Installer analytic account not configured!'))
            if not zona:
                raise osv.except_osv(_('Error!'),_('Installer and Customer zone does not match!'))
            data = {
                'name': zone.name + ' - ' + address.zip + ' - ' + address.partner_id.name,
                'code': address.partner_id.ref + '-' + address.zip,
                'partner_id': address.partner_id.id,
                'pricelist_id': address.partner_id.property_product_pricelist.id,
                'to_invoice': self._get_default_invoice_type(cr, uid, context),
                'parent_id': parent_analy,
            }
            if not address.analytic:
                id = account_obj.create(cr, uid, data)
                self.write(cr, uid, [address.id], {'analytic': id})
            else:
                account_obj.write(cr, uid, address.analytic.id, data)
        return True
    
res_partner_address()