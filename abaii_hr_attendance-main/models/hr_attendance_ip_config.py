from odoo import models, fields, api
from odoo.exceptions import ValidationError
import ipaddress


class HrAttendanceIpConfig(models.Model):
    _name = 'hr.attendance.ip.config'
    _description = 'Cấu hình IP Chấm công'
    _order = 'sequence, name'

    name = fields.Char(
        string='Tên WiFi',
        required=True,
        help='Tên mô tả cho điểm WiFi (VD: WiFi Tầng 1, WiFi Phòng họp)'
    )
    
    ip_address = fields.Char(
        string='Địa chỉ IP',
        required=True,
        help='Địa chỉ IP được phép chấm công'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        required=True,
        default=lambda self: self.env.company
    )
    
    active = fields.Boolean(
        string='Kích hoạt',
        default=True,
        help='Bỏ tích để tạm thời vô hiệu hóa IP này'
    )
    
    description = fields.Text(
        string='Mô tả',
        help='Mô tả chi tiết về điểm WiFi này'
    )
    
    sequence = fields.Integer(
        string='Thứ tự',
        default=10,
        help='Thứ tự hiển thị'
    )

    @api.constrains('ip_address')
    def _check_ip_address(self):
        """Kiểm tra định dạng IP address"""
        for record in self:
            if record.ip_address:
                try:
                    ipaddress.ip_address(record.ip_address)
                except ValueError:
                    raise ValidationError(
                        f'Địa chỉ IP "{record.ip_address}" không hợp lệ. '
                        'Vui lòng nhập đúng định dạng IP (VD: 192.168.1.100)'
                    )

    @api.constrains('ip_address', 'company_id')
    def _check_unique_ip(self):
        """Kiểm tra IP không bị trùng lặp trong cùng công ty"""
        for record in self:
            if record.ip_address and record.company_id:
                existing = self.search([
                    ('ip_address', '=', record.ip_address),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id),
                    ('active', '=', True)
                ])
                if existing:
                    raise ValidationError(
                        f'Địa chỉ IP "{record.ip_address}" đã được sử dụng. '
                        'Mỗi IP chỉ được cấu hình một lần trong cùng công ty.'
                    )

    def name_get(self):
        """Hiển thị tên và IP trong dropdown"""
        result = []
        for record in self:
            name = f'{record.name} ({record.ip_address})'
            result.append((record.id, name))
        return result

    @api.model
    def is_ip_allowed(self, ip_address, company_id=None):
        """
        Kiểm tra IP có được phép chấm công không
        
        Args:
            ip_address (str): IP cần kiểm tra
            company_id (int): ID công ty (mặc định là công ty hiện tại)
            
        Returns:
            bool: True nếu IP được phép, False nếu không
        """
        if not company_id:
            company_id = self.env.company.id
            
        allowed_ips = self.search([
            ('company_id', '=', company_id),
            ('active', '=', True)
        ])
        
        return ip_address in allowed_ips.mapped('ip_address')