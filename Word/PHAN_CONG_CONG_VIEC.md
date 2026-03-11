# 👥 PHÂN CÔNG CÔNG VIỆC NHÓM (5 NGƯỜI)
## ĐỒ ÁN: MÔ HÌNH N-GRAM CHO DỰ ĐOÁN TỪ TIẾNG VIỆT

---

## 📋 TỔNG QUAN PHÂN CÔNG

**Nhóm:** 5 thành viên  
**Thời gian:** 8 tuần (Tháng 2 - Tháng 4, 2026)  
**Ngày báo cáo lần 1:** Tuần 4 (11/03/2026) ✅  
**Ngày báo cáo lần 2:** Tuần 8 (Dự kiến 08/04/2026)  

---

## 👤 THÀNH VIÊN 1: TRƯỞNG NHÓM - TỔNG QUAN & QUẢN LÝ

### 🎯 **Vai trò chính:**
- **Quản lý dự án:** Lập kế hoạch, theo dõi tiến độ, điều phối công việc
- **Tích hợp hệ thống:** Đảm bảo các module hoạt động cùng nhau
- **Báo cáo & Trình bày:** Tổng hợp báo cáo, chuẩn bị slide, thuyết trình

---

### 📝 **Công việc cụ thể:**

#### **GIAI ĐOẠN 1: TUẦN 1-2 (Đã hoàn thành ✅)**
- ✅ Định nghĩa phạm vi đề tài
- ✅ Phân công công việc cho 5 người
- ✅ Thiết lập Git repository
- ✅ Tạo cấu trúc thư mục project
- ✅ Viết file README.md hướng dẫn

**Deliverables:**
- ✅ `README.md` - Tổng quan dự án
- ✅ `PHAN_CONG_CONG_VIEC.md` - File phân công này
- ✅ Cấu trúc thư mục: `dataset/`, `Word/`, code files

---

#### **GIAI ĐOẠN 2: TUẦN 3-4 (Đã hoàn thành ✅)**
- ✅ Tích hợp các module từ thành viên 2, 3, 4
- ✅ Test pipeline hoàn chỉnh: Crawl → Preprocess → Build N-gram
- ✅ Tạo báo cáo tiến độ lần 1
- ✅ Chuẩn bị slide thuyết trình

**Deliverables:**
- ✅ `BAO_CAO_TIEN_DO_LAN_1.md` - Báo cáo chi tiết
- ✅ `SLIDE_TIEN_DO_LAN_1.md` - Slide thuyết trình
- ✅ Kiểm tra và fix lỗi tích hợp

---

#### **GIAI ĐOẠN 3: TUẦN 5-6 (Đang thực hiện 🔄)**
- 🔄 Tích hợp module đánh giá mô hình (từ Thành viên 3)
- 🔄 Tích hợp module dự đoán (từ Thành viên 4)
- 🔄 Review code toàn bộ dự án
- 🔄 Viết tài liệu hướng dẫn sử dụng

**Deliverables:**
- 📋 `USER_GUIDE.md` - Hướng dẫn sử dụng cho người dùng cuối
- 📋 Integration testing report
- 📋 Code review notes

---

#### **GIAI ĐOẠN 4: TUẦN 7-8 (Sắp tới 📅)**
- 📅 Tổng hợp kết quả từ tất cả thành viên
- 📅 Viết báo cáo cuối cùng
- 📅 Chuẩn bị slide thuyết trình cuối kỳ
- 📅 Demo ứng dụng
- 📅 Nộp bài và thuyết trình

**Deliverables:**
- 📋 `BAO_CAO_CUOI_KY.pdf` - Báo cáo hoàn chỉnh (20-30 trang)
- 📋 `SLIDE_THUYET_TRINH.pptx` - Slide thuyết trình (15-20 slides)
- 📋 Video demo ứng dụng (3-5 phút)

---

### ⏰ **Thời gian ước tính:** 80 giờ (20 giờ/tuần × 4 tuần)

---

## 👤 THÀNH VIÊN 2: THU THẬP DỮ LIỆU (DATA ENGINEER)

