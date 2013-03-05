
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

from osv import osv
from osv import fields

class hr_employee_formation(osv.osv):

    _name = 'hr.employee.formation'
    _description = 'Employee Formation'
   
    _columns = {# Empleado
                'employee_id':fields.many2one('hr.employee', 'Employee', ondelete='cascade'),
                # Curso de Formacion
                #'formation_id':fields.many2one('formation', 'Curse', domain=[('type','=',type)]),
                'formation_id':fields.many2one('formation', 'Curse'),
                # Descripción
                'name':fields.char('Name', size=64, required=True),
                # Codigo
                'code':fields.char('Code', size=64, required=True),
                # Tipo de Curso (Externo/Interno)
                'type': fields.selection([('Internal','Internal'),
                                          ('External','External')],
                                         'Type', required=True), 
                # Fecha Inicio
                'start_date':fields.date('Start Date'),
                # Fecha Inicio
                'end_date':fields.date('End Date'),
                # Realizado
                'realized':fields.boolean('Realized'),
                } 
    
    _defaults = {'type': lambda self, cr, uid, c: c.get('type', False),
                 }
    
    def onchange_formation(self, cr, uid, ids, formation_id, context=None):
        res={} 
        if formation_id:
            formation_obj = self.pool.get('formation')
            formation = formation_obj.browse(cr,uid,formation_id)
            res = {'name': formation.name,
                   'code': formation.code,
                   'start_date': formation.start_date,
                   'end_date': formation.end_date,
                   'realized': formation.realized,
                   }
            
        return {'value': res}   
        
hr_employee_formation()
