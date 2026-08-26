# Danh Sách Tickets: OKF v2.3 Dual-Engine Technical Standards Pipeline

> **Căn cứ:** [Đặc tả Kỹ thuật SPEC-OKF-V2-3-DUAL-ENGINE](../../specs/spec-okf-v2-3-dual-engine-pipeline.md) & [ADR 0034](../../../../docs/adr/0034-okf-v2-3-dual-engine-technical-standards.md)
> **Quy tắc thực thi:** Chỉ thực hiện các ticket nằm ở **Biên giới (Frontier)** — là những ticket không bị chặn hoặc tất cả blockers của nó đã hoàn thành `[x]`.

---

## Ticket 1: Xây dựng Bộ Công Cụ Tự Động Hóa Auto-Compositor & Table Matrix Builder

**Nghiệp vụ cần làm:**  
Xây dựng công cụ CLI tự động hóa cho Spoke/Platform (`scripts/modernize_annex_engine.py`) có khả năng:
1. Quét DOCX/PDF để tự động phát hiện các sơ đồ đa nhánh và ghép thành 1 file ảnh composite đơn nhất (`hinh_*.png`) căn giữa trên nền trắng với nhãn phụ nhúng trực tiếp.
2. Tự động chuyển đổi bảng tra đa chiều thành Markdown GFM, bảo toàn $100\%$ các cột, tự động xử lý các ô giá trị kép (`+`/`-`) bằng thẻ `<br>`, và tách chú thích chân bảng.
3. Tự động nhận diện công thức toán để xuất ra KaTeX khối `$$ ... \tag{X.Y} $$`.

**Bị chặn bởi:** Không có — Biên giới Frontier (Bắt đầu ngay).

- [x] Tạo module `scripts/modernize_annex_engine.py` hỗ trợ các lệnh `composite-figures`, `build-matrix-tables`, `convert-math`.
- [x] Thử nghiệm chạy thành công trên dữ liệu mẫu của TCVN 2737:2023.
- [x] Tích hợp kiểm tra tự động vào `validate_legal_spoke.py`.

---

## Ticket 2: Hiện đại hóa toàn diện Phụ lục E (Hệ số hiệu ứng giật $G_f$)

