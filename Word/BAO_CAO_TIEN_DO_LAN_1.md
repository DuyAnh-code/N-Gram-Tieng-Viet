# 📊 BÁO CÁO TIẾN ĐỘ LẦN 1
## ĐỒ ÁN: MÔ HÌNH N-GRAM CHO DỰ ĐOÁN TỪ TIẾNG VIỆT

---

## 📋 THÔNG TIN ĐỒ ÁN

- **Tên đề tài:** Xây dựng mô hình N-gram để dự đoán từ tiếp theo trong văn bản tiếng Việt
- **Môn học:** Các Phương Pháp Học Máy
- **Năm học:** 2025-2026
- **Thời gian báo cáo:** Tháng 3 năm 2026

---

## 🎯 PHẦN 1: XÁC ĐỊNH PHẠM VI ĐỀ TÀI

### 1.1. Bối cảnh và lý do chọn đề tài

#### Tại sao chọn mô hình N-gram?
Mô hình N-gram là một trong những kỹ thuật cơ bản và quan trọng nhất trong **Natural Language Processing (NLP)**. Đây là nền tảng để hiểu các mô hình ngôn ngữ phức tạp hơn như RNN, LSTM, và Transformer.

**Ưu điểm của N-gram:**
- ✅ **Đơn giản và dễ hiểu:** Không cần kiến thức sâu về Deep Learning
- ✅ **Hiệu quả với dữ liệu vừa:** Hoạt động tốt với 500-5,000 bài báo
- ✅ **Tốc độ nhanh:** Training và inference trong vài phút
- ✅ **Khả năng giải thích cao:** Có thể phân tích và debug dễ dàng
- ✅ **Nền tảng vững chắc:** Là tiền đề cho các mô hình hiện đại

#### Tại sao chọn tiếng Việt?
Tiếng Việt có những đặc điểm riêng biệt so với tiếng Anh:
- 🇻🇳 **Không có khoảng trắng tự nhiên giữa các từ** (word segmentation)
- 🇻🇳 **Cấu trúc ngữ pháp khác biệt** (SVO vs SOV)
- 🇻🇳 **Dấu thanh và dấu nặng** ảnh hưởng nghĩa
- 🇻🇳 **Từ ghép phổ biến:** "học sinh", "thành phố"
- 🇻🇳 **Stopwords đặc thù:** "và", "là", "có", "được"

→ **Thách thức:** Cần công cụ tách từ chuyên biệt (Underthesea, VnCoreNLP)

### 1.2. Phạm vi nghiên cứu

#### **Giới hạn về dữ liệu:**
- **Nguồn:** Tin tức từ các trang báo uy tín (VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí)
- **Lĩnh vực:** Tin tức tổng hợp (đời sống, kinh tế, xã hội, giải trí, thể thao...)
- **Quy mô:** 500-2,000 bài báo, tương đương 200,000-1,000,000 từ
- **Thời gian:** Dữ liệu gần đây (2025-2026) để đảm bảo tính thời sự

**Lý do chọn tin tức:**
- ✅ Văn phong chuẩn mực, ngôn ngữ trang trọng
- ✅ Cấu trúc câu rõ ràng, logic
- ✅ Dễ thu thập và cập nhật
- ✅ Đa dạng chủ đề và từ vựng
- ✅ Phù hợp cho auto-complete và text generation

#### **Giới hạn về mô hình:**
- **Loại mô hình:** N-gram từ 1-gram đến 4-gram
- **Không bao gồm:** 
  - ❌ Deep Learning models (LSTM, Transformer)
  - ❌ Word embeddings (Word2Vec, GloVe)
  - ❌ Contextualized embeddings (BERT, PhoBERT)
- **Lý do:** Tập trung vào nền tảng, hiểu rõ bản chất của language modeling

#### **Giới hạn về ứng dụng:**
- ✅ Dự đoán từ tiếp theo (next word prediction)
- ✅ Tạo văn bản tự động (text generation)
- ✅ Phân tích tần suất từ và N-gram
- ❌ Không bao gồm: dịch máy, sentiment analysis, NER

### 1.3. Câu hỏi nghiên cứu

Đề tài tập trung trả lời các câu hỏi sau:

1. **Câu hỏi 1:** Làm thế nào để thu thập và xử lý dữ liệu tiếng Việt hiệu quả?
   - Giải quyết: Web scraping, text cleaning, tokenization

2. **Câu hỏi 2:** Mô hình N-gram nào (Unigram, Bigram, Trigram, 4-gram) cho kết quả tốt nhất cho tiếng Việt?
   - Giải quyết: Đánh giá bằng Perplexity, Accuracy, Coverage

