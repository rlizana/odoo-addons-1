# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Ting (http://www.ting.es) All Rights Reserved.
#    Copyright (c) 2011 Acysos S.L. (http://acysos.com) All Rights Reserved
#                       Ignacio Ibeas Izquierdo <ignacio@acysos.com>
#    Copyright (c) 2011 NaN Projectes de Programari Lliure, S.L.
#                       http://www.NaN-tic.com
#                   
#    $Id$
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
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv,fields
import time
from datetime import datetime
import netsvc
import tools
import math
from tools.translate import _
import pooler


from dateutil.relativedelta import relativedelta




class l10n_es_aeat_mod340(osv.osv):
   
    def button_calculate(self, cr, uid, ids,  args, context=None):
        
        if not context:
            context = {}

        calculate_obj = self.pool.get('l10n.es.aeat.mod340.calculate_records')
        calculate_obj._wkf_calculate_records(cr, uid, ids, context)   
        
        
        return True
    
    def button_recalculate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        calculate_obj = self. pool.get('l10n.es.aeat.mod340.calculate_records')
        calculate_obj._calculate_records(cr, uid, ids, context)

        return True

    def button_export(self, cr, uid, ids, context=None):
        #FUNCION CALCADA DEL MODELO 347, inoperativa de momento
        
        #raise osv.except_osv(_('No disponible:'), _('En desarrollo'))
        
        if context is None:
            context = {}

        export_obj = self.pool.get("l10n.es.aeat.mod340.export_to_boe")
        export_obj._export_boe_file(cr, uid, ids, self.browse(cr, uid, ids and ids[0]))

        return True
    
    def button_test(self, cr, uid, ids, context=None):
        error_log = []
        for mod340 in self.browse(cr, uid, ids):
            if not mod340.company_id.partner_id.vat:
                    error_log.append({
                        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'nif',
                        'name': _('This company dont have NIF'),
                        'mod340_id': mod340.id,
                    })
                
            fecha_ini = False
            fecha_fin = False
            
            dec_year =mod340.fiscalyear_id.date_start.split('-')[0]
            
            mod = mod340.period

            if mod >= '01' and mod <= '12':
                fecha_ini = datetime.strptime('%s-%s-01' % (dec_year, mod), '%Y-%m-%d')
                fecha_fin = fecha_ini + relativedelta(months=+1, days=-1)

            if mod in ('1T', '2T', '3T', '4T'):
                month = ( ( int(mod[0])-1 ) * 3 ) + 1
                fecha_ini = datetime.strptime('%s-%s-01' % (dec_year, month), '%Y-%m-%d')
                fecha_fin = fecha_ini + relativedelta(months=+3, days=-1)
                mod = '%02d' % month
            
            account_period_id = self.pool.get('account.period').search(cr,uid,[('date_start','=',fecha_ini),('date_stop','=',fecha_fin)])
            if not account_period_id:
                    error_log.append({
                        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'date',
                        'name': _('El periodo seleccionado no coincide con los periodos del año fiscal: %s') %dec_year,
                        'mod340_id': mod340.id,
                    })
            
            domain = [('period_id', '=',account_period_id[0]), ('state', 'not in', ('draft','proforma','proforma2','cancel'))]

            invoice_ids = self.pool.get('account.invoice').search(cr, uid, domain, context=context)
            for invoice in self.pool.get('account.invoice').browse(cr, uid, invoice_ids, context):
                exists = False
                if (invoice.state in ['open','paid']):
                    if not invoice.partner_id.vat and invoice.journal_id.invoice_key != 'J':    
                        for error in error_log:
                            if error['name'].find('invoice.partner_id.name') != -1:
                                exists= True
                        if not exists:
                            error_log.append({
                                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'type': 'nif',
                                'name': _('La siguiente empresa no tiene asignado nif: %s') %invoice.partner_id.name,
                                'mod340_id': mod340.id,
                            })
            for tax_line in invoice.tax_line:
                        if tax_line.name.find('IRPF') == -1:
                            tax_description = tax_line.name.split(' - ')
                            if len(tax_description) == 2: name = tax_description[1]
                            if len(tax_description) == 1: name = tax_description[0]
                            account_tax = self.pool.get('account.tax').browse(cr, uid, self.pool.get('account.tax').search(cr, uid, [('name','=',name)], context=context))
                            if not account_tax:
                               error_log.append({
                                    'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'type': 'vat',
                                    'name': _('IVA mal configurado en la factura: %s') %invoice.number,
                                    'mod340_id': mod340.id,
                                })
            for error in error_log:
                self.pool.get('l10n.es.aeat.mod340.test').create(cr, uid, error)
        return True
        
    def _name_get(self, cr, uid, ids, field_name, arg, context={}):
        """
        Returns the report name
        """
        result = {}
        for report in self.browse(cr, uid, ids, context):
            result[report.id] = report.number
        return result
    
    def _get_number_records( self, cr, uid,ids, field_name, args,context ):
        
        result = {} 
        for id in ids:
            result[id] = {}.fromkeys(['number_records','total_taxable','total_sharetax','total'], 0.0)
    
        for model in self.browse(cr, uid, ids,context):

            for issue in model.issued:
                    result[model.id]['number_records'] += len( issue.tax_line_ids )
                    result[model.id]['total_taxable'] +=issue.base_tax
                    result[model.id]['total_sharetax'] +=issue.amount_tax
                    result[model.id]['total'] +=issue.base_tax + issue.amount_tax

            for issue in model.received:
                    result[model.id]['number_records'] += len( issue.tax_line_ids )
                    result[model.id]['total_taxable'] +=issue.base_tax
                    result[model.id]['total_sharetax'] +=issue.amount_tax
                    result[model.id]['total'] +=issue.base_tax + issue.amount_tax

        return result



    _inherit = "l10n.es.aeat.report"
    _name = 'l10n.es.aeat.mod340'
    _description = 'Model 340'
    _columns = {
        'name': fields.function(_name_get, method=True, type="char", size="64", string="Name"),
        'contact_phone': fields.char("Phone", size=9),
        'phone_contact' : fields.char('Phone Contact',size=9),
        'name_contact' : fields.char('Name And Surname Contact',size=40),
        'period': fields.selection([
            ('1T','First quarter'),('2T','Second quarter'),('3T','Third quarter'),
            ('4T','Fourth quarter'),('01','January'),('02','February'),('03','March'),('04','April'),
            ('05','May'),('06','June'),('07','July'),('08','August'),('09','September'),('10','October'),
            ('11','November'),('12','December')
            ], 'Period'),
        'issued': fields.one2many('l10n.es.aeat.mod340.issued','mod340_id','Invoices Issued'),
        'received': fields.one2many('l10n.es.aeat.mod340.received','mod340_id','Invoices Received'),
        'investment': fields.one2many('l10n.es.aeat.mod340.investment','mod340_id','Property Investment'),
        'intracomunitarias': fields.one2many('l10n.es.aeat.mod340.intracomunitarias','mod340_id','Operations Intracomunitarias'),
        
        'test': fields.one2many('l10n.es.aeat.mod340.test','mod340_id','Invoices Received'),
        'ean13': fields.char('Electronic Code VAT reverse charge', size=16),

        'total_taxable':  fields.function( _get_number_records, method=True, type='float',   string='Total Taxable',    multi='recalc', help="The declaration will include partners with the total of operations over this limit"),
        'total_sharetax': fields.function( _get_number_records, method=True, type='float',   string='Total Share Tax',  multi='recalc', help="The declaration will include partners with the total of operations over this limit"),
        'number_records': fields.function( _get_number_records, method=True, type='integer', string='Records',          multi='recalc', help="The declaration will include partners with the total of operations over this limit"),
        'total':          fields.function( _get_number_records, method=True, type='float',   string="Total" ,           multi='recalc', help="The declaration will include partners with the total of operations over this limit"),
        'calculation_date': fields.date('Calculation date', readonly=True),
    }
    _defaults = {
        'support_type' : lambda *a: 'Telemático',
        'number' : lambda *a: '340',
        'type': lambda *a: 'Normal'
               }

    def set_done(self, cr, uid, id, *args):
        self.write(cr,uid,id,{'calculation_date': time.strftime('%Y-%m-%d'),'state': 'done',})
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'l10n.es.aeat.mod340', id, 'done', cr)
        return True
    
    def _check_report_lines(self, cr, uid, ids, context=None):
        """checks report lines"""
