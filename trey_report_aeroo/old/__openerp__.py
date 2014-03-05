# -*- coding: utf-8 -*-
{
    'name': 'Conversor de ficheros a pdf',
    'version': '0.1',
    'category': 'Generic modules',
    'description': """
         Conversion de ficheros a pdf usando un comando 
    """,
    'author': 'Equipo de trey',
    'website': '',
    
    'depends': ['base','report_aeroo'],
    'init_xml': [],
    'update_xml': [
        'aeroo_pdf_convert_view.xml',
        'aeroo_pdf_convert_data.xml',        
    ],
    'demo_xml': [],
    'installable': True,
    'certificate': '',
}
