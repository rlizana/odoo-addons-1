# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields         #siempre se ha de poner
from datetime import date, datetime 
import wizard
import base64
import pooler
import time

import netsvc

class setitria_mods_import_dev_c19_wizard(osv.osv_memory):
    
    
    def _process_record_51(self, cr, uid, st_data, line, context=None):
       
       
        #
        # Add a new group to the statement groups
        #
        st_group = {}
        st_data['groups'] = st_data.get('groups', [])
        st_data['groups'].append(st_group)


        #
        # Set the group values
        #        
        st_group .update({
                'nif_empresa'   : line[4:13],
                'sufijo'        : line[13:16],
                'fecha_fich'    : time.strftime('%Y-%m-%d', time.strptime(line[16:22], '%d%m%y')),
                'cliente'       : line[28:68].strip(),
                'entidad'       : line[88:92],
                'oficina'       : line[92:96],
                'nom_entitat'   : line[108:148].strip(),
                '_num_records'  : 1,
                'num_records'   : 0,
                '_num_dev'      : 0,
                'num_dev'       : 0,
                'import'        : 0,
                'groups'        : []
            })
        
        
        return st_group;
    
    def _process_record_53(self, cr, uid, st_data, line, context=None):
       
        super = st_data['groups'][-1]
        
        #
        # Add a new group to the statement groups
        #
        st_group = {}
        super['groups'] = super.get('groups', [])
        super['groups'].append(st_group)
        
        st_group.update({
                    'nif'           : line[4:13],
                    'sufijo'        : line[13:16],
                    'fecha'         : time.strftime('%Y-%m-%d', time.strptime(line[22:28], '%d%m%y')),
                    'nombrecl'      : line[28:68].strip(),
                    'entidad'       : line[68:72],
                    'oficina'       : line[72:76],
                    'dc'            : line[76:78],
                    'ncc'           : line[78:88],
                    '_num_records'  : 1,
                    'num_records'   : 0,
                    '_num_dev'      : 0,
                    'num_dev'       : 0,
                    'import'        : 0,
                    'lineas'         : []
            })
        
        return st_group 
   
   
    def _process_record_56(self, cr, uid, st_data, line, context=None):
        super   = st_data['groups'][-1]
        super2  = super['groups'][-1]
        
        
        #
        # Add a new line to the statement lines
        #
        st_line = {}
        super2['lineas'] = super2.get('lineas', [])
        super2['lineas'].append(st_line)

        #
        # Set the line values
        #
        st_line.update({
            'nif'           : line[4:13],
            'sufijo'        : line[13:16],
            'codi_ref'      : line[16:28].strip(),
            'nombre_titular': line[28:68].strip(),
            'entidad'       : line[68:72],
            'oficina'       : line[72:76],
            'dc'            : line[76:78],
            'ncc'           : line[78:88],
            'importe'       : float(line[88:96])+(float(line[96:98])/100),
            'codi_dev'      : line[98:104].strip(),
            'codi_ref_int'  : line[104:114].strip(),
            'concepto'      : line[114:154].strip(),
            'motivo_dev'    : line[154:155].strip()
        })

        super2['_num_records']  += 1
        super2['_num_dev']      += 1
        super2['import']        += st_line['importe']
        
        return st_line
    
    def _process_record_58(self, cr, uid, st_data, line, context=None):
        super   = st_data['groups'][-1]
        super2  = super['groups'][-1]
        
        super2['_num_records'] += 1
        
        
        devolucions = float(line[104:114])
        registres   = float(line[114:124])
        importe     = float(line[88:96])+(float(line[96:98])/100)
        
        
        
        ################################################
        ##   CHECKS A NIVEL DE GRUP
        ################################################
        if devolucions != super2['_num_dev'] :
            raise osv.except_osv('Error in C19 file', 'El numero de devolucions no coincideix amb el definit al grup. (linea: %s)' % (super['_num_records'] + super2['_num_records']))
        if registres != super2['_num_records']:
            raise osv.except_osv('Error in C19 file', 'El numero de registres no coincideix amb el definit al grup. (linea: %s)' % (super['_num_records'] + super2['_num_records']))
        if abs(importe - super2['import'] ) > 0.005:
            raise osv.except_osv('Error in C19 file', "L'import dels registres no coincideix amb el definit al grup. (linea: %s)" % (super['_num_records'] + super2['_num_records']))
        
        
        
        super2['num_dev']       = devolucions
        super2['import']        = importe
        super2['num_records']   = registres
        
        super['_num_records']   += super2['num_records']
        super['import']         += importe
        super['_num_dev']       += devolucions
        
        return super2
    
    
    def _process_record_59(self, cr, uid, st_data, line, context):
        super   = st_data['groups'][-1]
        
        super['_num_records'] += 1
        
        devolucions = float(line[104:114])
        registres   = float(line[114:124])
        importe     = float(line[88:96])+(float(line[96:98])/100)
        
        
        ################################################
        ##   CHECKS A NIVEL DE CAPÇALERA SUPERIOR
        ################################################
        if devolucions != super['_num_dev'] :
            raise osv.except_osv('Error in C19 file', 'El numero de devolucions no coincideix amb el definit al total. (linea: %s)' % (super['_num_records']))
        if registres != super['_num_records']:
            raise osv.except_osv('Error in C19 file', 'El numero de registres no coincideix amb el definit al total. (linea: %s)' % (super['_num_records']))
        if abs(importe - super['import'] ) > 0.005:
            raise osv.except_osv('Error in C19 file', "L'import dels registres no coincideix amb el deffecha_fichinit al total. (linea: %s)" % (super['_num_records']))
        
        
        super['num_dev']       = devolucions
        super['import']        = importe
        super['num_records']   = registres
        
        
        return super
    
    
    
    def _load_c19_file(self, cr, uid, file_contents, context=None):
        if context is None:
            context = {}
        
        st_data = {
                'groups' : []
            }
        
        #
        # Read the C19 file
        #
        decoded_file_contents = base64.decodestring(file_contents)
        try:
            unicode(decoded_file_contents, 'utf8')
        except Exception, ex: # Si no puede convertir a UTF-8 es que debe estar en ISO-8859-1: Lo convertimos
            #hem quitat l'ultim
            decoded_file_contents = unicode(decoded_file_contents, 'iso-8859-1')#.encode('utf-8')    
        
        #
        # Process the file lines
        #
        for line in decoded_file_contents.split("\n"):
            if len(line) == 0:
                continue
            if not (line[2:4] == '90'):
                raise osv.except_osv('Error in C19 file', 'data code %s is not valid.' % line[2:4])
            if line[0:2] == '51': # Registro cabecera de cuenta (obligatorio)
                self._process_record_51(cr, uid, st_data, line, context)
            elif line[0:2] == '53': # Registro cabecera de ordenante (obligatorio)
                self._process_record_53(cr, uid, st_data, line, context)
            elif line[0:2] == '56': # Registros individual obligatorio
                self._process_record_56(cr, uid, st_data, line, context)
            elif line[0:2] == '58': # Registro total de ordenante
                self._process_record_58(cr, uid, st_data, line, context)
            elif line[0:2] == '59': # Registro total general
                self._process_record_59(cr, uid, st_data, line, context)
            elif ord(line[0]) == 26: # CTRL-Z (^Z), is often used as an end-of-file marker in DOS
                pass
            else:
                raise osv.except_osv('Error in C19 file', 'Record type %s is not valid.' % line[0:2])

        return st_data
    
    def _attach_file_to_fitxer(self, cr, uid, file_contents, file_name, fitxer_id, context=None):
        """
        Attachs a file to the given fitxer de rebuts retornats
        """
        if context is None:
            context = {}
        pool = pooler.get_pool(cr.dbname)
        attachment_facade = pool.get('ir.attachment')
        
        attachment_name = 'Fitxer Rebuts Retornat'

        #
        # Remove the previous statement file attachment (if any)
        #
        ids = attachment_facade.search(cr, uid, [
                    ('res_id', '=', fitxer_id),
                    ('res_model', '=', 'setitria.fitxerretornat'),
                    ('name', '=', attachment_name),
                ], context=context)
        if ids:
            attachment_facade.unlink(cr, uid, ids, context)

        #
        # Create the new attachment
        #
        res = attachment_facade.create(cr, uid, {
                    'name': attachment_name,
                    'datas': file_contents,
                    'datas_fname': file_name,
                    'res_model': 'setitria.fitxerretornat',
                    'res_id': fitxer_id,
                }, context=context)

        return res
    
    def import_action(self, cr, uid, ids, context=None):
        """
        Imports the C19 file selected by the user on the wizard form
        """
        if context is None:
            context = {}
        
        pool    = pooler.get_pool(cr.dbname)
        factura = pool.get('account.invoice')
        banc    = pool.get('res.bank')
        apunt   = pool.get('account.move.line')
        reconc  = pool.get('account.move.reconcile')
        fitxer  = pool.get('setitria.fitxerretornat')
        lineafit= pool.get('setitria.fitxerretornat.line')
        pay_line= pool.get('payment.line')      
        account_obj = pool.get('account.account')
        partner_obj = pool.get('res.partner')
        
        for c19_wizard in self.browse(cr,uid,ids,context):
            # Load the file data into the st_data dictionary
            st_data = self._load_c19_file(cr, uid, c19_wizard.file, context=context)
            
            for grupoTotal in st_data['groups']:    # per cada grup gran (en principi un per fitxer, pero aixó no es pot control-lar)
                
                banc_id = False
                banc_id = banc.search(cr, uid,[('code', '=', grupoTotal['entidad'])])
                
                if not banc_id:
                    raise osv.except_osv('Error tractant el fitxer', "El codi del banc indicat al fitxer no existeix")
                else:
                    banc_id=banc_id[0]
                    
                values = {
                            'date'      : grupoTotal['fecha_fich'],
                            'date_imp'  : date.today().isoformat(),
                            'name'      : c19_wizard.file_name,
                            'banc_id'   : banc_id
                          }
                
                fitxer_id = fitxer.create(cr, uid, values,context=context)
                
                for grupo in grupoTotal['groups']:  # per cada grup (agrupacio de rebuts per dia)
                    for linea in grupo['lineas']:   # per cada rebut
                        ids = factura.search(cr,uid,[('number','=',linea['codi_ref'])])
                        if not ids:
                            ids = factura.search(cr,uid,[('internal_number','=',linea['codi_ref'])])
                            if not ids:
                                ids = factura.search(cr,uid,[('name','=',linea['codi_ref'])])
                                if not ids:
                                    ids = factura.search(cr,uid,[('reference','=',linea['codi_ref'])])
                        
                        print 'Sufijo: '+ str(linea['sufijo'])
                        print 'codi_ref: '+ str(linea['codi_ref'])
                        print 'nombre_titular: '+ str(linea['nombre_titular'])
                        print 'entidad: '+ str(linea['entidad'])
                        print 'oficina: '+ str(linea['oficina'])
                        print 'dc: '+ str(linea['dc'])
                        print 'ncc: '+ str(linea['ncc'])
                        print 'importe: '+ str(linea['importe'])
                        print 'codi_dev: '+ str(linea['codi_dev'])
                        print 'codi_ref_int: '+ str(linea['codi_ref_int'])
                        print 'concepto: '+ str(linea['concepto'])
                        print 'motivo_dev: '+ str(linea['motivo_dev'])
                        
                        partner = partner_obj.search(cr, uid, [('ref', '=', linea['codi_ref'][5:])])
