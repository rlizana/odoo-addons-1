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


class import_fuellog(osv.osv_memory):
    """Import Fuel log"""
    _name = 'import.fuellog'
    _description = 'Import Fuel Log'
    _columns = {
        'data': fields.binary('File', required=True),
        'name': fields.char('Filename', 256, required=False),
    }

    def action_import(self, cr, uid, ids, context=None):
        """
        Load Fuel Log from the CSV file.
        """
        res = {}
        refuel_obj = self.pool.get('fleet.fuellog')
        vehic_obj = self.pool.get('fleet.vehicles')
        supplier_obj = self.pool.get('stock.location')

        model_obj  = self.pool.get('ir.model.data')
        
        for wiz in self.browse(cr, uid, ids, context):
            if not wiz.data:
                raise osv.except_osv(_('UserError'), _("You need to select a file!"))
            # Decode the file data
            data = base64.b64decode(wiz.data)
            file_type = (wiz.name).split('.')
            input=cStringIO.StringIO(data)
            input.seek(0)
            filename = wiz.name
            reader_info = []
             
            if file_type[1] == 'csv':
                     
                reader = csv.reader(input,
                                    delimiter=';',
                                    lineterminator='\r\n'
                                    )
                
                reader_info.extend(reader)
                del reader_info[0]

                keys = []
                values= {}
                keys= ['supplier','vehicle','date','time', 'cost', 'qty', 'totalcost', 'odometer','engine','driver']
                for i in range(len(reader_info)):
                    field = reader_info[i]
                
                    values = dict(zip(keys, field))
                
                    if file_type[1] == 'csv':
                        stripped = 0
                        values ['vehicle'] = values ['vehicle'].strip()
#                        try:
#                            stripped = str(int(values ['vehicle'].strip()))
#                            values ['vehicle'] = 'bus ' + values ['vehicle'].strip()            
#                        except:
#                            if values ['vehicle'].strip() != stripped:
#                                values ['vehicle'] = values ['vehicle'].strip()
                        # fields to convert from str to another type
                        values ['supplier'] = values ['supplier'].strip()
                        values ['date'] = values ['date'].strip()
                        values ['time'] = values ['time'].strip()
                        values ['cost'] = float (values ['cost'].strip())
                        values ['qty'] = float (values ['qty'].strip())
                        values ['totalcost'] = float (values ['totalcost'].strip())
                        values ['odometer'] = int(float(values ['odometer'].strip()))
                        values ['engine'] = float(values ['engine'].strip())
                        values ['driver'] = values ['driver'].strip()
                                         
                    if values['supplier']:
                        supp_id = supplier_obj.search(cr, uid, [('name', '=', values['supplier'])])
                        if supp_id == []:
                            location = supplier_obj.create(cr,uid,{ 
                                                      'name' : values['supplier'], 
                                                      'active' : 1,
                                                      'usage': 'internal',
                                                      'allocation_method' :'fifo',
                                                      'chained_location_type': 'none',
                                                      'chained_auto_packing': 'manual',
                                                      })
                        else: location = supp_id[0]
                    if values ['vehicle']:
                        vehic_id = vehic_obj.search(cr, uid, [('name', '=', values['vehicle'])])
                        if vehic_id != []:
                            # Vehicle Odometer actualization
                            vehic_obj.write(cr, uid, vehic_id[0],{'actodometer': values ['odometer']})
#                         Load Data
                            refuel = refuel_obj.create(cr,uid,{ 
                                                           'log_no': 'Log:' + values['date']+ '/Line-' + str(i),
                                                           'supplier' : location,
                                                           'vehicle': vehic_id[0],
                                                           'cost' : values ['cost'],
                                                           'qty' : values ['qty'],
                                                           'totalcost' : values ['totalcost'],
                                                           'odometer' : values ['odometer'],
                                                           'd_number': values ['driver'],
                                                           'engine': values ['engine'],
                                                           'date': values ['date'],
                                                           'time': values ['time']
                                                           })                    
            else:
                    print "Not a .csv file"
        return res

      
import_fuellog()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
