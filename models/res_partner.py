# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
# 03, 11, Uttar, Dhaka
#
#############################################################################
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """ This class inherited to add some extra fields and functions in the
        Partner """
    _inherit = 'res.partner'

    customer_supplier = fields.Char(string="Customer Supplier Id",
                                    domain="[('state', '=', 'validated')]",
                                    help="Unique id for partners")
    hide_button = fields.Boolean(default=False, string='Hide Approve Button',
                                 help="TChecking the box enables to hide the "
                                      "approve button")
    hide_button_validate = fields.Boolean(default=False,
                                          string='Hide Validate Button',
                                          help="This boolean field is used to "
                                               "hide the Validate button")
    state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'),
                              ('approved', 'Approved')], default='draft',
                             string='Status',
                             help="The status of contacts")
    # Account field
    property_account_receivable_id = fields.Many2one('account.account', required=False)
    property_account_payable_id = fields.Many2one('account.account', required=False)

    _sql_constraints = [
        ('id_uniq', 'unique (customer_supplier)', 'The partner id unique !')
    ]

    def action_validate(self):
        """  Method of button validate to validate customer or supplier """
        for rec in self:
            rec.hide_button_validate = True
            rec.write({'state': 'validated'})

    def action_approve(self):
        """ Method of button approve to approve customer or supplier """
        for rec in self:
            rec.hide_button = True
            rec.write({'state': 'approved'})

    def write(self, values):
        """ To raise validation error when validator changes the state"""
        if 'state' in values:
            new_state = values.get('state')
            if new_state == 'approved' or self.state == 'approved':
                if not self.env.user.has_group(
                        'itl_customer_supplier_approval.'
                        'customer_supplier_approval_group_approval'):
                    raise ValidationError(
                        _("Only Manager can perform that move!"))
            if new_state == 'validated' or self.state == 'draft':
                if not self.env.user.has_group(
                        'itl_customer_supplier_approval.'
                        'customer_supplier_approval_group_validation'):
                    raise ValidationError(
                        _("Only Managers can perform that move!"))
        return super().write(values)