#                        partner = partner_obj.search(cr, uid, [('ref', '=', linea['codi_ref'][len(linea['sufijo']):])])
                       
                        if partner:
                            part = partner_obj.browse(cr, uid, partner[0])
                            id_compte_430 = part.property_account_receivable.id
                        else:
                            raise osv.except_osv('Error', 'Partner not found containing %s Reference number.' % linea['codi_ref'])
                        
                        ids = False
                        pline = False
                        pline_ids = pay_line.search(cr, uid, [('ml_inv_ref', '=', int(linea['codi_dev']))])
                        for line in pline_ids:
                            pline = pay_line.browse(cr,uid,line)
                            if pline.id == int(linea['codi_ref_int']):
                                break
                            else:
                                pline = False
                        
                        if pline and pline.ml_inv_ref:
                            if pline.ml_inv_ref.id == int(linea['codi_dev']):
                                ids = pline.ml_inv_ref.id
                        
                        if ids:
                            values = {
                                      'fitxer_id'   : fitxer_id,
                                      'invoice_id'  : ids,
                                      'date'        : grupo['fecha'],
                                      'motiu_dev'   : linea['motivo_dev']
                                    }
                            
                            fact_obj = factura.browse(cr,uid,ids)
                            id_linea = apunt.search(cr, uid,[
                                                             ('account_id','=',id_compte_430),
                                                             ('debit','=',fact_obj.amount_total),
 #                                                            ('date','=',grupo['fecha'])
#                                                             ,('reconcile_id','=',False)
                                                        ])
                            if id_linea:
                                ids_mov = []
                                
                                