**Nghiệp vụ cần làm:**  
Áp dụng chuẩn OKF v2.3 để hiện đại hóa toàn diện Phụ lục E (TCVN 2737:2023):
1. Ghép sơ đồ dao động công trình ([Hình E.1](file:///D:/GitHubProjects/ccba-legal-knowledge/legal_docs/03_tcvn/tcvn_2737_2023/annexes/phu_luc_e_mot_so_cong_thuc_don_gian_tinh_he_so_hieu_ung.md#hinh-e_1)) thành ảnh composite căn giữa.
2. Chuyển đổi $100\%$ công thức giải tích ($E.1 	o E.4$) sang KaTeX chuẩn.
3. Đóng gói Visual Card JSON `fig_e_1_gust_factor.json` và Solver Python `calc_gust_factor_gf` trong `formulas/wind_load_tcvn2737.py`.
4. Viết bộ Unit Tests Ground Truth trong `tests/test_wind_load_solvers.py`.

**Bị chặn bởi:** `Ticket 1`.

- [x] Phụ lục E đạt Visual Parity $100\%$ với bố cục căn giữa hoàn hảo.
- [x] Visual Card `fig_e_1_equivalent_footprint.json` nạp và tính toán tham số thành công.
- [x] Solver `calc_gust_factor_gf` & `calc_equivalent_building_dimensions` vượt qua $100\%$ test cases kiểm chuẩn.
- [x] Vượt qua 10 Cổng Master CI Gate.

---

## Ticket 3: Hiện đại hóa toàn diện Phụ lục C (Bản đồ phân vùng gió $W_0$) & Phụ lục D (Dạng địa hình)

**Nghiệp vụ cần làm:**  
Áp dụng chuẩn OKF v2.3 để hiện đại hóa Phụ lục C và Phụ lục D:
1. Chuẩn hóa Bảng C.1 và C.2 (phân vùng áp lực gió cơ sở $W_0$ cho 63 tỉnh thành) và Hình D.1 (minh họa 4 dạng địa hình A, B, C, D).
2. Xây dựng Solver tự động tra cứu áp lực gió $W_0$ theo tỉnh/huyện/xã (`calc_base_wind_pressure_w0`) và hệ số độ cao $k(z)$ theo 4 dạng địa hình (`calc_terrain_height_factor_kz`).
3. Đăng ký vào Facade Master `SymbolicFormulaSolver`.

**Bị chặn bởi:** `Ticket 1`.

- [x] Toàn bộ bảng phân vùng gió 63 tỉnh thành được số hóa đầy đủ và chính xác $100\%$.
- [x] Solver tra $W_0$ và $k(z)$ hoạt động chính xác với mọi địa danh Việt Nam.
- [x] Unit Tests kiểm chuẩn tra cứu cho Hà Nội, TP.HCM, Đà Nẵng, Hải Phòng, Cần Thơ.
- [x] Vượt qua 10 Cổng Master CI Gate.

---

## Ticket 4: Hiện đại hóa Phụ lục G & H (Kiểm tra Độ võng & Chuyển vị giới hạn)

**Nghiệp vụ cần làm:**  
1. Chuẩn hóa toàn bộ các Bảng G.1 $	o$ G.5 và Bảng H.1 trong Phụ lục G và H.
2. Xây dựng Solver Python `check_deflection_and_drift_limits` kiểm tra điều kiện an toàn $f_u \le [f_u]$ cho dầm, sàn, tường ngăn và khung nhà nhiều tầng.
3. Xuất báo cáo giải trình kiểm tra chuyển vị phục vụ hồ sơ thẩm tra kết cấu.

**Bị chặn bởi:** `Ticket 1`.

- [x] Toàn bộ 6 bảng tra giới hạn độ võng/chuyển vị được chuẩn hóa GFM ma trận đầy đủ.
- [x] Solver kiểm tra chuyển vị trả về kết luận tuân thủ (`is_compliant`) rõ ràng.
- [x] Unit Tests bao phủ các loại kết cấu nhà 1 tầng, nhà nhiều tầng, dầm cầu trục.
- [x] Vượt qua 10 Cổng Master CI Gate.

---

## Ticket 5: Xây dựng Bộ Giải Tải Trọng Gió Toàn Trình (Chương 10 TCVN 2737)

**Nghiệp vụ cần làm:**  
Tích hợp toàn bộ các phân hệ rời rạc thành một bộ giải toàn trình:
$$W_k = W_0 \cdot k(z_e) \cdot c_e \cdot G_f$$
- Tự động lấy $W_0$ từ Phụ lục C (Ticket 3).
- Tự động tính $k(z_e)$ từ Phụ lục D (Ticket 3).
- Tự động tra hệ số $c_e$ từ Phụ lục F (Đã hoàn thành).
- Tự động tính hệ số giật $G_f$ từ Phụ lục E (Ticket 2).
- Tự động xuất Bảng tải trọng gió tiêu chuẩn trên từng mét vuông bề mặt công trình và báo cáo thuyết minh hoàn chỉnh nộp cơ quan thẩm duyệt.

**Bị chặn bởi:** `Ticket 2`, `Ticket 3`.

- [x] Hàm `calc_total_wind_load_standard` (và `calc_full_wind_load_tcvn2737`) thực thi tích hợp end-to-end thành công.
- [x] Xuất báo cáo Markdown thuyết minh tải trọng gió hoàn chỉnh cho công trình thực tế.
- [x] Unit Tests tích hợp toàn trình đạt $100\%$ pass rate.
- [x] Vượt qua 10 Cổng Master CI Gate.
