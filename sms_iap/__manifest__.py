# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SMS IAP',
    'version': '2.2.1',
    'category': 'Hidden/Tools',
    'summary': 'SMS Text Messaging',
    'description': """
This module gives a framework for SMS text messaging
----------------------------------------------------

The service is provided by the In App Purchase Odoo platform.
""",
    'depends': [
        'sms'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/config_api_sms_iap.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
