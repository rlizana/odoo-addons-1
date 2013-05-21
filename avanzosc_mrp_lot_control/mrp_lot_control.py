# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc (Daniel) <http://www.avanzosc.com>
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

from osv import fields,osv
import decimal_precision as dp
from datetime import datetime, timedelta
from tools.translate import _

class stock_production_lot(osv.osv):
    
    _inherit =  'stock.production.lot'
    _description = 'Production lot'
    
    _columns = {
                'production_lots_id' : fields.many2one('stock.production.lot', 'Production Lots'),
                'product_lots' : fields.one2many('stock.production.lot','production_lots_id','Lots Related')
        }

stock_production_lot()

class product_loting_rel(osv.osv_memory):
    
    _name = 'product.loting.rel'
    _description = 'Production loting relation'
       
    _columns = {
                'product' : fields.many2one('product.product', 'Product',size=64, required=True),
                #'serial': fields.char('Production Lot', size=64, required=True),
                'product_lot' : fields.many2one('stock.production.lot', 'Production Lots',required=True),
                'mrp_lot' : fields.many2one('mrp.lot.assign', 'Master product',size=64),
                'required_amount': fields.integer('Required Amount'),
                
                }

product_loting_rel()

class mrp_lot_assign (osv.osv):
    
    def default_get(self,cr,uid,fields_list,context=None):
        
        values = {}
        context['product_qty'] = 1
        context['mode'] = 'consume_produce'
        data = self.browse(cr, uid, context['active_ids'][0], context=context)
        production_id = context.get('active_id', False)
        stock_move_obj= self.pool.get('stock.move')
        production_obj = self.pool.get('mrp.production.product.line')
        product_obj = self.pool.get('product.product')
        lot_obj = self.pool.get('stock.production.lot')
        wizard_lot = self.pool.get('mrp.lot.assign')
        stmove_list = stock_move_obj.search(cr,uid,[('production_id','=',production_id)])
        stmove_reg = stock_move_obj.browse(cr,uid,stmove_list[0]) # Movimiento del producto a producir
        id_list = production_obj.search(cr,uid,[('production_id','=',production_id)])
        production_dic = production_obj.read (cr,uid, id_list,['id', 'product_id'])
        prod_lot_dic= list(production_dic) # copy of the production lines / # product id list to be loted
        n=0
        for product in production_dic:
            product_reg = product_obj.browse (cr,uid, product['product_id'][0])
            if not product_reg.track_production :
                prod_lot_dic.pop(n) # update list with lot products
            else:
                n= n+1
        context['prod_produ'] = stmove_reg.product_id.id # ID de producto a producir
        context['st_move_prod'] = stmove_reg.id # ID Movimiento de producto a producir
        context['prod_lot_dic'] = prod_lot_dic 
        context['ids'] = context['active_ids']

        prod_lst = []
        for prod in prod_lot_dic: # Crear lista de productos a enlotar
            produce_val = {'product': prod['product_id'][0]}
            prod_lst.append(produce_val)
            values = {'product': context['prod_produ'],
                      'product_lots': prod_lst,
                      'context' : context,
                      'production_id': production_id
                      }
        return values
    
    _name = "mrp.lot.assign"
    _description = "Lot Assign"
    
    _columns = {
        'product': fields.many2one('product.product', 'Product1', size=128, required=True),
        'lot_serial': fields.char('Prod. Serial', size=128, required=True),
        'quantity_produced': fields.integer('Quantity', required=True),
        'product_lots': fields.one2many('product.loting.rel','mrp_lot','Lots'),
        'production_id': fields.many2one('mrp.production', 'Production ID'),
        }
    
    def onchange_quantity_produced(self, cr, uid, ids, production_id, quantity_produced, product_lots, context=None):
        mrp_production_obj = self.pool.get('mrp.production')
        mrp_bom_obj = self.pool.get('mrp.bom')
        res={} 
        if production_id and quantity_produced:
            mrp_production = mrp_production_obj.browse(cr,uid,production_id)
            prod_lst = []
            for product_lot in product_lots:
                my_dic = product_lot[2]
                my_product_id = my_dic.get('product')
                if mrp_production.bom_id:
                    mrp_bom = mrp_bom_obj.browse(cr,uid,mrp_production.bom_id.id)
                    if mrp_bom.bom_lines:
                        for bon_lines in mrp_bom.bom_lines:
                            if bon_lines.product_id.id == my_product_id:
                                produce_val = {'product': my_product_id,
                                               'required_amount': quantity_produced * bon_lines.product_qty,
                                               'product_lot': my_dic.get('product_lot')}
                                prod_lst.append(produce_val)
                            
            res = {'quantity_produced': quantity_produced,
                   'product_lots': prod_lst}
            
        return {'value': res} 
    
    def assign_lot (self, cr, uid, ids, context=None):
        
        data_lotasing = self.browse(cr, uid, ids[0], context=context)
        stock_move_obj= self.pool.get('stock.move')
        mrp_product_obj= self.pool.get('mrp.product.produce')
        mrp_production_obj= self.pool.get('mrp.production')
        
        production_id = context.get('active_id', False)
        product_qty = data_lotasing.quantity_produced
        mode = 'consume_produce'
        
        #crear lote de producto a producir
        lot_obj = self.pool.get('stock.production.lot')
        
        # Create master product production lot    
        master_prod_val ={'product_id': data_lotasing.product.id,
                           'name': data_lotasing.lot_serial,
                           'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'),
                  }
        master_produc_lot = lot_obj.create(cr,uid,master_prod_val)
        
        quehayaqui = data_lotasing.product_lots
        # Controla ids de movimientos de la produccion 
        mrp_production = mrp_production_obj.browse(cr,uid,production_id) # production move id lst
        reg_lst = mrp_production.move_lines 
        mrp_move_ids_lst = [] # id list of current production movements
        for reg in reg_lst:
            mrp_move_ids_lst.append(reg.id)
                                           
        for prod_lot_id in data_lotasing.product_lots : # create product lots
            
            produce_prod_val ={'production_lots_id' : master_produc_lot}
            lot_id = prod_lot_id.product_lot.id
            lot_obj.write(cr,uid,lot_id,produce_prod_val)
            product_lst_mod = []  # Controla ids de movimientos de la produccion 
            #Lista de Ids de los movimientos del product_id
            product_lst = stock_move_obj.search(cr,uid,[('product_id','=',prod_lot_id.product.id),'|',('state','=','assigned'),('state','=','confirmed')])
            for item in product_lst:
                if mrp_move_ids_lst.count(item) == 1:
                    product_lst_mod.append(item)
            st_mov_pro= stock_move_obj.browse(cr,uid,product_lst_mod[0])
            stock_move_obj.write(cr,uid,st_mov_pro.id,{'prodlot_id':lot_id})
        
        #asignar lote al movimiento producto maestro
        stmove_list = stock_move_obj.search(cr,uid,[('production_id','=',production_id)])
        stmove_reg = stock_move_obj.browse(cr,uid,stmove_list[0])
        stock_move = stock_move_obj.browse(cr,uid,stmove_reg.id)
        stock_move_obj.write(cr,uid,stock_move.id,{'prodlot_id':master_produc_lot}) 
                 
        # final de control de ids de movimientos de la produccion
        #do_produce
        assert production_id, "Production Id should be specified in context as a Active ID"
        self.pool.get('mrp.production').action_produce(cr, uid, production_id,
                            product_qty, mode, context=context)
        return {}
        
mrp_lot_assign  ()

