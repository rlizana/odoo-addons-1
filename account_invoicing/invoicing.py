##############################################################################
#
# Copyright (c) 2008-2009 SIA "KN dati". (http://kndati.lv) All Rights Reserved.
#                    General contacts <info@kndati.lv>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import fields,osv
import netsvc
import tools
import math
import re
from tools.translate import _
from mx import DateTime
from mx.DateTime import now
import time, locale
import traceback, sys

def _change_state(self, cr, uid, ids, field, field_type, field_id, value1_char, value1_bool, \
        value1_int, value2_int, value1_float, value2_float, value1_date, value2_date, value1_datetime, value2_datetime, cond_value):
    data = {}
    if field_id:
        field_name = self.pool.get('ir.model.fields').browse(cr, uid, field_id, {}).name
    else:
        field_name = 'count'
    if not field:
        return {'value':{},'state':False}
    else:
        cond_type = self.pool.get('inv.rec_type').browse(cr, uid, field).value
        data['state'] = self.pool.get('inv.rec_type').browse(cr, uid, field).type
        value = self.pool.get('inv.rec_type').browse(cr, uid, field).value
        if data['state']!='[many2one]' and data['state']!='[one2many]' and data['state']!='[many2many]' and data['state']!='[boolean]' \
                and data['state']!='[char]' and data['state']!='[selection]':
            if value=='between' or value=='not between':
                data['state'] += '|2|'
            else:
                data['state'] += '|1|'
        if value!='between' and value!='not between':
            data['value2_int'] = 0
            data['value2_float'] = 0
            data['value2_date'] = ''
            data['value2_datetime'] = ''

        res = ''
        if cond_type == 'equal to':
            operator = ' == '
        elif cond_type == 'not equal to':
            operator = ' != '
        elif cond_type == 'greater than':
            operator = ' > '
        elif cond_type == 'less than':
            operator = ' < '
        elif cond_type == 'greater than or equal to':
            operator = ' >= '
        elif cond_type == 'less than or equal to':
            operator = ' <= '
        elif cond_type == 'regexp':
            operator = ' match '
        else:
            operator = ''

        if cond_type!='between' and cond_type!='not between':
            if field_type == '[char]' or field_type == '[selection]':
                res = field_name + operator + "'"+(value1_char and unicode(value1_char, "UTF-8") or '')+"'" or ''
            elif field_type == '[boolean]':
                res = field_name + operator + str(value1_bool) or ''
            elif field_type == '[integer]':
                res = field_name + operator + str(value1_int) or ''
            elif field_type == '[float]':
                res = field_name + operator + str(value1_float) or ''
            elif field_type == '[date]':
                res = field_name + operator + str(value1_date) or ''
            elif field_type == '[datetime]':
                res = field_name + operator + str(value1_datetime) or ''
        elif cond_type=='between':
            if field_type == '[integer]':
                res = '(' + field_name + ' >= ' + str(value1_int)+')'
                if value2_int != None:
                    res += ' and ('+field_name+ ' <= ' + str(value2_int)+')' or ''
            elif field_type == '[float]':
                res = '(' + field_name + ' >= ' + str(value1_float)+')'
                if value2_float != None:
                    res += ' and ('+field_name+ ' <= ' + str(value2_float)+')' or ''
            elif field_type == '[date]':
                res = '(' + field_name + ' >= ' + str(value1_date)+')'
                if value2_date:
                    res += ' and ('+field_name+ ' <= ' + str(value2_date)+')' or ''
            elif field_type == '[datetime]':
                res += '(' + field_name + ' >= ' + str(value1_datetime)+')'
                if value2_datetime:
                    res += ' and ('+field_name+ ' <= ' + str(value2_datetime)+')' or ''
        elif cond_type=='not between':
            if field_type == '[integer]':
                res = '(' + field_name + ' <= ' + str(value1_int)+')' or ''
                if value2_int != None:
                    res += ' and ('+field_name+ ' >= ' + str(value2_int)+')' or ''
            elif field_type == '[float]':
                res = '(' + field_name + ' <= ' + str(value1_float)+')'
                if value2_float != None:
                    res += ' and ('+field_name+ ' >= ' + str(value2_float)+')' or ''
            elif field_type == '[date]':
                res = '(' + field_name + ' <= \'' + str(value1_date)+'\')'
                if value2_date:
                    res += ' and ('+field_name+ ' >= \'' + str(value2_date)+'\')' or ''
            elif field_type == '[datetime]':
                res = '(' + field_name + ' <= \'' + str(value1_datetime)+'\')'
                if value2_datetime:
                    res += ' and ('+field_name+ ' >= \'' + str(value2_datetime)+'\')' or ''

        if cond_type=='in' or cond_type=='not in':
            res = field_name + ' ' + cond_type
            if cond_value and cond_value != None:
                res += ' ['+cond_value+']' or ''
        data['name'] = res
    return data

#def convert_date(self, date):
#    return time.strftime(locale.nl_langinfo(locale.D_FMT), time.strptime(date, '%Y-%m-%d'))

def convert_date(self, date):
    if len(date)==10:
        return date[8:10]+'.'+date[5:7]+'.'+date[:4]+'.'
    elif len(date)==7:
        return date[5:7]+'.'+date[:4]+'.'
    return date+'.'

def reconvert_date(self, date):
    try:
        if len(date)==11:
            retval = date[6:10]+'-'+date[3:5]+'-'+date[:2]
            DateTime.strptime(retval, '%Y-%m-%d')
            return retval
        elif len(date)==8:
            retval = date[3:7]+'-'+date[:2]+'-01'
            DateTime.strptime(retval, '%Y-%m-%d')
            return retval
        else:
            retval = date[:4]+'-01-01'
            DateTime.strptime(retval, '%Y-%m-%d')
            return retval
    except Exception, e:
        return '1900-01-01'

def find_req_users(self, cr, uid, service):
    result = []
    admin_id = self.pool.get('res.users').search(cr, uid, [('login','=','admin')])[0]
    srv = self.pool.get('inv.service').browse(cr, uid, service, {})
    tgroup = map(int, srv.req_users)
    #Structure changes in 6.0. Commented 5 lines
    #tg_obj = self.pool.get('hr.timesheet.group')
    #for wt in tgroup:
    #    user = tg_obj.browse(cr, uid, wt, {}).manager.id
    #    if user not in result:
    #        result.append(user)

    tg_obj = self.pool.get('hr.employee')
    wts = tg_obj.search(cr, uid, [('user_id', 'in', tgroup)])
    for emp in tg_obj.browse(cr, uid, wts, {}):
        if emp.department_id:
            if emp.department_id.manager_id and emp.id == emp.department_id.manager_id.id:
                user = emp.department_id.manager_id.id
                if user not in result:
                    result.append(user)
    #emp_obj = self.pool.get('hr.employee')
    #emp_ids = emp_obj.search(cr, uid, [])
    #for id in emp_ids:
    #    emp_rec = emp_obj.browse(cr, uid, id, {})
    #    for r in map(int, srv.req_users):
    #        if r in map(int, emp_rec.workgroups):
    #            user = emp_rec.user_id.id
    #            if user not in result:
    #                result.append(emp_rec.user_id.id)
    if result and result[0]:
        return result
    else:
        return [admin_id]

def create_request(self, cr, uid, subject, req_text, service):
    req_users = find_req_users(self, cr, uid, service)
    admin_id = self.pool.get('res.users').search(cr, uid, [('login','=','admin')])[0]
    for user_id in req_users:
        req_values = {'name':subject,'act_from':admin_id,'act_to':user_id,'date_sent':time.strftime('%Y-%m-%d %H:%M:%S'),'body':req_text,'state':'waiting','priority':'2'}
        id = self.pool.get('res.request').create(cr, uid, req_values)
        cr.execute('select act_from,act_to,body,date_sent from res_request where id=%s', (id,))
        values = cr.dictfetchone()
        if len(values['body']) > 128:
            values['name'] = values['body'][:125] + '...'
        else:
            values['name'] = values['body'] or '/'
        values['req_id'] = id
        self.pool.get('res.request.history').create(cr, uid, values)
    return True

class rec_type(osv.osv):
    _name = "inv.rec_type"
    _rec_name = "value"

    _columns = {
        'type': fields.char('Type', size=64, required=True),
        'value': fields.char('Value', size=64, required=True),
    }

rec_type()

