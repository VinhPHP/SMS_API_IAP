# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SMS(models.Model):
    _inherit = 'sms.sms'

    failure_type = fields.Selection([
        ('509', 'Brandname chưa được khai báo'),
        ('399', 'MT của đối tác bị lặp'),
        ('398', 'Không tìm thấy đối tác'),
        ('397', 'Không tìm thấy nhà cung cấp'),
        ('396', 'Không tìm thấy phiên dịch vụ'),
        ('395', 'Địa chỉ IP không được đăng ký'),
        ('394', 'Đối tác không tìm thấy với User gửi'),
        ('393', 'Sai account hoặc password gửi tin'),
        ('392', 'Không tìm thấy Telcos, số điện thoại bị sai'),
        ('359', 'Phiên không tồn tại hoặc chưa được kích hoạt'),
        ('360', 'Số điện thoại có trong danh sách từ chối nhận tin'),
        ('357', 'Dịch vụ không tồn tại hoặc chưa được kích hoạt'),
        ('356', 'Mã dịch vụ để trống'),
        ('253', 'Thêm mới vào bảng Concentrator bị sai'),
        ('304', 'MT gửi lặp (cùng 1 nội dung gửi tới 1 số điện thoại trong thời gian ngắn)'),
        ('511', 'Chưa khai báo SessionPrefix'),
        ('510', 'Không được phép gửi MT chủ động'),
        ('515', 'Độ dài vượt quá quy định của Telcos'),
        ('530', 'Từ khóa bị chặn bởi Telcos (Keyword was block by Telco)'),
        ('535', 'Số Điện thoại 11 số đã chuyển về 10 số'),
        ('536', 'Mẫu Template phải bắt đầu bằng [QC] hoặc (QC)'),
        ('537', 'Template chưa được khai báo'),
        ('0', 'Gửi thành công'),
    ], copy=False)



    def _postprocess_iap_sent_sms(self, iap_results, failure_reason=None, unlink_failed=False, unlink_sent=False):
        todelete_sms_ids = []
        if unlink_failed:
            todelete_sms_ids += [item['sms_id'] for item in iap_results if item['StatusCode'] != '0']
        if unlink_sent:
            todelete_sms_ids += [item['sms_id'] for item in iap_results if item['StatusCode'] == '0']

        for sms in iap_results:
            if sms['StatusCode'] != '0' and not unlink_failed:
                self.env['sms.sms'].sudo().browse(sms['sms_id']).write({
                    'state': 'error',
                    'failure_type': sms['StatusCode'],
                })
            if sms['StatusCode'] != '0' and not unlink_sent:
                self.env['sms.sms'].sudo().browse(sms['sms_id']).write({
                    'state': 'sent',
                    'failure_type': False,
                })
            notifications = self.env['mail.notification'].sudo().search([
                ('notification_type', '=', 'sms'),
                ('sms_id', '=', sms['sms_id']),
                ('notification_status', 'not in', ('sent', 'canceled')),
            ])
            if notifications:
                notifications.write({
                    'notification_status': 'sent' if sms['StatusCode'] == '0' else 'exception',
                    'failure_type': sms['StatusCode'],
                    'failure_reason': failure_reason if failure_reason else False,
                })
        self.mail_message_id._notify_message_notification_update()

        if todelete_sms_ids:
            self.browse(todelete_sms_ids).sudo().unlink()
