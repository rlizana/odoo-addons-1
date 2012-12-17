{
    "name" : "Invoicing / Billing",
    "version" : "1.0",
    "author" : "KN dati, SIA, Avanzosc",
    "description" : """Complete universal addon for issuing bills on any type of TinyERP/OpenERP data objects (models). Setup agreements for automatic customer billing on scheduld intervals.
    Features:
    * user frienly yet powerfull;
    * fully automatic creation of analytic journal entries for further invoicing;
    * definition of various methodologies - business logic;
    * choose code constructor (Python) for fast deployment or manual expressions for advanced business logic or combine both of them;
    * unlimited count of methodologies per virtual service;
    
    Suitable for billing (non exaustive list):
    * Hosting (e-mail, web-hosting etc.);
    * Utilities;
    * Telecom;
    * Service;
    """,
    "website" : "http://kndati.lv",
    "license" : "GPL-2",
    "category" : "Generic Modules/Accounting",
    "depends" : ["base", "product", "account", "hr", "hr_timesheet_invoice"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["invoicing.xml", "invoicing_menu.xml", "data/invoicing_data.xml", "inv_wizard.xml", "security/ir.model.access.csv"],
    "active":False,
    "installable":True,
}
