
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2012 Daniel (AvanzOSC). All Rights Reserved
#    25/07/2012
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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


from osv import fields, osv, orm
from tools import ustr
from tools.translate import _
import StringIO
import base64
import csv
import tools
import cStringIO
import string
from collections import defaultdict
import os
import tempfile
from datetime import datetime
import time

try:
    import pyExcelerator as xl
except:
    print 'pyExcelerator Python module not installed'


class import_inventory(osv.osv_memory):
    """Import inventory"""
    _name = 'import.inventory'
    _description = 'Import inventory'
    _columns = {
        'data': fields.binary('File', required=True),
        'name': fields.char('Filename', 256, required=False),
        'location': fields.many2one('stock.location','Ubicacion')
    }

    def action_import(self, cr, uid, ids, context=None):
        """
        Load Provider data from the CSV file.
        """
        res = {}
        stoc_loc_obj = self.pool.get('stock.location')
        company_obj = self.pool.get('res.company')
        supplier_obj = self.pool.get('res.partner')
        inventory_obj = self.pool.get('stock.inventory')
        inventory_line_obj = self.pool.get('stock.inventory.line')
        model_obj  = self.pool.get('ir.model.data')
        product_obj = self.pool.get('product.product')
        
        for wiz in self.browse(cr, uid, ids, context):
            if not wiz.data:
                raise osv.except_osv(_('UserError'), _("You need to select a file!"))
            # Decode the file data
            data = base64.b64decode(wiz.data)
            file_type = (wiz.name).split('.')[1]
            ext = file_type.lower()
            input=cStringIO.StringIO(data)
            input.seek(0)
            filename = wiz.name
            location = wiz.location
            #base_provider_location = stoc_loc_obj.search(cr,uid,[('name','=','Suppliers')])
            
#            prov_loc_name = locat_provideer.name
#            if locat_provideer.name == 'Proveedores' or not provideer.property_stock_supplier :
#                provi_view = {'name': provideer.name,'location_id': base_provider_location[0],'active':True ,'usage':'view', 'chained_location_type':'none','chained_auto_packing' :'manual'}
#                provi_view_id = stoc_loc_obj.create(cr,uid,provi_view)
#                provi_val = {'name': 'Stock','location_id': provi_view_id, 'active':True ,'usage':'internal', 'chained_location_type':'none','chained_auto_packing' :'manual', 'chained_delay':'0'}
#                provi_location = stoc_loc_obj.create(cr,uid,provi_val)
#                supplier_obj.write(cr,uid,provideer.id,{'property_stock_supplier':provi_location})
#            else:
                
            provi_location = location.id
            
            reader_info = []       
             
            if ext == 'csv':
                reader = csv.reader(input,
                                    delimiter=',',
                                    lineterminator='\r\n'
                                    )
                
                reader_info.extend(reader)
                del reader_info[0]

                keys = []
                values= {}
                # crear inventario
                fecha = time.strftime('%Y%m%d')
                company_lst = company_obj.search(cr,uid,[])
                invent_val = {'name': fecha, 'date': fecha, 'company_id':company_lst[0] }
                inventory = inventory_obj.create(cr,uid,invent_val)
                # Inventario creado
                
                keys= ['ref', 'sto_qty']
                for i in range(len(reader_info)):
                    val = {}
                    field = reader_info[i]
                    values = dict(zip(keys, field))
                    prod_list = []
                    prod_list = product_obj.search(cr,uid,[('default_code','=',values['ref'])])
                    if prod_list != []  : # Crear linea de inventario
                        product = product_obj.browse(cr,uid,prod_list[0])
                        val['product_id'] = product.id
                        val['product_uom'] = product.uom_id.id 
                        val['product_qty'] = values['sto_qty']
                        val['location_id'] =  provi_location
                        val['inventory_id'] = inventory
                        inventory_line = inventory_line_obj.create(cr,uid,val)                       
#                        print "Producto: " + str (product.name) + " Ref: " + str(values['ref']) + " Cantidad: " + str(values['sto_qty'])
                    #else:
                       # print " Referencia: " + str(values['ref']) + " Cantidad: " + str(values['sto_qty'])
            else:
                    print "Not a .csv file"
        return res

      
import_inventory()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
