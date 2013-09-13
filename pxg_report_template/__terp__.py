{
	"name" : "Template Report pxg_report_template",
	"version" : "0.1",
	"description" : """This module is a model to generate custom reports using pxgo_openoffice_reports
 .-Model report adds quality report to a packing.  
""",
	"author" : "Ana Juaristi",
	"website" : " http://www.openerpsite.com",
	"depends" : [ 
		'pxgo_openoffice_reports',
	],
	"category" : "Custom Modules",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : [ 
		'pxg_report_template.xml',
	],
	"active": False,
	"installable": True
}