### 🎯 **Vai trò chính:**
- **Web Scraping:** Thu thập dữ liệu từ các trang báo
- **Data Quality:** Kiểm tra và đảm bảo chất lượng dữ liệu
- **Data Pipeline:** Xây dựng quy trình tự động hóa

---

### 📝 **Công việc cụ thể:**

#### **GIAI ĐOẠN 1: TUẦN 1-2 (Đã hoàn thành ✅)**
- ✅ Nghiên cứu các trang báo (VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí)
- ✅ Phân tích cấu trúc HTML của từng trang
- ✅ Viết code `crawler_links.py` - Thu thập danh sách URL
- ✅ Viết code `crawler_content.py` - Trích xuất nội dung

**Deliverables:**
- ✅ `crawler_links.py` - Crawl links từ trang danh mục
- ✅ `crawler_content.py` - Lấy title + content từ URL
- ✅ `save_data.py` - Lưu vào CSV
- ✅ Test với 50-100 bài thử nghiệm

---

#### **GIAI ĐOẠN 2: TUẦN 2-3 (Đã hoàn thành ✅)**
- ✅ Viết `crawler.py` - Crawler đơn nguồn (VnExpress)
- ✅ Thu thập 6,463 bài từ VnExpress (14 categories)
- ✅ Viết `multi_source_crawler.py` - Crawler đa nguồn
- ✅ Implement checkpoint system (lưu tiến trình)
- ✅ Xử lý lỗi: timeout, 404, encoding issues

**Deliverables:**
- ✅ `crawler.py` - Hoàn chỉnh
- ✅ `multi_source_crawler.py` - Hoàn chỉnh
- ✅ `dataset/news.csv` - 6,463 bài báo
- ✅ Thống kê: phân bố theo nguồn, chủ đề

---

#### **GIAI ĐOẠN 3: TUẦN 4-5 (Maintenance 🔧)**
- 🔧 Bổ sung dữ liệu từ các nguồn khác (Tuổi Trẻ, Thanh Niên, Dân Trí)
- 🔧 Nâng tổng số bài lên 10,000+ (nếu cần)
- 🔧 Viết `merge_csv.py` - Gộp dữ liệu từ nhiều file
- 🔧 Làm sạch dữ liệu: loại bỏ trùng lặp, null values

**Deliverables:**
- 📋 `merge_csv.py` - Gộp và làm sạch dữ liệu
- 📋 `dataset/news_all_sources.csv` - Dữ liệu từ 4 nguồn
- 📋 Data quality report

---

#### **GIAI ĐOẠN 4: TUẦN 6-8 (Phân tích 📊)**
- 📅 Phân tích đặc điểm dữ liệu thu thập được
- 📅 So sánh văn phong giữa các trang báo
- 📅 Viết phần "Phương pháp thu thập dữ liệu" trong báo cáo
- 📅 Tạo biểu đồ phân bố dữ liệu

**Deliverables:**
- 📋 Phần báo cáo về Data Collection (5-7 trang)
- 📋 Biểu đồ: phân bố theo nguồn, chủ đề, độ dài
- 📋 Bảng so sánh đặc điểm các nguồn tin

---

### ⏰ **Thời gian ước tính:** 60 giờ (15 giờ/tuần × 4 tuần)

---

## 👤 THÀNH VIÊN 3: TIỀN XỬ LÝ & ĐÁNH GIÁ MÔ HÌNH (ML ENGINEER)

### 🎯 **Vai trò chính:**
- **Preprocessing:** Tiền xử lý văn bản tiếng Việt
- **Model Evaluation:** Đánh giá hiệu suất các mô hình N-gram
- **Optimization:** Tối ưu hóa code và thuật toán

---

### 📝 **Công việc cụ thể:**

#### **GIAI ĐOẠN 1: TUẦN 2-3 (Đã hoàn thành ✅)**
- ✅ Nghiên cứu thư viện `underthesea` cho tiếng Việt
- ✅ Viết hàm `preprocess_text()` - Tiền xử lý văn bản
- ✅ Xử lý: lowercase, remove special chars, tokenization
- ✅ Xây dựng pipeline tiền xử lý 7 bước
- ✅ Test với 50 bài thử nghiệm

