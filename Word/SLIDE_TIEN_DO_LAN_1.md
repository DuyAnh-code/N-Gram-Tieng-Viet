# 📊 TIẾN ĐỘ THỰC HIỆN (YÊU CẦU TỐI THIỂU)

---

## 1️⃣ BÁO CÁO TIẾN ĐỘ LẦN 1

### 📌 **Xác định phạm vi đề tài và phương pháp thu thập dữ liệu**

---

### 🎯 **1.1. Phạm vi đề tài**

#### **Tên đề tài:**
**"Xây dựng mô hình N-gram để dự đoán từ tiếp theo trong văn bản tiếng Việt"**

#### **Giới hạn nghiên cứu:**

**📚 Về mô hình:**
- Xây dựng 4 mô hình: **Unigram, Bigram, Trigram, 4-gram**
- Không sử dụng Deep Learning (LSTM, Transformer)
- Tập trung vào nền tảng Language Model cơ bản

**📰 Về dữ liệu:**
- **Nguồn:** Tin tức từ 4 trang báo lớn (VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí)
- **Lĩnh vực:** Tin tức tổng hợp (thời sự, kinh tế, giải trí, thể thao, pháp luật...)
- **Quy mô mục tiêu:** 1,000-2,000 bài báo (~400,000-800,000 từ)

**🎯 Về ứng dụng:**
- Dự đoán từ tiếp theo (Next Word Prediction)
- Tạo văn bản tự động (Text Generation)
- Phân tích tần suất từ và N-gram

---

### 🔍 **1.2. Phương pháp thu thập dữ liệu**

#### **A. Phương pháp: Web Scraping**

**Công cụ sử dụng:**
- `requests` - Gửi HTTP requests
- `BeautifulSoup4` - Parse HTML
- `pandas` - Xử lý và lưu trữ dữ liệu
- `tqdm` - Hiển thị tiến trình

**Quy trình 6 bước:**

```
[1. Chọn nguồn] → [2. Crawl links] → [3. Trích xuất nội dung] 
→ [4. Làm sạch] → [5. Lưu CSV] → [6. Kiểm tra chất lượng]
```

---

#### **B. Nguồn dữ liệu chi tiết**

| **Nguồn**     | **Số bài** | **Chủ đề**           | **Đặc điểm**                    |
|---------------|------------|----------------------|--------------------------------|
| 📰 VnExpress  | 500        | 14 categories        | Ngắn gọn, súc tích             |
| 📰 Tuổi Trẻ   | 300        | 10+ categories       | Dài, chuyên sâu                |
| 📰 Thanh Niên | 350        | 12 categories        | Gần gũi, dễ hiểu               |
| 📰 Dân Trí    | 150        | 8+ categories        | Cân bằng, khách quan           |
| **TỔNG**      | **1,300**  | **Đa dạng**          | **~400,000 từ**                |

---

#### **C. Kiến trúc hệ thống**

```
┌─────────────────────────────────────────────┐
│         MULTI-SOURCE CRAWLER                │
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │VnExpress│  │Tuổi Trẻ │  │Thanh Niên│    │
│  │ Parser  │  │ Parser  │  │ Parser  │     │
│  └────┬────┘  └────┬────┘  └────┬────┘     │
│       └───────────┼───────────┘            │
│                   ▼                        │
│       ┌───────────────────────┐            │
│       │   Content Extractor   │            │
│       │ (Title + Content)     │            │
│       └───────────┬───────────┘            │
│                   ▼                        │
│       ┌───────────────────────┐            │
│       │   Data Validator      │            │
│       │ (Quality Control)     │            │
│       └───────────┬───────────┘            │
│                   ▼                        │
│       ┌───────────────────────┐            │
│       │    CSV Storage        │            │
│       │  dataset/news.csv     │            │
│       └───────────────────────┘            │
└─────────────────────────────────────────────┘
```

---

#### **D. Tuân thủ Web Scraping Ethics**

✅ **Kiểm tra robots.txt** - Tôn trọng quy định của website  
✅ **Rate Limiting** - Delay 1-2 giây giữa các request  
✅ **User-Agent Header** - Khai báo rõ mục đích nghiên cứu  
✅ **Retry mechanism** - Xử lý lỗi gracefully  
✅ **Chỉ mục đích học tập** - Không thương mại hóa  

---

#### **E. Kiểm soát chất lượng**

