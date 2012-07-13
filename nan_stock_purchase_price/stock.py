# -*- encoding: latin-1 -*-
##############################################################################
#
# Copyright (c) 2009 Ángel Álvarez - NaN  (http://www.nan-tic.com) All Rights Reserved.
#
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from osv import fields,osv
from tools.translate import _
import netsvc

class stock_move(osv.osv):
    _inherit = 'stock.move'

    _columns = {
        'received_quantity': fields.float('Received Quantity', help='Quantity of product received'),
    }

stock_move()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    def action_scanner_confirm(self, cr, uid, ids, context=None):
        """
        Function picked from nan_stock_scanner module.
        """
        for picking in self.browse(cr, uid, ids, context):
            new_picking = None
            new_moves = []

            if picking.purchase_id:
                currency = picking.purchase_id.pricelist_id.currency_id.id
            else:
                currency = 0

            complete, too_many, too_few , none = [], [], [],[]
            for move in picking.move_lines:
                if move.received_quantity == None or move.received_quantity == False or move.received_quantity == 0:
                    none.append( move )
                elif move.product_qty == move.received_quantity:
                    complete.append(move)
                elif move.product_qty > move.received_quantity:
                    too_few.append(move)
                else:
                    too_many.append(move)

                if len( none) == len( picking.move_lines):
                    return {'new_picking': False}

                # Average price computation
                if picking.type == 'in' and move.product_id.cost_method == 'average' and move.purchase_line_id:
                    product = self.pool.get('product.product').browse(cr, uid, move.product_id.id, context)
                    user = self.pool.get('res.users').browse(cr, uid, uid, context)

                    price = move.purchase_line_id.price_unit
                    price_uom = move.purchase_line_id.product_uom.id

                    qty = move.received_quantity
                    qty = self.pool.get('product.uom')._compute_qty(cr, uid, move.product_uom.id, qty, product.uom_id.id)

                    if (qty > 0):
                        new_price = self.pool.get('res.currency').compute(cr, uid, currency, user.company_id.currency_id.id, price)
                        new_price = self.pool.get('product.uom')._compute_price(cr, uid, price_uom, new_price, product.uom_id.id)
                        if product.qty_available<=0:
                            #new_std_price = new_price
                            new_std_price = move.purchase_line_id.price_unit
                        else:
                            new_std_price = move.purchase_line_id.price_unit
                            self.pool.get('product.product').write(cr, uid, [product.id], {
                            'standard_price': new_std_price
                            }, context)
                            self.pool.get('stock.move').write(cr, uid, [move.id], {
                            'price_unit': new_price
                            }, context)
                            
                            #Comentado Dani
#                            new_std_price = ((product.standard_price * product.qty_available)\
#                                + (new_price * qty))/(product.qty_available + qty)
#                        self.pool.get('product.product').write(cr, uid, [product.id], {
#                            'standard_price': new_std_price
#                        }, context)
#                        self.pool.get('stock.move').write(cr, uid, [move.id], {
#                            'price_unit': new_price
#                        }, context)             
            if len(too_many) >0 or len(too_few) > 0 or len(none) > 0:
                new_picking = self.copy(cr, uid, picking.id, {
                    'name': self.pool.get('ir.sequence').get(cr, uid, 'stock.picking'),
                    'move_lines' : [],
                    'state':'draft',
                    }, context)
 
            for move in too_few:
                if move.received_quantity <> 0:
                    new_obj = self.pool.get('stock.move').copy(cr, uid, move.id, {
                        'product_qty' : move.received_quantity,
                        'product_uos_qty': move.received_quantity,
                        'picking_id' : new_picking,
                        'state': 'assigned',
                        'move_dest_id': False,
                        'price_unit': move.price_unit,

                    }, context)
                self.pool.get('stock.move').write(cr, uid, [move.id], {
                    'product_qty' : move.product_qty - move.received_quantity,
                    'product_uos_qty':move.product_qty - move.received_quantity,
                    'prodlot_id': None,
                    'received_quantity':0,
                }, context)

            if new_picking:
                self.pool.get('stock.move').write(cr, uid, [c.id for c in complete], {'picking_id': new_picking}, context)
                for move in too_many:
                    self.pool.get('stock.move').write(cr, uid, [move.id], {
                        'product_qty' : received_quantity,
                        'product_uos_qty': received_quantity,
                        'picking_id': new_picking,
                    }, context)
            else:
                for move in too_many:
                    self.pool.get('stock.move').write(cr, uid, [move.id], {
                        'product_qty': received_quantity,
                        'product_uos_qty': received_quantity,
                        'prodlot_id':False,
                    }, context)

            # At first we confirm the new picking (if necessary)
            wf_service = netsvc.LocalService("workflow")
            if new_picking:
                wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)

            # Then we finish the good picking
            if new_picking:
                self.write(cr, uid, [picking.id], {'backorder_id': new_picking}, context)
                self.action_move(cr, uid, [new_picking], context)
                wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_done', cr)
                wf_service.trg_write(uid, 'stock.picking', picking.id, cr)
            else:
                self.action_move(cr, uid, [picking.id], context)
                wf_service.trg_validate(uid, 'stock.picking', picking.id, 'button_done', cr)

        return {'new_picking':new_picking or False}