**Deliverables:**
- ✅ `preprocess.py` - Hoàn chỉnh
- ✅ Hàm `preprocess_text()` với 7 bước
- ✅ Test results trên 50 bài mẫu

---

#### **GIAI ĐOẠN 2: TUẦN 3-4 (Đã hoàn thành ✅)**
- ✅ Xử lý 6,463 bài từ `news.csv`
- ✅ Tối ưu hóa: chỉ xử lý bài MỚI (tiết kiệm 87% thời gian)
- ✅ Tạo file `news_processed.csv` - 664 bài đã tokenize
- ✅ Phân tích thống kê: 271K từ, 21K từ duy nhất
- ✅ Tạo file `preprocessing_stats.txt`

**Deliverables:**
- ✅ `dataset/news_processed.csv` - 664 bài đã xử lý
- ✅ `dataset/preprocessing_stats.txt` - Thống kê
- ✅ Top 20 từ xuất hiện nhiều nhất

---

#### **GIAI ĐOẠN 3: TUẦN 5-6 (Đang thực hiện 🔄)**
- 🔄 Viết `evaluate_model.py` - Đánh giá mô hình
- 🔄 Tính **Perplexity** cho 4 mô hình (1-gram → 4-gram)
- 🔄 Tính **Accuracy** trên tập test (20% dữ liệu)
- 🔄 So sánh hiệu suất các mô hình
- 🔄 Tìm mô hình tốt nhất cho tiếng Việt

**Deliverables:**
- 📋 `evaluate_model.py` - Hoàn chỉnh
- 📋 `dataset/evaluation_report.txt` - Kết quả đánh giá
- 📋 Bảng so sánh Perplexity của 4 mô hình
- 📋 Biểu đồ so sánh hiệu suất

---

#### **GIAI ĐOẠN 4: TUẦN 7-8 (Sắp tới 📅)**
- 📅 Implement **Smoothing techniques** (Laplace, Kneser-Ney)
- 📅 Xử lý **OOV (Out of Vocabulary)** words
- 📅 Viết phần "Tiền xử lý & Đánh giá" trong báo cáo
- 📅 Phân tích ưu/nhược điểm từng mô hình

**Deliverables:**
- 📋 Smoothing implementation
- 📋 OOV handling mechanism
- 📋 Phần báo cáo về Preprocessing & Evaluation (8-10 trang)
- 📋 Recommendations: mô hình nào tốt nhất?

---

### ⏰ **Thời gian ước tính:** 70 giờ (17.5 giờ/tuần × 4 tuần)

---

## 👤 THÀNH VIÊN 4: XÂY DỰNG MÔ HÌNH & ỨNG DỤNG (BACKEND DEVELOPER)

### 🎯 **Vai trò chính:**
- **Model Building:** Xây dựng các mô hình N-gram
- **Prediction System:** Phát triển hệ thống dự đoán từ
- **Application:** Tạo demo ứng dụng

---

### 📝 **Công việc cụ thể:**

#### **GIAI ĐOẠN 1: TUẦN 3-4 (Đã hoàn thành ✅)**
- ✅ Nghiên cứu thuật toán N-gram
- ✅ Viết `build_ngram.py` - Xây dựng mô hình
- ✅ Generate 1-gram, 2-gram, 3-gram, 4-gram
- ✅ Đếm tần suất xuất hiện
- ✅ Tính xác suất P(w | context)

**Deliverables:**
- ✅ `build_ngram.py` - Hoàn chỉnh
- ✅ `dataset/1gram_model.json` - 100K unigrams
- ✅ `dataset/2gram_model.json` - 1.1M bigrams
- ✅ `dataset/3gram_model.json` - 2.1M trigrams
- ✅ `dataset/4gram_model.json` - 2.3M 4-grams

---