**Tiêu chí loại bỏ:**
- ❌ Bài < 50 từ (quá ngắn)
- ❌ Bài trùng lặp (dựa vào URL và title similarity)
- ❌ Encoding không hợp lệ
- ❌ Nội dung không đầy đủ (thiếu tiêu đề hoặc nội dung)

**Metrics:**
- ✅ Tỷ lệ thành công: **95%+**
- ✅ Tỷ lệ trùng lặp: **< 10%**
- ✅ Độ dài trung bình: **300-500 từ/bài**

---

### 📊 **1.3. Kết quả thu thập dữ liệu**

#### **Thống kê tổng quan:**

```
📁 File dữ liệu: dataset/news.csv
📊 Tổng số bài: 6,463 bài
📝 Tổng số từ: ~2,718,209 từ (sau tokenization)
📏 Trung bình: ~420 từ/bài
💾 Kích thước file: ~15 MB
🕒 Thời gian thu thập: ~8 giờ (với rate limiting)
```

#### **Phân bố theo chủ đề:**

| **Chủ đề**        | **Số bài** | **% Tổng** |
|-------------------|------------|------------|
| Thời sự           | 1,616      | 25%        |
| Kinh tế           | 1,163      | 18%        |
| Giải trí          | 970        | 15%        |
| Thể thao          | 775        | 12%        |
| Pháp luật         | 647        | 10%        |
| Giáo dục          | 517        | 8%         |
| Khác              | 775        | 12%        |
| **TỔNG**          | **6,463**  | **100%**   |

---

## 2️⃣ THỰC HIỆN TIỀN XỬ LÝ CƠ BẢN TRÊN TẬP DỮ LIỆU THU THẬP ĐƯỢC

---

### 🔧 **2.1. Quy trình tiền xử lý**

#### **Pipeline 7 bước:**

```
[Raw Text] 
    ↓ 
[1. Lowercase] → "Tôi Đang Học" → "tôi đang học"
    ↓
[2. Remove special chars] → "abc!@#" → "abc"
    ↓
[3. Remove numbers] → "năm 2026" → "năm"
    ↓
[4. Word Tokenization] → "tôi đang học" → ["tôi", "đang", "học"]
    ↓
[5. Remove stopwords] (Optional) → ["tôi", "đang", "học"] → ["tôi", "học"]
    ↓
[6. Filter short words] → ["a", "tôi"] → ["tôi"]
    ↓
[7. Save to CSV]
```

---

### 🛠️ **2.2. Công cụ và thư viện**

**Thư viện chính:**
- `underthesea` - **Word Tokenization** cho tiếng Việt
- `pandas` - Xử lý dữ liệu dạng bảng
- `re` (regex) - Làm sạch văn bản
- `tqdm` - Theo dõi tiến trình

**Lý do chọn Underthesea:**
- ✅ Chuyên biệt cho tiếng Việt
- ✅ Xử lý từ ghép tốt: "học sinh", "thành phố"
- ✅ Tách từ chính xác: "học_sinh" thay vì "học" + "sinh"
- ✅ Dễ sử dụng, tốc độ nhanh

---

### 📝 **2.3. Xử lý đặc thù tiếng Việt**

#### **Thách thức:**

**1. Không có khoảng trắng tự nhiên**
```
English: "I am learning"    → ["I", "am", "learning"] ✅
Tiếng Việt: "tôi đang học" → ["tôi", "đang", "học"] ❓ "học sinh"?
```

**2. Từ ghép phổ biến**
```
❌ SAI: "học" + "sinh" → 2 từ riêng biệt
✅ ĐÚNG: "học_sinh" → 1 từ ghép
```

**3. Stopwords đặc thù**
```
Tiếng Việt: "và", "của", "có", "được", "cho", "từ"...
(50+ stopwords thường gặp)
```

**Giải pháp:**
```python
from underthesea import word_tokenize

text = "Tôi là học sinh thành phố Hồ Chí Minh"
tokens = word_tokenize(text, format="text")
# Output: ["tôi", "là", "học_sinh", "thành_phố", "hồ_chí_minh"]
```

---

### ⚡ **2.4. Tối ưu hóa: Chỉ xử lý bài MỚI**

#### **Vấn đề cũ:**
```
Có 6,463 bài đã xử lý
→ Crawl thêm 1,000 bài mới
→ Xử lý lại TẤT CẢ 7,463 bài (~62 phút) ❌ CHẬM!
```

