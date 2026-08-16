# 🗺️ Wayfinding Map: Xây dựng Hệ thống Tri thức Mở (OKF System) CCBA Tích hợp NotebookLM & AI Agents

> **Trạng thái:** Active  
> **Repository:** `d:\GitHubProjects\ccba-legal-knowledge`  
> **Chủ sở hữu:** CCBA Agent Platform  

---

## 🎯 1. Điểm đích (Destination)

Xây dựng hoàn chỉnh **Hệ thống Tri thức Mở CCBA (OKF System v0.2)** được tích hợp tự động với **Google NotebookLM Cloud** và **AI Gateway (`ccba-ai`)**, cho phép các AI Agents trong CCBA Platform tự động tra cứu (Pre-flight RAG Query), tự phản biện 2 vòng (Double-Pass Adversarial Review), và tự động đồng bộ ngược tri thức mới (Write-back Loop) để phục vụ cho các buổi thảo luận định hướng kiến trúc & tư vấn pháp lý/BIM chất lượng cao.

---

## 📝 2. Ghi chú (Notes)

- **Nguyên tắc Kiến trúc:** Tuân thủ 100% Hiến pháp Platform (`AGENTS.md`), Reuse-First Gate, KISS, và chuẩn **OKF v0.2 Native-First**.
- **Kỹ năng Nạp kèm:** [notebooklm-connector](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/skills/notebooklm-connector/SKILL.md), [hybrid-rag-search](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/skills/hybrid-rag-search/SKILL.md), [grilling](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/skills/grilling/SKILL.md), [maskara-privacy](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/skills/maskara/SKILL.md).
- **Primary Notebook Target:** `71cef22b-f4b2-4c7f-9e63-78d19c69904f` (Google Cloud Knowledge Catalog Tools and Samples / CCBA Brain).

---

## ✅ 3. Quyết định Đã chốt (Decisions so far)

- [x] **[Xác thực & Kết nối NotebookLM Cloud](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/notebooklm_helper.py)**: Nâng cấp `notebooklm-py` v0.7.3, vá seam context manager trong `ccba_notebooklm`, kết nối thành công 41 Notebooks Cloud.
- [x] **[Mô hình Kiến trúc 2 Lớp](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/skills/notebooklm-connector/SKILL.md)**: Chốt kết hợp *Ingestion-time LLM Wiki (OKF)* + *Query-time Agentic RAG (NotebookLM)* qua Model Context Protocol (MCP).
- [x] **[Cơ chế Bảo mật Maskara Gate](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/skills/maskara/SKILL.md)**: Nghiêm cấm đẩy API Keys/PII thô lên Cloud, tự động che giấu (redact) trước khi sync.
- [x] **[Khai báo Workspace Context Binding](file:///d:/GitHubProjects/ccba-legal-knowledge/.md/workspace_context.yaml)**: Tạo tệp `.md/workspace_context.yaml` cố định `primary_notebook_id: "71cef22b-f4b2-4c7f-9e63-78d19c69904f"`.
- [x] **[Chuẩn hóa OKF v0.2 Bundle Template](file:///d:/GitHubProjects/ccba-legal-knowledge/.md/templates/okf_bundle_template.md)**: Tạo tệp mẫu OKF chứa 5 Tín hiệu Tin cậy (*provenance, trust_score, lifecycle, stale_after, attestation*).
- [x] **[Tích hợp Pre-flight RAG Hook vào Workflows](file:///d:/GitHubProjects/ccba-legal-knowledge/.agents/workflows/ccba-grill-with-docs.md)**: Nâng cấp workflow `/ccba-grill-with-docs` tự động tra cứu NotebookLM Cloud trước khi phỏng vấn Socrates.

---

## 🚩 4. Ticket Đang Chờ Thực Hiện (Frontier Ticket)

### 🎫 [Ticket-04] [Grilling HITL] Phỏng vấn Phân rã Danh mục Tri thức Vận hành CCBA
- **Mục tiêu:** Thực hiện phỏng vấn Socrates dồn dập với bạn để xác định và phân loại 4 nhóm tri thức cốt lõi (Pháp lý/QCVN, BIM Standard, Thầu/Hợp đồng, Software Architecture) cần xây dựng trong Spoke này.
- **Loại:** `Grilling [HITL]` | **Assignee:** Agent & User

---

## 🌫️ 5. Chưa xác định rõ (Not yet specified - In the Fog)

- **Cơ chế Tự động Phát hiện & Giải quyết Mâu thuẫn Pháp lý (Legal Diffing & Overriding):** Khi Nghị định/Thông tư mới ban hành thay thế VBPL cũ, cơ chế tự động đánh dấu `lifecycle: deprecated` cho các tệp OKF cũ trên NotebookLM sẽ triển khai ra sao?
- **Garbage Collection & Quota Management khi Scale UP:** Chiến lược tự dọn dẹp các bản nguồn tạm khi số lượng tệp OKF vượt quá 90% Quota của tài khoản Pro/Consumer.

---

## ⛔ 6. Ngoài phạm vi (Out of scope)

- Xây dựng giao diện Frontend/Web UI riêng (sử dụng trực tiếp Google NotebookLM Web và Antigravity IDE UI).
- Hardcode API Keys trong code (tuân thủ tuyệt đối Rule 3).

---
*Cập nhật bởi CCBA Wayfinder Agent — 2026-07-26*
