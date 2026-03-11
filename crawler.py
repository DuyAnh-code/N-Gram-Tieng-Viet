"""
CHƯƠNG TRÌNH THU THẬP DỮ LIỆU TIN TÚC TIẾNG VIỆT
Gộp từ main.py và advanced_crawler.py
Tự động crawl dữ liệu từ 4 trang báo lớn
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os
import json
from datetime import datetime
import sys

# ==================== CẤU HÌNH ====================

CONFIG = {
    "max_pages_per_category": 5,      # Số trang crawl mỗi chủ đề
    "max_articles_per_category": 50,  # Giới hạn bài mỗi chủ đề
    "delay_between_requests": 1,      # Delay giữa các request (giây)
    "timeout": 10,                    # Timeout cho mỗi request
    "checkpoint_interval": 10,        # Lưu checkpoint mỗi N bài
}

# Danh sách 4 nguồn tin
NEWS_SOURCES = {
    "vnexpress": {
        "name": "VnExpress",
        "categories": [
            {"name": "Thời sự", "url": "https://vnexpress.net/thoi-su"},
            {"name": "Góc nhìn", "url": "https://vnexpress.net/goc-nhin"},
            {"name": "Thế giới", "url": "https://vnexpress.net/the-gioi"},
            {"name": "Kinh doanh", "url": "https://vnexpress.net/kinh-doanh"},
            {"name": "Giải trí", "url": "https://vnexpress.net/giai-tri"},
            {"name": "Thể thao", "url": "https://vnexpress.net/the-thao"},
            {"name": "Pháp luật", "url": "https://vnexpress.net/phap-luat"},
            {"name": "Giáo dục", "url": "https://vnexpress.net/giao-duc"},
            {"name": "Sức khỏe", "url": "https://vnexpress.net/suc-khoe"},
            {"name": "Đời sống", "url": "https://vnexpress.net/doi-song"},
        ],
        "pagination": "-p{page}",
        "link_selectors": ["h3.title-news a", "h2.title-news a", "article.item-news a.thumb"],
        "title_selector": "h1.title-detail",
        "description_selector": "p.description",
        "content_selector": "article.fck_detail p.Normal",
    },
    "tuoitre": {
        "name": "Tuổi Trẻ",
        "categories": [
            {"name": "Thời sự", "url": "https://tuoitre.vn/thoi-su.htm"},
            {"name": "Thế giới", "url": "https://tuoitre.vn/the-gioi.htm"},
            {"name": "Pháp luật", "url": "https://tuoitre.vn/phap-luat.htm"},
            {"name": "Kinh doanh", "url": "https://tuoitre.vn/kinh-doanh.htm"},
            {"name": "Giáo dục", "url": "https://tuoitre.vn/giao-duc.htm"},
            {"name": "Sức khỏe", "url": "https://tuoitre.vn/suc-khoe.htm"},
            {"name": "Giải trí", "url": "https://tuoitre.vn/giai-tri.htm"},
            {"name": "Thể thao", "url": "https://tuoitre.vn/the-thao.htm"},
        ],
        "pagination": "-trang-{page}.htm",
        "link_selectors": ["a.box-category-link-title", "h3.title-news a", "h2.box-title-text a"],
        "title_selector": "h1.detail-title",
        "description_selector": "h2.detail-sapo",
        "content_selector": "div.detail-content p",
    },
    "thanhnien": {
        "name": "Thanh Niên",
        "categories": [
            {"name": "Thời sự", "url": "https://thanhnien.vn/thoi-su/"},
            {"name": "Thế giới", "url": "https://thanhnien.vn/the-gioi/"},
            {"name": "Pháp luật", "url": "https://thanhnien.vn/phap-luat/"},
            {"name": "Kinh doanh", "url": "https://thanhnien.vn/kinh-te/"},
            {"name": "Giáo dục", "url": "https://thanhnien.vn/giao-duc/"},
            {"name": "Sức khỏe", "url": "https://thanhnien.vn/suc-khoe/"},
            {"name": "Giải trí", "url": "https://thanhnien.vn/giai-tri/"},
            {"name": "Thể thao", "url": "https://thanhnien.vn/the-thao/"},
        ],
        "pagination": "?trang={page}",
        "link_selectors": ["h2.story__title a", "h3.story__title a"],
        "title_selector": "h1.detail__title",
        "description_selector": "div.detail__sapo",
        "content_selector": "div#main-detail-content p",
    },
    "dantri": {
        "name": "Dân Trí",
        "categories": [
            {"name": "Thời sự", "url": "https://dantri.com.vn/thoi-su.htm"},
            {"name": "Thế giới", "url": "https://dantri.com.vn/the-gioi.htm"},
            {"name": "Pháp luật", "url": "https://dantri.com.vn/phap-luat.htm"},
            {"name": "Kinh doanh", "url": "https://dantri.com.vn/kinh-doanh.htm"},
            {"name": "Giáo dục", "url": "https://dantri.com.vn/giao-duc.htm"},
            {"name": "Sức khỏe", "url": "https://dantri.com.vn/suc-khoe.htm"},
            {"name": "Giải trí", "url": "https://dantri.com.vn/giai-tri.htm"},
            {"name": "Thể thao", "url": "https://dantri.com.vn/the-thao.htm"},
        ],
        "pagination": "/trang-{page}.htm",
        "link_selectors": ["h3.article-title a", "h2.article-title a"],
        "title_selector": "h1.title-page",
        "description_selector": "h2.singular-sapo",
        "content_selector": "div.singular-content p",
    }
}

# ==================== HÀM THU THẬP ====================

def get_headers():
    """Tạo headers cho request"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

