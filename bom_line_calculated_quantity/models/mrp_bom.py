# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields, tools, exceptions, _
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval as eval


class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    @api.model
    def _factor(self, factor, product_efficiency, product_rounding,
                bom_line=None):
        if not bom_line:
            return super(MrpBom, self)._factor(
                factor, product_efficiency, product_rounding)
        qty = bom_line.calculate_expression()
        # if None it means that at least one of the attributes on formula
        # not exists in product attributes. In this case product qty going to
        # be 0
        formula_qty = 0 if qty is None else qty or 1
        return super(MrpBom, self)._factor(
            factor*formula_qty, product_efficiency, product_rounding)


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    formula = fields.Text(string='Formula')

    def _prepare_acts(self):
        production = self.env.context.get('production')
        return production.product_attribute_ids

    def _normalize_formula(self):
        return self.formula.strip().split(' ')

    def calculate_expression(self):
        if self.formula:
            normalized_formula = self._normalize_formula()
            acts = self._prepare_acts()
            return self.eval_expression(normalized_formula, acts)
        else:
            return False

    def _get_val(self, val, acts):
        field = val.split('.')
        res = False
        try:
            return float(val)
        except ValueError:
            if field and field[0] in ['self', 'parent']:
                if field[0] == 'self':
                    value = self.product_id.attribute_value_ids.filtered(
                        lambda x: x.attribute_code == field[1])
                    if not value.attribute_id.attr_type == 'numeric':
                        raise exceptions.ValidationError(
                            "attribute with code {} must be numeric".format(
                            value.attribute_id.attribute_code))
                    res = value.numeric_value
                else:
                    res = float(self.bom_id.product_tmpl_id[field[
                        1]])
            elif field:
                value = acts.filtered(
                    lambda x: x.attribute_id.attribute_code == field[0]
                )
                attr_type = value.attribute_id.attr_type
                if value.attribute_id.attr_type == 'numeric':
                    res = value.value_id.numeric_value
                elif attr_type == 'range':
                    res = value.custom_value
                else:
                    if value:
                        raise exceptions.ValidationError(
                            "attribute with code {} must be numeric or "
                            "range".format(value.attribute_id.attribute_code))
                    else:
                        # value attribute is not in the attributes of
                        # production product
                        return None

        return res

    def eval_expression(self, formula, acts):
        operators = ['-', '+', '*', '/']
        stack = []
        for val in formula:
            if val in operators:
                op1 = stack.pop()
                op2 = stack.pop()
                result = eval('{} {} {}'.format(op2, val, op1))
                stack.append(result)
            else:
                value = self._get_val(val, acts)
                if value is None:
                    return value
                stack.append(value)
        return stack.pop()
