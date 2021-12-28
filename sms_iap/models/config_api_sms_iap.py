# -*- coding: utf-8 -*-


from odoo import _, api, models, fields
import requests
from dateutil.relativedelta import relativedelta
import ast
import json
import math
from odoo.exceptions import UserError
from odoo.exceptions import except_orm

class ConfigApiSMSIAP(models.Model):
    _name = 'config.api.sms.iap'

    name = fields.Char(string='Name')
    params_ids = fields.One2many('config.api.sms.iap.params', 'api_id', string='Params')
    description = fields.Text(string='Description')
    type = fields.Selection([('sms', 'SMS'), ('zns', 'ZNS'), ('sms_zns', 'SMS and ZNS')], default='sms', string='Type')

    def action_check_api(self):
        url = self.name
        params = {}
        for i in self.params_ids:
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
        params.update({"PhoneNumber": '99999999999',
                       "MsgContent": 'TEST API'})

        try:
            data = requests.post(url, data=json.dumps(params),
                                   headers={"Content-Type": "application/json", }).text

            message = _("Connection Test Successful!")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            raise UserError(_("Connection failed: " + str(e)))


class ConfigApiSMSIAPParams(models.Model):
    _name = 'config.api.sms.iap.params'

    name = fields.Char(string='Name', default='Params')
    api_id = fields.Many2one('config.api.sms.iap', string='Api')
    key = fields.Char(string='Key')
    value = fields.Text(string='Value')
    note = fields.Text(string='Note')
    type = fields.Selection([('integer', 'Integer'),
                             ('float', 'Float'),
                             ('string', 'String'),
                             ('dict', 'Dict'),
                             ('array', 'Array')], string='Type', default='string')