#                                for mov_line in fact_obj.move_lines:
#                                    ids_mov.append(mov_line.id)
#                                    if mov_line.reconcile_id:
#                                        id_reconcile = mov_line.reconcile_id.id
#                                        break
#                                    
#                                if id_reconcile:
#                                    apunt.write(cr,uid,id_linea,{'reconcile_id':id_reconcile},context)
#                                else:
#                                id_reconcile = reconc.create(cr,uid,{
#                                                                     'name' : 'DEV FACT %s' % linea['codi_dev'],
#                                                                     'type' : 'DEV FACT'
#                                                                     },context)
                                for linea in id_linea:
                                    line_obj = apunt.browse(cr,uid,linea)
                                    invoice_id = line_obj.invoice.id
                                    if invoice_id == ids:
                                        apunt.write(cr,uid,line_obj.id,{'reconcile_id':False},context)
                                        wf_service = netsvc.LocalService("workflow")
                                        wf_service.trg_validate(uid, 'account.invoice', ids, 'open_test', cr)
#                                        ids_mov.append(linea)
                                
                                
                                
                                values['state'] = 'valid' 
                            else:                              
                                values['notes'] = "No s'ha trobat el apunt de contraprestació de la factura"
                            
                            lineafit.create(cr,uid,values,context=context)
                        else:
                            raise osv.except_osv('Error tractant el fitxer', 'La factura no es troba.(%s)' % linea['codi_dev'])
                        
                # Attach the C43 file to the current statement
                self._attach_file_to_fitxer(cr, uid, c19_wizard.file, c19_wizard.file_name, fitxer_id)          
        
        return {}
 
 
 
    _name = 'setitria.mods.import.dev.c19.wizard'
    
    _columns = {
        'file': fields.binary('Arxiu de retornats del Banc', required=True, filename='file_name'),
        'file_name': fields.char('Arxiu de retornats del Banc', size=64)
        }
    