#### **Giải pháp mới:**
```
Có 6,463 bài đã xử lý
→ Crawl thêm 1,000 bài mới
→ CHỈ xử lý 1,000 bài mới (~8 phút) ✅ NHANH!
→ Gộp với 6,463 bài cũ
```

**Thuật toán:**
```python
# 1. Đọc file gốc (news.csv)
df_raw = pd.read_csv("news.csv")  # 7,463 bài

# 2. Đọc file đã xử lý (news_processed.csv)
df_processed = pd.read_csv("news_processed.csv")  # 6,463 bài

# 3. Tìm bài MỚI (dựa vào URL)
processed_urls = set(df_processed['url'])
df_new = df_raw[~df_raw['url'].isin(processed_urls)]  # 1,000 bài

# 4. CHỈ xử lý bài mới
df_new['tokens'] = df_new['content'].apply(preprocess_text)

# 5. Gộp với dữ liệu cũ
df_final = pd.concat([df_processed, df_new])  # 7,463 bài
```

**Lợi ích:**
- ⚡ **Tiết kiệm 87% thời gian** (8 phút thay vì 62 phút)
- 💾 **Không lãng phí tài nguyên** (chỉ xử lý 1 lần)
- 📈 **Scale tốt** (với 1 triệu bài vẫn nhanh)

---

### 📊 **2.5. Kết quả tiền xử lý**

#### **Thống kê sau xử lý:**

```
📁 Input: dataset/news.csv (6,463 bài)
📁 Output: dataset/news_processed.csv (664 bài đã tokenize)
📊 Tổng số từ: 271,819 từ
📊 Số từ duy nhất: 21,188 từ
📏 Trung bình: 409 từ/bài
⏱️ Thời gian xử lý: ~53 phút (lần đầu), ~0.8 phút (lần sau)
```

#### **Top 10 từ xuất hiện nhiều nhất:**

| **STT** | **Từ**      | **Tần suất** | **% Corpus** |
|---------|-------------|--------------|--------------|
| 1       | tp_hcm      | 5,234        | 1.93%        |
| 2       | việt_nam    | 4,876        | 1.79%        |
| 3       | năm         | 3,421        | 1.26%        |
| 4       | người       | 3,187        | 1.17%        |
| 5       | ngày        | 2,945        | 1.08%        |
| 6       | tỉnh        | 2,834        | 1.04%        |
| 7       | hà_nội      | 2,712        | 1.00%        |
| 8       | ông         | 2,634        | 0.97%        |
| 9       | tháng       | 2,456        | 0.90%        |
| 10      | đồng        | 2,389        | 0.88%        |

---

## 3️⃣ TÌM HIỂU TỔNG QUAN PHƯƠNG PHÁP/THUẬT TOÁN ÁP DỤNG

---

### 🎯 **3.1. Mô hình N-gram là gì?**

#### **Định nghĩa:**
N-gram là một chuỗi liên tiếp gồm **N từ** trong văn bản. Mô hình N-gram dự đoán xác suất từ tiếp theo dựa trên **(N-1) từ trước đó**.

**Công thức xác suất:**
```
P(w_n | w_1, w_2, ..., w_{n-1}) 
    ≈ P(w_n | w_{n-N+1}, ..., w_{n-1})
```

---

#### **Các loại N-gram:**

**1️⃣ Unigram (1-gram):**
```
Câu: "tôi đang học python"
Unigrams: ["tôi"], ["đang"], ["học"], ["python"]

P("python" | context) = Count("python") / Total_words
→ KHÔNG phụ thuộc ngữ cảnh
```

**2️⃣ Bigram (2-gram):**
```
Câu: "tôi đang học python"
Bigrams: ["tôi", "đang"], ["đang", "học"], ["học", "python"]

P("python" | "học") = Count("học python") / Count("học")
→ Phụ thuộc 1 từ trước
```

**3️⃣ Trigram (3-gram):**
```
Câu: "tôi đang học python"
Trigrams: ["tôi", "đang", "học"], ["đang", "học", "python"]

P("python" | "đang học") = Count("đang học python") / Count("đang học")
→ Phụ thuộc 2 từ trước
```

**4️⃣ 4-gram:**
```
Câu: "tôi đang học ngôn ngữ python"
4-grams: ["tôi", "đang", "học", "ngôn"], ["đang", "học", "ngôn", "ngữ"], ...

P("python" | "học ngôn ngữ") = Count("học ngôn ngữ python") / Count("học ngôn ngữ")
→ Phụ thuộc 3 từ trước
```

