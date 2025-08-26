from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    attendance_ip_config_ids = fields.One2many(
        'hr.attendance.ip.config',
        'company_id',
        string='Danh sách IP được phép chấm công',
        help='Cấu hình các địa chỉ IP được phép thực hiện chấm công'
    )
    
    attendance_ip_restriction_enabled = fields.Boolean(
        string='Bật kiểm soát IP chấm công',
        default=True,
        help='Tích để bật tính năng kiểm soát IP khi chấm công'
    )
    
    attendance_ip_count = fields.Integer(
        string='Số lượng IP',
        compute='_compute_attendance_ip_count'
    )

    def _compute_attendance_ip_count(self):
        """Tính số lượng IP đã cấu hình"""
        for company in self:
            company.attendance_ip_count = len(company.attendance_ip_config_ids.filtered('active'))

    def action_view_attendance_ip_config(self):
        """Mở form quản lý IP"""
        self.ensure_one()
        return {
            'name': 'Cấu hình IP Chấm công',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.attendance.ip.config',
            'view_mode': 'list,form',
            'domain': [('company_id', '=', self.id)],
            'context': {
                'default_company_id': self.id,
                'search_default_active': 1,
            },
            'target': 'current',
        }