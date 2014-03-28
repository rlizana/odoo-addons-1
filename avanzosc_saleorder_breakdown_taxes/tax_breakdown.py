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
import decimal_precision as dp

class tax_breakdown(osv.osv):

    _name = 'tax.breakdown'
    _description = 'Tax Breakdown'

    _columns = {# Pedido de Venta
                'sale_id': fields.many2one('sale.order', 'Sale Order', ondelete='cascade'),
                # Albaran
                'picking_id': fields.many2one('stock.picking', 'Stock Picking', ondelete='cascade'),
                # Impuesto
                'tax_id': fields.many2one('account.tax', 'Tax'),
                # Importe Neto
                'untaxed_amount': fields.float('Untaxed Amount', digits_compute=dp.get_precision('Sale Price')),
                # Impuestos
                'taxation_amount': fields.float('Taxation', digits_compute=dp.get_precision('Sale Price')),
                # Total
                'total_amount': fields.float('Total', digits_compute=dp.get_precision('Sale Price')),
                }

tax_breakdown()