#### **GIAI ĐOẠN 2: TUẦN 4-5 (Đã hoàn thành ✅)**
- ✅ Tạo file `ngram_report.txt` - Báo cáo thống kê
- ✅ Phân tích: số lượng n-grams, kích thước file
- ✅ Tối ưu hóa: lưu trữ JSON thay vì Pickle
- ✅ Test tốc độ load model

**Deliverables:**
- ✅ `dataset/ngram_report.txt` - Thống kê chi tiết
- ✅ Benchmark: thời gian build, load model
- ✅ So sánh kích thước file (JSON vs Pickle)

---

#### **GIAI ĐOẠN 3: TUẦN 6-7 (Đang thực hiện 🔄)**
- 🔄 Viết `ngram_predictor.py` - Ứng dụng dự đoán từ
- 🔄 Chức năng 1: Dự đoán từ tiếp theo (Next Word Prediction)
- 🔄 Chức năng 2: Sinh văn bản tự động (Text Generation)
- 🔄 Chức năng 3: Gợi ý top-K từ phổ biến
- 🔄 Implement backoff mechanism (4-gram → 3-gram → 2-gram → 1-gram)

**Deliverables:**
- 📋 `ngram_predictor.py` - Hoàn chỉnh
- 📋 CLI interface: user-friendly
- 📋 Demo với 20+ ví dụ thực tế
- 📋 Test accuracy trên tập test

---

#### **GIAI ĐOẠN 4: TUẦN 8 (Sắp tới 📅)**
- 📅 Tạo GUI đơn giản (Tkinter hoặc Streamlit)
- 📅 Deploy demo online (Streamlit Cloud hoặc Hugging Face Spaces)
- 📅 Viết phần "Xây dựng mô hình & Ứng dụng" trong báo cáo
- 📅 Quay video demo

**Deliverables:**
- 📋 GUI application (Tkinter hoặc Streamlit)
- 📋 Online demo (public URL)
- 📋 Phần báo cáo về Model & Application (8-10 trang)
- 📋 Video demo 3-5 phút

---

### ⏰ **Thời gian ước tính:** 70 giờ (17.5 giờ/tuần × 4 tuần)

---

## 👤 THÀNH VIÊN 5: TRỰC QUAN HÓA & BÁO CÁO (DATA ANALYST)

### 🎯 **Vai trò chính:**
- **Data Visualization:** Tạo biểu đồ, bảng biểu
- **Report Writing:** Viết báo cáo, slide thuyết trình
- **Documentation:** Tài liệu hóa code, hướng dẫn sử dụng

---

### 📝 **Công việc cụ thể:**

#### **GIAI ĐOẠN 1: TUẦN 3-4 (Đã hoàn thành ✅)**
- ✅ Viết `visualize.py` - Trực quan hóa dữ liệu
- ✅ Tạo 2 biểu đồ chất lượng cao (300 DPI)
- ✅ Biểu đồ 1: So sánh hiệu suất mô hình
- ✅ Biểu đồ 2: Phân tích từ vựng và N-gram phổ biến

**Deliverables:**
- ✅ `visualize.py` - Hoàn chỉnh
- ✅ `dataset/model_comparison_detailed.png`
- ✅ `dataset/vocabulary_analysis_detailed.png`
- ✅ Sử dụng matplotlib, seaborn

---

#### **GIAI ĐOẠN 2: TUẦN 4-5 (Đã hoàn thành ✅)**
- ✅ Viết báo cáo tiến độ lần 1 (cùng Thành viên 1)
- ✅ Tạo slide thuyết trình
- ✅ Design layout chuyên nghiệp
- ✅ Thêm biểu đồ, bảng, sơ đồ

**Deliverables:**
- ✅ `Word/BAO_CAO_TIEN_DO_LAN_1.md`
- ✅ `Word/SLIDE_TIEN_DO_LAN_1.md`
- ✅ 50+ slides với nội dung chi tiết

---

#### **GIAI ĐOẠN 3: TUẦN 6-7 (Đang thực hiện 🔄)**
- 🔄 Tạo biểu đồ so sánh Perplexity (từ kết quả Thành viên 3)
- 🔄 Tạo biểu đồ Accuracy vs Model Size
- 🔄 Tạo bảng so sánh ưu/nhược điểm các mô hình
- 🔄 Viết phần "Kết quả thực nghiệm" trong báo cáo