---

### 📐 **3.2. Công thức toán học**

#### **A. Maximum Likelihood Estimation (MLE):**

**Bigram:**
```
P(w_i | w_{i-1}) = Count(w_{i-1}, w_i) / Count(w_{i-1})
```

**Trigram:**
```
P(w_i | w_{i-2}, w_{i-1}) = Count(w_{i-2}, w_{i-1}, w_i) / Count(w_{i-2}, w_{i-1})
```

**Ví dụ Bigram:**
```
Câu: "tôi đi học. tôi đi chơi. tôi đi làm."

Count("tôi đi") = 3
Count("đi học") = 1
Count("đi chơi") = 1
Count("đi làm") = 1

P("học" | "đi") = 1/3 = 33.3%
P("chơi" | "đi") = 1/3 = 33.3%
P("làm" | "đi") = 1/3 = 33.3%
```

---

#### **B. Perplexity - Đánh giá mô hình:**

**Công thức:**
```
Perplexity = 2^(-1/N × Σ log_2 P(w_i | context))

Với: N = tổng số từ
```

**Ý nghĩa:**
- 📉 **Perplexity thấp** → Mô hình dự đoán tốt (ít "ngạc nhiên")
- 📈 **Perplexity cao** → Mô hình dự đoán kém (rất "ngạc nhiên")

**Ví dụ:**
```
Mô hình A: Perplexity = 50  ✅ TỐT
Mô hình B: Perplexity = 200 ❌ KÉM
→ Mô hình A dự đoán chính xác hơn
```

---

### 🏗️ **3.3. Kiến trúc hệ thống**

```
┌──────────────────────────────────────────────┐
│           N-GRAM PIPELINE                     │
│                                               │
│  [1] Raw Data (news.csv)                     │
│       ↓                                       │
│  [2] Preprocessing (preprocess.py)           │
│       → Tokenization                         │
│       → Clean text                           │
│       ↓                                       │
│  [3] Build N-grams (build_ngram.py)          │
│       → Generate 1,2,3,4-grams               │
│       → Count frequencies                    │
│       → Calculate probabilities              │
│       ↓                                       │
│  [4] Model Files                             │
│       → 1gram_model.json (100K n-grams)     │
│       → 2gram_model.json (1.1M n-grams)     │
│       → 3gram_model.json (2.1M n-grams)     │
│       → 4gram_model.json (2.3M n-grams)     │
│       ↓                                       │
│  [5] Evaluation (evaluate_model.py)          │
│       → Calculate Perplexity                 │
│       → Accuracy on test set                 │
│       ↓                                       │
│  [6] Prediction (ngram_predictor.py)         │
│       → Next word prediction                 │
│       → Text generation                      │
│       ↓                                       │
│  [7] Visualization (visualize.py)            │
│       → Model comparison charts              │
│       → Vocabulary analysis                  │
└──────────────────────────────────────────────┘
```

---

### 📊 **3.4. Kết quả xây dựng mô hình**

#### **Thống kê các mô hình:**

| **Mô hình** | **Tổng N-gram** | **N-gram duy nhất** | **Kích thước file** |
|-------------|-----------------|---------------------|---------------------|
| 1-gram      | 2,718,209       | 100,506             | ~2 MB               |
| 2-gram      | 2,711,746       | 1,161,104           | ~25 MB              |
| 3-gram      | 2,705,283       | 2,107,656           | ~58 MB              |
| 4-gram      | 2,698,820       | 2,341,756           | ~72 MB              |

#### **Phân tích:**

**📊 Quan sát:**
- N càng lớn → Số N-gram duy nhất càng tăng
- 4-gram có 2.3M n-grams → Rất nhiều tổ hợp
- Nguy cơ: **Data sparsity** (nhiều n-gram chỉ xuất hiện 1 lần)

**💡 Nhận xét:**
- ✅ **Unigram:** Đơn giản, nhanh, nhưng không có ngữ cảnh
- ✅ **Bigram:** Cân bằng tốt, phù hợp với dữ liệu vừa
- ✅ **Trigram:** Ngữ cảnh tốt, cần dữ liệu lớn
- ⚠️ **4-gram:** Rất nhiều n-gram hiếm, dễ overfitting

---

### 🎯 **3.5. Ứng dụng thực tế**

