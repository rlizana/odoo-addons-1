{
	"name" : "Report report_quality_steel",
	"version" : "0.1",
	"description" : """This module adds:
 .-New report adds quality report to a packing. (Steel industry) 
 .- To use this report you should use nan_quality_test module
 .- Report will be right printed only if you associate a lot in an outgoing picking, and a quality test to the product lot on each line.
 .- I recomend installing steel_quatily_test module wich will install the test template to use in steel industry companies
""",
	"author" : "Ana Juaristi",
	"website" : " http://www.openerpsite.com",
	"depends" : [ 
		'stock',
	],
	"category" : "Custom Modules",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : [ 
		'report_quality_steel.xml',
	],
	"active": False,
	"installable": True
}
