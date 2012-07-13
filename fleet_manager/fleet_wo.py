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

from osv import osv, fields
import pooler
import time

class fleet_workorder(osv.osv):
    _name="fleet.wo"
    _description="Work Orders for Fleet Maintainance"
    _rec_name="wono"
    def wo_seq_get(self, cr, uid):
        pool_seq=self.pool.get('ir.sequence')
        cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='fleet.wo' and active=True")
        res = cr.dictfetchone()
        if res:
            if res['number_next']:
                return pool_seq._process(res['prefix']) + '%%0%sd' % res['padding'] % res['number_next'] + pool_seq._process(res['suffix'])
            else:
                return pool_seq._process(res['prefix']) + pool_seq._process(res['suffix'])
        return False
    
    def create(self, cr, user, vals, context=None):
        name=self.pool.get('ir.sequence').get(cr, user, 'fleet.wo')
        return super(fleet_workorder,self).create(cr, user, vals, context)
    
    _columns={
              'wono':fields.char('Work Order no',size=20,required=True),
              'description':fields.char('Order Narration',size=100),
              #'vehicle':fields.one2many('fleet.vehicles','Vehicle'), Depreciated
              'tasks':fields.one2many('fleet.wo.tasks','workorder','Tasks in Work Order'),
              'rdate':fields.date('Order Date',required=True),
              'instr':fields.char('Instructions',size=64)
              }
    _defaults={
               'wono':lambda obj,cr,uid,context: obj.pool.get('fleet.wo').wo_seq_get(cr,uid)
               }
    _sql_constraints = [
        ('uniq_wo_no', 'unique (wono)', 'The Work order no must be unique !')
    ]
fleet_workorder()

class fleet_wo_tasks(osv.osv):
    _name="fleet.wo.tasks"
    _description="Work Order Tasks"
    _rec_name="taskno"
    
    def _get_vehicle_wo(self, cr, uid, ids, field_name, arg, context):
        for i in ids:
            print "i is >>>" + str(i)
        return False
    
    def wt_seq_get(self, cr, uid):
        pool_seq=self.pool.get('ir.sequence')
        cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='fleet.wo.tasks' and active=True")
        res = cr.dictfetchone()
        if res:
            if res['number_next']:
                return pool_seq._process(res['prefix']) + '%%0%sd' % res['padding'] % res['number_next'] + pool_seq._process(res['suffix'])
            else:
                return pool_seq._process(res['prefix']) + pool_seq._process(res['suffix'])
        return False    
    
    def create(self, cr, user, vals, context=None):
        name=self.pool.get('ir.sequence').get(cr, user, 'fleet.wo.tasks')
        return super(fleet_wo_tasks,self).create(cr, user, vals, context)
    
    def on_change_servitem(cr, uid, ids, servitem,some):
        if servitem:
            print "service item is:" + servitem
        else:
            print "Theres no servitem"
    _columns={
              'taskno':fields.char('Task No',size=20,required=True),
              #'vehicle':fields.function(_get_vehicle_wo,method=True,string="Vehicle",store=True,type='many2one', obj="fleet.vehicles"), Depreciated
              'workorder':fields.many2one('fleet.wo','parent work Order',ondelete='cascade'),
              'vehicle':fields.many2one('fleet.vehicles','Vehicle',required=True),
              'servitem':fields.many2one('fleet.service.items','Service Task',required=True),
              'duedate':fields.date('Due Date'),
              'scheddate':fields.date('Scheduled Date'),
              'assignee':fields.many2one('hr.employee','Assigned Employee',required=True),
              'supervisor':fields.many2one('hr.employee','Supervisor'),
              'wosysgen':fields.boolean('System Generated'),
              'spares':fields.one2many('fleet.wo.tasks.spares','wotask','Spares Required'),
              'state':fields.selection([
                                         ('notstarted','Not Started'),
                                         ('inprogress','In Progress'),
                                         ('planningneeded','Planning Needed'),
                                         ('awaitingparts','Waiting for Spares'),
                                         ('testing','Test/Inspection'),
                                         ('complete','Complete'),
                                         ('cancel','Cancel')
                                         ],'Task Status',required=True),
                                         
              
              }
    _defaults={
               'taskno':lambda obj,cr,uid,context: obj.pool.get('fleet.wo.tasks').wt_seq_get(cr,uid),
               'state':lambda *a:'notstarted'
               }
    
    _sql_constraints = [
        ('uniq_task_no', 'unique (taskno)', 'The task no must be unique !')
    ]
    
    