3. **Câu hỏi 3:** Làm thế nào để xử lý N-gram chưa xuất hiện (unseen n-grams)?
   - Giải quyết: Backoff mechanism, Laplace smoothing

4. **Câu hỏi 4:** Mô hình có thể ứng dụng thực tế như thế nào?
   - Giải quyết: Xây dựng ứng dụng demo dự đoán từ

### 1.4. Đóng góp của đề tài

**Đóng góp về kỹ thuật:**
- 📚 Xây dựng pipeline hoàn chỉnh cho NLP tiếng Việt
- 📚 So sánh chi tiết các mô hình N-gram
- 📚 Implement các kỹ thuật đánh giá mô hình

**Đóng góp về dữ liệu:**
- 📊 Tạo dataset tin tức tiếng Việt từ nhiều nguồn
- 📊 Phân tích đặc điểm ngôn ngữ tin tức Việt Nam
- 📊 Chia sẻ công cụ thu thập dữ liệu

**Đóng góp về ứng dụng:**
- 💡 Ứng dụng thực tế cho auto-complete
- 💡 Demo trực quan và dễ sử dụng
- 💡 Mã nguồn mở cho cộng đồng

---

## 📊 PHẦN 2: PHƯƠNG PHÁP THU THẬP DỮ LIỆU

### 2.1. Tổng quan phương pháp

Đề tài sử dụng **Web Scraping** để thu thập dữ liệu văn bản tiếng Việt từ các trang tin tức trực tuyến. Đây là phương pháp phổ biến trong NLP khi cần lượng dữ liệu lớn và đa dạng.

**Quy trình thu thập dữ liệu:**
```
[1. Chọn nguồn] → [2. Thu thập links] → [3. Trích xuất nội dung] 
    → [4. Làm sạch] → [5. Lưu trữ] → [6. Kiểm tra chất lượng]
```

### 2.2. Lựa chọn nguồn dữ liệu

#### **Nguồn 1: VnExpress (vnexpress.net)**
- **Đặc điểm:**
  - Trang báo điện tử lớn nhất Việt Nam
  - Lượng truy cập: 50+ triệu/tháng
  - Cập nhật liên tục 24/7
  - Văn phong: Ngắn gọn, súc tích, tin nhanh
  
- **Chủ đề thu thập (14 chủ đề):**
  1. Thời sự (chinh-tri)
  2. Kinh doanh (kinh-doanh)
  3. Giải trí (giai-tri)
  4. Thể thao (the-thao)
  5. Pháp luật (phap-luat)
  6. Giáo dục (giao-duc)
  7. Sức khỏe (suc-khoe)
  8. Đời sống (doi-song)
  9. Du lịch (du-lich)
  10. Khoa học (khoa-hoc)
  11. Số hóa (so-hoa)
  12. Xe (xe)
  13. Ý kiến (y-kien)
  14. Tâm sự (tam-su)

- **Cấu trúc HTML:**
  - URL danh sách: `https://vnexpress.net/{category}`
  - Thẻ tiêu đề: `<h3 class="title-news">`
  - Thẻ nội dung: `<article class="fck_detail">`

#### **Nguồn 2: Tuổi Trẻ (tuoitre.vn)**
- **Đặc điểm:**
  - Báo thanh niên, phong cách trẻ trung
  - Nội dung dài và chuyên sâu hơn
  - Nhiều bài phân tích, bình luận
  - Văn phong: Trang trọng, học thuật

- **Chủ đề thu thập (10+ chủ đề):**
  - Thời sự, Kinh tế, Pháp luật
  - Giáo dục, Sức khỏe, Du lịch
  - Văn hóa, Thể thao, Công nghệ

#### **Nguồn 3: Thanh Niên (thanhnien.vn)**
- **Đặc điểm:**
  - Phong cách gần gũi, dễ hiểu
  - Nhiều tin địa phương
  - Cập nhật nhanh về giải trí, thể thao

#### **Nguồn 4: Dân Trí (dantri.com.vn)**
- **Đặc điểm:**
  - Cân bằng giữa tin nhanh và chuyên sâu
  - Nhiều chủ đề đa dạng
  - Văn phong trung lập, khách quan

### 2.3. Kiến trúc hệ thống thu thập dữ liệu

#### **Kiến trúc tổng thể:**

