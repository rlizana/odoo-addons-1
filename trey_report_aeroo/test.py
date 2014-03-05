#!/usr/bin/python

import os
import sys
import commands                    

filename = '/tmp/document_base'
for i in range(0,100) :
	commands.getstatusoutput('cp %s.odt %s_%s.odt'  % (filename,filename, i))
	commands.getstatusoutput('/usr/bin/libreoffice --invisible --headless --norestore --convert-to pdf:writer_pdf_Export --outdir /tmp/ %s_%s.odt'  % (filename, i))
	stat, out = commands.getstatusoutput('/usr/bin/libreoffice --invisible --headless --norestore --convert-to pdf:writer_pdf_Export --outdir /tmp/ %s_%s.odt'  % (filename, i))
	print 'Fichero %s_%s.odt : %s' % (filename,i,stat)