setitria_mods_import_dev_c19_wizard()


class setitria_fitxerretornat(osv.osv):
    _name = "setitria.fitxerretornat"
    _description = 'Fitxer Rebuts Retornats'
    
    
    def _get_rebuts(self, cr, uid, ids, context=None):
        list_fitxer = [ l.fitxer_id.id for l in  self.pool.get('setitria.fitxerretornat.line').browse(cr, uid, ids, context=context)]
        return list_fitxer
    
    def _calcul_state(self, cr, uid, ids, name, arg, context=None):
        if not ids: return {}
        res = {}
        for id in ids:
            res[id] = ['incomplete']
            
        cr.execute('''
            SELECT
                a.id,
               COALESCE(max(b.state),'incomplete')
            FROM
                     setitria_fitxerretornat a
                LEFT OUTER JOIN
                    setitria_fitxerretornat_line b
                        ON
                            a.id=b.fitxer_id
            WHERE
                a.id IN %s 
            GROUP BY 
                a.id
            ''',(tuple(ids),))
        
        for oid,state in cr.fetchall():
            res[oid] = state
                        
        return res
        
    _columns = {
        'date'      : fields.date('Data del fitxer'),
        'banc_id'   : fields.many2one('res.bank','Banc origen'),
        'name'      : fields.char("Nom de l'arxiu", size=64, required=True),
        'date_imp'  : fields.date("Data d'importació del fitxer"),
        'lines_id'  : fields.one2many('setitria.fitxerretornat.line','fitxer_id'),
        'notes'     : fields.text('Notes'),
        'state'     : fields.function(_calcul_state, method=True, string='Estat', type='selection', selection=[
                                            ('incomplete', 'Incomplert'),
                                            ('valid', 'Complert')
                                        ],
                                        store = {
                                                 'setitria.fitxerretornat.line': (_get_rebuts, ['state'], 10),
                                                 }
        ),
    }
    
    _sql_constraints = [
        ('no repetit', 'UNIQUE (date, banc_id, name)',  'Error, introduint dades previament cargades'),
    ]
        
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attachment_facade = self.pool.get('ir.attachment')
        
        attachment_name = 'Fitxer Rebuts Retornat'
        
        for id in ids:
            #
            # Remove the previous statement file attachment (if any)
            #
            id_at = attachment_facade.search(cr, uid, [
                        ('res_id', '=', id),
                        ('res_model', '=', 'setitria.fitxerretornat'),
                        ('name', '=', attachment_name),
                    ], context=context)
            if id_at:
                attachment_facade.unlink(cr, uid, id_at, context)
        
        ret = super(setitria_fitxerretornat,self).unlink(cr,uid,ids,context=context)
        return ret;
    
