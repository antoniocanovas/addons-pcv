# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class EventEvent(models.Model):
    _inherit = "event.event"

    event_registrations_open = fields.Boolean(compute=False)

