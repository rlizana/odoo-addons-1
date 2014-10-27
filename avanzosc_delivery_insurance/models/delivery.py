
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Campos (danielcampos@avanzosc.es) Date: 27/10/2014
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.osv import fields, orm


class DeliveryCarrier(orm.Model):
    _inherit = 'delivery.carrier'

    _columns = {'insurance': fields.boolean('Add Insurance Cost'),
                'insurance_type': fields.selection(
                    [('sale_price', 'By Sale Price'),
                     ('fixed', 'Fixed Price')], 'Insurance Type'),
                'insurance_amount': fields.float('Amount'),
                'insurance_percentage': fields.float('Percentage',
                                                     digits=(16, 4))
                }
    _defaults = {
        'insurance_type': lambda *args: 'fixed',
    }


class DeliveryGrid(orm.Model):
    _inherit = 'delivery.grid'

    def get_price_from_picking(self, cr, uid, id, total, weight, volume,
                               context=None):
        res = super(DeliveryGrid, self).get_price_from_picking(
            cr, uid, id, total, weight, volume, context=context)
        sale_obj = self.pool['sale.order']
        if 'order_id' in context:
            order = sale_obj.browse(cr, uid, context['order_id'], context)
            if order.carrier_id and order.carrier_id.insurance:
                carrier = order.carrier_id
                if carrier.insurance_type == 'sale_price':
                    insurance = (order.amount_untaxed *
                                 carrier.insurance_percentage)
                else:
                    insurance = carrier.insurance_amount
                res = res + insurance
        return res
