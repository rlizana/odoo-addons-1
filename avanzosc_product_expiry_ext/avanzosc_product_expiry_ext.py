# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
#    Copyright (C) 2011 - 2013 Avanzosc <http://www.avanzosc.com>
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

from osv import fields, osv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import pooler

class stock_production_lot(osv.osv):

    _inherit = 'stock.production.lot'

    _columns = {
        'current_date':fields.datetime('Current Date'),
    }

    _defaults = {
        'current_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

stock_production_lot()