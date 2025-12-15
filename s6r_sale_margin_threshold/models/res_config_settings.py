# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    blocking_transaction_order = fields.Boolean(
        related='company_id.blocking_transaction_order',
        readonly=False,
        help="If enabled, sales orders with margins below the minimum threshold "
             "cannot be confirmed or sent.",
    )
    sale_min_margin_percent = fields.Float(
        related='company_id.sale_min_margin_percent',
        readonly=False,
        help="Minimum allowed margin percentage per sales order line.",

    )

    def set_values(self):
        res = super().set_values()
        if not self.blocking_transaction_order and self.sale_min_margin_percent:
            self.sale_min_margin_percent = 0.0
        return res
