
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Campos (danielcampos@avanzosc.es) Date: 18/09/2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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


from openerp.osv import fields, orm
import decimal_precision as dp


class l10n_es_tesoreria_pagos_period_plan(orm.Model):
    _inherit='l10n.es.tesoreria.pagos.period.plan'

    def _sel_subject_func (self, cr, uid, context=None):
        obj = self.pool.get('payment.type.forecast')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['name', 'id'], context)
        res = [(r['id'], r['name']) for r in res]
        return res

    _columns={
              'paytypeforec':fields.many2one('payment.type.forecast',
                                             'Payment Type Forecast',
                                             selection=_sel_subject_func),
              'forecast': fields.float(
                    'Forecast', digits_compute=dp.get_precision('Account')),
    }

    def period_forecast_date(self, cr, uid, partner, fortype, date,
                             tr_plan_id, context=None):
         # Calcula el precio medio de las lineas SEGUN FECHA ANTERIOR de un
         # mismo tipo de previsión y un mismo partner
        med = 0
        peri_for_lst = self.search(
            cr, uid, [('paytypeforec', '=', fortype),
                      ('partner_id', '=', partner),
                      ('fecha', '<=', date),
                      ('plan_tesoreria_id', '=', tr_plan_id)], context=context)
        n = 0
        wiz_forecast_obj = self.pool['wiz.forecast']
        for period_forecast_id in peri_for_lst:
            period_reg = self.browse(cr, uid, period_forecast_id, context)
            n = n+1
            if period_reg.importe > 0:
                med = med + period_reg.importe
        if n > 0:
            calc = med / n
        else:
            calc = med
        return calc
#    def period_forecast_date(self, cr, uid, partner, fortype, date,
#                             context=None):
#         # Calcula el precio medio de las lineas SEGUN FECHA ANTERIOR de un
#         # mismo tipo de previsión y un mismo partner
#        # Tiene en cuenta la fecha y que tenga una factura validada 
#        med = 0
#        peri_for_lst = self.search(cr,uid,[('paytypeforec', '=', fortype),
#                                           ('partner_id', '=', partner),
#                                           ('fecha', '<=', date)])
#        n = 0
#        wiz_forecast_obj = self.pool['wiz.forecast']
#        for period_forecast_id in peri_for_lst:
#            period_reg = self.browse(cr, uid, period_forecast_id, context)
#            invoice = wiz_forecast_obj.invoice_validated(cr, uid,
#                                                         period_forecast_id,
#                                                         context)
#            if invoice:
#                n = n+1
#                if period_reg.importe > 0:
#                    med = med + period_reg.importe
#        if n > 0:
#            calc = med / n
#        else:
#            calc = med
#        return calc

    def write(self, cr, uid, ids, vals, context=None):
        value = super(l10n_es_tesoreria_pagos_period_plan, self).write(
            cr, uid, ids, vals, context)
        # duplicar linea
        # wiz_forecast_obj = self.pool['wiz.forecast']
        if not isinstance(ids, int):
            forecast_line = self.browse(cr,uid, ids[0], context)
            if 'fecha' not in vals:
                if forecast_line.fecha:
                    vals['fecha'] = forecast_line.fecha
            if 'paytypeforec' not in vals:
                if forecast_line.paytypeforec:
                    vals['paytypeforec'] = forecast_line.paytypeforec.id
            if 'partner_id' not in vals:
                if forecast_line.partner_id:
                    vals['partner_id'] = forecast_line.partner_id.id
        if 'fecha' and 'paytypeforec' and 'partner_id' in vals:
            current_fc_line = self.browse(cr, uid, ids[0], context)
            tr_plan = current_fc_line.plan_tesoreria_id
            if vals['fecha']:  # La linea tiene fecha
                fore_type_id = vals['paytypeforec']
                partner_id = vals['partner_id']
                date = vals['fecha']
                # busca lineas del mismo tipo/partner y fecha mayor
                forecast_lst = self.search(
                    cr, uid, [('paytypeforec', '=', fore_type_id),
                              ('partner_id', '=', partner_id),
                              ('fecha', '>', date),
                              ('plan_tesoreria_id', '=', tr_plan.id)],
                            context=context)
                if forecast_lst != []:  # Hay lineas para actualizar
                    info = self.period_forecast_date(
                        cr, uid, partner_id, fore_type_id, date, tr_plan.id,
                        context)
                    for forecast_id in forecast_lst:
#                        invoice = wiz_forecast_obj.invoice_validated(
#                            cr, uid, forecast_id, context)
#                        if not invoice:
                        self.write(cr, uid, forecast_id,{'forecast': info,
                                                     'importe': info})
        return value
