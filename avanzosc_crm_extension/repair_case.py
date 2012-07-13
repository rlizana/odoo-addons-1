# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    21/02/2012
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the  GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from osv import fields, osv
from tools.translate import _
import pooler
import time   


class crm_case (osv.osv):
    _description= 'crm.case  Inheritance'
    _inherit = 'crm.case'
    _columns = {
        'idvehicle': fields.many2one('fleet.vehicles','Vehicle',required=True),
        'section_id': fields.many2one('crm.case.section', 'Section', select=True),
        'crm_user_id': fields.many2one('res.users', 'Driver', required=True),
        'ref3' : fields.many2one('mrp.repair','Repair Ref.'),
        
    }
    
    def _get_default_user(self, cr, uid, context):
        if context.get('portal', False):
            return False
        return uid
    
    _defaults = {
        'crm_user_id': _get_default_user,
        }
    
    def case_log(self, cr, uid, ids,context={}, email=False, *args):
        user = self.pool.get('res.users').browse (cr,uid, uid)
        u_name = user.name
        #case = self.pool.get('crm.case').browse (cr,uid,ids[0])
        case = self.browse (cr,uid,ids[0])
        if case.state == 'draft':
            self.write(cr, uid, case.id, {'description': case.description,
                                          }, context=context)
        else: self.write(cr, uid, case.id, {'description': u_name + ': ' + case.description,
                                          }, context=context)
        desc = case.description
        super(crm_case, self).case_log(cr, uid, ids, *args)
        return True
    
    def case_close(self, cr, uid, ids, *args):
        case = self.pool.get('crm.case').browse (cr,uid,ids[0])
        if case.state == 'draft':
            raise osv.except_osv('Case in ' + _('draft') + ' state!',' You need to open it.')
        elif case.state == 'open' :
            if case.description :
                context={}
                self.write(cr, uid, case.id, {'description': _(': Case Closed!') + "\n" + _('Reason')  + ': ' + case.description,
                    }, context=context)
                super(crm_case, self).case_close(cr, uid, ids, *args)
            else: raise osv.except_osv(_('Close Error!'),_('The case needs a reason to close it.'))
        return True
    
    def case_open(self, cr, uid, ids, *args):
        case_objs = self.pool.get('crm.case')
        case = case_objs.browse (cr,uid,ids[0])
        context={}
        if case.state == 'draft':
            if case.description :
                self.write(cr, uid, case.id, {'description': _('Open') + ': ' + case.description,
                    }, context=context)
                super(crm_case, self).case_log(cr, uid, ids, email=False, *args)
        super(crm_case, self).case_open(cr, uid, ids, *args)
        return True
    
    def case_cancel(self, cr, uid, ids, *args):
        case = self.pool.get('crm.case').browse (cr,uid,ids[0])
        if case.state == 'draft':
            raise osv.except_osv(_('Case in draft state!'),_(' You need to open it.'))
        elif case.state == 'open' :
            if case.description :
                context={}
                self.write(cr, uid, case.id, {'description': _('Case Canceled!') + "\n" + _('Reason')  + ': ' + case.description,
                    }, context=context)
                super(crm_case, self).case_cancel(cr, uid, ids, *args)
            else: raise osv.except_osv(_('Cancel Error!'),_('The case needs a reason to cancel it.'))
        return True
    
    def case_pending(self, cr, uid, ids, *args):
        case_objs = self.pool.get('crm.case')
        case = case_objs.browse (cr,uid,ids[0])
        context={}
        if case.state == 'draft':
            if case.description :
                self.write(cr, uid, case.id, {'description': _('Pending: ') + case.description,
                    }, context=context)
                super(crm_case, self).case_log(cr, uid, ids, email=False, *args)
        super(crm_case, self).case_pending(cr, uid, ids, *args)
        return True    

crm_case()

