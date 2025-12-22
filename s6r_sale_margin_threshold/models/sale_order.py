# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    minimum_margin_violation = fields.Boolean(
        string="Minimum Margin Violation Error",
        compute="_compute_minimum_margin_violation",
        store=True
    )

    @api.depends("order_line.minimum_margin_violation")
    def _compute_minimum_margin_violation(self):
        for order in self:
            order.minimum_margin_violation = any(
                line.minimum_margin_violation for line in order.order_line)

    def _check_min_margin(self):
        company = self.company_id
        if not company.blocking_transaction_order:
            return

        blocking_lines = self.order_line.filtered(
            lambda line: line.minimum_margin_violation
        )
        if blocking_lines:
            min_margin = company.sale_min_margin_percent
            lines_msg = []
            for line in blocking_lines:
                product = line.product_id.display_name
                lines_msg.append(_(
                    "- %(product)s: %(margin_percent).2f%% (minimum %(min_margin).2f%%)",
                    product=product,
                    margin_percent=line.margin_percent * 100,
                    min_margin=min_margin * 100
                ))
            raise UserError(_(
                "The operation cannot be completed because the following order lines "
                "have a margin below the allowed threshold:\n\n%(lines)s"
            ) % {'lines': "\n".join(lines_msg)})

    def action_confirm(self):
        self._check_min_margin()
        return super().action_confirm()

    def action_quotation_send(self):
        self._check_min_margin()
        return super().action_quotation_send()
