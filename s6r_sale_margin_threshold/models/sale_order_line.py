# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import _, api, models, fields
from odoo.tools.float_utils import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    minimum_margin_violation = fields.Boolean(
        compute="_compute_minimum_margin_violation",
        store=True,
    )

    @api.depends("margin_percent",
                 "order_id.state",
                 "company_id.blocking_transaction_order",
                 "company_id.sale_min_margin_percent")
    def _compute_minimum_margin_violation(self):
        for line in self:
            if not line.product_id or line.order_id.state not in ("draft", "sent"):
                line.minimum_margin_violation = False
                continue
            line.minimum_margin_violation = (
                    line.company_id.blocking_transaction_order and
                    float_compare(
                        line.margin_percent,
                        line.company_id.sale_min_margin_percent,
                        precision_digits=2
                    ) < 0
            )

    @api.onchange("margin_percent")
    def _onchange_margin_alert(self):
        blocking_transaction_order = self.company_id.blocking_transaction_order
        min_margin = self.company_id.sale_min_margin_percent
        if (self.product_id and blocking_transaction_order and
                float_compare(
                    self.margin_percent, min_margin, precision_digits=2
                ) < 0):
            return {
                "warning": {
                    "title": _("Insufficient margin"),
                    "message": _(
                        "%(product)s: The margin (%(margin_percent).2f%%) "
                        "is less than the minimum allowed margin (%(min_margin).2f%%)."
                    ) % {"product": self.product_id.display_name,
                         "margin_percent": self.margin_percent * 100,
                         "min_margin": min_margin * 100},
                }
            }