#### **Scenario 1: Auto-complete (Gợi ý từ)**
```
User nhập: "tôi đang"
→ Mô hình dự đoán: 
   1. "học" (35%)
   2. "làm" (28%)
   3. "đi" (18%)
   4. "ăn" (12%)
   5. "chơi" (7%)
```

#### **Scenario 2: Text Generation (Tạo văn bản)**
```
Seed: "việt nam"
→ Mô hình sinh: "việt nam đang phát triển kinh tế..."
→ Tiếp tục: "kinh tế đất nước ngày càng..."
```

#### **Scenario 3: Spell Checking (Sửa lỗi chính tả)**
```
Input: "tôi dang học"  ❌
→ Mô hình nhận biết "dang" bất thường
→ Gợi ý: "đang" (vì "tôi đang học" phổ biến hơn)
```

---

## 🎬 **TÓM TẮT BÁO CÁO LẦN 1**

### ✅ **Đã hoàn thành:**

**1️⃣ Xác định phạm vi:**
- ✅ Đề tài rõ ràng: Mô hình N-gram cho tiếng Việt
- ✅ Giới hạn hợp lý: 1K-2K bài, 4 mô hình
- ✅ Ứng dụng cụ thể: Dự đoán từ + Text generation

**2️⃣ Thu thập dữ liệu:**
- ✅ 6,463 bài từ 4 nguồn tin uy tín
- ✅ ~2.7 triệu từ sau tokenization
- ✅ Đa dạng 14+ chủ đề
- ✅ Tuân thủ Web Scraping Ethics

**3️⃣ Tiền xử lý:**
- ✅ Pipeline 7 bước hoàn chỉnh
- ✅ Xử lý đặc thù tiếng Việt (word segmentation)
- ✅ Tối ưu: chỉ xử lý bài mới (tiết kiệm 87% thời gian)
- ✅ 664 bài đã tokenize, 271K từ, 21K từ duy nhất

**4️⃣ Xây dựng mô hình:**
- ✅ 4 mô hình: 1-gram, 2-gram, 3-gram, 4-gram
- ✅ Tổng 2.3M 4-grams duy nhất
- ✅ Lưu trữ định dạng JSON, dễ load

---

### 🎯 **Bước tiếp theo (Báo cáo lần 2):**

**1️⃣ Đánh giá mô hình:**
- Tính Perplexity cho 4 mô hình
- So sánh hiệu suất
- Chọn mô hình tốt nhất

**2️⃣ Xây dựng ứng dụng:**
- Phát triển `ngram_predictor.py`
- Demo dự đoán từ real-time
- Giao diện thân thiện

**3️⃣ Trực quan hóa:**
- ✅ Đã có 2 biểu đồ chất lượng cao
- Thêm biểu đồ so sánh Perplexity

**4️⃣ Viết báo cáo cuối:**
- Tổng hợp kết quả
- Phân tích ưu/nhược điểm
- Đề xuất cải tiến

---

## 📎 **PHỤ LỤC**

### **File đã tạo:**
```
✅ dataset/news.csv                          (6,463 bài gốc)
✅ dataset/news_processed.csv                (664 bài đã xử lý)
✅ dataset/1gram_model.json                  (100K 1-grams)
✅ dataset/2gram_model.json                  (1.1M 2-grams)
✅ dataset/3gram_model.json                  (2.1M 3-grams)
✅ dataset/4gram_model.json                  (2.3M 4-grams)
✅ dataset/ngram_report.txt                  (Báo cáo thống kê)
✅ dataset/model_comparison_detailed.png     (Biểu đồ so sánh)
✅ dataset/vocabulary_analysis_detailed.png  (Biểu đồ từ vựng)
```

### **Code repository:**
```
✅ crawler.py                  (Thu thập dữ liệu đơn nguồn)
✅ multi_source_crawler.py     (Thu thập đa nguồn)
✅ preprocess.py               (Tiền xử lý văn bản)
✅ build_ngram.py              (Xây dựng mô hình)
✅ evaluate_model.py           (Đánh giá mô hình)
✅ ngram_predictor.py          (Dự đoán từ)
✅ visualize.py                (Trực quan hóa)
```

---

**🎓 Cảm ơn quý thầy cô đã theo dõi!**

---

*📅 Ngày báo cáo: Tháng 3/2026*  
*📧 Liên hệ: [email@student.edu.vn]*
