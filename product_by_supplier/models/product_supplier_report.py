
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Campos (danielcampos@avanzosc.es) Date: 30/09/2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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

from openerp.osv import orm, fields
import tools


class ProductSupplierReport(orm.Model):
    _name = 'product.supplier.report'
    _auto = False

    _columns = {
        'supplier': fields.many2one('res.partner', 'Supplier'),
        'product': fields.many2one('product.template', 'Producto'),
        'default_code': fields.char('Código Producto', size=128),
        'supplier_code': fields.char('Código Producto Proveedor', size=128),
    }
    _order = 'supplier asc, product asc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'product_supplier_report')
        cr.execute("""
        CREATE OR REPLACE VIEW product_supplier_report AS (
                SELECT
                    min(concat(psi.id, rp.id)) as id,
                    rp.id as supplier,
                    pt.id as product,
                    psi.product_code as supplier_code,
                    pp.default_code as default_code
                FROM res_partner as rp
                INNER JOIN product_supplierinfo psi on rp.id = psi.name
                INNER JOIN product_template pt on psi.product_id = pt.id
                INNER JOIN  product_product pp ON pt.id = pp.product_tmpl_id
                GROUP BY
                    rp.id, pt.id, psi.id, pp.default_code
                ORDER BY
                    rp.id, pt.id, psi.id, pp.default_code
            )
        """)