class mrp_repair (osv.osv):
    
    _description= 'mrp.repair Inheritance'
    _inherit= 'mrp.repair'
    _columns = {
        'case': fields.many2one('crm.case', 'Claim',size=64, readonly=True),
        'preventive':fields.boolean('Is preventive'),
        'idvehicle':fields.many2one('fleet.vehicles','Vehicle')
        }
    
    def action_confirm(self, cr, uid, ids, *args):
        mrp_repair_obj = self.pool.get('mrp.repair').browse (cr,uid,ids[0])
        case_id = mrp_repair_obj.case
        if case_id:
            case = self.pool.get('crm.case').browse(cr, uid, case_id.id)
            data = {    
                 'name': _('Open'),
                 'som': case.som.id,
                 'canal_id': case.canal_id.id,
                 'user_id': uid,
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'case_id': case.id,
                 'section_id': case.section_id.id,
                 #'description' : _('Repair Accepted'),
                 'description' : _('Reparación Aceptada'),
                 }
            obj = self.pool.get('crm.case.history')
            obj.create(cr, uid, data)
        super(mrp_repair, self).action_confirm(cr, uid, ids, *args)      
        return True
    
    def action_repair_start(self, cr, uid, ids, context=None):
        mrp_repair_obj = self.pool.get('mrp.repair').browse (cr, uid, ids[0])
        case_id = mrp_repair_obj.case
        if case_id:
            if case_id.state != 'Open':
                case_objs = self.pool.get('crm.case')
                case = case_objs.browse(cr, uid, case_id.id)
                data = {    
                 'name': _('Open'),
                 'som': case.som.id,
                 'canal_id': case.canal_id.id,
                 'user_id': uid,
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'case_id': case.id,
                 'section_id': case.section_id.id,
                 #'description' : _('Working Started'),
                 'description' : _('Reparación Iniciada'),
                 }
                obj = self.pool.get('crm.case.history')
                obj.create(cr, uid, data)
                case_objs.write(cr, uid, case.id, {'state': _('open')})
        super(mrp_repair, self).action_repair_start(cr, uid, ids)
        return True

    

    def action_repair_done(self, cr, uid, ids, context=None):
        mrp_repair_obj = self.pool.get('mrp.repair').browse (cr, uid, ids[0])
        case_id = mrp_repair_obj.case
        if case_id:
            if case_id.state != 'done':
                case_objs = self.pool.get('crm.case')
                case = case_objs.browse(cr, uid, case_id.id)
                data = {    
                 'name': _('Open'),
                 'som': case.som.id,
                 'canal_id': case.canal_id.id,
                 'user_id': uid,
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'case_id': case.id,
                 'section_id': case.section_id.id,
                 #'description' : _('Work Done'),
                 'description' : _('Reparación Completada'),
                 }
                obj = self.pool.get('crm.case.history')
                obj.create(cr, uid, data)
                case_objs.write(cr,uid,case.id,{'state': 'done'})
        super(mrp_repair, self).action_repair_done(cr, uid, ids)
        return True

mrp_repair()

class stock_move (osv.osv):
    
    _description= 'stock.move Inheritance'
    _inherit= 'stock.move'
    _columns = {
                }

    def action_confirm(self, cr, uid, ids, context={}):
        pool = pooler.get_pool(cr.dbname)
        repair_objs = pool.get('mrp.repair')
        repair_id = repair_objs.search(cr,uid,[('move_id', '=',ids[0])])
        if repair_id != []:
            repair = repair_objs.browse(cr,uid,repair_id[0])
            case_id = repair.case
            if case_id:
                case_objs = pool.get('crm.case')
                case = case_objs.browse (cr,uid,case_id.id)
                data = {    
                        'name': _('Open'),
                        'som': case.som.id,
                        'canal_id': case.canal_id.id,
                        'user_id': uid,
                        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'case_id': case.id,
                        'section_id': case.section_id.id,
                        'description' : _('Vehicle Arrived')
                        }
                obj = pool.get('crm.case.history')
                obj.create(cr, uid, data)
                case_objs.write(cr,uid,case.id,{'state': 'open'})
        super(stock_move, self).action_confirm(cr, uid, ids,context)
        return []
    
stock_move()