class method(osv.osv):
    _name = "inv.method"
    _rec_name = "name"

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'model_id': fields.many2one('ir.model', 'Model', states={'close':[('readonly',True)]}, required=True),
        'partner_field': fields.many2one('ir.model.fields', 'Field', domain="[('model_id', '=', model_id),('relation','=', ref)]", required=True),
        'ref': fields.selection([('res.partner','Partner'),('res.partner.address','Contact')], 'Field', required=True),
        'rec_filter_ids': fields.one2many('inv.rec_filter', 'method_id', 'Filters',  states={'open':[('readonly',True)]}),
        'calc_base': fields.selection([('field','Field'),('count','Count')], 'Calculation base', required=True),
        'calc_ids': fields.one2many('inv.calc', 'method_id', 'Calculation', ondelete='cascade', states={'open':[('readonly',True)]}),
        'state': fields.selection([('open', 'Open'),('close','Close')], 'State', select=True, readonly=True),
        'manual': fields.boolean('Manual', states={'open':[('readonly',True)]}),
        'source': fields.text('Source', states={'open':[('readonly',True)]}),
    }

    def _get_source(self, cr, uid, ids):
        filter_obj = self.pool.get('inv.rec_filter')
        cond_obj = self.pool.get('inv.rec_filter_cond')
        for p in self.browse(cr, uid, ids, {}):
            if p.manual:
                return True
            model = p.model_id.model
            result = 'obj = self.pool.get(\''+model+'\')\n'
            if p.ref == 'res.partner.address':
                result += 'model_ids = obj.search(cr, uid, [(\''+p.partner_field.name+'\', \'in\', contact_ids)])\n'
            else:
                result += 'model_ids = obj.search(cr, uid, [(\''+p.partner_field.name+'\', \'=\', partner_id)])\n'
            filter_ids = filter_obj.search(cr, uid, [('method_id','=',p.id)])
            result += "for cur_object in obj.browse(cr, uid, model_ids, {}):\n\tresult = True\n"
            for r in filter_obj.browse(cr, uid, filter_ids, {}):
                cond_ids = cond_obj.search(cr, uid, [('rec_filter_id','=',r.id)])
                if r.var == 'count': continue
                for s in cond_obj.browse(cr, uid, cond_ids, {}):
                    result += s.code
            result += '\n\tif result:\n\t\tmas_aft.append(cur_object.id)\n'

            for r in filter_obj.browse(cr, uid, filter_ids, {}):
                cond_ids = cond_obj.search(cr, uid, [('rec_filter_id','=',r.id)])
                if r.var == 'field': continue
                result += '\ncount = len(model_ids)\n'
                for s in cond_obj.browse(cr, uid, cond_ids, {}):
                    result += s.code

        cr.execute("""
                UPDATE inv_method
                SET source = %s
                WHERE id in (%s)
               """, (result, ','.join(map(str,ids))))
        return True

    def on_model_change(self, cr, uid, ids, field):
        return {'value':{'partner_field':False}}

    def action_create_meth(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'close'})
        wf_service = netsvc.LocalService("workflow")
        for inv_id in ids:
            wf_service.trg_create(uid, 'inv.metod', inv_id, cr)
        return True

    def action_test_source(self, cr, uid, ids, *args):
        mas_before = []
        mas_after = []
        agr = self.pool.get('inv.agreement')
        agr_ids = agr.search(cr, uid, [])
        if agr_ids == []:
            raise osv.except_osv(_('Warning!'), _('Code it is impossible tested, because there is not an agreement!'))
        for p in self.browse(cr, uid, ids, {}):
            if p.source:
                for r in agr.browse(cr, uid, agr_ids, {}):
                    localspace = {"self":self,"cr":cr,"uid":uid,"re":re,"mas_aft":mas_after,"partner_id":r.partner_id.id,"contact_ids":map(int, r.partner_id.address)}
                    try:
                        exec p.source in localspace
                        mas_before = localspace['model_ids']
                        mas_after = localspace['mas_aft']
                        rec = 'Number of records before: ' + str(len(mas_before)) + '\nNumber of records after: ' + str(len(mas_after))
                        raise osv.except_osv(_('Information'),_(rec))
                        break
                    except (SyntaxError, NameError, IndexError), exc:
                        raise osv.except_osv(_('Error!'), _(exc))
                    #except Exception, e:
                    #    tb_s = reduce(lambda x, y: x+y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
                    #    create_request(self, cr, uid, tb_s, r.service.id)
                    #    break

        return True

    def sort_calc_list(self, cr, uid, calc_ids):
        res_list = {}
        for l in self.pool.get('inv.calc').browse(cr, uid, calc_ids, {}):
            res_list[l.sequence] = l.id
        res = res_list.items()
        res.sort()
        return [r[1] for r in res]

    def _run_filters(self, cr, uid, ids, agr_id, context={}):
        acc_lines = []
        agr = self.pool.get('inv.agreement')
        r = agr.browse(cr, uid, agr_id, {})
        d_list = self.pool.get('inv.date_list')
        current_date = now().strftime('%Y-%m-%d')
        if r.service.invoicing == 'period':
            full_date_list = map(int, r.date_list)
            date_list1 = d_list.search(cr, uid, [('id','in',full_date_list),('status','=','wait')])
            date_list2 = d_list.search(cr, uid, [('id','in',full_date_list),('status','=','process')])
            date_list = date_list2 + date_list1
            if not date_list: return True
            date_list.reverse()
            date_id = date_list.pop()
            date = d_list.browse(cr, uid, date_id, {}).date
            pdate1 = DateTime.strptime(d_list.browse(cr, uid, date_id, {}).pdate1, '%Y-%m-%d')
            pdate2 = DateTime.strptime(d_list.browse(cr, uid, date_id, {}).pdate2, '%Y-%m-%d')
        else:
            date = current_date
            date_id = False
            pdate1 = False
            pdate2 = False
            date_list = []
        try:
            if date <= current_date and r.service.invoicing=='period':
                d_list.write(cr, uid, date_id, {'status':'process'})
            for p in self.browse(cr, uid, ids, {}):
                mas_after = []
                localspace = {"self":self,"cr":cr,"uid":uid,"re":re,"mas_aft":mas_after,"partner_id":r.partner_id.id,"contact_ids":map(int, r.partner_id.address),"pdate1":pdate1,"pdate2":pdate2,"invoice_date":date,"agre":r}
                exec p.source in localspace
                mas_after = localspace['mas_aft']
                if len(mas_after) > 0:
                    calc_ids = map(int, p.calc_ids)
                    calc_seq = self.sort_calc_list(cr, uid, calc_ids)
                    calc_res = False
                    for c_id in calc_seq:
                        c = self.pool.get('inv.calc').browse(cr, uid, c_id, {})
                        #if c.var == 'count':
                        calc_localspace = {"self":self,"cr":cr,"uid":uid,"re":re,"obj_ids":mas_after,"count":len(mas_after),"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,"agre":r}
                        exec c.code in calc_localspace
                        pos = 0
                        for result in calc_localspace['res_list']:
                            if result:
                                calc_res = True
                                line = {"agr_id":agr_id,"user_id":uid,"amount":0}
                                # Analityc Entries, field Description
                                if c.description == 'empty':
                                    line['name'] = ' '
                                elif c.description == 'date':
                                    line['name'] = convert_date(self, current_date)
                                elif c.description == 'period':
                                    period = d_list.browse(cr, uid, date_id, {}).period
                                    line['name'] = period
                                elif c.description == 'field' and c.descr_field:
                                    line['name'] = ''
                                    rec_id = mas_after[pos]
                                    #for rec_id in mas_after:
                                    localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,'d_list':d_list,"agre":r}
                                    cr.execute("SELECT ttype, relation FROM ir_model_fields WHERE name='"+c.descr_field.name+"' and model='"+p.model_id.model+"'")
                                    query_res = cr.fetchone()
                                    if query_res[0] == 'many2one':
                                        field_value = "ids = self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+c.descr_field.name+".id\n"
                                        field_value += "field_val = self.pool.get('"+query_res[1]+"').name_get(cr, uid, [ids], {})"
                                    elif query_res[0] == 'one2many' or query_res[0] == 'many2many':
                                        field_value = "ids = map(int, self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+c.descr_field.name+")\n"
                                        field_value += "field_val = self.pool.get('"+query_res[1]+"').name_get(cr, uid, ids, {})"
                                    else:
                                        field_value = "field_val = self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+c.descr_field.name
                                    exec field_value in localspace
                                    if query_res[0] == 'many2one' or query_res[0] == 'one2many' or query_res[0] == 'many2many':
                                        res = ''
                                        for n in localspace['field_val']:
                                            if n != localspace['field_val'][0]:
                                                res += '; '
                                            if n[1][0]!='(' and n[1][-1]!=')':
                                                name = "'"+n[1]+"'"
                                            else:
                                                name = n[1]
                                            temp = 'name='+name
                                            exec temp in localspace
                                            if type(localspace['name'])==tuple:
                                                res += localspace['name'][0][1]
                                            else:
                                                res += localspace['name']
                                        line['name'] += res
                                    else:
                                        line['name'] += str(localspace['field_val'])
                                    #if rec_id!=mas_after[-1] and localspace['field_val']: line['name'] += '; '

                                elif c.description == 'expression':
                                    if (c.descr_express).find('rec_id') != -1:
                                        line['name'] = ''
                                        #for rec_id in mas_after:
                                        rec_id = mas_after[pos]
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"desc":'','convert_date':convert_date,'now':now,'d_list':d_list,'date_id':date_id,'pdate1':pdate1,'pdate2':pdate2,"calc_date":date,"agre":r}
                                        exec c.descr_express in localspace
                                        if type(localspace['desc'])==list:
                                            for l in localspace['desc']:
                                                line['name'] += l[1]
                                                if l != localspace['desc'][-1]: line['name'] += '; '
                                        else:
                                            line['name'] += localspace['desc']
                                        #if rec_id!=mas_after[-1]: line['name'] += '; '
                                    else:
                                        rec_id = mas_after[pos]
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"desc":'','convert_date':convert_date,'now':now,'d_list':d_list,'date_id':date_id,'pdate1':pdate1,'pdate2':pdate2,"calc_date":date,"agre":r}
                                        exec c.descr_express in localspace
                                        line['name'] = localspace['desc']
                                else:
                                    line['name'] = ' '
                                # Analityc Entries, field Quantity
                                if c.quantity == 'eqone':
                                    line['unit_amount'] = 1
                                elif c.quantity == 'count':
                                    line['unit_amount'] = len(mas_after)
                                elif c.quantity == 'expression' or c.quantity == 'field':
                                    if (c.quantity_express).find('rec_id') != -1:
                                        line['unit_amount'] = 0
                                        rec_id = mas_after[pos]
                                        #for rec_id in mas_after:
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,"agre":r,"quant":''}
                                        exec c.quantity_express in localspace
                                        if type(localspace['quant'])==list:
                                            for l in localspace['quant']:
                                                line['unit_amount'] += l[1]
                                        else:
                                            line['unit_amount'] = localspace['quant']
                                    else:
                                        rec_id = mas_after[pos]
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,'mas_after':mas_after,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,"agre":r,"quant":''}
                                        exec c.quantity_express in localspace
                                        line['unit_amount'] = localspace['quant']
                                else:
                                    line['unit_amount'] = 0
                                # Analityc Entries, field Analytic Account
                                line['account_id'] = r.analytic_account.id
                                # Analityc Entries, field Analytic journal
                                line['journal_id'] = r.service.journal_id.id
                                # Analityc Entries, field General account
                                #if r.partner_id.property_account_receivable:
                                line['general_account_id'] = c.product_id.product_tmpl_id.property_account_expense.id or c.product_id.categ_id.property_account_expense_categ.id
                                # Analityc Entries, field Product
                                line['product_id'] = c.product_id.id
                                # Analityc Entries, field Product UoM
                                line['product_uom_id'] = c.product_id.uom_id.id
                                # Analityc Entries, field Invoicing
                                line['to_invoice'] = c.invoicing_id.id
                                if r.service.purch_pricelist_id:
                                    ppl = r.service.purch_pricelist_id.id
                                    line['amount'] = -self.pool.get('product.pricelist').price_get(cr, uid, [ppl], line['product_id'], line['unit_amount'] or 1.0, r.partner_id.id)[ppl]
                                elif r.service.pricelist_id:
                                    spl = r.service.pricelist_id.id
                                    line['sale_amount'] = self.pool.get('product.pricelist').price_get(cr, uid, [spl], line['product_id'], line['unit_amount'] or 1.0, r.partner_id.id)[spl]
                                if r.service.invoicing == 'trigger':
                                    date_id = d_list.create(cr, uid, {'agreement_id':r.id,'status':'inv','date':date,'state':'filled'})
                                    line['invlog_id'] = date_id
                                    acc_lines.append(self.pool.get('account.analytic.line').create(cr, uid, line))
                                else:
                                    line['invlog_id'] = date_id
                                if date <= current_date and r.service.invoicing=='period':
                                    cr.rollback()
                                    acc_lines.append(self.pool.get('account.analytic.line').create(cr, uid, line))
                                    d_list.write(cr, uid, date_id, {'status':'inv'})
                                    cr.commit()
                            pos += 1
                    if not calc_res and date_id:
                        d_list.write(cr, uid, date_id, {'status':'error'})
                        agr.write(cr, uid, [agr_id], {'state':'error'})
                        req_body = '- Methodology: '+p.name+'\n- Calculation:\n'+c.code+'\n- Calculation result: False'
                        create_request(self, cr, uid, 'Calculation result is False', req_body, r.service.id)
        except Exception, e:
            cr.rollback()
            if date <= current_date and r.service.invoicing=='period':
                d_list.write(cr, uid, date_id, {'status':'error'})
                agr.write(cr, uid, [agr_id], {'state':'error'})
                cr.commit()
            tb_s = reduce(lambda x, y: x+y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
            create_request(self, cr, uid, 'Error in executed code', tb_s, r.service.id)
        return acc_lines

    _defaults = {
        'calc_base' : lambda *a: 'count',
        'state': lambda *a: 'open',
        'ref': lambda *a: 'res.partner',
    }

    _constraints = [
            (_get_source, '', ['source']),
        ]

method()

class rec_filter(osv.osv):
    _name = "inv.rec_filter"
    _rec_name = "filters"

    def _get_field_type(self, cr, uid, ids, field_name, arg=None, context={}):
        res={}
        for p in self.browse(cr, uid, ids, context):
            if p.field_id:
                temp = p.field_id.ttype
                res[p.id]='['+temp+']'
            else:
                res[p.id]='[integer]'
        return res

    def _get_filters(self, cr, uid, ids, field, arg=None, context={}):
        res = {}
        obj = self.pool.get('inv.rec_filter_cond')
        for p in self.browse(cr, uid, ids, context):
            temp = ''
            cond_ids = map(int, p.condition_id)
            if cond_ids == []:
                if p.field_id:
                    temp = p.field_id.name
                else:
                    temp = 'count'
            for r in obj.browse(cr, uid, cond_ids, context):
                if r.id == cond_ids[0]:
                    if len(cond_ids) > 1:
                        temp = '('+r.name+')'
                    else:
                        temp = r.name
                else:
                    temp += ' or ('+r.name+')'
            res[p.id] = temp
        return res

    _columns = {
        'filters': fields.function(_get_filters, method=True, string='Filters', type='char', size=128),
        'method_id': fields.many2one('inv.method', 'Methodology'),
        'field_id': fields.many2one('ir.model.fields', 'Field', domain="[('model_id', '=', parent.model_id),('ttype','!=','binary')]", states={'def':[('readonly',True)],'undef1':[('readonly',True)]}),
        #'condition_id': fields.one2many('inv.rec_filter_cond', 'rec_filter_id', 'Condition'),
        'field_type': fields.function(_get_field_type, method=True, string='Ttype', type='char'),
        'state': fields.selection([('def', 'Defined'),('undef1', 'Undefined'),('undef2', 'Undefined')], 'State', readonly=True),
        'var': fields.selection([('field', 'Field'),('count', 'Count')], 'Variable', states={'def':[('readonly',True)]}),
        'temp_field_id': fields.many2one('ir.model.fields', 'Temp Field', domain="[('model_id', '=', parent.model_id),('ttype','!=','selection'),('ttype','!=','binary')]"),
        'temp_var': fields.selection([('field', 'Field'),('count', 'Count')], 'Temp Variable'),
    }

    def change_field_type(self, cr, uid, ids, field, var):
        data = {}
        if not field:
            return {'value':{}}
        elif var == 'count':
            data['field_id'] = False
        else:
            data['field_type'] = '['+self.pool.get('ir.model.fields').browse(cr, uid, field).ttype+']'
            data['filters'] = self.pool.get('ir.model.fields').browse(cr, uid, field).name
        return {'value':data}

    def change_var(self, cr, uid, ids, field):
        data = {}
        if not field:
            return {'value':{}}
        elif field == 'count':
            data['field_type'] = '[integer]'
            data['field_id'] = False
            data['state'] = 'undef1'
        else:
            data['field_type'] = ''
            data['state'] = 'undef2'
        return {'value':data}

    def change_condition(self, cr, uid, ids, condition_id, field_id, var, relation):
        data = {}
        temp = ''
        obj = self.pool.get('inv.rec_filter_cond')
        for r in condition_id:
            if r[2] != {}:
                if r == condition_id[0]:
                    if len(condition_id) > 1:
                        temp = '('+r[2]['name']+')'
                    else:
                        temp = r[2]['name']
                else:
                    temp += ' or ('+r[2]['name']+')'
        data['filters'] = temp
        if relation:
            data['state'] = 'def'
        else:
            data['state'] = 'def'
        data['temp_field_id'] = field_id
        data['temp_var'] = var
        return {'value':data}

    def name_get(self, cr, user, ids, context={}):
        if not len(ids):
            return []
        res = []
        for r in self.read(cr, user, ids, ['method_id', 'field_id', 'calc_id']):
            if r['field_id']:
                if r['method_id']:
                    name = str(r['method_id'][1])
                    name +=', '
                else:
                    name = str(r['calc_id'][1])
                    name +=', '
                name += str(r['field_id'][1])
                res.append((r['id'], name))
        return res

    def create(self, cr, uid, vals, context={}):
        if not context:
            context={}
        vals=vals.copy()
        vals['state'] = 'def'
        vals['var'] = vals['temp_var']
        vals['field_id'] = vals['temp_field_id']
        c = context.copy()
        c['novalidate'] = True
        result = super(rec_filter, self).create(cr, uid, vals, c)
        return result

    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context={}
        for r in self.browse(cr, uid, ids, {}):
            vals=vals.copy()
            vals['state'] = 'def'
        return super(rec_filter, self).write(cr, uid, ids, vals, context=context)

    def unlink(self, cr, uid, ids, context):
        conditions = map(int, self.browse(cr, uid, ids[0], {}).condition_id)
        self.pool.get('inv.rec_filter_cond').unlink(cr, uid, conditions, context)
        osv.osv.unlink(self, cr, uid, ids, context)
        return True

    _defaults = {
        'var' : lambda *a: 'field',
        'state' : lambda *a: 'undef2',
        'field_type' : lambda *a: '[integer]',
    }

rec_filter()

class calc_filter(osv.osv):
    _name = 'inv.calc_filter'
    _inherit = 'inv.rec_filter'

    def _get_var(self, cr, uid, context={}):
        if 'calc_base' in context.keys():
            return context['calc_base']
        return 'count'

    _columns = {
        #'calc_id': fields.many2one('inv.calc', 'Calculation'),
        #'condition_id': fields.one2many('inv.rec_filter_cond', 'calc_filter_id', 'Condition'),
    }

    def create(self, cr, uid, vals, context={}):
        if not context:
            context={}
        vals=vals.copy()
        vals['state'] = 'def'
        vals['var'] = vals['temp_var']
        vals['field_id'] = vals['temp_field_id']
        c = context.copy()
        c['novalidate'] = True
        result = super(calc_filter, self).create(cr, uid, vals, c)
        return result

    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context={}
        for r in self.browse(cr, uid, ids, {}):
            vals=vals.copy()
            vals['state'] = 'def'
        return super(calc_filter, self).write(cr, uid, ids, vals, context=context)

    _defaults = {
        'var' : _get_var,
        'state' : lambda *a: 'undef1',
    }

calc_filter()

class rec_filter_cond(osv.osv):
    _name = "inv.rec_filter_cond"
    _rec_name = "rec_filter_id"

#    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context={}, toolbar=False):
#        result = super(osv.osv, self).fields_view_get(cr, uid, view_id,view_type,context)
#        return result

    def _change_state(self, cr, uid, ids, field, arg=None, context={}):
        res = {}
        for p in self.browse(cr, uid, ids, context):
            if p:
                if p.rec_filter_id:
                    filter_id = p.rec_filter_id
                elif p.calc_filter_id:
                    filter_id = p.calc_filter_id
                ctype = filter_id.field_type
                value = p.cond_type.value
                if ctype!='[many2one]' and ctype!='[one2many]' and ctype!='[many2many]' and ctype!='[boolean]' \
                        and ctype!='[char]' and ctype!='[selection]':
                    if value=='between' or value=='not between':
                        res[p.id] = ctype + '|2|'
                    else:
                        res[p.id] = ctype + '|1|'
                else:
                    res[p.id] = ctype
        return res

    def _get_name(self, cr, uid, ids, field, arg=None, context={}):
        res = {}
        for r in self.browse(cr, uid, ids, context):
            if r.rec_filter_id:
                filter_id = r.rec_filter_id
                model = 'inv.rec_filter'
            elif r.calc_filter_id:
                filter_id = r.calc_filter_id
                model = 'inv.calc_filter'
            if filter_id.var != 'count':
                field = filter_id.field_id.name
                filter_field_type = self.pool.get(model).browse(cr, uid, filter_id.id, {}).field_type
            else:
                field = 'count'
                filter_field_type = '[integer]'
            if r.cond_type.value == 'equal to':
                operator = ' == '
            elif r.cond_type.value == 'not equal to':
                operator = ' != '
            elif r.cond_type.value == 'greater than':
                operator = ' > '
            elif r.cond_type.value == 'less than':
                operator = ' < '
            elif r.cond_type.value == 'greater than or equal to':
                operator = ' >= '
            elif r.cond_type.value == 'less than or equal to':
                operator = ' <= '
            elif r.cond_type.value == 'regexp':
                operator = ' match '
            else:
                operator = ''
                
            if r.cond_type.value!='between' and r.cond_type.value!='not between':
                if filter_field_type == '[char]' or filter_field_type == '[selection]':
                    res[r.id] = field + operator + "'"+r.value1_char+"'" or ''
                elif filter_field_type == '[boolean]':
                    res[r.id] = field + operator + str(r.value1_bool) or ''
                elif filter_field_type == '[integer]':
                    res[r.id] = field + operator + str(r.value1_int) or ''
                elif filter_field_type == '[float]':
                    res[r.id] = field + operator + str(r.value1_float) or ''
                elif filter_field_type == '[date]':
                    res[r.id] = field + operator + str(r.value1_date) or ''
                elif filter_field_type == '[datetime]':
                    res[r.id] = field + operator + str(r.value1_datetime) or ''
            elif r.cond_type.value=='between':
                if filter_field_type == '[integer]':
                    res[r.id] = '(' + field + ' >= ' + str(r.value1_int)+')'
                    if r.value2_int != None:
                        res[r.id] += ' and ('+field+ ' <= ' + str(r.value2_int)+')' or ''
                elif filter_field_type == '[float]':
                    res[r.id] = '(' + field + ' >= ' + str(r.value1_float)+')'
                    if r.value2_float != None:
                        res[r.id] += ' and ('+field+ ' <= ' + str(r.value2_float)+')' or ''
                elif filter_field_type == '[date]':
                    res[r.id] = '(' + field + ' >= ' + str(r.value1_date)+')'
                    if r.value2_date:
                        res[r.id] += ' and ('+field+ ' <= ' + str(r.value2_date)+')' or ''
                elif filter_field_type == '[datetime]':
                    res[r.id] += '(' + field + ' >= ' + str(r.value1_datetime)+')'
                    if r.value2_datetime:
                        res[r.id] += ' and ('+field+ ' <= ' + str(r.value2_datetime)+')' or ''
            elif r.cond_type.value=='not between':
                if filter_field_type == '[integer]':
                    res[r.id] = '(' + field + ' <= ' + str(r.value1_int)+')' or ''
                    if r.value2_int != None:
                        res[r.id] += ' and ('+field+ ' >= ' + str(r.value2_int)+')' or ''
                elif filter_field_type == '[float]':
                    res[r.id] = '(' + field + ' <= ' + str(r.value1_float)+')'
                    if r.value2_float != None:
                        res[r.id] += ' and ('+field+ ' >= ' + str(r.value2_float)+')' or ''
                elif filter_field_type == '[date]':
                    res[r.id] = '(' + field + ' <= \'' + str(r.value1_date)+'\')'
                    if r.value2_date:
                        res[r.id] += ' and ('+field+ ' >= \'' + str(r.value2_date)+'\')' or ''
                elif filter_field_type == '[datetime]':
                    res[r.id] = '(' + field + ' <= \'' + str(r.value1_datetime)+'\')'
                    if r.value2_datetime:
                        res[r.id] += ' and ('+field+ ' >= \'' + str(r.value2_datetime)+'\')' or ''
    
            if r.cond_type.value=='in' or r.cond_type.value=='not in':
                res[r.id] = field + ' ' + r.cond_type.value
                if r.cond_value and r.cond_value != None:
                    res[r.id] += ' ['+r.cond_value+']' or ''
        
        return res

    def _get_code(self, cr, uid, ids, field, arg=None, context={}):
        res = {}
        comment = {}
        for r in self.browse(cr, uid, ids, context):
            if r.rec_filter_id:
                filter_id = r.rec_filter_id
                filter_model = 'inv.rec_filter'
            elif r.calc_filter_id:
                filter_id = r.calc_filter_id
                filter_model = 'inv.calc_filter'
            rec_filter = self.pool.get(filter_model).browse(cr, uid, filter_id.id, {})
            if rec_filter.var == 'count':
                filter_field_type = '[integer]'
            else:
                filter_field_type = rec_filter.field_type
            if r.cond_type.value == 'equal to':
                operator = ' == '
            elif r.cond_type.value == 'not equal to':
                operator = ' != '
            elif r.cond_type.value == 'greater than':
                operator = ' > '
            elif r.cond_type.value == 'less than':
                operator = ' < '
            elif r.cond_type.value == 'greater than or equal to':
                operator = ' >= '
            elif r.cond_type.value == 'less than or equal to':
                operator = ' <= '
            elif r.cond_type.value == 'regexp':
                operator = 'match'
            else:
                operator = ''

            if rec_filter.var == 'count':
                if r.id != ids[0]:
                    res[r.id] = 'if '+r.name+' :\n'
                    res[r.id] += '\tresult &= True\nelse:\n\tresult &= False\n'
                else:
                    res[r.id] = 'result = True\n'
                    res[r.id] += 'if '+r.name+' :\n'
                    res[r.id] += '\tresult &= True\nelse:\n\tresult &= False\n'
                continue

            if filter_id.field_id.ttype == 'many2one':
                if filter_id.filters != comment:
                    comment = filter_id.filters
                    field = "#"+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+"\n\tif cur_object."+filter_id.field_id.name+".id "+r.cond_type.value+" ["+r.cond_value+"]:\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n"
                else:
                    field = "\tif cur_object."+filter_id.field_id.name+".id "+r.cond_type.value+" ["+r.cond_value+"]:\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n"
                res[r.id] = field
            elif filter_id.field_id.ttype == 'many2many' or filter_id.field_id.ttype == 'one2many':
                if filter_id.filters != comment:
                    comment = filter_id.filters
                    field = "#"+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters
                    if r.cond_type.value == 'in':
                        field += "\n\ttemp = 0"
                        field += "\n\tfor x in ["+r.cond_value+"]:\n\t\tif x "+r.cond_type.value+" map(int, cur_object."+filter_id.field_id.name+"):\n\t\t\ttemp += 1\n\tresult &= bool(temp)\n"
                    else:
                        field += "\n\tfor x in ["+r.cond_value+"]:\n\t\tif x "+r.cond_type.value+" map(int, cur_object."+filter_id.field_id.name+"):\n\t\t\tresult &= True\n\t\telse:\n\t\t\tresult &= False\n"
                else:
                    field = "\tfor x in ["+r.cond_value+"]:\n\t\tif x "+r.cond_type.value+" map(int, cur_object."+filter_id.field_id.name+"):\n\t\t\tresult &= True\n\t\telse:\n\t\t\tresult &= False\n"
                res[r.id] = field
            else:
                field = 'cur_object.'+filter_id.field_id.name
                
            if r.cond_type.value!='between' and r.cond_type.value!='not between':
                if filter_field_type == '[char]' and operator == 'match':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif re." + operator + "('"+r.value1_char+"', "+field+") != None:\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif re." + operator + "('"+r.value1_char+"', "+field+") != None:\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                elif filter_field_type == '[char]' or filter_field_type == '[selection]':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif " + field + operator + "'"+r.value1_char+"':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif " + field + operator + "'"+r.value1_char+"':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                elif filter_field_type == '[boolean]':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif " + field + operator + str(r.value1_bool)+":\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif " + field + operator + str(r.value1_bool)+":\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                elif filter_field_type == '[integer]':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif " + field + operator + str(r.value1_int)+":\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif " + field + operator + str(r.value1_int)+":\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                elif filter_field_type == '[float]':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif " + field + operator + str(r.value1_float)+":\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif " + field + operator + str(r.value1_float)+":\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                elif filter_field_type == '[date]':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif " + field + operator + '\'' + str(r.value1_date)+"\':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif " + field + operator + '\'' + str(r.value1_date)+"\':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                elif filter_field_type == '[datetime]':
                    if comment != filter_id.filters:
                        comment = filter_id.filters
                        res[r.id] = "#"+len(comment)*'-'+"#\n# "+comment+"\n\tif " + field + operator + '\'' + str(r.value1_datetime)+"\':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
                    else:
                        res[r.id] = "\tif " + field + operator + '\'' + str(r.value1_datetime)+"\':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n" or ''
            elif r.cond_type.value=='between':
                if filter_field_type == '[integer]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' >= ' + str(r.value1_int)+')'
                    if r.value2_int != None:
                        res[r.id] += ' and ('+field+ ' <= ' + str(r.value2_int)+')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
                elif filter_field_type == '[float]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' >= ' + str(r.value1_float)+')'
                    if r.value2_float != None:
                        res[r.id] += ' and ('+field+ ' <= ' + str(r.value2_float)+')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
                elif filter_field_type == '[date]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' >= \'' + str(r.value1_date)+'\')'
                    if r.value2_date:
                        res[r.id] += ' and ('+field+ ' <= \'' + str(r.value2_date)+'\'):\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
                elif filter_field_type == '[datetime]':
                    res[r.id] += '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' >= \'' + str(r.value1_datetime)+'\')'
                    if r.value2_datetime:
                        res[r.id] += ' and ('+field+ ' <= \'' + str(r.value2_datetime)+'\')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
            elif r.cond_type.value=='not between':
                if filter_field_type == '[integer]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' <= ' + str(r.value1_int)+')'
                    if r.value2_int != None:
                        res[r.id] += ' and ('+field+ ' >= ' + str(r.value2_int)+')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
                elif filter_field_type == '[float]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' <= ' + str(r.value1_float)+')'
                    if r.value2_float != None:
                        res[r.id] += ' and ('+field+ ' >= ' + str(r.value2_float)+')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
                elif filter_field_type == '[date]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' <= \'' + str(r.value1_date)+'\')'
                    if r.value2_date:
                        res[r.id] += ' and ('+field+ ' >= \'' + str(r.value2_date)+'\')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
                elif filter_field_type == '[datetime]':
                    res[r.id] = '#'+len(filter_id.filters)*'-'+"#\n# "+filter_id.filters+'\n\tif (' + field + ' <= \'' + str(r.value1_datetime)+'\')'
                    if r.value2_datetime:
                        res[r.id] += ' and ('+field+ ' >= \'' + str(r.value2_datetime)+'\')'+':\n\t\tresult &= True\n\telse:\n\t\tresult &= False\n' or ''
        return res

    _columns = {
        'name': fields.function(_get_name, method=True, string='Filter coditions', type='char', size=128),
        'code': fields.function(_get_code, method=True, string='Code', type='char', size=128),
        #'rec_filter_id': fields.many2one('inv.rec_filter', 'Filter'),
        'cond_type': fields.many2one('inv.rec_type', 'Condition type', domain="[('type', '=', parent.field_type)]", required=True),
        'state': fields.function(_change_state, method=True, string='State', type='char', size=128),
        #'cond_value': fields.one2many('inv.cond_value', 'rec_filter_cond_id', 'Condition value', states={'[many2many]':[('readonly',False)],'[many2one]':[('readonly',False)],'[one2many]':[('readonly',False)]},readonly=True),
        'cond_value': fields.char('Condition value', size=128, states={'[many2many]':[('readonly',False),('required',True)],'[many2one]':[('readonly',False),('required',True)],'[one2many]':[('readonly',False),('required',True)]},readonly=True),
        'value1_char': fields.char('Char', size=256, states={'[char]':[('readonly',False),('required',True)],'[selection]':[('readonly',False),('required',True)]}, readonly=True),
        'value1_bool': fields.boolean('Boolean', states={'[boolean]':[('readonly',False),('required',True)]}, readonly=True),
        'value1_int': fields.integer('Integer1', states={'[integer]|1|':[('readonly',False),('required',True)],'[integer]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value2_int': fields.integer('Integer2', states={'[integer]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value1_float': fields.float('Float1', states={'[float]|1|':[('readonly',False)],'[float]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value2_float': fields.float('Float2', states={'[float]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value1_date': fields.date('Date1', states={'[date]|1|':[('readonly',False),('required',True)],'[date]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value2_date': fields.date('Date2', states={'[date]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value1_datetime': fields.date('DateTime1', states={'[datetime]|1|':[('readonly',False),('required',True)],'[datetime]|2|':[('readonly',False),('required',True)]}, readonly=True),
        'value2_datetime': fields.date('DateTime2', states={'[datetime]|2|':[('readonly',False),('required',True)]}, readonly=True),
    }

    def on_change_state(self, cr, uid, ids, field, field_type, field_id, value1_char, value1_bool, \
            value1_int, value2_int, value1_float, value2_float, value1_date, value2_date, value1_datetime, value2_datetime, cond_value):
        data = _change_state(self, cr, uid, ids, field, field_type, field_id, value1_char, value1_bool, \
            value1_int, value2_int, value1_float, value2_float, value1_date, value2_date, value1_datetime, value2_datetime, cond_value)
        return {'value':data}

rec_filter_cond()

class service(osv.osv):
    _name = "inv.service"
    _rec_name = "name"

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'method_ids': fields.many2many('inv.method', 'inv_serv_meth_rel', 'service_id', 'method_id', 'Methodologies'),
        'journal_id': fields.many2one('account.analytic.journal', 'Analytic Journal', required=True),
        'analytic_account_branch': fields.many2one('account.analytic.account', 'Analytic account branch', required=True),
        'pricelist_id': fields.many2one('product.pricelist', 'Sale Pricelist', domain="[('type','=','sale')]"),
        'purch_pricelist_id': fields.many2one('product.pricelist', 'Purchase Pricelist', domain="[('type','=','purchase')]"),
        'invoicing': fields.selection([('trigger','Trigger'),('period','Period')], 'Invoicing based on'),
        'interval_unit': fields.selection([('days','Day(s)'),('weeks','Week(s)'),('months','Month(s)'),('years','Year(s)')], 'Interval Unit'),
        'int_unit_number': fields.integer('Invoice Every'),
        'cron_offset': fields.integer('Cron offset(hours)'),
        'req_users': fields.many2many('res.users', 'inv_req_users_rel', 'inv_id', 'tgroup_id', 'Work Team'),
    }

    def _test_int_unit_number(self, cr, uid, ids):
        for x in self.browse(cr, uid, ids, {}):
            if x.int_unit_number < 1:
                raise osv.except_osv(_('Input data error!'), _('"Invoice Every" field cannot be less than 1!'))
                return False
        return True

    _defaults = {
        'invoicing' : lambda *a: 'period',
        'interval_unit' : lambda *a: 'months',
        'int_unit_number' : lambda *a: 1,
    }

    _constraints = [
            (_test_int_unit_number, '', ['int_unit_number']),
        ]

service()

class calc(osv.osv):
    _name = "inv.calc"
    _rec_name = "method_id"

    def _get_model(self, cr, uid, context={}):
        if 'model_id' in context.keys():
            return context['model_id']
        return ''

    def _get_invoice_factor(self, cr, uid, context):
        obj = self.pool.get('hr_timesheet_invoice.factor')
        ids = obj.search(cr, uid, [])
        for r in obj.browse(cr, uid, ids, {}):
            if r.factor == 0.0:
                return r.id
        return False

    _columns = {
        'method_id': fields.many2one('inv.method', 'Methodology', ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product', domain="[('type','=',product_type)]", required=True),
        'invoicing_id': fields.many2one('hr_timesheet_invoice.factor', 'Invoicing', required=True),
        'sequence': fields.integer('Calculation Sequence'),
        'calculations': fields.one2many('inv.calc_filter', 'calc_id', 'Calculation lines'),
        'description': fields.many2one('inv.description', 'Description', domain="[('id','=', False)]", ondelete="cascade", required=True),
        'quantity': fields.many2one('inv.quantity', 'Quantity',  domain="[('id','=', False)]", ondelete='cascade', required=True),
        'descr_express': fields.text('Expression'),
        'descr_field': fields.many2one('ir.model.fields', 'Value of', domain="[('model_id','=', parent.model_id)]"),
        'quantity_express': fields.text('Expression'),
        'quantity_field': fields.many2one('ir.model.fields', 'Value of', domain="[('model_id','=', parent.model_id)]"),
        'description': fields.selection([('empty', 'Empty'),('date', 'Calculation Date'),('period', 'Calculation Period'),('field','Field'),('expression','Expression')],'Set description', required=True),
        'quantity': fields.selection([('eqone','One'),('count','Total Count'),('field','Field'),('expression','Expression')], 'Set quantity', required=True),
        'product_type': fields.selection([('product','Stockable Product'),('consu', 'Consumable'),('service','Service')], 'Product Type', required=True),
        'code': fields.text('Code'),
        'manual': fields.boolean('Manual', select=False),
        'model_id': fields.many2one('ir.model', 'Model', domain="[('id','=', parent.model_id)]", required=True),
    }

    _defaults = {
        'sequence' : lambda *a: 99,
        'invoicing_id': _get_invoice_factor,
        'description': lambda *a: 'date',
        'quantity': lambda *a: 'eqone',
        'product_type': lambda *a: 'service',
        'model_id': _get_model,
    }

    _order = 'sequence'

    def _field_value(self, cr, uid, value_id, method_id, res_var):
        method = self.pool.get('inv.method')
        p = method.browse(cr, uid, method_id, {})
        value = self.pool.get('ir.model.fields').browse(cr, uid, value_id, {}).name
        if value_id:
            cr.execute("SELECT ttype, relation FROM ir_model_fields WHERE name='"+value+"' and model='"+p.model_id.model+"'")
            query_res = cr.fetchone()
            if query_res[0] == 'many2one':
                field_value = "ids = self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+value+".id\n"
                field_value += res_var+" = self.pool.get('"+query_res[1]+"').name_get(cr, uid, [ids], {})"
            elif query_res[0] == 'one2many' or query_res[0] == 'many2many':
                field_value = "ids = map(int, self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+value+")\n"
                field_value += res_var+" = self.pool.get('"+query_res[1]+"').name_get(cr, uid, ids, {})"
            else:
                field_value = res_var+" = self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+value

        return field_value

    def change_descr(self, cr, uid, ids, field, value_id, method_id):
        data = {}
        if not field:
            return {'value':{}}
        else:
            if field=='empty':
                data['descr_express'] = ''
                data['descr_field'] = False
            elif field=='expression':
                data['descr_field'] = False
            elif field=='field' and value_id:
                data['descr_express'] = self._field_value(cr, uid, value_id, method_id, 'desc')
            elif field=='field':
                data['descr_express'] = ''
            elif field=='date':
                data['descr_field'] = False
                data['descr_express'] = "desc = convert_date(self, now().strftime('%Y-%m-%d'))"
            elif field=='period':
                data['descr_field'] = False
                data['descr_express'] = "desc = d_list.browse(cr, uid, date_id, {}).period"
        return {'value':data}

    def change_quant(self, cr, uid, ids, field, value_id, method_id):
        data = {}
        if not field:
            return {'value':{}}
        else:
            if field=='eqone':
                data['quantity_express'] = 'quant = 1'
                data['quantity_field'] = False
            elif field=='count':
                data['quantity_express'] = 'quant = len(mas_after)'
                data['quantity_field'] = False
            elif field=='expression':
                data['quantity_field'] = False
            elif field=='field' and value_id:
                data['quantity_express'] = self._field_value(cr, uid, value_id, method_id, 'quant')
        return {'value':data}

    def _test_fields(self, cr, uid, ids):
        result = ''
        cur_id = "".join(map(str, ids))
        obj = self.browse(cr, uid, int(cur_id), {})
        if (obj.description == 'field' and not obj.descr_field) or (obj.quantity == 'field' and not obj.quantity_field):
            raise osv.except_osv(_('No field value!'), _('Field "Value of" not defined !'))
            return False
        return True

    def _get_code(self, cr, uid, ids):
        result = ''
        cur_id = "".join(map(str, ids))
        obj = self.browse(cr, uid, int(cur_id), {})
        if not obj.method_id or obj.manual:
            return True
        calc_filter_obj = self.pool.get('inv.calc_filter')
        cond_obj = self.pool.get('inv.rec_filter_cond')
        calc_filter_ids = calc_filter_obj.search(cr, uid, [('calc_id','=',obj.id)])
        model = obj.method_id.model_id.model
        result += 'obj = self.pool.get(\''+model+'\')\nres_list = []\n'
        result += "for cur_object in obj.browse(cr, uid, obj_ids, {}):\n\tresult = True\n"
        for s in calc_filter_obj.browse(cr, uid, calc_filter_ids, {}):
            if s.var == 'count': continue
            for c in map(int, s.condition_id):
                result += cond_obj.browse(cr, uid, c, {}).code
        result += '\n'
        for s in calc_filter_obj.browse(cr, uid, calc_filter_ids, {}):
            if s.var == 'field': continue
            for c in map(int, s.condition_id):
                result += cond_obj.browse(cr, uid, c, {}).code
        result += "\tres_list.append(result)\n"
        cr.execute("""
                UPDATE inv_calc
                SET code = %s
                WHERE id in (%s)
               """, (result, ','.join(map(str,ids))))
        return True

    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context={}
        vals=vals.copy()
        if 'description' in vals and (vals['description']=='empty' or vals['description']=='date' or vals['description']=='period'):
            vals['descr_field'] = False
        elif 'description' in vals and vals['description']=='expression':
            vals['descr_field'] = False
        if 'quantity' in vals and (vals['quantity']=='one' or vals['quantity']=='count'):
            vals['quantity_field'] = False
        elif 'quantity' in vals and vals['quantity']=='expression':
            vals['quantity_field'] = False
        return super(calc, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context={}):
        if not context:
            context={}
        maxseq = 1
        ids = self.search(cr, uid, [])
        if ids == []:
            vals=vals.copy()
            vals['sequence'] = maxseq
        for r in self.browse(cr, uid, ids, {}):
            if r.sequence >= maxseq:
                maxseq = r.sequence
                vals=vals.copy()
                vals['sequence'] = maxseq + 1
        c = context.copy()
        c['novalidate'] = True
        result = super(calc, self).create(cr, uid, vals, c)
        return result

    def calc_field_type(self, cr, uid, ids, field1, field2):
        data = {}
        if field2 == 'count':
            data['field_type'] = '[integer]'
            data['field'] = False
            return {'value':data}
        elif not field1:
            data['field_type'] = ''
            return {'value':data}
        else:
            data['field_type'] = '['+self.pool.get('ir.model.fields').browse(cr, uid, field1).ttype+']'
        return {'value':data}

    _constraints = [
            (_get_code, '', ['code']),
        (_test_fields, '', ['descr_field', 'quantity_field']),
        ]

calc()

class agreement(osv.osv):
    _name = "inv.agreement"
    _rec_name = "name"

    def _number_of_calls(self, cr, uid, ids, field, arg=None, context={}):
        res = {}
        remaining = 0

        for r in self.browse(cr, uid, ids, context):
            if r.service.invoicing == 'trigger':
                res[r.id] = -1
                continue
            if r.signed_date < now().strftime('%Y-%m-%d'):
                signed_date = now().strftime('%Y-%m-%d')
            else:
                signed_date = r.signed_date
            if r.state != 'done' and r.service.invoicing == 'period':
                if r.cron_id:
                    cron_ids = r.cron_id.id
                    remaining = self.pool.get('ir.cron').browse(cr, uid, cron_ids, {}).numbercall
                elif r.cur_effect_date and signed_date and r.service.interval_unit and r.service.int_unit_number:
                    period = DateTime.strptime(r.cur_effect_date, '%Y-%m-%d') - DateTime.strptime(signed_date , '%Y-%m-%d')
                    if r.service.interval_unit == 'days':
                        remaining = int(period.day / r.service.int_unit_number)
                    elif r.service.interval_unit == 'weeks':
                        remaining = int(period.day / 7.0 / r.service.int_unit_number)
                    elif r.service.interval_unit == 'months':
                        remaining = int(round(period.day / 30.0 / r.service.int_unit_number))
                    elif r.service.interval_unit == 'years':
                        remaining = int(period.day / 365.0 / r.service.int_unit_number)
                        if r.payment == 'start': 
                            remaining += 1
            res[r.id] = remaining
        return res

    def _number_of_uninv_entries(self, cr, uid, ids, field, arg=None, context={}):
        res = {}

        lines_obj = self.pool.get('account.analytic.line')
        for r in self.browse(cr, uid, ids, context):
            count = len(lines_obj.search(cr, uid, [('agr_id', '=', r.id),('invoice_id','=',False)], context=context))
            if arg:
                statement = "if count"
                for a in arg:
                    if a[1]=='=': a[1]='=='
                    statement += a[1]+str(a[2])
                    if a!=arg[-1]:
                        statement += " and count"
                statement+=':\n\tres = count'
                localspace = {"count":count,'res':False}
                exec statement in localspace
                if localspace['res']:
                    res[r.id] = localspace['res']
            else:    
                res[r.id] = count
        return res

    _columns = {
        'name': fields.char('Description', size=64, states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'number': fields.char('Agreement Number', size=32, help="Leave empty to get the number assigned by a sequence.", states={'running':[('readonly',True)],'done':[('readonly',True)]}, required=False),
        'partner_id': fields.many2one('res.partner', 'Partner', states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'state': fields.selection([('draft','Draft'),('running','Running'), ('done','Done'), ('error', 'Error')], 'State', required=True),
        'signed_date': fields.date('Start Date', help="Date when agreement was signed.", states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'partner_signed_date': fields.date('Signed on', help="Date when agreement was signed.", states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'init_effect_date': fields.date('Period End Date', readonly=True),
        'period_unit_number': fields.integer('Period', help="Period time to prolong the next agreement", states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'period_unit': fields.selection([('days','Day(s)'),('weeks','Week(s)'),('months','Month(s)'),('years','Year(s)')], 'Unit', states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'cur_effect_date': fields.date('Expire Date', help="Resembles the current validity period.", states={'running':[('readonly',True)], 'done':[('readonly',True)]}),
        'analytic_account': fields.many2one('account.analytic.account', 'Analytic Account', help='Leave empty to let the system create an account in a branch defined by the Service.', states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'service': fields.many2one('inv.service', 'Service', states={'running':[('readonly',True)],'done':[('readonly',True)]}, required=True),
        'analytic_entries': fields.one2many('account.analytic.line', 'agr_id', 'Entries', readonly=True),
        'date_list': fields.one2many('inv.date_list', 'agreement_id', 'Invoice Log',states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'prolong': fields.selection([('recurrs','Prolong'),('unlimited','Unlimited Term'),('fixed','Fixed Term')], 'Prolongation', help="Sets whether to prolong the agreement for the next term or not.", states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'recurr_unit_number': fields.integer('Interval', help="Time before current validity expires to prolong the agreement for the next term.", states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'recurr_unit': fields.selection([('days','Day(s)'),('weeks','Week(s)'),('months','Month(s)'),('years','Year(s)')], 'Unit', states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'payment': fields.selection([('start','In advance'),('end','After')], 'Payment', states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'cron_id': fields.many2one('ir.cron', 'Scheduler'),
        'cron_nextdate': fields.many2one('ir.cron', 'Set next date'),
        'repeat' : fields.boolean('Repeat missed', states={'running':[('readonly',True)],'done':[('readonly',True)]}),
        'active' : fields.boolean('Active', states={'running':[('readonly',True)]}),
        'calls': fields.function(_number_of_calls, method=True, string='Number of invoices', help="Number of invoices to be written.", type='integer'),
        'uninv_entries_count': fields.function(_number_of_uninv_entries, method=True, string='Uninvoiced analytic entries', help="Number of uninvoiced analytic entries.", type='integer'),
    }

    def _test_recurr_unit_number(self, cr, uid, ids):
        for x in self.browse(cr, uid, ids, {}):
            if x.recurr_unit_number < 1:
                raise osv.except_osv(_('Input data error!'), _('"Number of Units" field cannot be less than 1 !'))
                return False
        return True

    _defaults = {
        'state' : lambda *a: 'draft',
        'payment' : lambda *a: 'end',
        'recurr_unit_number' : lambda *a: 1,
        'recurr_unit' : lambda *a: 'months',
        'prolong' : lambda *a: 'recurrs',
        'repeat': lambda *a: True,
        'active': lambda *a: True,
        'signed_date' : lambda *a: now().strftime('%Y-%m-%d'),
        'period_unit_number': lambda *a: 1,
        'period_unit': lambda *a: 'months',
    }

    _constraints = [
            (_test_recurr_unit_number, '', ['recurr_unit_number']),
        ]

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for agr in self.browse(cr, uid, ids):
            if agr.name and agr.number:
                res.append((agr.id, agr.number + '/' + agr.name))
            elif not agr.name and agr.number:
                res.append((agr.id, agr.number))
            elif not agr.number and agr.name:
                res.append((agr.id, agr.name))
            else:
                res.append((agr.id, agr.partner_id.name))
        return res

    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}

        domain = []
        for a in args:
            if 'uninv_entries_count' in a:
                domain.append(a)
        limit1=None
        ids = super(agreement,self).search(cr, uid, [], offset, limit1, order, context=context, count=count)
        if domain:
            uninv_entries_count = self._number_of_uninv_entries(cr, uid, ids, 'uninv_entries_count', domain, context=context)
            res_ids = []
            for rec in uninv_entries_count:
                res_ids.append(rec)
            args.append(['id','in',res_ids])
        return super(agreement,self).search(cr, uid, args, offset, limit, order, context=context, count=count)

    def _set_next_date(self, cr, uid, id, context={}):
        obj = self.browse(cr, uid, id, {})
        self.pool.get('ir.cron').unlink(cr, uid, [obj.cron_nextdate.id])
        if obj.payment == 'start' and obj.service.invoicing != 'trigger':
            if obj.signed_date < now().strftime('%Y-%m-%d'):
                signed_date = now().strftime('%Y-%m-%d')
            else:
                signed_date = obj.signed_date
            temp = DateTime.strptime(signed_date, '%Y-%m-%d')
            if temp.day != 1 and obj.cron_id:
                if obj.service.interval_unit == 'days':
                    temp = temp + DateTime.RelativeDateTime(days=1)
                elif obj.service.interval_unit == 'weeks':
                    temp = temp + DateTime.RelativeDateTime(weekday=(DateTime.Monday,0), days=7)
                elif obj.service.interval_unit == 'months':
                    temp = temp + DateTime.RelativeDateTime(months=1, days=-temp.day+1)
                elif obj.service.interval_unit == 'years':
                    temp = temp + DateTime.RelativeDateTime(months=12-temp.month+1, days=-temp.day+1)
                temp += DateTime.RelativeDateTime(hours=obj.service.cron_offset)
            self.pool.get('ir.cron').write(cr, uid, obj.cron_id.id, {'nextcall':temp.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def _make_invoice_log(self, cr, uid, row, start_date, numbercall, increment_size, context={}):
        d_list = self.pool.get('inv.date_list')
        start_numbercall = numbercall
        while(numbercall > 0):
            date = start_date.strftime('%Y-%m-%d')
###########################################################
            if row.payment == 'end':
                if row.service.interval_unit == 'days':
                    date12 = DateTime.strptime(date, '%Y-%m-%d')
                    date1 = date12 - DateTime.RelativeDateTime(days=row.service.int_unit_number)
                    if date1.strftime('%Y-%m-%d') < row.signed_date:
                        date1 = DateTime.strptime(row.signed_date, '%Y-%m-%d')
                    date2 = date12 - DateTime.RelativeDateTime(days=1)
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    if row.service.int_unit_number > 1:
                        period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
                    else:
                        period = convert_date(self, date1.strftime('%Y-%m-%d'))
                elif row.service.interval_unit == 'weeks':
                    date12 = DateTime.strptime(date, '%Y-%m-%d')
                    date1 = date12 - DateTime.RelativeDateTime(days=row.service.int_unit_number*7)
                    if date1.strftime('%Y-%m-%d') < row.signed_date:
                        date1 = DateTime.strptime(row.signed_date, '%Y-%m-%d')
                    date2 = date12 - DateTime.RelativeDateTime(days=1)
                    if date2.strftime('%Y-%m-%d') > row.cur_effect_date or date2.strftime('%Y-%m-%d') > row.init_effect_date:
                        date2 = DateTime.strptime(row.cur_effect_date or row.init_effect_date, '%Y-%m-%d')
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    period = convert_date(self, date1.strftime('%Y-%m-%d')) + ' - ' + convert_date(self, date2.strftime('%Y-%m-%d'))
                elif row.service.interval_unit == 'months':
                    date_one = DateTime.strptime(date, '%Y-%m-%d')-DateTime.RelativeDateTime(months=row.service.int_unit_number)
                    date2 = date_one + DateTime.RelativeDateTime(months=row.service.int_unit_number)
                    date1 = date_one
                    date2 -= DateTime.RelativeDateTime(days=1)
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    if row.service.int_unit_number > 1:
                        period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
                    else:
                        period = convert_date(self, date_one.strftime('%Y-%m'))
                elif row.service.interval_unit == 'years':
                    date1 = DateTime.strptime(date, '%Y-%m-%d')
                    date2 = date1 + DateTime.RelativeDateTime(months=12*row.service.int_unit_number, days=-1)
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    if pdate2 > row.cur_effect_date or pdate2 > row.init_effect_date:
                        pdate2 = row.cur_effect_date or row.init_effect_date
                    period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
            elif row.payment == 'start':
                if row.service.interval_unit == 'days':
                    date12 = DateTime.strptime(date, '%Y-%m-%d')
                    date1 = date12
                    date2 = date12 + DateTime.RelativeDateTime(days=row.service.int_unit_number-1)
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    if row.service.int_unit_number > 1:
                        period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
                    else:
                        period = convert_date(self, pdate1)
                elif row.service.interval_unit == 'weeks':
                    date12 = DateTime.strptime(date, '%Y-%m-%d')
                    date1 = date12
                    date2 = date12 + DateTime.RelativeDateTime(weekday=(DateTime.Sunday,0), days=row.service.int_unit_number*7-7)
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
                elif row.service.interval_unit == 'months':
                    date1 = DateTime.strptime(date, '%Y-%m-%d')
                    date2 = date1 + DateTime.RelativeDateTime(months=row.service.int_unit_number, day=1, days=-1)
#                    if date2.strftime('%Y-%m-%d') > row.cur_effect_date:# or date2.strftime('%Y-%m-%d') > row.init_effect_date:
#                        date2 = DateTime.strptime(row.cur_effect_date or row.init_effect_date, '%Y-%m-%d')
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    if row.service.int_unit_number > 1:
                        period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
                    else:
                        date2 = date1 + DateTime.RelativeDateTime(months=1, day=1, days=-1)
#                        pdate1 = date1.strftime('%Y-%m-%d')
                        period = convert_date(self, date1.strftime('%Y-%m'))
                elif row.service.interval_unit == 'years':
                    date1 = DateTime.strptime(date, '%Y-%m-%d')
                    date2 = date1 + DateTime.RelativeDateTime(months=12*row.service.int_unit_number, days=-1)
                    pdate1 = date1.strftime('%Y-%m-%d')
                    pdate2 = date2.strftime('%Y-%m-%d')
                    period = convert_date(self, pdate1) + ' - ' + convert_date(self, pdate2)
#######################################################
            d_list.create(cr, uid, {'agreement_id':row.id, 'date':start_date.strftime('%Y-%m-%d'), 'period':period, 'pdate1':pdate1, 'pdate2':pdate2})
            if row.service.interval_unit == 'weeks' and numbercall==start_numbercall:
                start_date = DateTime.strptime(start_date.strftime('%Y-%m-%d'), '%Y-%m-%d')+DateTime.RelativeDateTime(weekday=(DateTime.Monday,0))
            elif row.service.interval_unit == 'months' and numbercall==start_numbercall:
                start_date = DateTime.strptime(start_date.strftime('%Y-%m-%d'), '%Y-%m-%d')+DateTime.RelativeDateTime(day=1)
            start_date += increment_size
            numbercall -= 1
        return start_date

    def _prolong_optimized(self, cr, uid, context={}):
        ids = self.search(cr, uid, [])
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.state != 'running':
                continue
            if obj.prolong == 'recurrs':
                if obj.service.interval_unit == 'days':
                    inc = {'days':obj.service.int_unit_number}
                elif obj.service.interval_unit == 'weeks':
                    inc = {'days':7*obj.service.int_unit_number}
                elif obj.service.interval_unit == 'months':
                    inc = {'months':obj.service.int_unit_number}
                elif obj.service.interval_unit == 'years':
                    inc = {'months':12*obj.service.int_unit_number}
                    
                if 'days' in inc:
                    increment=DateTime.RelativeDateTime(days=inc['days'])
                elif 'months' in inc:
                    increment=DateTime.RelativeDateTime(months=inc['months'])
                    
                next_start_date = self._get_start_date(cr, uid, obj)
                next_start_date = next_start_date - DateTime.RelativeDateTime(days=next_start_date.day-1)
                temp = now()
                numbercall = 0
                
                if next_start_date < temp:
                    period = temp - next_start_date
                    
                    if obj.service.interval_unit == 'days':
                        numbercall = int(round(period.day / obj.service.int_unit_number))
                        last_date = next_start_date + DateTime.RelativeDateTime(days=numbercall*inc['days'])
                    elif obj.service.interval_unit == 'weeks':
                        numbercall = int(round(period.day / 7.0 / obj.service.int_unit_number))
                        last_date = next_start_date + DateTime.RelativeDateTime(days=numbercall*inc['days'])
                    elif obj.service.interval_unit == 'months':
                        numbercall = int(math.ceil(period.day / 30.0 / obj.service.int_unit_number))
                        last_date = next_start_date + DateTime.RelativeDateTime(months=numbercall*inc['months'])
                    elif obj.service.interval_unit == 'years':
                        numbercall = int(round(period.day / 365.0 / obj.service.int_unit_number))
                        last_date = next_start_date + DateTime.RelativeDateTime(months=numbercall*inc['months'])
                else:
                    last_date = next_start_date
                
                period = last_date - temp
                    
                if (obj.recurr_unit == 'days' and period.days <= obj.recurr_unit_number) or \
                   (obj.recurr_unit == 'weeks' and period.days <= 7*obj.recurr_unit_number) or \
                   (obj.recurr_unit == 'months' and period.days <= 30*obj.recurr_unit_number) or \
                   (obj.recurr_unit == 'years' and period.days <= 365*obj.recurr_unit_number):
                    numbercall += 1
                
                if numbercall > 0:
                    next_start_date = self._make_invoice_log(cr, uid, obj, next_start_date, numbercall, increment, context=context)
                    self.write(cr, uid, [obj.id], {'cur_effect_date': next_start_date})
                    
            elif obj.prolong == 'unlimited':
                if (obj.recurr_unit == 'days' and t.day <= obj.recurr_unit_number) or \
                   (obj.recurr_unit == 'weeks' and t.day <= 7*obj.recurr_unit_number) or \
                   (obj.recurr_unit == 'months' and t.day <= 30*obj.recurr_unit_number) or \
                   (obj.recurr_unit == 'years' and t.day <= 365*obj.recurr_unit_number):
                    self.write(cr, uid, [id], {'cur_effect_date':'2099-01-01'})
#                    self.pool.get('ir.cron').write(cr, uid, obj.cron_id.id, {'numbercall':-1,'active':True})
            elif obj.prolong == 'fixed':
                inv_log = self.pool.get('inv.date_list')
                date_ids = map(int, obj.date_list)
                if not inv_log.search(cr, uid, [('id','in',date_ids),('status','!=','inv')]):
                    self.set_done(cr, uid, [obj.id], context=context) 
        return True

    def onchange_payment(self, cr, uid, ids, signed_date, cur_effect_date, service_id, payment):
        res = {}
        if signed_date < now().strftime('%Y-%m-%d'):
            signed_date = now().strftime('%Y-%m-%d')
        if service_id:
            obj = self.pool.get('inv.service').browse(cr, uid, service_id, {})
            if cur_effect_date and signed_date and obj.interval_unit and obj.int_unit_number:
                period = DateTime.strptime(cur_effect_date, '%Y-%m-%d') - DateTime.strptime(signed_date, '%Y-%m-%d')
                if obj.interval_unit == 'days':
                    res['calls'] = int(period.day / obj.int_unit_number)
                elif obj.interval_unit == 'weeks':
                    res['calls'] = int(period.day / 7.0 / obj.int_unit_number)
                elif obj.interval_unit == 'months':
                    res['calls'] = int(round(period.day / 30.0 / obj.int_unit_number))
                elif obj.interval_unit == 'years':
                    res['calls'] = int(period.day / 365.0 / obj.int_unit_number)
                    if payment == 'start': 
                        res['calls'] += 1
        return {'value':res}

    def _get_start_date(self, cr, uid, rec):
        if rec.service.invoicing == 'period':
            date_list = map(int, rec.date_list)
            dl_ids = self.pool.get('inv.date_list').search(cr, uid, [('id','in',date_list)])
            start_date = self.pool.get('inv.date_list').browse(cr, uid, dl_ids.pop(), {}).date

            if rec.service.interval_unit == 'days':
                increment_size = DateTime.RelativeDateTime(days=rec.service.int_unit_number)
            elif rec.service.interval_unit == 'weeks':
                increment_size = DateTime.RelativeDateTime(days=7*rec.service.int_unit_number)
            elif rec.service.interval_unit == 'months':
                increment_size = DateTime.RelativeDateTime(months=rec.service.int_unit_number)
            elif rec.service.interval_unit == 'years':
                increment_size = DateTime.RelativeDateTime(months=12*rec.service.int_unit_number)

            start_date = DateTime.strptime(start_date, '%Y-%m-%d')+increment_size

        if rec.service.invoicing == 'trigger':
            start_date = DateTime.strptime(rec.signed_date, '%Y-%m-%d')
        return start_date
    
    def _get_last_date(self, cr, uid, rec):
        if rec.service.invoicing == 'period':
            date_list = map(int, rec.date_list)
            dl_ids = self.pool.get('inv.date_list').search(cr, uid, [('id','in',date_list)])
            start_date = self.pool.get('inv.date_list').browse(cr, uid, dl_ids.pop(), {}).date
            start_date = DateTime.strptime(start_date, '%Y-%m-%d')
        return start_date
    
    def _calc_period(self,cr, uid, obj):
        if obj:
            if obj.period_unit == 'days':
                increment_size = DateTime.RelativeDateTime(days=obj.period_unit_number)
            elif obj.period_unit == 'weeks':
                increment_size = DateTime.RelativeDateTime(days=7*obj.period_unit_number)
            elif obj.period_unit == 'months':
                increment_size = DateTime.RelativeDateTime(months=obj.period_unit_number)
            elif obj.period_unit == 'years':
                increment_size = DateTime.RelativeDateTime(months=12*obj.period_unit_number)

            return DateTime.strptime(obj.signed_date, '%Y-%m-%d')+increment_size
        else:
            return False

    def set_process(self, cr, uid, ids, context={}):
        for row in self.browse(cr, uid, ids, {}):
            obj = self.browse(cr, uid, row.id, {})
            agr_period_data = self._calc_period(cr, uid, obj)
            if not agr_period_data:
                raise osv.except_osv(_('Invalid action !'), _('System could not calculate period range !'))
            else:
                self.write(cr, uid, [row.id], {'init_effect_date': agr_period_data.strftime('%Y-%m-%d')})                
            d_list = self.pool.get('inv.date_list')
            date_list = map(int, row.date_list)
            date_error_ids = d_list.search(cr, uid, [('id','in',date_list),('status','=','error')])
            if date_error_ids:
                raise osv.except_osv(_('Invalid action !'), _('This Agreement is not operable, some "Invoice Log" entries are in "Error" state. Please check "Invoice Log" tab.'))
            ids1 = map(int, obj.service.method_ids)
            if type(row.name)==unicode:
                name=row.name
            else:
                name=unicode(row.name or '', "UTF-8")
            res = {'name':name, 'model':'inv.method', 'args':[ids1,row.id], 'function':'_run_filters', 'user_id':uid, 'interval_type':row.service.interval_unit, 'interval_number':row.service.int_unit_number, 'doall':row.repeat}
            if res['name']:
                if type(row.partner_id.name)==unicode:
                    partner_name = row.partner_id.name
                else:
                    partner_name = unicode(row.partner_id.name or '', "UTF-8")
                res['name'] = partner_name+', '+name
                if len(res['name']) > 60:
                    res['name'] = res['name'][:57]+'...'
            else:
                res['name'] = row.partner_id.name

            if not row.repeat and row.signed_date < now().strftime('%Y-%m-%d'):
                signed_date = now().strftime('%Y-%m-%d')
            else:
                signed_date = row.signed_date
                
            if row.cur_effect_date and row.state == 'draft': # set to 'draft', never is going to be 'running' inside this method
                period = DateTime.strptime(row.cur_effect_date, '%Y-%m-%d') - DateTime.strptime(signed_date, '%Y-%m-%d')
            else:
                period = DateTime.strptime(row.init_effect_date, '%Y-%m-%d') - DateTime.strptime(signed_date, '%Y-%m-%d')
                
            if row.service.interval_unit == 'days':
                res['numbercall'] = int(period.day / row.service.int_unit_number)
                increment_size = DateTime.RelativeDateTime(days=res['interval_number'])
                if row.payment == 'end':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d') + increment_size
                elif row.payment == 'start':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d')
            elif row.service.interval_unit == 'weeks':
                res['numbercall'] = int(round(period.day / (7.0 * row.service.int_unit_number)))
                if period.day % (7.0 * row.service.int_unit_number) != 0:
                    res['numbercall'] += 1
                increment_size = DateTime.RelativeDateTime(days=7*res['interval_number'])
                if row.payment == 'end':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d') + increment_size
                    nextcall = nextcall + DateTime.RelativeDateTime(weekday=(DateTime.Monday,0))
                elif row.payment == 'start':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d') + DateTime.RelativeDateTime(weekday=(DateTime.Monday,0))
            elif row.service.interval_unit == 'months':
                res['numbercall'] = int(math.ceil(period.day / 30.0 / row.service.int_unit_number))
                increment_size = DateTime.RelativeDateTime(months=res['interval_number'])
                if row.payment == 'end':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d') + increment_size
                    nextcall = nextcall + DateTime.RelativeDateTime(days=-nextcall.day+1)
                elif row.payment == 'start':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d')+DateTime.RelativeDateTime(day=1)
            elif row.service.interval_unit == 'years':
                val = period.day / 365.0 / row.service.int_unit_number
                res['numbercall'] = int(round(val))
                #if row.payment == 'end' and period.day % (365.0 * row.service.int_unit_number) != 0 and val > round(val):
                #    res['numbercall'] += 1
                increment_size = DateTime.RelativeDateTime(months=12*res['interval_number'])
                #if row.payment == 'start': 
                #    res['numbercall'] += 1
                res['interval_type'] = 'months'
                res['interval_number'] = 12*res['interval_number']
                if row.payment == 'end':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d') + DateTime.RelativeDateTime(months=res['interval_number'])
                    nextcall = nextcall + DateTime.RelativeDateTime(months=-nextcall.month+1, days=-nextcall.day+1)
                elif row.payment == 'start':
                    nextcall = DateTime.strptime(signed_date, '%Y-%m-%d') + DateTime.RelativeDateTime(month=1,day=1)
            nextcalldate = DateTime.strptime(nextcall.strftime('%Y-%m-%d'), '%Y-%m-%d')+DateTime.RelativeDateTime(hours=row.service.cron_offset)
            res['nextcall'] = nextcalldate.strftime('%Y-%m-%d %H:%M:%S')

            if row.service.invoicing == 'period':
                if row.payment == 'end':
                    start_date = nextcalldate
                else:
                    start_date = DateTime.strptime(signed_date, '%Y-%m-%d')
                #d_list = self.pool.get('inv.date_list')
                #date_list = map(int, row.date_list)
                date_list_ids = d_list.search(cr, uid, [('id','in',date_list),('status','=','wait')])
                
                if not date_list:
                    start_date = self._make_invoice_log(cr, uid, row, start_date, res['numbercall'], increment_size, context=context)
                else:
                    dl_ids = d_list.search(cr, uid, [('id','in',date_list)])
                    start_date = d_list.browse(cr, uid, dl_ids.pop(), {}).date
                    start_date = DateTime.strptime(start_date, '%Y-%m-%d')+increment_size

                if date_list_ids:
                    res['numbercall'] = len(date_list_ids)
                    date_list_ids.reverse()
                    res['nextcall'] = d_list.browse(cr, uid, date_list_ids.pop(), {}).date

            if row.service.invoicing == 'trigger':
                res['interval_type'] = 'minutes'
                res['interval_number'] = 5
                res['doall'] = 0
                res['numbercall'] = -1
                res['nextcall'] = now().strftime('%Y-%m-%d %H:%M:%S')
                start_date = DateTime.strptime(signed_date, '%Y-%m-%d')

            if not obj.analytic_account:
                analyt_acc_ids = self.pool.get('account.analytic.account').search(cr, uid, [('name','=',obj.partner_id.name),('parent_id','=',obj.service.analytic_account_branch.id)], limit=1)
                if analyt_acc_ids:
                    analyt_acc_id = analyt_acc_ids[0]
                else:
                    invoice_factor = self.pool.get('hr_timesheet_invoice.factor').search(cr, uid, [('factor','=',0)], limit=1)
                    invoice_factor = invoice_factor and invoice_factor[0] or False
                    analytic_account_data = {'name':obj.partner_id.name,
                                 'parent_id':obj.service.analytic_account_branch.id,
                                 'partner_id':obj.partner_id.id,
                                 'to_invoice':invoice_factor,
                                 }
                    if obj.service.pricelist_id:
                        analytic_account_data['pricelist_id'] = obj.service.pricelist_id.id
                    elif obj.service.analytic_account_branch.pricelist_id:
                        analytic_account_data['pricelist_id'] = obj.service.analytic_account_branch.pricelist_id.id
                    elif obj.partner_id.property_product_pricelist:
                        analytic_account_data['pricelist_id'] = obj.partner_id.property_product_pricelist.id
                    analyt_acc_id = self.pool.get('account.analytic.account').create(cr, uid, analytic_account_data)
                self.write(cr, uid, [row.id], {'analytic_account':analyt_acc_id})
            #    self.write(cr, uid, [row.id], {'cron_id':id,'cron_nextdate':nextdate_id,'analytic_account':analyt_acc_id,'cur_effect_date':cur_date})
            #else:
            #    self.write(cr, uid, [row.id], {'cron_id':id,'cron_nextdate':nextdate_id,'cur_effect_date':cur_date})

            self.write(cr, uid, [row.id], {'state':'running'})
            if not row.cron_id:
                id = self.pool.get('ir.cron').create(cr, uid, res)
            else:
                if row.service.invoicing == 'period':
                    cron = self.pool.get('ir.cron').browse(cr, uid, row.cron_id.id, {})
                    nextcall = (DateTime.strptime(res['nextcall'][:10], '%Y-%m-%d')+DateTime.RelativeDateTime(hours=row.service.cron_offset)).strftime('%Y-%m-%d %H:%M:%S')
                    cr.execute("UPDATE ir_cron SET nextcall=%s WHERE id=%s", (nextcall, row.cron_id.id))
                    del res['nextcall']
                res['active'] = True
                res['doall'] = row.repeat
                self.pool.get('ir.cron').write(cr, uid, [row.cron_id.id], res)
                id = row.cron_id.id
            self.write(cr, uid, [row.id], {'cron_id':id})

            if row.service.invoicing == 'period':
                res['name'] = 'Set next call date'
                res['nextcall'] = (now()+DateTime.RelativeDateTime(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
                res['priority'] = 10
                res['numbercall'] = 1
                res['interval_type'] = 'days'
                res['interval_number'] = 1
                res['model'] = 'inv.agreement'
                res['args'] = [row.id]
                res['function'] = '_set_next_date'
                if not row.cron_nextdate:
                    nextdate_id = self.pool.get('ir.cron').create(cr, uid, res)
                else:
                    nextdate_id = row.cron_nextdate.id
            else: nextdate_id = False
            
            if row.cur_effect_date and not map(int, row.date_list):
                cur_date = row.cur_effect_date
            elif not row.cur_effect_date or (row.cur_effect_date and row.cur_effect_date < row.init_effect_date):
                cur_date = row.init_effect_date
            else:
                cur_date = row.cur_effect_date

            self.write(cr, uid, [row.id], {'cron_id':id,'cron_nextdate':nextdate_id,'cur_effect_date':cur_date})
            if self.read(cr, uid, [row.id], ['state'])[0]['state']=='draft':
                raise osv.except_osv(_('Invalid action !'), _('Agreement not possible running !'))
            else:
                d_list = self.pool.get('inv.date_list')
                d_list_ids = d_list.search(cr, uid, [('agreement_id','=',row.id)])
                d_list.write(cr, uid, d_list_ids, {'state':'process'})
                
        return True

    def set_done(self, cr, uid, ids, context={}):
        for r in self.browse(cr, uid, ids, {}):
	    if r.cron_id:
	      self.pool.get('ir.cron').write(cr, uid, r.cron_id.id, {'active':False})
        self.write(cr, uid, ids, {'state':'done'})
        return True

    def set_draft(self, cr, uid, ids, context={}):
        d_list = self.pool.get('inv.date_list')
        for r in self.browse(cr, uid, ids, {}):
            for id in map(int, r.date_list):
                if d_list.browse(cr, uid, id, {}).analytic_entries:
                    d_list.write(cr, uid, id, {'state':'filled'})
                else:
                    d_list.write(cr, uid, id, {'state':'empty'})
        #    unlink_ids = map(int, r.date_list)
        #    d_list.unlink(cr, uid, unlink_ids)
        self.write(cr, uid, ids, {'state':'draft'})
        return True

    def get_number(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {})
        return True

    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context={}
        log_obj = self.pool.get('inv.date_list')
        if isinstance(ids,int):
            ids = [ids]
        for r in self.browse(cr, uid, ids, {}):
            ################# if change payment #################
            if 'payment' in vals:
                log_ids = log_obj.search(cr, uid, [('id','in',map(int, r.date_list)),('status','=','wait')])
                if log_ids:
                    cr.execute("""
                            SELECT id
                            FROM inv_date_list
                            WHERE date=(SELECT min(date)
                                FROM inv_date_list
                                WHERE id in (%s))
                           """ % ','.join(map(str,log_ids))
                           )
                    min_date_id = cr.fetchone()[0]
                    if vals['payment']=='start':
                        pdate1 = log_obj.read(cr, uid, min_date_id, ['pdate1'])['pdate1']
                        pdate1 = DateTime.strptime(pdate1, '%Y-%m-%d') + DateTime.RelativeDateTime(hours=r.service.cron_offset)
                        self.pool.get('ir.cron').write(cr, uid, r.cron_id.id, {'nextcall':pdate1.strftime('%Y-%m-%d %H:%M:%S')})
                        for log_data in log_obj.read(cr, uid, log_ids, ['pdate1']):
                            temp = DateTime.strptime(log_data['pdate1'], '%Y-%m-%d') + DateTime.RelativeDateTime(hours=r.service.cron_offset)
                            res = log_obj.write(cr, uid, log_data['id'], {'date':temp.strftime('%Y-%m-%d')})
                    elif vals['payment']=='end':
                        log_obj.read(cr, uid, min_date_id, ['pdate2'])['pdate2']
                        pdate2 = log_obj.read(cr, uid, min_date_id, ['pdate2'])['pdate2']
                        pdate2 = DateTime.strptime(pdate2, '%Y-%m-%d') + DateTime.RelativeDateTime(hours=r.service.cron_offset, days=1)
                        self.pool.get('ir.cron').write(cr, uid, r.cron_id.id, {'nextcall':pdate2.strftime('%Y-%m-%d %H:%M:%S')})
                        for log_data in log_obj.read(cr, uid, log_ids, ['pdate2']):
                            temp = DateTime.strptime(log_data['pdate2'], '%Y-%m-%d') + DateTime.RelativeDateTime(hours=r.service.cron_offset, days=1) 
                            res = log_obj.write(cr, uid, log_data['id'], {'date':temp.strftime('%Y-%m-%d')})
            #####################################################
            if ('number' in vals and not vals['number']) or ('number' not in vals and not r.number):
                vals=vals.copy()
                vals['number'] = self.pool.get('ir.sequence').get(cr, uid, 'agreement.invoice.sequence')
        return super(agreement, self).write(cr, uid, ids, vals, context=context)

    def unlink(self, cr, uid, ids, context=None):
        agreements = self.read(cr, uid, ids, ['state', 'cron_id', 'cron_nextdate'])
        unlink_ids = []
        for agr in agreements:
            if agr['state'] == 'draft':
                unlink_ids.append(agr['id'])
                cron_ids = []
                if 'cron_id' in agr and agr['cron_id']:
                    cron_ids.append(agr['cron_id'][0])
                if 'cron_nextdate' in agr and agr['cron_nextdate']:
                    cron_ids.append(agr['cron_nextdate'][0])
                self.pool.get('ir.cron').unlink(cr, uid, cron_ids)
            else:
                raise osv.except_osv(_('Invalid action !'), _('Cannot delete agreement(s) which are already running !'))
        osv.osv.unlink(self, cr, uid, unlink_ids)
        return True

agreement()

class date_list(osv.osv):
    _name = "inv.date_list"
    _rec_name = "date"

    _columns = {
        'agreement_id':  fields.many2one('inv.agreement', 'Agreement'),
        'date': fields.date('Date', required=True, states={'filled':[('readonly',True)],'process':[('readonly',True)]}),
        'pdate1': fields.date('Period Date1', states={'filled':[('readonly',True)],'process':[('readonly',True)]}),
        'pdate2': fields.date('Period Date2', states={'filled':[('readonly',True)],'process':[('readonly',True)]}),
        #'status': fields.selection([('inv','Invoiced'),('wait','Waiting'),('process','Processing'),('error','Error')], 'State', states={'filled':[('readonly',True)],'process':[('readonly',True)]}),
        'status': fields.selection([('inv','Ready to be invoiced'),('part_inv','Partially Invoiced'),('inv_done','Invoiced'),('wait','Waiting'),('process','Processing'),('error','Error')],
             'State', states={'filled':[('readonly',True)],'process':[('readonly',True)]}),
        'state': fields.selection([('empty','Empty'),('filled','Filled'),('process','Processing')], 'State'),
        'analytic_entries': fields.one2many('account.analytic.line', 'invlog_id', 'Entries', states={'process':[('readonly',True)]}),
        'period': fields.char('Period', size=32, states={'filled':[('readonly',True)],'process':[('readonly',True)]}),
    }

    def _renew(self, cr, uid, ids, context={}):
        for r in self.browse(cr, uid, ids, {}):
            if r.agreement_id.state != 'draft':
                raise osv.except_osv(_('Invalid action !'), _('Cannot renew while Agreement not in Draft !'))
            if r.analytic_entries==[]:
                self.write(cr, uid, r.id, {'state':'empty','status':'wait'})
        return True

    def _change_state(self, cr, uid, ids, field, state):
        if field and state=='wait':
            raise osv.except_osv(_('Invalid action !'), _('Cannot set Waiting while field "Analitic Entries" not empty !'))
        return {}

    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context={}
        vals=vals.copy()
        keys=vals.keys()
        if 'analytic_entries' in keys and 'state' in keys and 'status' in keys and vals['analytic_entries'] and vals['status']=='wait':
            vals['status'] = 'inv'
            if vals['analytic_entries']: vals['state'] = 'filled'
        #if 'analytic_entries' not in keys:
        #    vals['state'] = 'empty'
        return super(date_list, self).write(cr, uid, ids, vals, context=context)

    _defaults = {
        'status' : lambda *a: 'wait',
        'state' : lambda *a: 'empty',
    }

date_list()

