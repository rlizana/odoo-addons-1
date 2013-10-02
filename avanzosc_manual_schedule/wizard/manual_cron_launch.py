# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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

from osv import osv
from osv import fields


class manual_cron_launch(osv.osv_memory):
    
    _name="manual.cron.launch"
    
    _columns = {
                'cron_list':fields.many2many('ir.cron', 'cron_wiz_rel', 'wiz_id', 'cron_id', string="Cron List"),
                }
    def execute_cron(self, cr, uid, ids, context=None):
        cron_obj = self.pool.get('ir.cron')
        
        if not context:
            context={}
    
        for wiz in self.browse(cr,uid,ids):
            cron_ids = []
            for cron in wiz.cron_list:
                if not cron.id in cron_ids:
                    cron_obj.run_jobs_manual([cron.id])
                    cr.commit()
        return {'type':'ir.actions.act_close_window'}
manual_cron_launch()