```
┌─────────────────────────────────────────────────┐
│            MULTI-SOURCE CRAWLER                  │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │VnExpress │  │Tuổi Trẻ  │  │Thanh Niên│       │
│  │  Parser  │  │  Parser  │  │  Parser  │  ...  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       └─────────────┼─────────────┘              │
│                     ▼                            │
│         ┌───────────────────────┐                │
│         │   Link Aggregator    │                │
│         │  (Loại bỏ trùng lặp)  │                │
│         └───────────┬───────────┘                │
│                     ▼                            │
│         ┌───────────────────────┐                │
│         │  Content Extractor    │                │
│         │  (Lấy tiêu đề + nội dung)│              │
│         └───────────┬───────────┘                │
│                     ▼                            │
│         ┌───────────────────────┐                │
│         │    Data Validator     │                │
│         │ (Kiểm tra độ dài, null)│               │
│         └───────────┬───────────┘                │
│                     ▼                            │
│         ┌───────────────────────┐                │
│         │   CSV Storage         │                │
│         │  (dataset/news*.csv)  │                │
│         └───────────────────────┘                │
└─────────────────────────────────────────────────┘
```

#### **Module chi tiết:**

**1. crawler_links.py** - Thu thập danh sách URL
```python
Chức năng:
- Truy cập trang danh sách tin tức
- Parse HTML để lấy các thẻ <a> chứa link
- Lọc link hợp lệ (loại bỏ quảng cáo, liên kết ngoài)
- Hỗ trợ pagination (crawl nhiều trang)
- Trả về: List[str] - danh sách URL bài báo
```

**2. crawler_content.py** - Trích xuất nội dung
```python
Chức năng:
- Nhận vào URL bài báo
- Request HTML và parse với BeautifulSoup
- Tìm thẻ chứa tiêu đề (title)
- Tìm thẻ chứa nội dung (content/article)
- Làm sạch HTML tags, scripts, ads
- Trả về: Dict[str, str] = {title, content, category, url}
```

**3. save_data.py** - Lưu trữ dữ liệu
```python
Chức năng:
- Nhận danh sách dictionary từ crawler
- Chuyển đổi sang pandas DataFrame
- Loại bỏ bài trùng lặp (dựa trên URL hoặc title)
- Kiểm tra dữ liệu null/empty
- Lưu vào CSV với encoding utf-8-sig
- Thống kê: số bài, số từ trung bình
```

**4. main.py** - Crawler đơn nguồn (VnExpress)
```python
Luồng hoạt động:
1. Chọn danh sách 14 categories
2. Với mỗi category:
   - Crawl N trang (pagination)
   - Mỗi trang lấy M bài báo
3. Tổng: 14 × N × M bài (ví dụ: 14 × 3 × 30 = 1,260 bài)
4. Checkpoint mỗi 50 bài
5. Lưu vào dataset/news.csv
```

**5. multi_source_crawler.py** - Crawler đa nguồn (4 nguồn)
```python
Luồng hoạt động:
1. Người dùng chọn nguồn (1-4 hoặc tất cả)
2. Với mỗi nguồn:
   - Load cấu hình parser riêng
   - Crawl theo categories của nguồn đó
3. Gộp dữ liệu từ tất cả nguồn
4. Loại bỏ trùng lặp giữa các nguồn (based on title similarity)
5. Lưu vào dataset/news_multi_source.csv
6. Tạo báo cáo thống kê theo nguồn
```

### 2.4. Kỹ thuật xử lý HTML

#### **Xử lý đa dạng cấu trúc HTML:**

Mỗi trang báo có cấu trúc HTML khác nhau. Đề tài sử dụng **strategy pattern** để xử lý:

```python
# Ví dụ: VnExpress
selectors_vnexpress = {
    'title': ['h1.title-detail', 'h1.title_news_detail'],
    'content': ['article.fck_detail', 'div.maincontent']
}

# Ví dụ: Tuổi Trẻ
selectors_tuoitre = {
    'title': ['h1.article-title', 'h1.detail-title'],
    'content': ['div.detail-content', 'div#main-detail-content']
}

# Fallback mechanism
for selector in selectors['title']:
    element = soup.select_one(selector)
    if element:
        title = element.get_text(strip=True)
        break
```

#### **Làm sạch nội dung:**

```python
Các bước làm sạch:
1. Loại bỏ HTML tags: <p>, <div>, <span>...
2. Loại bỏ scripts: <script>, <style>
3. Loại bỏ quảng cáo: class="ads", id="advertisement"
4. Loại bỏ ký tự đặc biệt: \n\n\n → \n
5. Loại bỏ khoảng trắng thừa: "  abc  " → "abc"
6. Decode HTML entities: &nbsp; → space, &quot; → "
```

### 2.5. Tuân thủ Web Scraping Ethics

#### **Nguyên tắc tuân thủ:**

**1. Kiểm tra robots.txt**
```python
# Ví dụ: https://vnexpress.net/robots.txt
User-agent: *
Disallow: /admin/
Disallow: /api/
Allow: /
Crawl-delay: 1

→ Tuân thủ: Không crawl /admin/, thêm delay 1 giây
```

**2. Rate Limiting**
```python
import time

for url in urls:
    content = crawl_content(url)
    save_data(content)
    time.sleep(1)  # Delay 1 giây giữa các request
```