stock_picking()

class stock_input_wizard_line( osv.osv_memory ):
    _name = 'stock.input.wizard.line'

    def _total_amount(self, cr, uid, price, quantity, discount, purchase_order_id, purchase_order_line_id, context):
        untaxed_amount = self._untaxed_amount(cr, uid, price, quantity, discount)  
        if purchase_order_line_id and purchase_order_id:
            purchase_order_line = self.pool.get('purchase.order.line').browse(cr, uid, purchase_order_line_id, context)
            purchase_order = self.pool.get('purchase.order').browse(cr, uid, purchase_order_id, context)

            # calculation of line with taxes
            taxes_value = 0.0
            if len(purchase_order_line.taxes_id) > 0:
                calculations =  self.pool.get('account.tax').compute(cr, uid,purchase_order_line.taxes_id , price,quantity, purchase_order.partner_address_id.id, purchase_order_line.product_id, purchase_order.partner_id)
                for dict_tax in calculations:
                    taxes_value += dict_tax['amount'] 
            return  untaxed_amount + taxes_value 

        return untaxed_amount
            
    def _untaxed_amount(self,cr,uid,price,quantity,discount):
        untaxed_amount = price * ((100.0-discount)/100.0) * quantity

        return untaxed_amount

    def _prices_on_product_uom(self,cr,uid,from_uom,prices,to_uom):
        result = []
        for price in prices:
            new_price = self.pool.get('product.uom')._compute_price(cr,uid,from_uom,price,to_uom)        
            result.append(new_price)
        return result
    
    def _prices_on_currency(self,cr,uid,from_currency,prices,to_currency):
        result = []
        for price in prices:
            new_price = self.pool.get('res.currency').compute(cr,uid,from_currency,to_currency,price)        
            result.append(new_price)
        return result

    def create( self, cr, uid, vals, context=None ):
        if 'price' in vals and 'product_id' in vals:
            product_id = vals['product_id']
            product = self.pool.get('product.product').browse(cr, uid, product_id, context)
            price = self.pool.get('product.uom')._compute_price(cr, uid, vals['product_uom'], vals['price'], product.uom_id.id)
            self.pool.get('product.product').write(cr, uid, product_id, {
                'last_purchase_price': price,
            }, context)

        move = self.pool.get('stock.move').browse(cr, uid, vals['stock_move_id'], context)
        if move.purchase_line_id:
            # Convert stock move UoM to order line's UoM
            price = self.pool.get('product.uom')._compute_price(cr, uid, vals['product_uom'], vals['price'], move.purchase_line_id.product_uom.id)
            if not 'discount' in vals:
                vals['discount'] = 0.0
            self.pool.get('purchase.order.line').write(cr, uid, [move.purchase_line_id.id], {
                'price_base': price,
                #'price_unit': price * (1-vals['discount']/100),
                'price_unit': price * (1-vals.get('discount',0.0)/100),
                'discount': vals['discount'],
            }, context)


        values = {
            'received_quantity': vals['quantity'],
        }
        if move.product_uom.id != vals['product_uom']:
            # Convert total stock move quantity to the same UoM used by the user
            values['product_qty'] = self.pool.get('product.uom')._compute_qty(cr, uid, move.product_uom.id, move.product_qty, vals['product_uom'])
            values['product_uom'] = vals['product_uom']
            values['product_uos'] = vals['product_uom']

        self.pool.get('stock.move').write(cr, uid, [move.id], values, context)

        return super(stock_input_wizard_line,self).create(cr, uid, vals, context)

    def on_change_fields(self, cr, uid, ids, product_id, quantity, product_uom, purchase_price, price, list_price, last_purchase_price, currency_id, discount, untaxed_amount, total_amount, purchase_order_id, purchase_order_line_id, stock_move_id, field_changed, context):
        if field_changed == 'product_uom' and stock_move_id:
            #prices calculation from product_uom
            move = self.pool.get('stock.move').browse(cr, uid, stock_move_id, context)
            product_uom_ori = move.product_uom.id
            if product_uom_ori != product_uom:
                new_prices = self._prices_on_product_uom(cr, uid, product_uom_ori, [purchase_price, price, list_price], product_uom)
                [purchase_price, price, list_price] = new_prices

        if field_changed == 'currency_id' and stock_move_id:
            #prices calculation from currency
            purchase_order = self.pool.get('purchase.order').browse(cr, uid, purchase_order_id, context)
            currency_ori = purchase_order.pricelist_id.currency_id.id
            if currency_ori != currency_id:
                new_prices = self._prices_on_currency(cr,uid,currency_ori,[purchase_price, price, list_price],currency_id)        
                [purchase_price, price, list_price] = new_prices

        total_amount = self._total_amount(cr,uid,price,quantity,discount,purchase_order_id,purchase_order_line_id, context)
        untaxed_amount = self._untaxed_amount(cr,uid,price,quantity,discount)
        
        return {
            'value': {
                        'product_id': product_id,
                        'quantity': quantity,
                        'product_uom': product_uom, 
                        'purchase_price': purchase_price, 
                        'price': price,
                        'list_price': list_price,
                        'last_purchase_price': last_purchase_price,
                        'currency_id': currency_id,
                        'discount': discount,
                        'untaxed_amount': untaxed_amount,
                        'total_amount': total_amount,
                        'purchase_order': purchase_order_id,
                        'purchase_order_line': purchase_order_line_id,
                        'stock_move_id': stock_move_id,
                }
        }

    _columns = {
        'product_id':fields.many2one( 'product.product','Product'),
        'quantity': fields.float('Quantity' ),
        'product_uom': fields.many2one( 'product.uom','Uom '),
        'purchase_price':fields.float('Purchase Price', readonly=True),
        'price':fields.float( 'Price'),
        'list_price': fields.float( 'List Price', readonly=True ), 
        'last_purchase_price': fields.float('Last Purchase Price', readonly=True),
        'currency_id':fields.many2one( 'res.currency','Currency', readonly=True),
        'discount': fields.float('Discount'),
        'untaxed_amount':fields.float('Untaxed Amount', readonly=True),
        'total_amount' : fields.float('Total Amount', readonly=True),
        'wizard_id': fields.many2one( 'stock.input.wizard', 'Wizard id'),
        'purchase_order_line': fields.many2one('purchase.order.line' ,'Purchase Order Line'),
        'purchase_order': fields.many2one( 'purchase.order'),
        'stock_picking': fields.many2one( 'stock.picking', 'Stock Picking'),
        'stock_move_id': fields.many2one( 'stock.move','Stock Picking Lines'),
    }

