# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models, fields
import requests
from dateutil.relativedelta import relativedelta
import ast
import json
import math
from odoo.exceptions import UserError
DEFAULT_ENDPOINT = 'https://iap-sms.odoo.com'


class SmsApi(models.AbstractModel):
    _inherit = 'sms.api'

    @api.model
    def _contact_iap(self, local_endpoint, params):
        # account = self.env['iap.account'].get('sms')
        # params['account_token'] = account.account_token
        # lấy url và params theo cấu hình
        config_api_sms = self.env['config.api.sms.iap'].sudo().search([('type', '=', 'sms')], limit=1)
        messages = params['messages']

        if config_api_sms:
            result = []
            url = config_api_sms.name
            params = {}
            for i in config_api_sms.params_ids:
                value = ''
                if i.type == 'string':
                    value = str(i.value)
                elif i.type == 'int':
                    value = int(i.value)
                elif i.type == 'float':
                    value = float(i.value)
                elif i.type == 'dict':
                    value = json.loads(i.value)
                elif i.type == 'array':
                    if '[' in i.value:
                        value = ast.literal_eval(i.value)
                    else:
                        value = i.value.split(',')
                params.update({i.key: value})
            for mes in messages:
                params.update({"PhoneNumber": mes['number'],
                               "MsgContent": mes['content']})

                data = requests.post(url, data=json.dumps(params),
                                       headers={"Content-Type": "application/json", }).text
                data = json.loads(data)
                data['sms_id'] = mes['res_id']
                result.append(data)

            # endpoint = self.env['ir.config_parameter'].sudo().get_param('sms.endpoint', DEFAULT_ENDPOINT)
            # TODO PRO, the default timeout is 15, do we have to increase it ?
            return result
        else:
            raise UserError(_("Please configure the API!"))