fleet_wo_tasks()

class fleet_wo_tasks_spares(osv.osv):
    _name="fleet.wo.tasks.spares"
    _description="WO Tasks spares requirement"
    _rec_name="spare_req_no"
    
    def wts_seq_get(self, cr, uid):
        pool_seq=self.pool.get('ir.sequence')
        cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='fleet.wo.tasks.spares' and active=True")
        res = cr.dictfetchone()
        if res:
            if res['number_next']:
                return pool_seq._process(res['prefix']) + '%%0%sd' % res['padding'] % res['number_next'] + pool_seq._process(res['suffix'])
            else:
                return pool_seq._process(res['prefix']) + pool_seq._process(res['suffix'])
        return False  
    
    def fetchunit(self,cr,uid,ids,productid):
        #print "Control is txed & Product id"
        #print productid
        if productid:
            product_obj = self.pool.get('product.product')
            product_obj = product_obj.browse(cr, uid, productid,False)
            #print product_obj
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            #print default_uom
            res={}
            res['unit']=default_uom
            #print res
            return {'value':res}
        else:
            return False
    
    def create(self, cr, user, vals, context=None):
        name=self.pool.get('ir.sequence').get(cr, user, 'fleet.wo.tasks.spares')
        return super(fleet_wo_tasks_spares,self).create(cr, user, vals, context) 
        
    _columns={
             'spare_req_no':fields.char('Spares Req. No',size=20,required=True),
             'wotask':fields.many2one('fleet.wo.tasks','Parent WO Task',ondelete="cascade"),
             'product':fields.many2one('product.product',domain=[('spare_ok','=','True')],string='Spare Part',required=True),
             'quantity':fields.float('Quantity',required=True),
             'unit':fields.many2one('product.uom','Unit Of Use',required=True),
             'state':fields.selection([
                                       ('draft','Request Draft'),
                                       ('approved','Pending Move'),
                                       ('moved','Spare Issued')
                                       ],'State/Status',required=True)
             }
    _defaults={
              'quantity': lambda *a: 1.00,
              'state': lambda *a:'draft',
              'spare_req_no': lambda obj,cr,uid,context: obj.pool.get('fleet.wo.tasks.spares').wts_seq_get(cr,uid),
              }
    _sql_constraints = [
        ('spare_req_no', 'unique (spare_req_no)', 'The spare request no must be unique!')
    ]
fleet_wo_tasks_spares()

class fleet_wo_tasks_labour(osv.osv):
    _name="fleet.wo.tasks.labour"
    _description="WO labour Tasks"
    _rec_name="lab_req_no"
    _columns={
             'lab_req_no':fields.char('Labour Req No',size=20,required=True),
             'partner':fields.many2one('res.partner','Workshop/Payee'),
             'description':fields.char('Description of work',size=64,required=True),
             'amount':fields.float('Amount',digits=(10,2),required=True),
             'verified':fields.many2one('hr.employee','Verified By'),
             'state': fields.selection([
                                        ('draft','Draft'),
                                        ('verified','Verified'), 
                                        ('paid','Paid'),
                                        ('audited','Audited')
                                        ], 'Status', readonly=True),
             }
    _defaults={
              'amount': lambda *a: 1.00,
              'state':lambda *a: 'draft',
              }
fleet_wo_tasks_labour()
    