setitria_fitxerretornat()

class setitria_fitxerretornat_line(osv.osv):
    _name = "setitria.fitxerretornat.line"
    _description = 'Lineas Fitxers Rebuts Retornats'
    
    _columns = {
        'fitxer_id' : fields.many2one('setitria.fitxerretornat','Fitxer Retornat',required=True, ondelete='cascade'),
        'motiu_dev' : fields.selection([
                                            ('0',"Import a cero"),
                                            ('1',"Incorriente"),
                                            ('2',"No domiciliat o compte cancel-lat"),
                                            ('3',"Oficina domiciliataria inexistent"),
                                            ('4',"Aplicació R.D. 338/90, sobre el NIF"),
                                            ('5',"Per ordre del client: error o baixa en la domiciliació"),
                                            ('6',"Per ordre del client: disconformitat amb l'import"),
                                            ('7',"Dec duplicat, indegut, erroni o falten dades "),
                                            ('8',"Sense utilitzar")
                                        ], 'Motiu de devolució'),
        'invoice_id': fields.many2one('account.invoice','Factura associada'),
        'date'      : fields.date('Data de retorn'),
        'state'     : fields.selection([
                                            ('incomplete', 'Incomplert'),
                                            ('valid', 'Complert')
                                        ],'Estat'),
        'notes'     : fields.text('Notes')
    }
    
    _defaults = {
        'state'  : 'incomplete'
    }
    
setitria_fitxerretornat_line()




