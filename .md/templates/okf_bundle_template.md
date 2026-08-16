---
id: "okf-doc-{{unique_id}}"
title: "{{document_title}}"
category: "{{category}}" # legal_vbpl | bim_standard | contract_tender | architecture_adr
tags: [okf, ccba, legal, bim]
version: "0.2.0"

# OKF v0.2 Trust Signals (Tín hiệu Tin cậy)
provenance:
  source_type: "notebooklm_cloud" # notebooklm_cloud | local_extraction | agent_generated
  source_notebook_id: "71cef22b-f4b2-4c7f-9e63-78d19c69904f"
  source_url: "{{source_url_or_filepath}}"
  extracted_at: "{{current_timestamp}}"

trust_score: 0.95 # Mức độ tin cậy từ 0.0 -> 1.0
lifecycle: "active" # active | draft | deprecated
stale_after: "2027-12-31" # Thời điểm hết hạn để Agent kiểm tra cập nhật VBPL mới

attestation:
  validator: "validate_docs.py"
  schema_version: "okf-v0.2"
  maskara_cleared: true
  status: "passed"
---

# {{document_title}}

## 📌 1. Tóm tắt Tổng quan (Executive Summary)
{{executive_summary}}

---

## 🏛️ 2. Nội dung Chi tiết Tri thức (Structured Content)
{{structured_content}}

---

## 🔗 3. Liên kết & Viện dẫn Pháp lý (Cross-References & Citations)
- **Văn bản pháp lý liên quan:** {{legal_references}}
- **Tiêu chuẩn / Quy chuẩn:** {{standards_references}}
- **Tài liệu tham chiếu:** [NotebookLM Grounding Source]({{source_url_or_filepath}})

---

## 📝 4. Nhật ký Thay đổi (Revision History)
- **{{created_date}}**: Khởi tạo bản thảo OKF v0.2 qua Agent Workflow.
