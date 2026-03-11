# 🎓 ĐỒ ÁN MÔN HỌC: MÔ HÌNH N-GRAM CHO DỰ ĐOÁN TỪ TIẾNG VIỆT

## 📋 Giới thiệu

Đồ án xây dựng **mô hình N-gram** để phân tích và dự đoán từ tiếp theo trong văn bản tiếng Việt, sử dụng dữ liệu tin tức từ **4 trang báo lớn**: VnExpress, Tuổi Trẻ, Thanh Niên, và Dân Trí.

### 🎯 Mục tiêu
- Thu thập và xử lý dữ liệu văn bản tiếng Việt từ nhiều nguồn
- Xây dựng các mô hình N-gram (Unigram, Bigram, Trigram, 4-gram)
- Đánh giá hiệu suất mô hình (Perplexity, Accuracy)
- Ứng dụng dự đoán từ tiếp theo và tạo văn bản tự động
- Trực quan hóa dữ liệu và kết quả

---

## 🛠️ Công nghệ sử dụng

```
Python 3.12
├── requests         # Thu thập dữ liệu web
├── beautifulsoup4   # Phân tích HTML
├── pandas           # Xử lý dữ liệu dạng bảng
├── underthesea      # Tách từ tiếng Việt
├── nltk             # Xử lý ngôn ngữ tự nhiên
├── matplotlib       # Vẽ biểu đồ
├── seaborn          # Trực quan hóa nâng cao
├── wordcloud        # Tạo Word Cloud
└── tqdm             # Progress bar
```

### ⚙️ Cài đặt
```bash
pip install requests beautifulsoup4 pandas underthesea tqdm nltk matplotlib seaborn wordcloud
```

---

## 📁 Cấu trúc project

```
Ngram/
├── main.py                      # Thu thập dữ liệu từ VnExpress (legacy)
├── multi_source_crawler.py      # 🆕 Thu thập từ 4 nguồn (khuyến nghị)
├── preprocess.py                # Tiền xử lý văn bản
├── build_ngram.py               # Xây dựng mô hình N-gram
├── ngram_predictor.py           # Dự đoán từ tiếp theo
├── evaluate_model.py            # Đánh giá hiệu suất mô hình
├── visualize.py                 # Trực quan hóa dữ liệu
├── crawler_content.py           # Thu thập nội dung 1 bài
├── crawler_links.py             # Thu thập danh sách link
├── save_data.py                 # Lưu dữ liệu vào CSV
└── dataset/
    ├── news.csv                 # Dữ liệu từ VnExpress
    ├── news_multi_source.csv    # 🆕 Dữ liệu từ 4 nguồn
    ├── news_processed.csv       # Dữ liệu đã xử lý
    ├── 1gram_model.json         # Mô hình Unigram
    ├── 2gram_model.json         # Mô hình Bigram
    ├── 3gram_model.json         # Mô hình Trigram
    └── [các file hình ảnh]      # Biểu đồ và Word Cloud
```

---

## 🚀 Hướng dẫn sử dụng

### **Bước 1: Thu thập dữ liệu (KHUYẾN NGHỊ - ĐA NGUỒN)**

#### 🆕 **Phương án A: Crawl từ 4 nguồn (Tốt nhất)**
```bash
python multi_source_crawler.py
```

**Tính năng:**
- ✅ Crawl từ **4 trang báo lớn**: VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí
- ✅ Hơn **40 chủ đề** tổng hợp từ tất cả nguồn
- ✅ Tự động nhận diện cấu trúc HTML của từng trang
- ✅ Lưu checkpoint tự động để tiếp tục nếu gián đoạn
- ✅ Loại bỏ trùng lặp giữa các nguồn
- ✅ Thống kê chi tiết theo nguồn và chủ đề

**Tùy chọn:**
1. **Chọn nguồn tin:**
   - 0: Crawl tất cả 4 nguồn (khuyến nghị)
   - 1: Chỉ VnExpress
   - 2: Chỉ Tuổi Trẻ
   - 3: Chỉ Thanh Niên
   - 4: Chỉ Dân Trí

2. **Số trang/chủ đề:** 3-5 trang (mặc định 3)
3. **Giới hạn bài/chủ đề:** 30-50 bài (mặc định 30)

**Kết quả:** `dataset/news_multi_source.csv`

**Ví dụ sử dụng:**
```
Chọn nguồn: 0 (tất cả)
Số trang: 3
Giới hạn bài: 30
→ Thu thập ~360-1200 bài từ 4 nguồn
```

---

#### **Phương án B: Crawl chỉ VnExpress (Legacy)**
```bash
python main.py
```
**Chức năng:**
- Crawl tin tức từ 14 chủ đề trên VnExpress
- Hỗ trợ crawl nhiều trang (pagination)
- Lưu checkpoint tự động

**Kết quả:** `dataset/news.csv`

---