#                if context is None: context = {}

#        for item in self.browse(cr, uid, ids, context):
#            ## Browse partner record lines to check if all are correct (all fields filled)
#            for partner_record in item.partner_record_ids:
#                if not partner_record.partner_state_code:
#                    raise osv.except_osv(_('Error!'), _("All partner state code field must be filled."))
#                if not partner_record.partner_vat:
#                    raise osv.except_osv(_('Error!'), _("All partner vat number field must be filled."))
#
#            for real_state_record in item.real_state_record_ids:
#                if not real_state_record.state_code:
#                    raise osv.except_osv(_('Error!'), _("All real state records state code field must be filled."))

        return True
    
    def check_report(self, cr, uid, ids, context=None):
        """Different check out in report"""
        if context is None: context = {}

        self._check_report_lines(cr, uid, ids, context)

        return True

    def action_confirm(self, cr, uid, ids, context=None):
        """set to done the report and check its records"""
        if context is None: context = {}

        self.check_report(cr, uid, ids, context)
        self.write(cr, uid, ids, {'state': 'done'})

        return True

    def confirm(self, cr, uid, ids, context=None):
        """set to done the report and check its records"""

        self.write(cr, uid, ids, {'state': 'done'})

        return True

    def cancel(self, cr, uid, ids, context=None):
        """set to done the report and check its records"""

        self.write(cr, uid, ids, {'state': 'canceled'})

        return True
    
