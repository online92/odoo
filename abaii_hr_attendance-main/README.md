# 🏢 Module Kiểm soát IP Chấm công

Module Odoo 18.0 cho phép kiểm soát chấm công dựa trên địa chỉ IP để đảm bảo nhân viên chỉ có thể chấm công từ WiFi văn phòng.

## 🚀 Tính năng chính

- ✅ **Quản lý danh sách IP**: Cấu hình nhiều địa chỉ IP được phép chấm công
- ✅ **Kiểm tra IP tự động**: Tự động lấy và kiểm tra IP khi nhân viên chấm công
- ✅ **Giao diện tiếng Việt**: Hoàn toàn bằng tiếng Việt, thân thiện với người Việt
- ✅ **Thông báo lỗi rõ ràng**: Hiển thị thông báo tiếng Việt khi IP không hợp lệ
- ✅ **Quản lý linh hoạt**: Bật/tắt từng IP, thêm mô tả cho mỗi điểm WiFi
- ✅ **Tích hợp sẵn**: Tích hợp vào Company Settings, không ảnh hưởng flow hiện có

## 📋 Yêu cầu hệ thống

- **Odoo**: 18.0+
- **Python**: 3.8+
- **Dependencies**: `hr_attendance`, `base`

## 📦 Cài đặt

### 1. Download module
```bash
git clone <repository-url> /path/to/odoo/addons/hr_attendance_ip_restriction
```

### 2. Cập nhật Odoo
```bash
# Restart Odoo service
sudo systemctl restart odoo

# Hoặc nếu chạy development mode
./odoo-bin -u hr_attendance_ip_restriction -d your_database
```

### 3. Cài đặt module
1. Vào **Apps → Update Apps List**
2. Tìm kiếm **"Kiểm soát IP Chấm công"**
3. Nhấn **Install**

## ⚙️ Cấu hình

### Bước 1: Cấu hình IP văn phòng
1. Vào **Cài đặt → Công ty**
2. Chọn tab **"IP Văn phòng"**
3. Tích **"Bật kiểm soát IP chấm công"**
4. Thêm danh sách IP được phép:

| Tên WiFi | Địa chỉ IP | Mô tả | Kích hoạt |
|----------|------------|-------|-----------|
| WiFi Tầng 1 | 192.168.1.100 | WiFi chính tầng 1 | ✅ |
| WiFi Tầng 2 | 192.168.1.101 | WiFi tầng 2 | ✅ |
| WiFi Phòng họp | 192.168.1.102 | WiFi phòng họp lớn | ✅ |

### Bước 2: Test chấm công
1. Nhân viên kết nối WiFi văn phòng
2. Thực hiện chấm công bình thường
3. Nếu IP đúng → ✅ Chấm công thành công
4. Nếu IP sai → ❌ Hiển thị thông báo lỗi

## 📱 Giao diện

### Company Settings - Tab IP Văn phòng
```
┌─── Cài đặt chung ───────────────────────────┐
│ ☑️ Bật kiểm soát IP chấm công                │
│ 📊 Số IP đã cấu hình: 3                     │
└─────────────────────────────────────────────┘

┌─── Danh sách IP được phép chấm công ───────┐
│ [+ Thêm dòng]                               │
│                                             │
│ WiFi Tầng 1    | 192.168.1.100 | Mô tả | ✅ │
│ WiFi Tầng 2    | 192.168.1.101 | Mô tả | ✅ │
│ WiFi Phòng họp | 192.168.1.102 | Mô tả | ✅ │
└─────────────────────────────────────────────┘
```

### Thông báo lỗi khi IP không hợp lệ
```
❌ Không thể chấm công từ vị trí này!

Bạn chỉ có thể chấm công từ WiFi văn phòng.
IP hiện tại: 192.168.0.50
IP được phép: 192.168.1.100, 192.168.1.101

Vui lòng kết nối WiFi văn phòng và thử lại.
```

## 🛠️ Cấu trúc module

```
hr_attendance_ip_restriction/
├── __manifest__.py                     # Manifest module
├── README.md                          # File này
├── models/
│   ├── __init__.py                    # Import models
│   ├── hr_attendance_ip_config.py     # Model quản lý IP
│   ├── res_company.py                 # Extend company
│   └── hr_attendance.py               # Override chấm công logic
├── views/
│   ├── hr_attendance_ip_config_views.xml  # Giao diện quản lý IP
│   └── res_company_views.xml              # Tab IP trong company
└── security/
    └── ir.model.access.csv            # Phân quyền truy cập
```

## 🔧 Troubleshooting

### Vấn đề: IP hiển thị 127.0.0.1 thay vì IP thực
**Nguyên nhân**: Server đang chạy sau proxy/load balancer

**Giải pháp**:
1. Kiểm tra log Odoo: `tail -f odoo.log | grep "Detected client IP"`
2. Cấu hình proxy headers đúng cách
3. Thêm IP thực vào danh sách tạm thời

### Vấn đề: Không chấm công được sau khi cài module
**Nguyên nhân**: Chưa cấu hình IP hoặc chưa bật tính năng

**Giải pháp**:
1. Vào Company Settings → Tab "IP Văn phòng"
2. Tích "Bật kiểm soát IP chấm công"
3. Thêm IP hiện tại vào danh sách

### Vấn đề: Cài đặt module bị lỗi
**Nguyên nhân**: Dependencies chưa đủ hoặc file bị lỗi

**Giải pháp**:
1. Kiểm tra module `hr_attendance` đã cài chưa
2. Check syntax các file Python/XML
3. Restart Odoo và thử lại

## 📊 Logging & Monitoring

Module ghi log chi tiết để debug:

```bash
# Theo dõi IP detection
tail -f odoo.log | grep "Check IP restriction"

# Theo dõi validation errors  
tail -f odoo.log | grep "IP restriction"

# Debug headers
tail -f odoo.log | grep "Detected client IP"
```

## 🔐 Bảo mật

- ✅ **Validation IP format**: Kiểm tra định dạng IP hợp lệ
- ✅ **No duplicate IPs**: Không cho phép IP trùng lặp trong cùng công ty
- ✅ **Role-based access**: Phân quyền theo HR Manager/User
- ✅ **Audit logging**: Ghi log tất cả hoạt động kiểm tra IP

## 📈 Performance

- 🚀 **Lightweight**: Ít impact đến performance chấm công
- 🚀 **Fast IP lookup**: Kiểm tra IP nhanh với database index
- 🚀 **Minimal overhead**: Chỉ check IP khi thực sự cần thiết

## 🤝 Đóng góp

1. Fork repository
2. Tạo branch tính năng: `git checkout -b feature/ten-tinh-nang`
3. Commit thay đổi: `git commit -am 'Thêm tính năng X'`
4. Push branch: `git push origin feature/ten-tinh-nang`
5. Tạo Pull Request

## 📄 License

Module này được phát hành dưới [LGPL-3 License](https://www.gnu.org/licenses/lgpl-3.0.html).

## 📞 Hỗ trợ

- **Issues**: Tạo issue tại GitHub repository
- **Email**: support@yourcompany.com
- **Documentation**: [Wiki page](link-to-wiki)

---

**Made with ❤️ for Vietnamese Odoo Community**

> 💡 **Tip**: Module này được thiết kế đặc biệt cho doanh nghiệp Việt Nam với giao diện hoàn toàn tiếng Việt và phù hợp với cách sử dụng thực tế.