**3. User-Agent Header**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Educational Research Bot)',
    'From': 'student@university.edu.vn'
}
response = requests.get(url, headers=headers)
```

**4. Xử lý lỗi và Retry**
```python
max_retries = 3
for i in range(max_retries):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            break
    except Exception as e:
        if i == max_retries - 1:
            log_error(f"Failed: {url}")
        time.sleep(2 ** i)  # Exponential backoff
```

### 2.6. Kiểm soát chất lượng dữ liệu

#### **Tiêu chí chất lượng:**

**1. Độ dài tối thiểu**
```python
MIN_CONTENT_LENGTH = 100  # ký tự
MIN_WORD_COUNT = 50       # từ

if len(content) < MIN_CONTENT_LENGTH:
    reject("Nội dung quá ngắn")
```

**2. Loại bỏ trùng lặp**
```python
# Dựa trên URL
df = df.drop_duplicates(subset=['url'])

# Dựa trên title (similarity > 80%)
from difflib import SequenceMatcher
def is_duplicate(title1, title2):
    ratio = SequenceMatcher(None, title1, title2).ratio()
    return ratio > 0.8
```

**3. Kiểm tra encoding**
```python
# Đảm bảo UTF-8 hợp lệ
content = content.encode('utf-8').decode('utf-8')

# Loại bỏ ký tự không in được
import re
content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
```

**4. Thống kê chất lượng**
```python
Metrics:
- Tỷ lệ thành công: 95%+ (số bài crawl thành công / tổng số URL)
- Tỷ lệ bị reject: <5% (bài không đạt tiêu chí)
- Tỷ lệ trùng lặp: <10%
- Độ dài trung bình: 300-500 từ/bài
```

### 2.7. Lưu trữ và format dữ liệu

#### **Format CSV:**

```csv
title,content,category,source,url,date_crawled
"Tiêu đề bài 1","Nội dung đầy đủ...","thoi-su","vnexpress","https://...","2026-03-10"
"Tiêu đề bài 2","Nội dung đầy đủ...","kinh-te","tuoitre","https://...","2026-03-10"
```

**Lý do chọn CSV:**
- ✅ Đơn giản, dễ đọc
- ✅ Tương thích với pandas
- ✅ Dễ chia sẻ và backup
- ✅ Hỗ trợ UTF-8 tốt

#### **Checkpoint system:**

```python
# Lưu checkpoint mỗi 50 bài
if len(articles) % 50 == 0:
    save_checkpoint(articles, f"checkpoint_{len(articles)}.csv")

# Khôi phục khi bị gián đoạn
if os.path.exists("checkpoint_latest.csv"):
    articles = load_checkpoint("checkpoint_latest.csv")
    print(f"Resume from {len(articles)} articles")
```

### 2.8. Kết quả thu thập

#### **Thống kê dữ liệu (ước tính):**

| Nguồn      | Số bài báo | Số từ trung bình | Tổng số từ   | % đóng góp |
|------------|------------|------------------|--------------|------------|
| VnExpress  | 500        | 250 từ           | 125,000 từ   | 35%        |
| Tuổi Trẻ   | 300        | 400 từ           | 120,000 từ   | 33%        |
| Thanh Niên | 350        | 300 từ           | 105,000 từ   | 29%        |
| Dân Trí    | 150        | 350 từ           | 52,500 từ    | 14%        |
| **TỔNG**   | **1,300**  | **310 từ**       | **402,500 từ**| **100%**  |

#### **Phân bố theo chủ đề:**

```
Thời sự/Chính trị:  25% (325 bài)
Kinh tế:            18% (234 bài)
Giải trí:           15% (195 bài)
Thể thao:           12% (156 bài)
Pháp luật:          10% (130 bài)
Khác:               20% (260 bài)
```

---

## 🎯 MỤC TIÊU ĐỒ ÁN

### Mục tiêu chính:
1. ✅ Thu thập dữ liệu văn bản tiếng Việt từ nhiều nguồn tin tức
2. ✅ Xây dựng pipeline tiền xử lý dữ liệu tiếng Việt
3. ✅ Xây dựng các mô hình N-gram (Unigram, Bigram, Trigram, 4-gram)
4. ✅ Đánh giá hiệu suất các mô hình
5. ✅ Phát triển ứng dụng dự đoán từ tiếp theo
6. ✅ Trực quan hóa dữ liệu và kết quả

### Ứng dụng thực tế:
- Dự đoán từ tiếp theo (auto-complete)
- Tạo văn bản tự động (text generation)
- Phân tích ngôn ngữ tiếng Việt
- Nền tảng cho các mô hình ngôn ngữ phức tạp hơn

---
