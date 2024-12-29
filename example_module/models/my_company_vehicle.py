# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class MyCompanyVehicle(models.Model):
    _name = "my.company.vehicle"
    _description = "Vehicles"

    name = fields.Char(string="Name", required=True)
    license_plate = fields.Char(string="License Plate", required=True)
    fuel_type = fields.Selection(
        selection=[
            ("gasoline", "Gasoline"),
            ("diesel", "Diesel"),
            ("electric", "Electric"),
        ],
        string="Fuel Type",
    )
    mileage = fields.Float(string="Mileage")
    last_service_date = fields.Date(string="Last Service Date")
    needs_service = fields.Boolean(
        string="Needs Service", compute="_compute_needs_service", store=True
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contact")

    @api.depends("mileage", "last_service_date")
    def _compute_needs_service(self):
        for record in self:
            service_due = (
                record.last_service_date
                and record.last_service_date <= date.today() - timedelta(days=180)
            )
            record.needs_service = record.mileage > 20000 or service_due

    @api.onchange("fuel_type")
    def _onchange_fuel_type(self):
        if self.fuel_type == "electric":
            self.mileage = 0

    @api.model
    def create(self, vals):
        if "license_plate" in vals and self.search(
            [("license_plate", "=", vals["license_plate"])]
        ):
            raise ValidationError(
                _("Vehicle with license plate %s already exists.")
                % vals["license_plate"]
            )

        return super(MyCompanyVehicle, self).create(vals)

    def action_schedule_service(self):
        raise ValidationError(_("Button without function."))
