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

"""inherits from stock.production.lot adds functionally for warn prodlot expiration"""

from osv import osv, fields
from datetime import datetime, timedelta
from tools.translate import _
import pooler

def _get_date(dtype):
    """overwirtes argument function for defaults methods"""
    def calc_date(self, cr, uid, context=None):
        """overwrites this method from product_expiry because if not is organic product and not have use_time, completed it with today date"""
        if context is None: context = {}
        if context.get('product_id', False):
            product = pooler.get_pool(cr.dbname).get('product.product').browse(cr, uid, [context['product_id']])[0]
            duree = getattr(product, dtype) or 0
            if duree:
                date = datetime.today() + timedelta(days=duree)
                return date.strftime('%Y-%m-%d %H:%M:%S')

        return False
    return calc_date

class stock_production_lot(osv.osv):
    """inherits from stock.production.lot adds functionally for warn prodlot expiration"""
    _inherit = 'stock.production.lot'

    def _get_if_expired(self, cr, uid, ids, field_name, arg, context=None):
        if context is None: context = {}
        res = {}
        for obj_prodlot_id in self.browse(cr, uid, ids):
            res[obj_prodlot_id.id] = {
                'expired': False,
                'alert': False
            }
            if obj_prodlot_id.dlc:
                #check if prodlot is expired
                if obj_prodlot_id.dlc < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                    res[obj_prodlot_id.id]['expired'] = True
            if obj_prodlot_id.alert_date:
                #check if prodlot is almost expired
                if obj_prodlot_id.alert_date < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                    res[obj_prodlot_id.id]['alert'] = True
        return res

    _columns = {
        'alert': fields.function(_get_if_expired, method=True, type="boolean", string="Expired Alert",
            store={'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, None, 20)}, multi="All"),
        'expired': fields.function(_get_if_expired, method=True, type="boolean", string="Expired",
            store={'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, None, 20)}, multi="All"),
    }

    _defaults = {
        'dlc': _get_date('life_time'),
        'dluo': _get_date('use_time'),
        'removal_date': _get_date('removal_time'),
        'alert_date': _get_date('alert_time'),
    }

    #pylint: disable-msg=W0613
    def searchfor_expired_prodlots(self, cr, uid, automatic=False, use_new_cursor=False, context={}):
        """cron that search for expired prodlots and mark its with expired everyday, send a notification too"""    
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ids = self.search(cr, uid, [('dlc', '<', today), ('expired', '=', False)])
        alert_ids = self.search(cr, uid, [('alert_date', '<', today), ('alert', '=', False)])
        print  str(today) + ': Product expiry revision done'
        all_ids = ids + alert_ids
        if all_ids:
            self.write(cr, uid, all_ids, {})
            group_id = self.pool.get('res.groups').search(cr, uid, [('name', '=', 'Production Lots / Expiration Notifications')])
            if group_id:
                group_id = group_id[0]
                res = self.pool.get('res.users').search(cr, uid, [('groups_id', 'in', [group_id])])
                if not isinstance(all_ids, list):
                    all_ids = [all_ids]      
                not_stock_prodlots = []
                for prodlot_id in all_ids:
                    prodlot_id = self.pool.get('stock.report.prodlots').search(cr, uid, [('location_id', '=', False)])
                    if prodlot_id:
                        not_stock_prodlots.append(prodlot_id)
                
                #
                # Create message for expired product lots
                #
                ids = list(set(ids) - set(not_stock_prodlots))
                expired_lots_names = ','.join(map(str, map(lambda x:x.name, self.browse(cr, uid, ids))))
                expired_lots_names = (isinstance(expired_lots_names, str) and unicode(expired_lots_names, 'utf-8', errors='replace')) or expired_lots_names
                
                alert_ids = list(set(alert_ids) - set(not_stock_prodlots))
                almost_expired_lots_names = ','.join(map(str, map(lambda x:x.name, self.browse(cr, uid, alert_ids))))
                almost_expired_lots_names = (isinstance(almost_expired_lots_names, str) and unicode(almost_expired_lots_names, 'utf-8', errors='replace')) or almost_expired_lots_names
                
                
                message = _("New production lots expired. Now you cannot use this prodlots definitely.\n\nLot names: %s\n\n") % (expired_lots_names,)
                message2 = _("New production lots ALMOST expired. Now you have to be careful with this prodlots.\n\nLot names: %s\n\n") % (almost_expired_lots_names,)
                
                for user_id in res:
                    if expired_lots_names:
                        self.pool.get('res.request').create(cr, uid, {
                                'name': _("Production Lots Expired"),
                                'body': message,
                                'state': 'waiting',
                                'act_from': uid,
                                'act_to': user_id,
                                'priority': '0'
                        })
                    if almost_expired_lots_names:
                        self.pool.get('res.request').create(cr, uid, {
                                'name': _("Production Lots Almost Expired"),
                                'body': message2,
                                'state': 'waiting',
                                'act_from': uid,
                                'act_to': user_id,
                                'priority': '0'
                            })
        return True

stock_production_lot()