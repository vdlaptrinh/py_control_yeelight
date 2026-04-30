# 💡 HƯỚNG DẪN SỬ DỤNG YEELIGHT CONTROLLER

## 📋 Mô tả
Ứng dụng điều khiển đèn Yeelight qua WiFi, cho phép bật/tắt, điều chỉnh độ sáng, nhiệt độ màu và các chế độ nhanh.

---

## 🚀 CÀI ĐẶT

### 1. Clone dự án (nếu chưa có)
```bash
git clone https://github.com/vdlaptrinh/py_control_yeelight.git
cd py_control_yeelight
```

### 2. Cài đặt Python
Đảm bảo bạn đã cài đặt **Python 3.7+**:
```bash
python3 --version
```

### 3. Cài đặt thư viện cần thiết
```bash
pip3 install yeelight
```

Hoặc cài đặt từ file requirements.txt (nếu có):
```bash
pip3 install -r requirements.txt
```

---

## 🖥️ KHỞI CHẠY ỨNG DỤNG

### Cách 1: Chạy trực tiếp file Python
```bash
cd py_control_yeelight
python3 yeelight_gui.py
```

### Cách 2: Sử dụng shortcut (Khuyên dùng)
- Mở Finder, điều hướng đến thư mục `yeelight`
- **Double-click** vào file `run_yeelight.command`
- Nếu báo lỗi permission, chạy lệnh:
```bash
chmod +x /Users/[user]/py_control_yeelight/run_yeelight.command
```

---

## 📖 HƯỚNG DẪN SỬ DỤNG

### Bước 1: Kết nối đèn
1. **Nhập IP đèn**: Nhập địa chỉ IP của đèn Yeelight vào ô "IP đèn"
   - Cách tìm IP: Vào router WiFi hoặc dùng app Yeelight trên điện thoại
   
2. **Hoặc Quét mạng**: Nhấn nút "🔍 Quét mạng" để tự động tìm đèn trong mạng LAN
   
3. **Kết nối**: Nhấn nút "🔌 Kết nối" để thiết lập kết nối

### Bước 2: Điều khiển đèn

#### 🔌 Điều khiển nguồn
- **⚡ BẬT ĐÈN**: Bật đèn
- **🔌 TẮT ĐÈN**: Tắt đèn
- **🔄 ĐẢO TRẠNG THÁI**: Chuyển đổi bật/tắt

#### ☀️ Điều chỉnh độ sáng
- Kéo thanh trượt để chọn độ sáng (0-100%)
- Nhấn "✅ ÁP DỤNG ĐỘ SÁNG" để áp dụng

#### 🌡️ Điều chỉnh nhiệt độ màu
- Kéo thanh trượt để chọn nhiệt độ màu (1700K - 6500K)
  - 1700K: Ánh sáng ấm (vàng)
  - 4000K: Ánh sáng trung tính
  - 6500K: Ánh sáng lạnh (trắng)
- Nhấn "✅ ÁP DỤNG NHIỆT ĐỘ" để áp dụng

#### ⚡ Chế độ nhanh
- **📖 Học tập**: 5000K, 100% độ sáng
- **📚 Đọc sách**: 4000K, 70% độ sáng
- **🌙 Thư giãn**: 2700K, 50% độ sáng
- **🎯 Tập trung**: 6000K, 90% độ sáng

#### 📊 Xem trạng thái
- Nhấn "🔄 CẬP NHẬT TRẠNG THÁI" để xem thông tin hiện tại của đèn

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Yêu cầu mạng
- Đèn Yeelight và máy tính phải **cùng kết nối một mạng WiFi**
- Đảm bảo không bị chặn bởi firewall

### 2. Bật LAN Control trên đèn
- Mở app **Yeelight** trên điện thoại
- Chọn đèn → Cài đặt → **Bật "LAN Control"** (Điều khiển qua mạng LAN)
- ⚠️ Nếu không bật, ứng dụng sẽ không kết nối được!

### 3. Tìm IP đèn
**Cách 1**: Dùng app Yeelight trên điện thoại (Vào thông tin đèn)
**Cách 2**: Dùng nút "🔍 Quét mạng" trong ứng dụng
**Cách 3**: Đăng nhập router WiFi để xem danh sách thiết bị

### 4. Lỗi thường gặp
| Lỗi | Nguyên nhân | Cách khắc phục |
|-----|-------------|----------------|
| Không tìm thấy đèn | Sai mạng WiFi | Kiểm tra cả đèn và máy cùng mạng |
| Lỗi kết nối | Chưa bật LAN Control | Bật LAN Control trong app Yeelight |
| Timeout | Đèn xa router | Đưa đèn gần router hơn |
| Không quét được | Firewall chặn | Tắt firewall hoặc thêm ngoại lệ |

### 5. Thoát ứng dụng
- Đóng cửa sổ ứng dụng để thoát
- Không cần thao tác tắt đèn, đèn sẽ giữ nguyên trạng thái

---

## 🛠️ CẤU TRÚC FILE

```
py_control_yeelight/
├── yeelight_controller.py    # Phiên bản dòng lệnh (CLI)
├── yeelight_gui.py          # Phiên bản giao diện (GUI) ⭐
├── run_yeelight.command     # Shortcut chạy ứng dụng
└── README.md               # File hướng dẫn này
```

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, hãy kiểm tra:
1. Đèn đã bật nguồn chưa?
2. Đã bật "LAN Control" chưa?
3. Cùng mạng WiFi chưa?
4. IP đèn có đúng không?

---

**Chúc bạn sử dụng ứng dụng thành công! 🎉**