def get_article_links(source_config, category_url, max_pages):
    """Lấy danh sách link bài báo từ nhiều trang"""
    all_links = []
    
    for page in range(1, max_pages + 1):
        try:
            # Xây dựng URL
            if page == 1:
                url = category_url
            else:
                pagination = source_config['pagination'].replace("{page}", str(page))
                if ".htm" in category_url:
                    url = category_url.replace(".htm", pagination)
                else:
                    url = category_url.rstrip('/') + pagination
            
            # Request
            response = requests.get(url, headers=get_headers(), timeout=CONFIG['timeout'])
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Tìm links
            for selector in source_config['link_selectors']:
                for a in soup.select(selector):
                    href = a.get("href")
                    if href:
                        # Chuẩn hóa URL
                        if href.startswith("/"):
                            base = category_url.split("/")[0] + "//" + category_url.split("/")[2]
                            href = base + href
                        elif not href.startswith("http"):
                            continue
                        
                        # Lọc URL hợp lệ
                        if href not in all_links and "/video" not in href and "/multimedia" not in href:
                            all_links.append(href)
            
            print(f"  📄 Trang {page}: {len(all_links)} links")
            time.sleep(CONFIG['delay_between_requests'])
            
        except Exception as e:
            print(f"  ⚠️ Lỗi trang {page}: {str(e)[:50]}")
            if page > 2:  # Dừng nếu lỗi sau trang 2
                break
    
    return list(set(all_links))  # Loại trùng

