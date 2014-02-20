
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2014 AvanzOSC (Daniel). All Rights Reserved
#    Date: 20/02/2014
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

import wizard
from osv import osv
from osv import fields
from tools.translate import _

class wizard_stpick_expectdate(osv.osv_memory):

    _name = 'wizard.stpick.expectdate'
    _description = 'Scheduled Date for Stock Picking Lines Wizard'
 
    _columns = {
                'schel_date': fields.datetime('Scheduled Date', required=True),
    }
    
    def set_scheduled_date(self,cr,uid,ids,context=None):
        
        res ={}
        if context is None:
            context = {}    
        data = self.browse(cr, uid, ids, context=context)
        picking_obj = self.pool.get('stock.picking')
        stk_move_obj = self.pool.get('stock.move')
        scheduled_date = data[0].schel_date
        if 'active_ids' in context:
            for picking_id in context['active_ids']:
                picking_reg = picking_obj.browse(cr,uid,picking_id)
                line_lst = picking_reg.move_lines
                for line in line_lst:
                    stk_move_obj.write(cr,uid,line.id,{
                                                       'date_expected': scheduled_date
                                                       })
                #actualiza albaran
                picking_obj.write(cr,uid,picking_reg.id,{
                                                         'min_date' : scheduled_date
                                                         })
        return res
    
wizard_stpick_expectdate()