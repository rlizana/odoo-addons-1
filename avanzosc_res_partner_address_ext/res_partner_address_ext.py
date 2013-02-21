
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
from l10n_es_toponyms.municipios_cpostal import cod_postales

comunidades={'00':'', '01':'EK', '02':'CM', '03':'PV', '04':'AN', '05':'CL', '06':'EX', '07':'IB', '08':'CA', '09':'CL', '10':'EX', '11':'AN', '12':'PV', '13':'CM', '14':'AN', '15':'GA', '16':'CM', '17':'CA', '18':'AN', '19':'CM', '20':'EK', '21':'AN', '22':'AR', '23':'AN', '24':'CL', '25':'CA', '26':'LR', '27':'GA', '28':'MA', '29':'AN', '30':'MU', '31':'NA', '32':'GA', '33':'AS', '34':'CL', '35':'IC', '36':'GA', '37':'CL', '38':'IC', '39':'CB', '40':'CL', '41':'AN', '42':'CL', '43':'CA', '44':'AR', '45':'CM', '46':'PV', '47':'CL', '48':'EK', '49':'CL', '50':'AR', '51':'CE', '52':'ME'}


class res_partner_address(osv.osv):
    
    _name = 'res.partner.address'
    _inherit = 'res.partner.address'
    
    #
    ### HEREDO LA FUNCION DE MODIFICAR
    def write(self, cr, uid, ids, vals, context=None):
        
        config_es_toponyms_obj = self.pool.get('config.es.toponyms')
        city_obj = self.pool.get('city.city')
        
        if not vals.has_key('city') and not vals.has_key('region') and not vals.has_key('state_id'):
            if vals.has_key('zip'):
                # Cojo la provincia
                idc = self.pool.get('res.country').search(cr, uid, [('code', '=', 'ES'),])
                if idc:
                    zip = vals.get('zip')[0:2]
                    ids2 = self.pool.get('res.country.state').search(cr, uid, [('country_id', '=', idc), ('code', '=', zip)])
                    if ids2:
                        vals.update({'state_id': ids2[0]})
                    # Cojo la Comunidad Autonoma    
                    if comunidades.has_key(zip):
                        code = comunidades.get(zip)
                        idc = self.pool.get('res.country.region').search(cr, uid, [('country_id', '=', idc),('code','=',code)])
                        if idc:
                            vals.update({'region': idc[0]})
                    
                # Cojo la ciudad
                zip = vals.get('zip')
                city = ""
                for m in cod_postales:
                    if str(m[0]) == str(zip):
                        vals.update({'city': m[1]})                 
                    
        result = super(res_partner_address,self).write(cr, uid, ids, vals, context)

        return result
  
res_partner_address()