**Deliverables:**
- 📋 `dataset/perplexity_comparison.png`
- 📋 `dataset/accuracy_chart.png`
- 📋 Bảng so sánh chi tiết (Excel hoặc LaTeX)
- 📋 Phần báo cáo về Results & Analysis (5-7 trang)

---

#### **GIAI ĐOẠN 4: TUẦN 7-8 (Sắp tới 📅)**
- 📅 Viết báo cáo cuối kỳ hoàn chỉnh (20-30 trang)
- 📅 Tạo slide thuyết trình cuối kỳ (15-20 slides)
- 📅 Thiết kế poster (A1 hoặc A0) nếu cần
- 📅 Proofread và format toàn bộ tài liệu

**Deliverables:**
- 📋 `BAO_CAO_CUOI_KY.pdf` - 20-30 trang, format chuẩn
- 📋 `SLIDE_THUYET_TRINH.pptx` - 15-20 slides
- 📋 `POSTER.pdf` - A1 hoặc A0 (nếu yêu cầu)
- 📋 Tất cả tài liệu đã được review

---

### ⏰ **Thời gian ước tính:** 60 giờ (15 giờ/tuần × 4 tuần)

---

## 📊 TỔNG HỢP CÔNG VIỆC THEO TUẦN

### **TUẦN 1-2: Khởi động dự án (Đã xong ✅)**
- Thành viên 1: Định nghĩa phạm vi, phân công
- Thành viên 2: Nghiên cứu web scraping, viết crawler_links + crawler_content
- Thành viên 3: Nghiên cứu underthesea, viết hàm preprocess_text
- Thành viên 4: Nghiên cứu thuật toán N-gram
- Thành viên 5: Setup visualization tools

---

### **TUẦN 3-4: Thu thập & xử lý dữ liệu (Đã xong ✅)**
- Thành viên 1: Tích hợp module, viết báo cáo lần 1
- Thành viên 2: Thu thập 6,463 bài, lưu vào news.csv
- Thành viên 3: Xử lý dữ liệu, tạo news_processed.csv
- Thành viên 4: Xây dựng 4 mô hình N-gram
- Thành viên 5: Tạo 2 biểu đồ, viết slide

**Milestone 1:** ✅ Báo cáo tiến độ lần 1 (11/03/2026)

---

### **TUẦN 5-6: Đánh giá & ứng dụng (Đang làm 🔄)**
- Thành viên 1: Tích hợp module đánh giá + dự đoán
- Thành viên 2: Bổ sung dữ liệu từ nguồn khác
- Thành viên 3: Đánh giá mô hình, tính Perplexity
- Thành viên 4: Xây dựng ứng dụng dự đoán từ
- Thành viên 5: Tạo biểu đồ kết quả

---

### **TUẦN 7-8: Hoàn thiện & báo cáo (Sắp tới 📅)**
- Thành viên 1: Tổng hợp báo cáo cuối, chuẩn bị demo
- Thành viên 2: Phân tích dữ liệu, viết phần Data Collection
- Thành viên 3: Viết phần Preprocessing & Evaluation
- Thành viên 4: Deploy demo online, quay video
- Thành viên 5: Viết báo cáo cuối kỳ, tạo slide thuyết trình

**Milestone 2:** 📅 Báo cáo cuối kỳ & Demo (08/04/2026)

---

## 🎯 KẾT QUẢ MONG ĐỢI

### **Thành phẩm cuối cùng:**

**1. Code & Models:**
```
✅ crawler.py, multi_source_crawler.py     (Thành viên 2)
✅ preprocess.py                           (Thành viên 3)
✅ build_ngram.py                          (Thành viên 4)
✅ evaluate_model.py                       (Thành viên 3)
✅ ngram_predictor.py                      (Thành viên 4)
✅ visualize.py                            (Thành viên 5)
✅ 4 mô hình: 1-4 gram models             (Thành viên 4)
```

