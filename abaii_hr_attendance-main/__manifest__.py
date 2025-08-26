{
    'name': 'Kiểm soát IP Chấm công',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Kiểm soát chấm công theo địa chỉ IP văn phòng',
    'description': """
Kiểm soát IP Chấm công
======================
Module này cho phép kiểm soát chấm công dựa trên địa chỉ IP để đảm bảo 
nhân viên chỉ có thể chấm công từ WiFi văn phòng.

Tính năng chính:
- Quản lý danh sách IP được phép chấm công
- Kiểm tra IP khi nhân viên check-in/check-out
- Giao diện quản lý IP trong cài đặt công ty
- Thông báo lỗi tiếng Việt khi IP không hợp lệ
    """,
    'author': 'Ricky Kien',
    'website': 'https://abaii.vn',
    'depends': ['hr_attendance', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_ip_config_views.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}