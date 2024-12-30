# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
# 03, 11, Uttar, Dhaka
#############################################################################
from odoo import fields, models


class SaleOrder(models.Model):
    """ Add domain value for inherited fields """
    _inherit = 'sale.order'

    partner_id = fields.Many2one("res.partner", string='Customer',
                                 domain="[('state', '=', 'approved')]",
                                 help="We can see the approved partner here")
