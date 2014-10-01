# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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

{
    "name": "Prev. Tesoreria Forecast Extension",
    "version": "1.1",
    "depends": ["l10n_es_prev_tesoreria"],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.com",
    "category": "Accounting",
    "description": """
    Este módulo extiende módulo prevision de tesoreria:
    - Añadida función para pago estimado según el tipo y empresa según
    pagos anteriores.
    - Añadido asistente que permite duplicar lineas de pagos periodicos.

    """,
    "init_xml": [],
    'update_xml': ["wizard/wiz_forecast_view.xml",
                   "views/tesoreria_forecast_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,

}