#class account_move(osv.osv):
#    _name = "account.move"
#    _inherit = "account.move"
#    
#    
#    #################################################################################
#    ##            FUNCIO QUE CREA ELS MOVIMENTS QUE HAN ESTAT PASSATS              ##
#    #################################################################################
#    ##    moviments : Llista amb els moviments que es volen crear
#    ##
#    ##            referencia  : referencia que es vol posar
#    ##
#    ##            periode     : periode al que es pertany el moviment
#    ##                default : el periode de la data del moviment
#    ##
#    ##            diari       : diari al que es vol afegir el moviment
#    ##
#    ##            estat       : estat al que es vol posar el moviment
#    ##                default : draft (esborrany)
#    ##
#    ##            data        : data que es vol assignar al moviment
#    ##                default : la data actual
#    ##
#    ##            notes       : notes que es volen afegir al moviment
#    ##
#    ##            company     : compañia on es vol crear el moviment
#    ##                default : la empresa amb id=1
#    ##
#    ##            apunts      : llista amb els apunts del moviment
#    ##
#    ##                    nom        : nom del apunt que es vol posar
#    ##
#    ##                    quantitat  : quantitat que es vol posar (es només a nivell informatiu)
#    ##
#    ##                    producte   : producte que es vol posar (només a nivell informatiu)
#    ##
#    ##                    debit      : l'import de debit
#    ##                        default: 0
#    ##
#    ##                    credit     : l'import de credit
#    ##                        default: 0
#    ##
#    ##                    compte     : compte al que esta assignat el apunt
#    ##                        default: compte del partner
#    ##
#    ##                    notes      : notes que es volen fer a l'apunt
#    ##
#    ##                    periode    : periode al que es vol assignar l'apunt
#    ##                        default: el periode de la data de l'apunt
#    ##
#    ##                    diari      : diari al que es vol assignar l'apunt
#    ##                        default: el diari del moviment
#    ##
#    ##                    partner    : tercer al que se li assigna el moviment
#    ##
#    ##                    data_cad   : data de "pagament" d'una linea
#    ##
#    ##                    data       : data de l'apunt
#    ##                        default: data del moviment
#    ##
#    ##                    data_crea  : data de creació de l'apunt
#    ##                        default: la data actual
#    ##
#    ##                    estat      : estat de l'apunt
#    ##                        default: draft
#    ##
#    ##                    compte_ana : compte analitic que es vol assignar a l'apunt
#    ##
#    #################################################################################
#    def traspas_contabilitat(self,cr,uid,moviments,context=None):
#        periode = self.pool.get('account.period')
#        diari   = self.pool.get('account.journal')
#        producte= self.pool.get('product.product')
#        compte  = self.pool.get('account.account')
#        partner = self.pool.get('res.partner')
#        lineas  = self.pool.get('account.move.line')
#        recon   = self.pool.get('account.move.reconcile')
#        
#        
#        llistaMessos = ['','Gener','Febrer','Març','Abril','Maig','Juny','Juliol','Agost','Setembre','Novembre','Octubre','Desembre']
#        
#        if context is None:
#            context={}
#        
#        for moviment in moviments:
#            
#            print moviment
#            
#            values = {}
#            if ('diari' in moviment) and moviment['diari']:
#                diari_id = diari.search(cr,uid,[('code','=',moviment['diari'])])
#                if diari_id:
#                    diari_id = diari_id[0]
#                else:
#                    raise osv.except_osv('Error traspassant comptabilitat', "El moviment no conte un diari valid")
#                
#                values['journal_id'] = diari_id
#                context['journal_id'] = diari_id
#            else:
#                raise osv.except_osv('Error traspassant comptabilitat', "El moviment no conte el diari on afegir-l'ho")
#            
#            if ('notes' in moviment) and moviment['notes']:
#                 values['notes'] = moviment['notes']
#                 
#            if ('referencia' in moviment) and moviment['referencia']:
#                 values['ref'] = moviment['referencia']
#            
#            if ('data' in moviment) and moviment['data']:
#                values['date'] = moviment['data']
#            else:
#                values['date'] = date.today().isoformat()
#            
#            if ('company' in moviment) and moviment['company']:
#                values['company_id'] = moviment['company']
#            else:
#                values['company_id'] = 1
#                
#            periodeid = False
#            if ('periode' in moviment) and moviment['periode']:
#                periode_id = periode.search(cr,uid,[('name','=',moviment['periode'])],context=context)
#                if periode_id:
#                    periodeid = periode_id[0]
#            else:
#                data = datetime.strptime(values['date'], '%Y-%m-%d')
#                nom_periode = ''
#                if moviment['diari'] == 'OBER' :
#                    nom_periode = 'Opertura Exercici ' + data.year
#                else:
#                    nom_periode = llistaMessos[data.month] + ' ' + str(data.year)
#                
#                periode_id = periode.search(cr,uid,[('name','=',nom_periode)])
#                if periode_id:
#                    periodeid = periode_id[0]
#                
#            if periodeid:
#                values['period_id'] = periodeid
#            
#                
#            move_id = self.create(cr,uid,values,context=context)
#            
#            if 'apunts' in moviment:
#                
#                for apunt in moviment['apunts']:
#                    print apunt
#                    
#                    values2={}
#                    context2 = context.copy()
#                    
#                    values2['move_id']      = move_id                    
#                    values2['company_id']   = values['company_id']
#                    
#                    
#                    if ('nom' in apunt) and apunt['nom']:
#                        values2['name'] = apunt['nom']
#                    else:
#                        raise osv.except_osv('Error traspassant comptabilitat', "L'apunt ha de contenir un nom")
#                    
#                    if ('quantitat' in apunt) and apunt['quantitat']:
#                         values2['quantity'] = apunt['quantitat']
#                   
#                    if ('producte' in apunt) and apunt['producte']:
#                        producte_id = producte.search(cr,uid,[('default_code','=',apunt['producte'])])
#                        if producte_id:
#                                values2['product_id'] = producte_id[0]
#                                
#                    values2['credit'] = apunt['credit']
#                    values2['debit']  = apunt['debit']
#                    
#                    if ('data' in apunt) and apunt['data']:
#                         values2['date'] = apunt['data']
#                    else:
#                         values2['date'] = values['date']
#                    
#                    periodeid = False
#                    if ('periode' in apunt) and apunt['periode']:
#                        periode_id = periode.search(cr,uid,[('name','=',apunt['periode'])],context=context2)
#                        if periode_id:
#                            periodeid = periode_id[0]
#                    else:
#                        data = datetime.strptime(values2['date'], '%Y-%m-%d')
#                        nom_periode = ''
#                        if apunt['diari'] == 'OBER' :
#                            nom_periode = 'Opertura Exercici ' + data.year
#                        else:
#                            nom_periode = llistaMessos[data.month] + ' ' + str(data.year)
#                        
#                        periode_id = periode.search(cr,uid,[('name','=',nom_periode)])
#                        if periode_id:
#                            periodeid = periode_id[0]
#                        
#                    if periodeid:
#                        values2['period_id'] = periodeid
#                    
#                    context2['period_id'] = periodeid
#                    
#                    if ('diari' in apunt) and apunt['diari']:
#                        diari_id = diari.search(cr,uid,[('code','=',apunt['diari'])])
#                        if diari_id:
#                            diari_id = diari_id[0]
#                        else:
#                            raise osv.except_osv('Error traspassant comptabilitat', "L'apunt no conte un diari valid")
#                        
#                        values2['journal_id'] = diari_id
#                        
#                    else:
#                        values2['journal_id'] = values['journal_id']
#                        
#                    context2['journal_id'] = values2['journal_id']
#                    
#                    if ('partner' in apunt) and apunt['partner']:
#                        partner_id = partner.search(cr,uid,[('ref','=',apunt['partner'])])
#                        if partner_id:
#                            values2['partner_id'] = partner_id[0]
#                            ret = lineas.onchange_partner_id(cr, uid, move_id, values2['partner_id'], None, values2['credit'], values2['debit'], values2['date'], values2['journal_id'] )
#                            values2.update(ret['value'])
#                    
#                    if ('compte' in apunt) and apunt['compte']:
#                        compte_id = compte.search(cr,uid,[('code','=',apunt['compte'])])
#                        if compte_id:
#                            values2['account_id'] = compte_id[0]
#                        
#                    ret = lineas.onchange_account_id(cr, uid, [], values2.get('account_id',False), values2.get('partner_id',False))
#                    values2.update(ret['value'])
#                    
#                    
#                    if ('data_cad' in apunt) and apunt['data_cad']:
#                        values2['date_maturity'] = apunt['data_cad']
#                    
#                    if ('data_crea' in apunt) and apunt['data_crea']:
#                        values2['date_created'] = apunt['data_crea']
#                        
#                    id_linea = lineas.create(cr,uid,values2,context=context2)
#                
#                    
#        return True
#    
#account_move()