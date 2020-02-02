from odoo import fields, models ,api, exceptions
from datetime import datetime

class overtime_detail(models.Model):
    _name = 'overtime.detail'
    _description = "Chi tiết làm thêm"
    _rec_name = 'employee'

    employee = fields.Many2one(comodel_name='hr.employee', string="Tên nhân viên", required=True)
    department = fields.Many2one(comodel_name='hr.department', string='Phòng ban', required=True)
    date = fields.Date(string='Ngày làm thêm', related='management.date', required=True)
    ot_rate = fields.Float(string='Tỷ lệ làm thêm', related='management.ot_rate')
    ot_time = fields.Float(string="Số giờ làm thêm", required=True)
    reason = fields.Char(string="Lý do làm thêm", size=100, required=True, related='management.reason')
    status = fields.Selection(string='Trạng thái', selection=[('draft', 'Nháp'),
                                                             ('wait', 'Chờ phê duyệt'),
                                                             ('done', 'Đã phê duyệt'),
                                                             ('reject', 'Bị từ chối')], default='draft')

    management = fields.Many2one(comodel_name='overtime.management', string='Phiếu làm thêm')

    @api.constrains('ot_time')
    def _check_ot_time(self):
        for record in self:
            if record.ot_time < 0.5 or record.ot_time > 16:
                raise exceptions.ValidationError("Số giờ làm thêm phải lớn hơn 0.5 giờ và nhỏ hơn 16 giờ")


    def change_wait(self):
        return self.write({'status': 'wait'})














