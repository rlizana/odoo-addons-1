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

class rec_filter_cond(osv.osv):
    _name = 'inv.rec_filter_cond'
    _inherit = 'inv.rec_filter_cond'

    _columns = {
            'rec_filter_id': fields.many2one('inv.rec_filter', 'Filter'),
            'calc_filter_id': fields.many2one('inv.calc_filter', 'Filter'),
    }

rec_filter_cond()

class rec_filter(osv.osv):
    _name = 'inv.rec_filter'
    _inherit = 'inv.rec_filter'

    _columns = {
            'condition_id': fields.one2many('inv.rec_filter_cond', 'rec_filter_id', 'Condition'),
    }

rec_filter()

class calc_filter(osv.osv):
    _name = 'inv.calc_filter'
    _inherit = 'inv.calc_filter'

    _columns = {
            'calc_id': fields.many2one('inv.calc', 'Calculation'),
            'condition_id': fields.one2many('inv.rec_filter_cond', 'calc_filter_id', 'Condition', required=True),
    }

calc_filter()

class account_analytic_line(osv.osv):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    _columns = {
        'agr_id' : fields.many2one('inv.agreement', 'Agreement'),
        'invlog_id' : fields.many2one('inv.date_list', 'Invoice Log'),
    }

account_analytic_line()


