# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
# 03, 11, Uttar, Dhaka
#
#############################################################################
from odoo import fields, models


class StockPicking(models.Model):
    """ Add domain value for inherited fields """
    _inherit = 'stock.picking'

    partner_id = fields.Many2one("res.partner", string='Receive From',
                                 domain="[('state', '=', 'approved')]",
                                 help="We can see the approved partner here")