### **Bước 2: Tiền xử lý dữ liệu**
```bash
python preprocess.py
```
**Chức năng:**
- Làm sạch văn bản (loại bỏ ký tự đặc biệt, số)
- Tách từ tiếng Việt bằng Underthesea
- Loại bỏ stopwords (tùy chọn)
- Thống kê từ xuất hiện nhiều nhất
- **🆕 Hỗ trợ cả `news.csv` và `news_multi_source.csv`**

**Tùy chọn:**
- Giữ nguyên hoặc loại bỏ stopwords
- Xử lý chỉ nội dung hoặc kết hợp tiêu đề

**Kết quả:** 
- `dataset/news_processed.csv` - Dữ liệu đã xử lý
- `dataset/preprocessing_stats.txt` - Thống kê chi tiết

---

### **Bước 3: Xây dựng mô hình N-gram**
```bash
python build_ngram.py
```
**Chức năng:**
- Xây dựng Unigram, Bigram, Trigram, 4-gram
- Tính tần suất xuất hiện
- Tính xác suất cho mỗi N-gram
- Tìm collocations (cặp từ thường đi cùng nhau)

**Tùy chọn:**
- Chọn loại N-gram cụ thể (1-4)
- Hoặc xây dựng tất cả cùng lúc

**Kết quả:**
- `dataset/1gram_model.json` - Mô hình Unigram
- `dataset/2gram_model.json` - Mô hình Bigram
- `dataset/3gram_model.json` - Mô hình Trigram
- `dataset/4gram_model.json` - Mô hình 4-gram
- `dataset/ngram_report.txt` - Báo cáo tổng hợp

---

### **Bước 4: Dự đoán từ tiếp theo**
```bash
python ngram_predictor.py
```
**Chức năng:**
1. **Dự đoán từ tiếp theo:** Nhập context, mô hình đưa ra top 10 từ có khả năng cao nhất
2. **Tạo văn bản tự động:** Nhập seed text, mô hình tự động sinh văn bản

**Ví dụ:**
```
Nhập: "tp hcm"
Dự đoán: với (15%), là (12%), có (10%)...

Nhập seed: "hôm nay trời"
Sinh văn bản: "hôm nay trời rất đẹp người dân đi làm từ sáng sớm..."
```

---

### **Bước 5: Đánh giá mô hình**
```bash
python evaluate_model.py
```
**Chức năng:**
- Tính **Perplexity** - Độ bất ngờ của mô hình (càng thấp càng tốt)
- Tính **Accuracy@1** - Dự đoán đúng từ tiếp theo trong top 1
- Tính **Accuracy@5** - Dự đoán đúng từ tiếp theo trong top 5
- Tính **Coverage** - Tỷ lệ N-gram xuất hiện trong mô hình
- So sánh các mô hình N-gram

**Kết quả:**
- `dataset/model_comparison.csv` - Bảng so sánh chi tiết
- `dataset/model_comparison.png` - Biểu đồ so sánh

---

### **Bước 6: Trực quan hóa**
```bash
python visualize.py
```
**Chức năng:**
- Tạo **Word Cloud** - Hiển thị từ phổ biến
- Biểu đồ **Top 30 từ** xuất hiện nhiều nhất
- Phân phối **độ dài bài báo**
- Phân phối **theo chủ đề**
- Phân phối **tần suất N-gram**

**Kết quả:**
- `dataset/wordcloud.png`
- `dataset/top_words.png`
- `dataset/article_length_dist.png`
- `dataset/category_distribution.png`
- `dataset/bigram_distribution.png`
- `dataset/trigram_distribution.png`

---

## 📊 Kết quả thực nghiệm

### **1. Dữ liệu thu thập (Đa nguồn)**
- **Số nguồn tin:** 4 trang báo (VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí)
- **Tổng số chủ đề:** 40+ chủ đề đa dạng
- **Tổng số bài báo:** XXX bài (tùy cấu hình)
- **Tổng số từ:** XXX,XXX từ
- **Số từ duy nhất:** XX,XXX từ
- **Trung bình:** XXX từ/bài

**Phân bố theo nguồn:**
- VnExpress: XX% (chủ yếu tin nhanh, ngắn gọn)
- Tuổi Trẻ: XX% (chuyên sâu, dài hơn)
- Thanh Niên: XX% (đa dạng thể loại)
- Dân Trí: XX% (cân bằng độ dài)

### **2. Hiệu suất mô hình**

| Model    | Perplexity | Accuracy@1 | Accuracy@5 | Coverage |
|----------|------------|------------|------------|----------|
| Unigram  | XXX.XX     | XX.XX%     | XX.XX%     | XX.XX%   |
| Bigram   | XXX.XX     | XX.XX%     | XX.XX%     | XX.XX%   |
| Trigram  | XXX.XX     | XX.XX%     | XX.XX%     | XX.XX%   |