l10n_es_aeat_mod340()

class l10n_es_aeat_mod340_issued(osv.osv):
    _name = 'l10n.es.aeat.mod340.issued'
    _description = 'Invoices invoice'
    _columns = {                        
        'mod340_id': fields.many2one('l10n.es.aeat.mod340','Model 340',ondelete="cascade"),
        'partner_id':fields.many2one('res.partner','Partner',ondelete="cascade"),
        'partner_vat':fields.char('Company CIF/NIF',size=12),
        'representative_vat': fields.char('L.R. VAT number', size=9, help="Legal Representative VAT number"),
        'partner_country_code': fields.char('Country Code', size=2),
        'invoice_id':fields.many2one('account.invoice','Invoice',ondelete="cascade"),
        'base_tax':fields.float('base tax bill',digits=(13,2)),
        'amount_tax':fields.float('amount of the tax',digits=(13,2)),
        'total':fields.float('total',digits=(13,2)),
        'tax_line_ids': fields.one2many('l10n.es.aeat.mod340.tax_line_issued', 'invoice_record_id', 'tax lines', states = {'done': [('readonly', True)]}),
    }
l10n_es_aeat_mod340_issued()

class l10n_es_aeat_mod340_received(osv.osv):
    _name = 'l10n.es.aeat.mod340.received'
    _description = 'Invoices Received'
    _inherit = 'l10n.es.aeat.mod340.issued'
    _columns = {
        'tax_line_ids': fields.one2many('l10n.es.aeat.mod340.tax_line_received', 'invoice_record_id', 'Tax lines', states = {'done': [('readonly', True)]}),
    }
l10n_es_aeat_mod340_received()

class l10n_es_aeat_mod340_investment(osv.osv):
    _name = 'l10n.es.aeat.mod340.investment'
    _description = 'Property Investment'
    _inherit = 'l10n.es.aeat.mod340.issued'
l10n_es_aeat_mod340_investment()

class l10n_es_aeat_mod340_intracomunitarias(osv.osv):
    _name = 'l10n.es.aeat.mod340.intracomunitarias'
    _description = 'Operations Intracomunitarias'
    _inherit = 'l10n.es.aeat.mod340.issued'
l10n_es_aeat_mod340_intracomunitarias()

class l10n_es_aeat_mod340_tax_line_issued(osv.osv):
    _name = 'l10n.es.aeat.mod340.tax_line_issued'
    _description = 'Mod340 vat lines issued'
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'tax_percentage': fields.float('Tax percentage',digits=(0,2)),
        'tax_amount': fields.float('Tax amount',digits=(13,2)),
        'base_amount': fields.float('Base tax bill',digits=(13,2)),
        'invoice_record_id': fields.many2one('l10n.es.aeat.mod340.issued', 'Invoice issued', required=True, ondelete="cascade", select=1),
    }
l10n_es_aeat_mod340_tax_line_issued()

class l10n_es_aeat_mod340_tax_line_received(osv.osv):
    _name = 'l10n.es.aeat.mod340.tax_line_received'
    _description = 'Mod340 vat lines received'
    _inherit = 'l10n.es.aeat.mod340.tax_line_issued'
    _columns = {
        'invoice_record_id': fields.many2one('l10n.es.aeat.mod340.received', 'Invoice received', required=True, ondelete="cascade", select=1),
    }
l10n_es_aeat_mod340_tax_line_received()

class l10n_es_aeat_mod340_test(osv.osv):
    _name = 'l10n.es.aeat.mod340.test'
    _description = 'Mod340 test results'

    _columns = {
        'name': fields.char('Description', size=64, required=False, readonly=False),
        'type': fields.selection([
            ('nif','NIF/CIF Error'),
            ('vat','VAT Error'),
            ('date','DATE Error'),
            ], 'Error Type'),
        'date': fields.datetime('Date'),
        'mod340_id': fields.many2one('l10n.es.aeat.mod340','Model 340',ondelete="cascade"),
    }
l10n_es_aeat_mod340_test()

#class account_journal(osv.osv):
#    _inherit = 'account.journal'
#
#    _columns = {
#        'invoice_key': fields.selection([
#            ('',''),
#            ('A','A Asiento resumen de facturas'),
#            ('B','B Asiento resumen de tique'),
#            ('F','F Adquisiciones realizadas por las agencias de viajes directamente en interés del viajero'),
#            ('G','G Régimen especial de grupo de entidades en IVA o IGIC'),
#            ('H','H Régimen especial de oro de inversión'),
#            ('I','I Inversión del Sujeto pasivo(ISP)'),
#            ('J','J Tiques'),
#            ('K','K Rectificación de errores registrales'),
#            ('L','L Adquisiciones a comerciantes minoristas del IGIC'),
#        ], 'Invoice Key'),
#    }
#account_journal()
