# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
# 03, 11, Uttar, Dhaka
#
#############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class ResPartner(models.Model):
    """ This class inherited to add some extra fields and functions in the
        Partner """
    _inherit = 'res.partner'

    customer_supplier = fields.Char(string="Customer Supplier Id",
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

    bd_sales_person = fields.Many2one('hr.employee', string="BD Sales Person",
                                      help="Assigned sales person from the Sales department.")

    manager_id = fields.Many2one(
        'hr.employee',
        string="Manager Name",
        compute="_compute_manager_id",
        store=True,
        help="Manager of the selected BD Sales Person."
    )

    @api.depends('bd_sales_person')
    def _compute_manager_id(self):
        """Compute the manager based on the selected BD Sales Person."""
        for record in self:
            if record.bd_sales_person and record.bd_sales_person.department_id:
                record.manager_id = record.bd_sales_person.department_id.manager_id
            else:
                record.manager_id = False



    _sql_constraints = [
        ('id_uniq', 'unique (customer_supplier)', 'The partner id unique !')
    ]

    def action_validate(self):
        """ Method of button validate to validate customer or supplier and notify the Sales department manager """
        for rec in self:
            # Hide validate button and update status
            rec.hide_button_validate = True
            rec.write({'state': 'validated'})

            # Find the Sales department and its manager
            sales_department = self.env['hr.department'].search([('name', '=', 'Sales')], limit=1)
            if not sales_department or not sales_department.manager_id:
                raise UserError("Sales department or its manager is not configured.")

            # Get the email template
            template = self.env.ref('itl_finance_module.mail_template_sales_team_lead')
            if not template:
                raise UserError("Mail template for Sales Team Lead is not found.")

            # Prepare custom email values, including the subject
            email_values = {
                'email_to': sales_department.manager_id.work_email,
                'subject': f"New Customer Approval Required: {rec.name}",
            }

            # Send the email using the template
            try:
                template.send_mail(rec.id, email_values=email_values, force_send=True)
            except Exception as e:
                raise ValidationError(f"An error occurred while sending the email: {str(e)}")

    # def action_approve(self):
    #     """ Method of button approve to approve customer or supplier """
    #     for rec in self:
    #         rec.hide_button = True
    #         rec.write({'state': 'approved'})

    def action_approve(self):
        """ Method of button approve to approve customer or supplier and notify employees who should get customer approval mails """
        for rec in self:
            # Hide the approve button and update the state
            rec.hide_button = True
            rec.write({'state': 'approved'})

            # Find employees who have is_mail_get_from_customer set to True
            employees = self.env['hr.employee'].search([('is_mail_get_from_customer', '=', True)])
            if not employees:
                raise UserError(
                    "No employees are configured to receive approval emails. Please set the field 'Is Need to Get Mail from Customer Approve' for at least one employee.")

            # Get the email template
            template = self.env.ref('itl_finance_module.mail_template_finance_team')
            if not template:
                raise UserError("Mail template for Sales Team Lead is not found.")

            # Prepare the email recipients
            email_recipients = ','.join(employees.mapped('work_email'))
            if not email_recipients:
                raise UserError("Selected employees do not have valid email addresses.")

            # Send the email to the selected employees
            try:
                email_values = {
                    'email_to': email_recipients,
                    'subject': f"Customer/Supplier Approved: {rec.name}",
                }
                template.send_mail(rec.id, email_values=email_values, force_send=True)
            except Exception as e:
                raise ValidationError(f"An error occurred while sending the email: {str(e)}")

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
