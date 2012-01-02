
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

#IMPORTS
from osv import osv
from osv import fields
from tools.translate import _

#TITLES - TITULOS
class titles(osv.osv):
    _name='titles'
    _desciption='titles'
    _columns = {
            'title_ids':fields.integer('title_ids',size=64),
            'name':fields.char('name',size=64),
    }
titles()

#DEGREE - CARRERAS UNIVERSITARIAS
class degree(osv.osv):
    _name = 'degree'
    _description = 'degree'
    
    _columns = {
            'active': fields.boolean('Active'),
            'numhours': fields.integer('Num.Hours',size=2),
            'degree_ids': fields.integer('Degree ids',size=64),
            'name': fields.char('Name',size=64),
            'letter': fields.char('Letter', size=64),
            'shortname': fields.char('Short name', size=64),
            'numcursos': fields.integer('Num.Courses'), 
            'impcredito': fields.integer('Imp Credit'),
            'gradoexp': fields.integer('Grado Exp'),
            'title': fields.many2one('titles','titles'),
            'boe': fields.char('boe',size=64),
            'textoboe': fields.text('TextBOE',size=64),
    }
degree()

#Inherit for ADD a many 2 one.
class training_offer(osv.osv):
    _inherit = 'training.offer'
    _columns = {
            
            'degree_ids': fields.many2one('degree','degree'),
            
    } 
training_offer()    