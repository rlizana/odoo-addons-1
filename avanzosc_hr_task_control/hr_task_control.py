
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 Daniel (AvanzOSC). All Rights Reserved
#    Date: 18/02/2013
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

from osv import fields,osv
from tools.translate import _
import pooler
import time  

class wizard_task (osv.osv_memory):
    
    _name = 'wizard.task'
    _description = 'Wizard task'
    _columns = {
                'task' : fields.many2one("project.task", "Task"),
                'time': fields.float('Hours', digits=(16,2), help="Expected time. hh:mm"),
                'description': fields.char ('Description/Notes', size=128),
    }
     
wizard_task()

class wizard_task_list (osv.osv_memory):
    
    def _task_list(self, cr, uid, context=None):

        project_task_obj = self.pool.get('project.task') 
        user_task_list = project_task_obj.search(cr,uid,[('user_id','=',context['emp_id']),('state','=','open')])
        task_list = []
        for task in user_task_list:
            task_dict = {
                         'task' : task,
                         'time' : 0.0,
                         'description' : ''
                        }
            task_list.append(task_dict)
        return  task_list
    
    def hour_control(self, cr, uid, ids, context=None):
        
        res = {}
        wizard_task_obj = self.pool.get('wizard.task')
        hr_sign_obj = self.pool.get('hr.sign.in.out')
        project_taskw_obj = self.pool.get('project.task.work')
        task_obj = self.pool.get('project.task')
        project_obj = self.pool.get('project.project')
        hr_emp_obj = self.pool.get('hr.employee')
        project_id_list = []
        data = self.browse(cr, uid, ids[0], context=context)
        data_hr_sign = context['sing_data']
        task_list = data.task_list
        total_time = 0
        task_id_list = []
        for task in task_list : # Time for all tasks
            total_time = total_time + task.time
        if total_time < 8:
            raise osv.except_osv(_('Warning!'), _('The entered time is below 8 hours!'))
        else :
            for tasking in task_list:
                task_reg = task_obj.browse(cr, uid, tasking.task.id, context=context)
                employee = hr_emp_obj.browse(cr, uid, context['emp_id'], context=context)
                user_id = employee.user_id
                resu = {'name': task_reg.name}
                if tasking.time > 0 : # Time assigned for current task
                    if total_time == 8 :
                        res = {
                           'name' : tasking.description,
                           'hours' : tasking.time,
                           'date' : time.strftime('%Y-%m-%d %H:%M:%S'),
                           'user_id' : user_id.id, #context['emp_id'],
                           'task_id' : task_reg.id,
                           'company_id' : task_reg.company_id.id,
                           }
                    else :
                        time_task = tasking.time * 8.0 / total_time
                        res = {
                           'name' : tasking.description,
                           'hours' : time_task,
                           'date' : time.strftime('%Y-%m-%d %H:%M:%S'),
                           'user_id' : user_id.id, #context['emp_id'],
                           'task_id' : task_reg.id,
                           'company_id' : task_reg.company_id.id,
                                }
                    project_taskw_obj.create(cr,uid,res, context=context)
                    if task_id_list == [] :
                        task_id_list = [task_reg.id]
                    else:
                        pid = task_reg.id
                        counter = project_id_list.count(pid)
                        if counter == 0:
                            task_id_list.append(pid)
        result= super(hr_sign_in_out, hr_sign_obj).sign_out(cr, uid, data_hr_sign, context)
        #update project hours
        names = ['effective_hours', 'progress_rate', 'total_hours', 'planned_hours']
        resu = {}
        for pid in task_id_list :
            task_reg = task_obj.browse(cr,uid,pid)
            resu['remaining_hours'] = task_reg.remaining_hours
            task_obj.write(cr,uid,task_reg.id,resu)     
        return {'type': 'ir.actions.act_window_close'} 
    
    
    """ Task List Time control """
    _name = 'wizard.task.list'
    _description = 'task list'
    _columns = {
                'task_list': fields.one2many('wizard.task','task_list_id','Task List'),          
        }
    
    _defaults = {
                # 'task_list': _task_list, # Current user open state task list
                 }

wizard_task_list()

class wizard_task (osv.osv_memory):
    
    _inherit = 'wizard.task'
    _description = 'Wizard task inherit'
    
    _columns = {
                'task_list_id' : fields.many2one("wizard.task.list", "Task List"),
                }
wizard_task() 

class hr_sign_in_out(osv.osv_memory):
    

    
    _inherit= 'hr.sign.in.out'
    _description = 'Sign In Sign Out wizard inheritance'
    
    
    def sign_out(self, cr, uid, data, context=None):
        
        wizard = {}
        if not context.has_key('emp_id'):
            context = { 
                       'emp_id' : data['emp_id'],
                       'sing_data' : data,
                        }
            wizard = {
                      'type': 'ir.actions.act_window',
                      'name' : 'View Task List',
                      'res_model': 'wizard.task.list',
                      'view_type': 'tree,form',
                      'view_mode': 'form',
                      #'res_id': task_list_id,
                      'target': 'new',
                      'context' : context,

                      }
        return wizard
    
hr_sign_in_out()

