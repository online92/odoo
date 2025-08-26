from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    ip_address = fields.Char(
        string='Địa chỉ IP',
        help='Địa chỉ IP khi thực hiện chấm công'
    )

    def _get_client_ip(self):
        """Lấy IP address của client"""
        try:
            # Thử lấy từ request context trước
            request = self.env.context.get('request')
            if not request:
                # Thử import request từ odoo.http
                try:
                    from odoo.http import request as http_request
                    if http_request and hasattr(http_request, 'httprequest'):
                        request = http_request
                except:
                    pass
            
            if request and hasattr(request, 'httprequest'):
                # Kiểm tra các header thường dùng cho proxy/load balancer
                environ = request.httprequest.environ
                ip = (
                    environ.get('HTTP_X_FORWARDED_FOR') or
                    environ.get('HTTP_X_REAL_IP') or  
                    environ.get('HTTP_CLIENT_IP') or
                    environ.get('HTTP_X_FORWARDED') or
                    environ.get('HTTP_FORWARDED_FOR') or
                    environ.get('HTTP_FORWARDED') or
                    environ.get('REMOTE_ADDR') or
                    request.httprequest.remote_addr or
                    '127.0.0.1'
                )
                
                # Nếu có nhiều IP (qua proxy), lấy IP đầu tiên
                if ',' in str(ip):
                    ip = str(ip).split(',')[0].strip()
                    
                # Log để debug
                _logger.info(f'Detected client IP: {ip} from headers: {dict(environ)}')
                return str(ip)
                
        except Exception as e:
            _logger.error(f'Error getting client IP: {e}')
            
        # Fallback cho trường hợp không lấy được IP
        _logger.warning('Cannot detect client IP, using localhost')
        return '127.0.0.1'

    def _check_ip_restriction(self, employee_id):
        """
        Kiểm tra IP có được phép chấm công không
        
        Args:
            employee_id (int): ID nhân viên
            
        Returns:
            str: IP address nếu hợp lệ
            
        Raises:
            UserError: Nếu IP không được phép
        """
        current_ip = self._get_client_ip()
        employee = self.env['hr.employee'].browse(employee_id)
        company = employee.company_id
        
        # Log để debug
        _logger.info(f'Check IP restriction: Employee {employee.name}, Current IP: {current_ip}, Company: {company.name}')
        
        # Nếu công ty không bật kiểm soát IP thì cho phép
        if not company.attendance_ip_restriction_enabled:
            _logger.info(f'IP restriction disabled for company {company.name}')
            return current_ip
            
        # Kiểm tra có IP nào được cấu hình không
        ip_config_model = self.env['hr.attendance.ip.config']
        allowed_ips = ip_config_model.search([
            ('company_id', '=', company.id),
            ('active', '=', True)
        ])
        
        if not allowed_ips:
            # Nếu chưa cấu hình IP nào thì cho phép (để tránh block khi mới cài đặt)
            _logger.warning(f'Chưa cấu hình IP cho công ty {company.name}. Cho phép chấm công từ IP {current_ip}')
            return current_ip
            
        # Kiểm tra IP hiện tại có trong danh sách cho phép không
        if current_ip not in allowed_ips.mapped('ip_address'):
            allowed_ip_list = ', '.join(allowed_ips.mapped('ip_address'))
            raise UserError(
                f'❌ Không thể chấm công từ vị trí này!\n\n'
                f'Bạn chỉ có thể chấm công từ WiFi văn phòng.\n'
                f'IP hiện tại: {current_ip}\n'
                f'IP được phép: {allowed_ip_list}\n\n'
                f'Vui lòng kết nối WiFi văn phòng và thử lại.'
            )
            
        return current_ip

    @api.model
    def create(self, vals):
        """Override create để kiểm tra IP khi tạo attendance"""
        if 'employee_id' in vals:
            # Kiểm tra IP và lưu vào record
            client_ip = self._check_ip_restriction(vals['employee_id'])
            vals['ip_address'] = client_ip
            
        return super(HrAttendance, self).create(vals)

    def write(self, vals):
        """Override write để kiểm tra IP khi cập nhật attendance"""
        # Chỉ kiểm tra IP khi thay đổi trạng thái check-in/out
        if any(field in vals for field in ['check_in', 'check_out']):
            for record in self:
                if record.employee_id:
                    client_ip = self._check_ip_restriction(record.employee_id.id)
                    vals['ip_address'] = client_ip
                    
        return super(HrAttendance, self).write(vals)