**2. Data:**
```
✅ dataset/news.csv              (6,463 bài - Thành viên 2)
✅ dataset/news_processed.csv    (664 bài - Thành viên 3)
✅ dataset/1-4gram_model.json    (4 models - Thành viên 4)
```

**3. Reports & Slides:**
```
✅ BAO_CAO_TIEN_DO_LAN_1.md      (Thành viên 1 + 5)
✅ SLIDE_TIEN_DO_LAN_1.md        (Thành viên 5)
📋 BAO_CAO_CUOI_KY.pdf           (20-30 trang - Thành viên 5)
📋 SLIDE_THUYET_TRINH.pptx       (15-20 slides - Thành viên 5)
```

**4. Visualizations:**
```
✅ model_comparison_detailed.png         (Thành viên 5)
✅ vocabulary_analysis_detailed.png      (Thành viên 5)
📋 perplexity_comparison.png            (Thành viên 5)
📋 accuracy_chart.png                   (Thành viên 5)
```

**5. Demo:**
```
📋 CLI Application              (Thành viên 4)
📋 GUI/Web demo                 (Thành viên 4)
📋 Video demo (3-5 phút)        (Thành viên 4)
📋 Online deployment            (Thành viên 4)
```

---

## 📞 LIÊN HỆ & HỢP TÁC

### **Họp nhóm:**
- **Tuần 1-4:** 2 lần/tuần (Thứ 3 và Thứ 6)
- **Tuần 5-8:** 3 lần/tuần (Thứ 2, 4, 6)
- **Địa điểm:** Online (Zoom/Google Meet) hoặc offline tại trường

### **Công cụ:**
- **Git/GitHub:** Quản lý code, version control
- **Google Drive:** Chia sẻ tài liệu, báo cáo
- **Telegram/Discord:** Giao tiếp hàng ngày
- **Trello/Notion:** Quản lý task, deadline

### **Quy tắc:**
- ✅ Commit code mỗi ngày (nếu có thay đổi)
- ✅ Báo cáo tiến độ mỗi tuần
- ✅ Review code của nhau trước khi merge
- ✅ Hỗ trợ nhau khi gặp khó khăn
- ✅ Deadline nghiêm túc, không trì hoãn

---

## ⚠️ BACKUP PLAN

### **Nếu thành viên nghỉ/bận:**
- **Thành viên 1 nghỉ:** Thành viên 5 đảm nhận quản lý tạm
- **Thành viên 2 nghỉ:** Thành viên 1 hỗ trợ crawl dữ liệu
- **Thành viên 3 nghỉ:** Thành viên 4 hỗ trợ preprocessing
- **Thành viên 4 nghỉ:** Thành viên 3 hỗ trợ build model
- **Thành viên 5 nghỉ:** Thành viên 1 hỗ trợ visualization

### **Nếu deadline chật:**
- Giảm số lượng dữ liệu: 6,463 → 2,000 bài
- Chỉ xây dựng 2-3 mô hình thay vì 4
- Đơn giản hóa demo: CLI thay vì GUI
- Tập trung vào phần cốt lõi: crawl → preprocess → build → evaluate

---

## 🎓 KẾT LUẬN

Phân công này đảm bảo:
- ✅ **Công bằng:** Mỗi người 60-80 giờ (15-20 giờ/tuần)
- ✅ **Rõ ràng:** Mỗi người có vai trò và deliverables cụ thể
- ✅ **Linh hoạt:** Có backup plan khi gặp vấn đề
- ✅ **Hiệu quả:** Phân công theo thế mạnh của từng người
- ✅ **Có milestone:** 2 mốc báo cáo quan trọng

**Mục tiêu:** Hoàn thành đồ án đạt điểm cao (8.5-9.5/10) với:
- Code chạy tốt
- Báo cáo chi tiết
- Demo ấn tượng
- Teamwork tốt

---

**💪 CHÚC NHÓM THÀNH CÔNG!**

---

*Cập nhật lần cuối: 11/03/2026*  
*Người tạo: Thành viên 1 (Trưởng nhóm)*
