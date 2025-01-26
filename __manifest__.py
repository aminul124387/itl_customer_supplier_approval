# -*- coding: utf-8 -*-
#############################################################################
# ITL Bangladesh Limited
# Author: ITL BD
#############################################################################
{
    'name': 'Customer/Supplier Approval',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """This module allows users to validate or approve contacts """,
    'description': """By this module, you can grant access to users to validate
                      or approve partners. Then you will be able to select only
                      approved partners on sales orders, purchase orders, 
                      invoices, bills or delivery orders.""",
    'author': ' Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'contacts', 'stock', 'sale_management', 'account',
                'purchase', ],
    'data': [
        'security/customer_supplier_approval_groups.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',

        # 'data/signup_mail_templates.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
