
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

class avanzosc_french_amortization(osv.osv):

    _name = 'avanzosc.french.amortization'
    _description = 'Avanzosc French Amortization'
   
    #
    ### FUNCION PARA CALCULAR LA CUOTA POR EL SISTEMA FRANCES DE AMORTIZACION
    #
    def calculate_french_amortization(self, cr, uid, requested_capital, interest, years):
        if requested_capital and interest and years:
            if requested_capital > 0 and interest > 0 and years > 0:
                interes = interest / 100
                ano2 = years * -1
                cuota = (requested_capital * (interes/12)) / (1-(1+(interes/12)) ** (ano2 * 12))
            else:
                cuota = 0         
        else:
            cuota = 0

            
        return cuota

avanzosc_french_amortization()