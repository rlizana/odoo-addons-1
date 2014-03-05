# -*- encoding: utf-8 -*-

import os, sys, traceback
import report
import base64
from osv import osv
from tools.translate import _
import tools
import pooler
import netsvc

from report.report_sxw import report_sxw, report_rml, browse_record_list, _fields_process
from report.pyPdf import PdfFileWriter, PdfFileReader

class trey_report_aeroo(report_sxw):

    # override needed to intercept the call to the proper 'create' method
    def create(self, cr, uid, ids, data, context=None):
        data.setdefault('model', context.get('active_model',False))
        pool = pooler.get_pool(cr.dbname)
        ir_obj = pool.get('ir.actions.report.xml')
        name = self.name.startswith('report.') and self.name[7:] or self.name
        report_xml_ids = ir_obj.search(cr, uid,
                [('report_name', '=', name)], context=context)
        if report_xml_ids:
            report_xml = ir_obj.browse(cr, uid, report_xml_ids[0], context=context)
            report_xml.report_rml = None
            report_xml.report_rml_content = None
            report_xml.report_sxw_content_data = None
            report_rml.report_sxw_content = None
            report_rml.report_sxw = None
            copies_ids = []
            if not report_xml.report_wizard and report_xml>1:
                while(report_xml.copies):
                    copies_ids.extend(ids)
                    report_xml.copies -= 1
            ids = copies_ids or ids
        else:
            title = ''
            report_file = tools.file_open(self.tmpl)
            try:
                rml = report_file.read()
                report_type= data.get('report_type', 'pdf')
                class a(object):
                    def __init__(self, *args, **argv):
                        for key,arg in argv.items():
                            setattr(self, key, arg)
                report_xml = a(title=title, report_type=report_type, report_rml_content=rml, \
                            name=title , attachment=False, header=self.header, process_sep=False)
            finally:
                report_file.close()
        report_type = report_xml.report_type
        if report_type in ['sxw','odt']:
            fnct = self.create_source_odt
        elif report_type in ['pdf','raw','txt','html']:
            fnct = self.create_source_pdf
        elif report_type=='html2html':
            fnct = self.create_source_html2html
        elif report_type=='mako2html':
            fnct = self.create_source_mako2html
        elif report_type=='aeroo':
            if report_xml.out_format.code in ['oo-pdf']:
                fnct = self.create_source_pdf
            elif report_xml.out_format.code in ['oo-odt','oo-ods','oo-doc','oo-xls','oo-csv','genshi-raw']:
                fnct = self.create_source_odt
            else:
                return super(Aeroo_report, self).create(cr, uid, ids, data, context)
        else:
            raise Exception('Unknown Report Type')
        return fnct(cr, uid, ids, data, report_xml, context)


    # Heredar funcion, llamar al super y meter los cambios para el tipo nuevo (creado previamente en data?)
    def create_aeroo_report(self, cr, uid, ids, data, report_xml, context=None, output='odt'):
        data, output = super(Aeroo_report, self).create_aeroo_report(cr, uid, ids, data, report_xml, context, output='odt')

        if output == 'oo-pdf-command' :        
            with open('/tmp/openerp_temp.odt','w') as f:
                f.write(data)
            f.close()

        import commands                    
        # stat, out = commands.getstatusoutput('/usr/bin/libreoffice --invisible --headless --convert-to pdf:writer_pdf_Export --outdir /tmp/ /tmp/openerp_temp.odt')
        stat, out = commands.getstatusoutput('/opt/libreoffice3.5/program/soffice --invisible --headless --convert-to pdf /tmp/openerp_temp.odt')

        print stat, out
        
        f = open('/tmp/openerp_temp.pdf','r')
        data = f.read()   
        f.close()     
        output = 'pdf'
        
        return res