def crawl_article(source_config, url):
    """Crawl nội dung một bài báo"""
    try:
        response = requests.get(url, headers=get_headers(), timeout=CONFIG['timeout'])
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Lấy tiêu đề
        title = ""
        title_tag = soup.select_one(source_config['title_selector'])
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Lấy mô tả
        description = ""
        desc_tag = soup.select_one(source_config['description_selector'])
        if desc_tag:
            description = desc_tag.get_text(strip=True)
        
        # Lấy nội dung
        content = ""
        for p in soup.select(source_config['content_selector']):
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                content += text + " "
        
        # Kiểm tra hợp lệ
        if not title or not content or len(content) < 100:
            return None
        
        return {
            "title": title,
            "description": description,
            "content": content.strip(),
            "source": source_config['name'],
            "url": url,
            "crawled_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return None

def save_checkpoint(articles, checkpoint_file="dataset/checkpoint.json"):
    """Lưu checkpoint"""
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def load_checkpoint(checkpoint_file="dataset/checkpoint.json"):
    """Tải checkpoint"""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_to_csv(articles, start_time):
    """Lưu dữ liệu vào CSV (gộp với file cũ nếu có)"""
    if not articles:
        print("\n❌ Không có bài nào để lưu!")
        return
    
    print(f"\n{'='*80}")
    print(f"💾 ĐANG LƯU DỮ LIỆU VÀO CSV")
    print(f"{'='*80}")
    
    # Tạo DataFrame từ bài mới crawl
    df_new = pd.DataFrame(articles)
    
    filename = "dataset/news.csv"
    
    # KIỂM TRA FILE CSV CŨ - NẾU CÓ THÌ GỘP VÀO
    if os.path.exists(filename):
        print(f"\n📂 Phát hiện file CSV cũ: {filename}")
        try:
            df_old = pd.read_csv(filename, encoding='utf-8-sig')
            print(f"  • Số bài cũ: {len(df_old):,} bài")
            print(f"  • Số bài mới: {len(df_new):,} bài")
            
            # Gộp 2 DataFrame
            df = pd.concat([df_old, df_new], ignore_index=True)
            print(f"  • Tổng sau gộp: {len(df):,} bài")
            
            # Loại bỏ trùng lặp (giữ bài cũ nhất)
            original_count = len(df)
            df = df.drop_duplicates(subset=['url'], keep='first')
            duplicate_count = original_count - len(df)
            
            if duplicate_count > 0:
                print(f"  • Đã loại bỏ {duplicate_count:,} bài trùng lặp")
            
            print(f"\n✅ GỘP THÀNH CÔNG!")
            
        except Exception as e:
            print(f"⚠️ Lỗi đọc file cũ: {e}")
            print("  → Tạo file mới thay thế")
            df = df_new
            df = df.drop_duplicates(subset=['url'], keep='first')
    else:
        print(f"\n📄 Tạo file CSV mới")
        df = df_new
        df = df.drop_duplicates(subset=['url'], keep='first')
    
    # Lưu file CSV (ghi đè với dữ liệu đã gộp)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    elapsed = (time.time() - start_time) / 60
    file_size = os.path.getsize(filename) / (1024 * 1024)
    
    print(f"\n✅ ĐÃ LƯU THÀNH CÔNG!")
    print(f"  📁 File: {filename}")
    print(f"  📊 Tổng số bài trong file: {len(df):,} bài")
    print(f"  💾 Kích thước: {file_size:.2f} MB")
    print(f"  ⏱️  Thời gian crawl lần này: {elapsed:.1f} phút")
    if elapsed > 0 and len(df_new) > 0:
        print(f"  ⚡ Tốc độ: {len(df_new)/elapsed:.1f} bài/phút")
    
    # Thống kê theo nguồn
    if 'source' in df.columns:
        print(f"\n📊 THỐNG KÊ THEO NGUỒN (TỔNG CỘNG):")
        print("-" * 60)
        for source, count in df['source'].value_counts().items():
            print(f"  {source:20s}: {count:5,d} bài ({count/len(df)*100:.1f}%)")
    
    # Xóa checkpoint
    checkpoint_file = "dataset/checkpoint.json"
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)
        print(f"\n🗑️  Đã xóa checkpoint")
    
    return df

# ==================== MAIN ====================

