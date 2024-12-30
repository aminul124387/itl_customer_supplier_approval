# -*- coding: utf-8 -*-
#############################################################################
#
# ITL Bangladesh Limited
# 03, 11, Uttar, Dhaka
#############################################################################
from odoo import fields, models


class PurchaseOrder(models.Model):
    """Add domain value for field partner_id in purchase order model """
    _inherit = 'purchase.order'

    partner_id = fields.Many2one("res.partner", string='Vendor',
                                 domain="[('state', '=', 'approved')]",
                                 help="We can see the approved partner here")
