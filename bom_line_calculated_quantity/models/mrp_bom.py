# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields, tools, exceptions, _
from openerp.exceptions import Warning as UserError


class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    @api.model
    def _factor(self, factor, product_efficiency, product_rounding,
                bom_line=None):
        if not bom_line:
            return super(MrpBom, self)._factor(
                factor, product_efficiency, product_rounding)
        formula_qty = bom_line.calculate_expression() or 1
        return super(MrpBom, self)._factor(
            factor*formula_qty, product_efficiency, product_rounding)


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    formula = fields.Text(string='Formula')

    def _normalize_formula(self):
        return self.formula.strip().split(' ')

    def calculate_expression(self):
        if self.formula:
            normalized_formula = self._normalize_formula()
            return self.eval_expression(normalized_formula)

    def _get_val(self, val):
        field = val.split('.')
        res = False
        if field and field[0] in ['self', 'parent']:
            if field[0] == 'self':
                res = float(self.product_id[field[1]])
            else:
                res = float(self.bom_id.product_tmpl_id[field[
                    1]])
        elif field:
            if not self.product_id:
                pass
            else:
                res = self.product_id.attribute_value_ids.filtered(
                    lambda x: x.attribute_id.attribute_code == field[0]
                                                              ).numeric_value
        return res

    def eval_expression(self, formula):
        operators = ['-', '+', '*', '/']
        stack = []
        for val in formula:
            if val in operators:
                op1 = stack.pop()
                op2 = stack.pop()
                result = eval('{} {} {}'.format(op2, val, op1))
                stack.append(result)
            else:
                stack.append(self._get_val(val))
        return stack.pop()

