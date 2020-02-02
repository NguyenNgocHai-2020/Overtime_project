from odoo import fields, models , api
from datetime import datetime

class overtime_management(models.Model):
    _name = "overtime.management"
    _description = "Phiếu làm thêm"
    # _rec_name = 'subject'

    subject = fields.Char(string='Mô tả', required=True)
    department = fields.Many2one(comodel_name='hr.department', string='Phòng ban',required=True)
    date = fields.Date(string='Ngày làm thêm', required=True, default=datetime.today())
    ot_rate = fields.Float("Tỷ lệ làm thêm", required=True)
    ot_sum = fields.Float("Tổng thời gian làm thêm", compute='_compute_ot_sum', store=True)
    reason = fields.Char(string='Lý do làm thêm', size=100, required=True)
    detail = fields.One2many(comodel_name='overtime.detail', inverse_name='management', string="Chi tiết làm thêm")
    status = fields.Selection(string="Trạng thái", selection=[('draft', 'Nháp'),
                                                             ('done', 'Đã phê duyệt'),
                                                             ('reject', 'Bị từ chối')], default='draft')

    def action_approved(self):
        for rec in self:
            if rec.detail:
                rec.detail.write({'status': 'done'})
            rec.status = 'done'

    def action_reject(self):
        for rec in self:
            if rec.detail:
                rec.detail.write({'status': 'reject'})
            rec.status = 'reject'

    @api.depends('ot_sum', 'detail.ot_time')
    def _compute_ot_sum(self):
        for record in self:
            if record.detail:
                record.ot_sum = sum([x.ot_time for x in record.detail])
            else:
                record.ot_sum = 0.0



