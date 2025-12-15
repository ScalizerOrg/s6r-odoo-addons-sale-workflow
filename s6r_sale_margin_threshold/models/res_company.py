# Copyright 2025 Scalizer (<https://www.scalizer.fr>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    blocking_transaction_order = fields.Boolean(
        string="Block Sales Orders Below Minimum Margin",
        default=False,
    )

    sale_min_margin_percent = fields.Float(
        string="Minimum margin (%)",
        default=0.0,
        help="Minimum margin percentage required to confirm or send a sales order.",
    )
