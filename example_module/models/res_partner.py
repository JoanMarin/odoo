# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_count = fields.Integer(
        string="Vehicle Count", compute="_compute_vehicle_count"
    )

    def _compute_vehicle_count(self):
        for record in self:
            record.vehicle_count = self.env["my.company.vehicle"].search_count(
                [("partner_id", "=", record.id)]
            )
