# ADR 0037: Hien Phap Bao Ton Nguyen Van Quy Pham & DOCX-to-Markdown Verbatim Parity Gate

## 1. Trang Thai (Status)
**ACCEPTED & ADOPTED** (2026-08-28)

## 2. Boi Canh (Context)
Trong he thong tri thuc phap ly xay dung (Legal Knowledge Base), than van ban quy pham phap luat (Luat, Nghi dinh, Thong tu, QCVN, TCVN) la **Mo neo Phap ly Toi thuong (Ground Truth)**.
1. **Rui ro khi dung LLM de tom tat/viet lai:** Moi hanh vi dung LLM de tom tat, dien dat lai (paraphrase), hoac cat bot dieu khoan deu co the lam meo mo cac che tai, dieu kien dinh luong hoac can cu phap ly, dan den sai lech nghiem trong khi Tham tra Thiet ke (QC Audit) va Tu van Phap ly (Legal Opinion).
2. **Yeu cau bao ton 100% nguyen van:** Toan bo tung cau, chu, dieu, khoan, diem, dau gach dau dong (\- \), dau cong (\&nbsp;&nbsp;+ \) va cong thuc ky thuat phai duoc trich xuat hoan toan xac dinh tu ban DOCX/PDF Cong bao goc.
3. **Can mot cong kiem dinh toan hoc tu dong:** Can co che do luong do trung khop nguyen van (Verbatim Parity Rate) giua DOCX nguon va Markdown dau ra de ngan chan triet de hien tuong mat mat noi dung trong CI pipeline.

## 3. Quyet Dinh Thiet Ke (Decision)

He thong thiet lap **Hien Phap Bao Ton Nguyen Van Quy Pham (Verbatim Normative Invariant)** voi cac nguyen tac cot tu:

### A. Quy Trinh Trich Xuat Xac Dinh Zero-LLM (Deterministic Python-docx AST Parser)
- Nghiem cam tuyet doi viec su dung LLM de sinh hoac viet lai than van ban Markdown quy pham.
- 100% than van ban Markdown phai duoc trich xuat bang Python-docx AST Parser xac dinh thong qua package ccba-legal-intel (docx_converter.py).

### B. Cong Kiem Dinh Nghiem Thu Master Gate 11 (DOCX-to-Markdown Verbatim Parity Gate)
- Tich hop Gate 11 truc tiep vao scripts/validate_legal_spoke.py.
- Co che doi soat: Tu dong trich xuat chuoi ky tu chuan hoa (normalized text stream) tu file DOCX nguon trong sources/<slug>.docx va so khop voi than Markdown <slug>.md.
- **Nguong chap thuan nghiem thu (Acceptance Threshold):** Verbatim Parity Rate >= 98.0%
- Cac truong hop do lech cho phep (<2.0%) chi bao gom: viec boc tach bang so lieu ra tables/, tach bieu mau ra templates/, chuyen doi cong thuc KaTeX, va cac the HTML dinh dang neo (<a id=...>).

### C. Co Che Bao Toan Ky Tu Dau Dong & Thoat Ky Tu Visual Parity (ADR 0029, ADR 0030)
- Bao ton 100% dau gach ngang dau dong - bang cu phap \- .
- Bao ton dau cong thut le dau dong + bang cu phap &nbsp;&nbsp;+ .
- Tu dong tach dong chu thich bang (CHU THICH:) ra khoi o du lieu CSV de giu sach du lieu tra cuu 2D.

## 4. He Qua & Loi Ich (Consequences)
- **Do tin cay Phap ly Tuyet doi (Absolute Legal Ground Truth):** Du lieu tri thuc dat do chuan xac tuong duong Cong bao, loai bo hoan toan rui ro ao giac phap ly.
- **Tu Dong Hoa Kiem Thu (Automated Verification):** Bat ky chinh sua thu cong hay loi chuyen doi nao lam mat dieu/khoan deu bi Gate 11 chan lai ngay lap tuc tai pre-commit / CI gate.
- **Khep kin Chuoi Quyet Dinh Kien Truc (ADR 0001 - 0037):** Dam bao tinh nhat quan toan dien tu khau cao (ADR 0031), phan ra (ADR 0021, ADR 0036), dong bo dam may (ADR 0035) den kiem dinh nghiem thu (ADR 0037).
