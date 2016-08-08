# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Bom line calculated quantity",
    "version": "1.0",
    "depends": ["product_attribute_code_field",
                "product_variant_default_code",
                "mrp_product_variants",
                "mrp_hook_extension",
                "product_attribute_types"
    ],
    "author": "OdooMRP team, "
              "AvanzOSC, ",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "mrp",
    "summary": "",
    "data": ['views/bom_line_view.xml',
             'views/product_attribute_view.xml'],
    "installable": True,
}
