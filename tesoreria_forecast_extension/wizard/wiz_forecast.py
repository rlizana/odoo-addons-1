
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
from openerp.tools.translate import _


class wiz_forecast(orm.TransientModel):
    _name = 'wiz.forecast'
    _description = 'Forecast actions Wizard'

    def calculate_period_forecast(self, cr, uid, forecas_lines,
                                  context=None):
        # Calcula el precio medio de TODAS las lineas de previsión de la lista
        # forecast_lines
        tes_pagpe_obj = self.pool['l10n.es.tesoreria.pagos.period.plan']
        med = 0
        n = 0
        calc = 0
        for period_forecast_id in forecas_lines:
            n = n+1
            period_reg = tes_pagpe_obj.browse(cr, uid,
                                              period_forecast_id, context)
            if period_reg.importe > 0:
                med = med + period_reg.importe
        if n > 0:
            calc = med / n
        else:
            calc = med
        return calc

    def action_duplicate(self, cr, uid, ids, context=None):
        """
        Duplicate forecast
        """
        res = {}
        #data = self.browse(cr, uid, context['active_ids'][0], context=context)
        tes_pagpe_obj = self.pool['l10n.es.tesoreria.pagos.period.plan']
        tes_sheet = self.pool['l10n.es.tesoreria.plantilla']
        if 'active_id' in context:
            teso_reg = tes_pagpe_obj.browse(cr,uid,context['active_id'])
            dup_fore = teso_reg.paytypeforec.id
            dup_part = teso_reg.partner_id.id
            info = self.calculate_period_forecast(
                cr, uid, context['active_ids'], context)
            tes_pagpe_obj.copy(cr, uid, teso_reg.id,
                               {'forecast': info, 'importe': info,
                                'factura_id': False}, context)
        return res

    def invoice_validated(self, cr, uid, forecast_id, context=None):
        # Comprueba si la linea de previsión tiene su factura validada
        tes_pagpe_obj = self.pool['l10n.es.tesoreria.pagos.period.plan']
        teso_reg = tes_pagpe_obj.browse(cr, uid, forecast_id, context)
        invoice = False
        if teso_reg.factura_id:
            if (teso_reg.factura_id.state == 'open' or
                    teso_reg.factura_id.state == 'paid'):
                invoice = True
        return invoice