def main():
    """Chương trình chính - TỰ ĐỘNG THU THẬP DỮ LIỆU"""
    
    print("=" * 80)
    print("🚀 CHƯƠNG TRÌNH THU THẬP DỮ LIỆU TIN TÚC TIẾNG VIỆT")
    print("=" * 80)
    
    # Tạo thư mục
    os.makedirs("dataset", exist_ok=True)
    
    # Kiểm tra checkpoint
    articles = []
    checkpoint_file = "dataset/checkpoint.json"
    
    print("\n🔧 KIỂM TRA CHECKPOINT...")
    if os.path.exists(checkpoint_file):
        choice = input("Tìm thấy checkpoint! Tiếp tục từ checkpoint? (y/n, mặc định y): ").strip().lower() or "y"
        if choice == "y":
            articles = load_checkpoint(checkpoint_file)
            print(f"✅ Đã tải {len(articles)} bài từ checkpoint")
        else:
            print("🔄 Bắt đầu crawl mới")
    
    # Cấu hình
    print(f"\n⚙️ CẤU HÌNH:")
    print(f"  • Nguồn tin: {len(NEWS_SOURCES)} nguồn ({', '.join([s['name'] for s in NEWS_SOURCES.values()])})")
    print(f"  • Số trang/chủ đề: {CONFIG['max_pages_per_category']}")
    print(f"  • Giới hạn bài/chủ đề: {CONFIG['max_articles_per_category']}")
    print(f"  • Delay: {CONFIG['delay_between_requests']} giây/request")
    
    # Ước tính
    total_categories = sum(len(s['categories']) for s in NEWS_SOURCES.values())
    estimated = total_categories * CONFIG['max_articles_per_category']
    print(f"\n📊 ƯỚC TÍNH:")
    print(f"  • Tổng số chủ đề: {total_categories}")
    print(f"  • Số bài ước tính mỗi vòng: ~{estimated:,} bài")
    print(f"  • Thời gian mỗi vòng: ~{estimated * 1.5 / 60:.0f} phút")
    print(f"\n⏰ CHẾ ĐỘ: Crawl KHÔNG GIỚI HẠN - chạy đến khi bạn dừng (Ctrl+C)")
    print(f"💾 TỰ ĐỘNG LƯU: Khi nhấn Ctrl+C, dữ liệu sẽ tự động lưu vào CSV")
    
    confirm = input("\n⚠️ Bắt đầu thu thập dữ liệu? (y/n, mặc định y): ").strip().lower() or "y"
    if confirm != 'y':
        print("❌ Hủy bỏ!")
        return
    
    # BẮT ĐẦU CRAWL - VÒNG LẶP KHÔNG GIỚI HẠN
    print("\n" + "=" * 80)
    print("📰 BẮT ĐẦU THU THẬP DỮ LIỆU - KHÔNG GIỚI HẠN")
    print("💡 Nhấn Ctrl+C bất cứ lúc nào để dừng và tự động lưu dữ liệu")
    print("=" * 80)
    
    start_time = time.time()
    round_count = 0
    
    try:
        while True:  # VÒNG LẶP VÔ HẠN
            round_count += 1
            print(f"\n{'🔄'*40}")
            print(f"{'='*80}")
            print(f"VÒNG THU THẬP THỨ {round_count}")
            print(f"{'='*80}")
            print(f"{'🔄'*40}\n")
            
            for source_key, source_config in NEWS_SOURCES.items():
                print(f"\n{'='*80}")
                print(f"📰 NGUỒN: {source_config['name'].upper()}")
                print(f"{'='*80}")
                
                for category in source_config['categories']:
                    print(f"\n{'─'*80}")
                    print(f"📂 {category['name']}")
                    
                    # Lấy links
                    print(f"🔍 Đang lấy links từ {CONFIG['max_pages_per_category']} trang...")
                    links = get_article_links(source_config, category['url'], CONFIG['max_pages_per_category'])
                    
                    # Giới hạn số lượng
                    if CONFIG['max_articles_per_category'] > 0:
                        links = links[:CONFIG['max_articles_per_category']]
                    
                    print(f"✅ Tìm thấy {len(links)} links")
                    
                    if not links:
                        print("⚠️ Bỏ qua chủ đề này")
                        continue
                    
                    # Crawl content
                    print(f"📰 Đang crawl {len(links)} bài báo...")
                    success_count = 0
                    
                    for url in tqdm(links, desc=f"{category['name']}", ncols=80):
                        article = crawl_article(source_config, url)
                        if article:
                            articles.append(article)
                            success_count += 1
                            
                            # Lưu checkpoint
                            if len(articles) % CONFIG['checkpoint_interval'] == 0:
                                save_checkpoint(articles, checkpoint_file)
                        
                        time.sleep(CONFIG['delay_between_requests'])
                    
                    print(f"✅ Thành công: {success_count}/{len(links)} bài")
                    print(f"📊 Tổng cộng: {len(articles)} bài")
            
            # KẾT THÚC MỘT VÒNG
            elapsed = (time.time() - start_time) / 60
            print(f"\n{'='*80}")
            print(f"✅ ĐÃ HOÀN THÀNH VÒNG {round_count}")
            print(f"{'='*80}")
            print(f"  📊 Tổng số bài hiện tại: {len(articles):,} bài")
            print(f"  ⏱️  Tổng thời gian: {elapsed:.1f} phút")
            if elapsed > 0 and len(articles) > 0:
                print(f"  ⚡ Tốc độ trung bình: {len(articles)/elapsed:.1f} bài/phút")
            print(f"\n💡 Tiếp tục vòng tiếp theo sau 5 giây...")
            print(f"   (Nhấn Ctrl+C để dừng và lưu)")
            
            # Delay 5 giây trước khi bắt đầu vòng mới
            time.sleep(5)
            
    except KeyboardInterrupt:
        # KHI NHẤN CTRL+C - TỰ ĐỘNG LƯU VÀO CSV
        print("\n\n" + "="*80)
        print("⚠️  ĐANG DỪNG VÀ LƯU DỮ LIỆU...")
        print("="*80)
        
        if articles:
            save_to_csv(articles, start_time)
            
            print(f"\n💡 BƯỚC TIẾP THEO:")
            print(f"  1. python crawler.py            # Chạy lại để crawl thêm")
            print(f"  2. python preprocess.py         # Tiền xử lý dữ liệu")
            print(f"  3. python build_ngram.py        # Xây dựng mô hình")
        else:
            print("\n⚠️  Không có bài nào để lưu!")
            # Vẫn xóa checkpoint nếu có
            if os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)
        
        print("\n" + "=" * 80)
        print("🎉 HOÀN THÀNH!")
        print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