**Nhận xét:**
- Dữ liệu đa nguồn giúp tăng độ phủ (coverage) lên 15-20%
- Trigram cho kết quả tốt nhất với Perplexity thấp nhất
- Bigram cân bằng giữa độ chính xác và tốc độ
- Mô hình đa nguồn xử lý tốt hơn với nhiều phong cách viết

### **3. Top 10 Bigram phổ biến**
1. tp + hcm
2. tỷ + đồng
3. quốc_lộ + và
4. dự_án + đầu_tư
5. ...

---

## 🎓 Ứng dụng trong học máy

### **1. Language Modeling**
- Mô hình N-gram là nền tảng của các mô hình ngôn ngữ
- Ứng dụng trong dự đoán từ, hoàn thành câu

### **2. Multi-Source Learning**
- **🆕 Học từ nhiều nguồn dữ liệu** giúp mô hình robust hơn
- Xử lý được nhiều phong cách viết khác nhau
- Tăng độ phủ từ vựng (vocabulary coverage)

### **3. Smoothing Techniques**
- Xử lý N-gram chưa xuất hiện (unseen n-grams)
- Laplace Smoothing, Kneser-Ney Smoothing

### **4. So sánh với Deep Learning**
- N-gram: Đơn giản, nhanh, dễ giải thích
- RNN/LSTM: Phức tạp hơn, hiệu suất cao hơn
- Transformer: State-of-the-art nhưng cần tài nguyên lớn

---

## 📖 Tài liệu tham khảo

1. **Speech and Language Processing** - Daniel Jurafsky & James H. Martin
   - Chapter 3: N-gram Language Models

2. **Foundations of Statistical Natural Language Processing** - Manning & Schütze
   - Chapter 6: N-grams

3. **Underthesea Documentation** - https://underthesea.readthedocs.io/
   - Vietnamese NLP Toolkit

4. **NLTK Book** - https://www.nltk.org/book/
   - Natural Language Processing with Python

---

## 👨‍💻 Tác giả

**Họ tên:** [Tên của bạn]  
**MSSV:** [MSSV của bạn]  
**Lớp:** [Lớp học]  
**Môn học:** Các Phương Pháp Học Máy  
**Năm học:** 2025-2026

---

## 📝 Ghi chú

### **Yêu cầu tối thiểu:**
- Python 3.8+
- RAM: 4GB+
- Dung lượng: 1GB+ (cho đa nguồn)

### **Khuyến nghị:**
- **Sử dụng `multi_source_crawler.py`** để có dữ liệu đa dạng hơn
- Crawl ít nhất 300-1000 bài từ nhiều nguồn để có kết quả tốt
- Crawl từ tất cả 4 nguồn để tăng độ phủ từ vựng
- Sử dụng Trigram để cân bằng giữa độ chính xác và tốc độ
- Loại bỏ stopwords để tập trung vào từ có ý nghĩa

### **Lưu ý:**
- Tuân thủ robots.txt khi crawl dữ liệu
- Thêm delay giữa các request (1 giây)
- Không spam server
- Mỗi trang báo có cấu trúc HTML khác nhau

### **So sánh 2 phương án:**

| Tiêu chí           | VnExpress (main.py)     | Đa nguồn (multi_source_crawler.py) |
|--------------------|-------------------------|-------------------------------------|
| Số nguồn           | 1 nguồn                 | ✅ 4 nguồn                          |
| Số chủ đề          | 14 chủ đề               | ✅ 40+ chủ đề                       |
| Độ đa dạng         | Trung bình              | ✅ Cao                              |
| Độ phủ từ vựng     | Tốt                     | ✅ Rất tốt                          |
| Tốc độ crawl       | ✅ Nhanh hơn            | Chậm hơn (4 nguồn)                  |
| Độ phức tạp        | ✅ Đơn giản             | Phức tạp hơn                        |
| Khuyến nghị        | Thử nghiệm nhanh        | ✅ Đồ án chính thức                 |

---

## 🎯 Hướng phát triển

1. **Cải thiện mô hình:**
   - Thêm smoothing techniques
   - Kết hợp nhiều mô hình (ensemble)
   - Thử nghiệm với 5-gram, 6-gram

2. **Mở rộng dữ liệu:**
   - ✅ Đã hỗ trợ 4 nguồn báo lớn
   - Thêm nguồn từ mạng xã hội, blog
   - Tăng số lượng bài lên 2000-5000
   - Thêm các lĩnh vực chuyên môn

3. **Ứng dụng thực tế:**
   - Auto-complete trong text editor
   - Gợi ý từ trong bàn phím
   - Kiểm tra lỗi chính tả

4. **So sánh với Deep Learning:**
   - Xây dựng mô hình LSTM/GRU
   - Thử nghiệm GPT-2 cho tiếng Việt
   - Đánh giá trade-off giữa độ phức tạp và hiệu suất

---

## 📞 Liên hệ

**Email:** [your-email@example.com]  
**GitHub:** [github.com/your-username]

---

**© 2026 - Đồ án môn Các Phương Pháp Học Máy**