stock_input_wizard_line()


class stock_input_wizard(osv.osv_memory):
    _name = 'stock.input.wizard'

    def _default_picking_id(self,cr,uid,context=None):
        if not context:
            context = {}
        return context.get('active_id', False)

    def _default_line_ids(self, cr, uid,context=None):
        if context is None:
            context = {}
        if not 'active_id' in context:
            return {}

        result = []

        picking = self.pool.get('stock.picking').browse(cr, uid, context['active_id'], context)
        #For each line of stock picking
        for move in picking.move_lines:
            product = move.product_id
            if move.purchase_line_id:
                #Mod Dani price_base = move.purchase_line_id.price_base
                price_base = move.purchase_line_id.price_subtotal
                discount = move.purchase_line_id.discount
                untaxed_amount = move.purchase_line_id.price_subtotal
                purchase_order_line_id = move.purchase_line_id.id 
            else:
                price_base = product.standard_price
                discount = 0.0
                untaxed_amount = self.pool.get('stock.input.wizard.line')._untaxed_amount(cr, uid, price_base, move.product_qty, discount)
                purchase_order_line_id = False 

            purchase_id = picking.purchase_id and picking.purchase_id.id or False

            if purchase_id:
                # prices calculation from supplier and his price list 
                pricelist_id = picking.purchase_id.pricelist_id.id
                partner_id = picking.purchase_id.partner_id.id
                list_price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist_id], product.id, 1.0, partner_id)[pricelist_id]
            else:
                pricelist_id = False
                list_price = 0.0

            # calculation of line with taxes
            total_amount = self.pool.get('stock.input.wizard.line')._total_amount(cr, uid, price_base, move.product_qty, discount, purchase_id, purchase_order_line_id, context)

            result += [{
                    'product_id': move.product_id.id,
                    'quantity': move.product_qty,
                    'product_uom': move.product_uom.id, 
                    'purchase_price': price_base, 
                    'price': price_base,
                    'list_price': list_price,
                    'last_purchase_price': product.last_purchase_price,
                    'currency_id': picking.purchase_id and picking.purchase_id.pricelist_id.currency_id.id or False,
                    'discount': discount,
                    'untaxed_amount': untaxed_amount,
                    'total_amount': total_amount,
                    'purchase_order': purchase_id,
                    'purchase_order_line': purchase_order_line_id,
                    'stock_move_id': move.id,
            }]
        return result

    def accept_and_write(self,cr,uid,ids,context=None):
        return {}

    def on_cancel(self, cr, uid, ids, context=None):
        return {}

    def _wizard_line_values(self, stock_move_id, list):
        #list with format [ [0,0,dictionary0], [ 0,0,dictionary1], ...]
        if list:
            for line in list:
                dictionary = line[2]
                if 'stock_move_id' in dictionary:
                    if dictionary['stock_move_id'] == stock_move_id:
                        return dictionary
        return False

    def _wizard_line_orphan(self,list):
        #list with format [ [0,0,dictionary0], [ 0,0,dictionary1], ...]
        if list:
            for line in list:
                dictionary = line[2]
                if 'stock_move_id' in dictionary:
                    if not dictionary['stock_move_id']:
                        raise osv.except_osv(_('Warning'), _('You are trying to create a new line on wrong place. You should create it on Stock picking.'))
        return False

    def create( self, cr, uid, vals, context=None ):
        if context is None:
            context = {}
        if 'active_id' in context:
            vals.update({'picking_id':context['active_id']})
        if 'picking_id' in vals:
            picking_id = vals['picking_id']
            # We will create a wizard_line for each line of stock picking. 
            # If there is any 'vals', we will take the values from vals, otherwise we'll take values from stock picking
            picking = self.pool.get('stock.picking').browse(cr, uid, picking_id, context)
            for move in picking.move_lines:
                #search if this line has values (true when we modified any value on wizard_line)
                if 'line_ids' in vals:
                    line_vals = self._wizard_line_values(move.id, vals['line_ids'])
                    if not line_vals: # Patch to correct calculation if no changes are made
                        if not move.price_unit:
                            # mod dani pricebak = self.pool.get('purchase.order.line').read(cr, uid, move.purchase_line_id.id,['price_base','discount'])
                            pricebak = self.pool.get('purchase.order.line').read(cr, uid, move.purchase_line_id.id,['price_subtotal','discount'])
                            line_vals = {
                                         'stock_move_id': move.id,
                                         'product_id': move.product_id.id,
                                         'product_uom': move.product_uom.id,
                                         #mod dani 'price': pricebak['price_base'],
                                         'price': pricebak['price_subtotal'],
                                         'quantity': move.product_qty,
                                         'discount': pricebak['discount']
                                         }
                         #   pricebak = self.pool.get('product.product').read(cr, uid, move.product_id.id, 'standard_price')
                        else:
                            #if no values, then we put values from line of stock picking
                            line_vals = {
                                         'stock_move_id': move.id,
                                         'product_id': move.product_id.id,
                                         'product_uom': move.product_uom.id,
                                         'price': move.price_unit,
                                         'quantity': move.product_qty,
#                                        'discount': move.purchase_line_id.discount
                                         }
                #creating the wizard_line
                wizard_line_id = self.pool.get('stock.input.wizard.line').create(cr, uid, line_vals, context)

            #Check if there is any new wizard_line (not included on stock picking)
            self._wizard_line_orphan(vals['line_ids'])

            self.pool.get('stock.picking').action_scanner_confirm(cr, uid, [picking_id], context)

        return True

    _columns = {
        'picking_id':fields.many2one('stock.picking','Picking', readonly=True),
        'line_ids': fields.one2many('stock.input.wizard.line', 'wizard_id', 'Lines'),
    }

    _defaults = {
            'picking_id': _default_picking_id,
            'line_ids': _default_line_ids,
    }


stock_input_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
