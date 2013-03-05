# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from datetime import datetime, timedelta
import time

from osv import osv
from osv import fields

from tools.translate import _
 
class import_template_employes(osv.osv_memory):

    _name = 'import.template.employes'
    _description = "Import Template Employes"
 
    _columns = {# Fecha Comienzo
                'start_date':fields.date('Start Date', required=True),
                # Fecha Fin
                'end_date':fields.date('End Date', required=True),
                # Plantilla
                'festive_template_id':fields.many2one('festive.template', 'Template', required=True),
                # Lineas
                'import_template_employes_line_ids':fields.one2many('import.template.employes.line','import_template_employes_id','Employes'),
         }
    
    #
    ### Esta función se ejecuta antes de mostrar el wizard
    #
    def default_get(self, cr, uid, fields_list, context=None):
        
        vals = []
        
        employee_obj = self.pool.get('hr.employee')
        
        data = context and context.get('active_ids', []) or []
        
        for employee in employee_obj.browse(cr, uid, data, []):
            line_vals = {'employee_id': employee.id,
                         'selected': True}  
            vals.append(line_vals)  
                
        return {'import_template_employes_line_ids':vals}  

    #
    ### Función
    #
    def action_import_template_employes(self, cr, uid, ids, context=None):

        res={}
        
        festive_template_line_obj = self.pool.get('festive.template.line')
        estimated_calendar_resources_obj = self.pool.get('estimated.calendar.resources')
        hr_employee_calendar_obj = self.pool.get('hr.employee.calendar')
                   
        for wiz in self.browse(cr,uid,ids,context):
            start_date = wiz.start_date
            start_year = int(str(start_date[0:4]))
            end_date = wiz.end_date
            end_year = int(str(end_date[0:4]))
            src_temp = wiz.festive_template_id
            
            data={}
            
            if start_year <> end_year:
                raise osv.except_osv('Import Template Error', 'Start and End Year are differents')
            if end_date < start_date:
                raise osv.except_osv('Import Template Error', 'End Date < Start Date')
                

            for template_employe in wiz.import_template_employes_line_ids:
                if template_employe.selected == True:
                    fec_ini = start_date
                    fec_ini = datetime.strptime(fec_ini,'%Y-%m-%d')
                    fec_fin = end_date
                    fec_fin = datetime.strptime(fec_fin,'%Y-%m-%d')
                     
                    while fec_ini <= fec_fin:                          
                        my_date_alpha = str(fec_ini)
                        my_date = my_date_alpha[0:10]
                        my_date_year = my_date[0:4]
                        
                        # Miro que exista el calendario para el trabajador.
                        hr_employee_calendar_ids = hr_employee_calendar_obj.search(cr, uid,[('employee_id','=', template_employe.employee_id.id),
                                                                                            ('year', '=', my_date_year)])   
                        
                        if not hr_employee_calendar_ids:
                            line_vals = {'employee_id' : template_employe.employee_id.id,
                                         'year': my_date_year,
                                         'name': 'Calendar ' + str(my_date_year),
                                         }  
                            hr_employee_calendar_id = hr_employee_calendar_obj.create(cr, uid, line_vals) 
                        else:
                            hr_employee_calendar_id = hr_employee_calendar_ids[0]        
                        
                        festive_template_line_ids = festive_template_line_obj.search(cr, uid,[('festive_template_id','=', src_temp.id),
                                                                                              ('date', '=', my_date)])   
                        
                        if not festive_template_line_ids:        
                            estimated_calendar_resources_ids = estimated_calendar_resources_obj.search(cr, uid,[('hr_employee_calendar_id','=', hr_employee_calendar_id),
                                                                                                                ('date', '=', my_date)])  
                            if not estimated_calendar_resources_ids:
                                line_vals = {'hr_employee_calendar_id' : hr_employee_calendar_id,
                                             'date': my_date,
                                             'hours': 8,
                                             }  
                                estimated_calendar_resources_id = estimated_calendar_resources_obj.create(cr, uid, line_vals)  
                            else:
                                estimated_calendar_resources_obj.write(cr,uid,estimated_calendar_resources_ids,{'name': False,
                                                                                                                'hours': 8})            
                        else:
                            festive_template = festive_template_line_obj.browse(cr,uid, festive_template_line_ids[0])
                            estimated_calendar_resources_ids = estimated_calendar_resources_obj.search(cr, uid,[('hr_employee_calendar_id','=', hr_employee_calendar_id),
                                                                                                                ('date', '=', my_date)])  
                            if not estimated_calendar_resources_ids:
                                line_vals = {'hr_employee_calendar_id' : hr_employee_calendar_id,
                                             'date': my_date,
                                             'name': festive_template.name,
                                             'hours': 0,
                                             'background_color': festive_template.background_color,
                                             }  
                                estimated_calendar_resources_id = estimated_calendar_resources_obj.create(cr, uid, line_vals)  
                            else:
                                estimated_calendar_resources_obj.write(cr,uid,estimated_calendar_resources_ids,{'name': festive_template.name,
                                                                                                                'hours': 0,
                                                                                                                'background_color': festive_template.background_color,}) 
                            
                        # Sumo 1 día a la fecha
                        fec_ini = fec_ini + timedelta(days=1)
                        fec_ini.strftime('%Y-%m-%d')
  
        return {'type': 'ir.actions.act_window_close'}
    
    
import_template_employes()