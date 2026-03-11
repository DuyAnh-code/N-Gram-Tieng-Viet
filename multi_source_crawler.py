import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os
import json
from datetime import datetime

# Cấu hình cho từng nguồn tin
NEWS_SOURCES = {
    "vnexpress": {
        "name": "VnExpress",
        "categories": {
            "1": {"name": "Thời sự", "url": "https://vnexpress.net/thoi-su"},
            "2": {"name": "Góc nhìn", "url": "https://vnexpress.net/goc-nhin"},
            "3": {"name": "Thế giới", "url": "https://vnexpress.net/the-gioi"},
            "4": {"name": "Kinh doanh", "url": "https://vnexpress.net/kinh-doanh"},
            "5": {"name": "Giải trí", "url": "https://vnexpress.net/giai-tri"},
            "6": {"name": "Thể thao", "url": "https://vnexpress.net/the-thao"},
            "7": {"name": "Pháp luật", "url": "https://vnexpress.net/phap-luat"},
            "8": {"name": "Giáo dục", "url": "https://vnexpress.net/giao-duc"},
            "9": {"name": "Sức khỏe", "url": "https://vnexpress.net/suc-khoe"},
            "10": {"name": "Đời sống", "url": "https://vnexpress.net/doi-song"},
        },
        "selectors": {
            "links": ["h3.title-news a", "h2.title-news a", "h3 a.thumb-art", "article.item-news a.thumb"],
            "title": "h1.title-detail",
            "description": "p.description",
            "content": "article.fck_detail p.Normal",
            "category": "ul.breadcrumb li",
            "time": "span.date"
        },
        "pagination": "-p{page}"
    },
    "tuoitre": {
        "name": "Tuổi Trẻ",
        "categories": {
            "1": {"name": "Thời sự", "url": "https://tuoitre.vn/thoi-su.htm"},
            "2": {"name": "Thế giới", "url": "https://tuoitre.vn/the-gioi.htm"},
            "3": {"name": "Pháp luật", "url": "https://tuoitre.vn/phap-luat.htm"},
            "4": {"name": "Kinh doanh", "url": "https://tuoitre.vn/kinh-doanh.htm"},
            "5": {"name": "Giáo dục", "url": "https://tuoitre.vn/giao-duc.htm"},
            "6": {"name": "Sức khỏe", "url": "https://tuoitre.vn/suc-khoe.htm"},
            "7": {"name": "Văn hóa", "url": "https://tuoitre.vn/van-hoa.htm"},
            "8": {"name": "Giải trí", "url": "https://tuoitre.vn/giai-tri.htm"},
            "9": {"name": "Thể thao", "url": "https://tuoitre.vn/the-thao.htm"},
            "10": {"name": "Xe", "url": "https://tuoitre.vn/xe.htm"},
        },
        "selectors": {
            "links": ["h3.title-news a", "h2.box-title-text a", "a.box-category-link-title"],
            "title": "h1.detail-title",
            "description": "h2.detail-sapo",
            "content": "div.detail-content p",
            "category": "ul.detail-breadcrumb li a",
            "time": "div.detail-time"
        },
        "pagination": "-trang-{page}.htm"
    },
    "thanhnien": {
        "name": "Thanh Niên",
        "categories": {
            "1": {"name": "Thời sự", "url": "https://thanhnien.vn/thoi-su/"},
            "2": {"name": "Thế giới", "url": "https://thanhnien.vn/the-gioi/"},
            "3": {"name": "Pháp luật", "url": "https://thanhnien.vn/phap-luat/"},
            "4": {"name": "Kinh doanh", "url": "https://thanhnien.vn/kinh-te/"},
            "5": {"name": "Giáo dục", "url": "https://thanhnien.vn/giao-duc/"},
            "6": {"name": "Sức khỏe", "url": "https://thanhnien.vn/suc-khoe/"},
            "7": {"name": "Đời sống", "url": "https://thanhnien.vn/doi-song/"},
            "8": {"name": "Giải trí", "url": "https://thanhnien.vn/giai-tri/"},
            "9": {"name": "Thể thao", "url": "https://thanhnien.vn/the-thao/"},
            "10": {"name": "Công nghệ", "url": "https://thanhnien.vn/cong-nghe/"},
        },
        "selectors": {
            "links": ["h2.story__title a", "h3.story__title a", "a.story__thumb"],
            "title": "h1.detail__title",
            "description": "div.detail__sapo",
            "content": "div#main-detail-content p",
            "category": "ul.detail__breadcrumb li a",
            "time": "div.detail__meta time"
        },
        "pagination": "?trang={page}"
    },
    "dantri": {
        "name": "Dân Trí",
        "categories": {
            "1": {"name": "Thời sự", "url": "https://dantri.com.vn/thoi-su.htm"},
            "2": {"name": "Thế giới", "url": "https://dantri.com.vn/the-gioi.htm"},
            "3": {"name": "Pháp luật", "url": "https://dantri.com.vn/phap-luat.htm"},
            "4": {"name": "Kinh doanh", "url": "https://dantri.com.vn/kinh-doanh.htm"},
            "5": {"name": "Giáo dục", "url": "https://dantri.com.vn/giao-duc.htm"},
            "6": {"name": "Sức khỏe", "url": "https://dantri.com.vn/suc-khoe.htm"},
            "7": {"name": "Đời sống", "url": "https://dantri.com.vn/doi-song.htm"},
            "8": {"name": "Giải trí", "url": "https://dantri.com.vn/giai-tri.htm"},
            "9": {"name": "Thể thao", "url": "https://dantri.com.vn/the-thao.htm"},
            "10": {"name": "Xe", "url": "https://dantri.com.vn/xe.htm"},
        },
        "selectors": {
            "links": ["h3.article-title a", "h2.article-title a", "a.article-thumb"],
            "title": "h1.title-page",
            "description": "h2.singular-sapo",
            "content": "div.singular-content p",
            "category": "ul.breadcrumb li a",
            "time": "span.author-time"
        },
        "pagination": "/trang-{page}.htm"
    }
}

class MultiSourceCrawler:
    def __init__(self, source_key):
        self.source = NEWS_SOURCES.get(source_key)
        self.source_key = source_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def get_article_links(self, category_url, max_pages=5):
        """Lấy danh sách link bài báo từ nhiều trang"""
        all_links = []
        
        for page in range(1, max_pages + 1):
            try:
                # Xây dựng URL phân trang
                if page == 1:
                    url = category_url
                else:
                    pagination = self.source['pagination']
                    if "{page}" in pagination:
                        url = category_url.replace(".htm", pagination.replace("{page}", str(page)))
                        if ".htm" not in url:
                            url = category_url.rstrip('/') + pagination.replace("{page}", str(page))
                    else:
                        url = category_url + pagination.replace("{page}", str(page))
                
                response = requests.get(url, headers=self.headers, timeout=15)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Tìm link bài báo bằng nhiều selector
                for selector in self.source['selectors']['links']:
                    for a in soup.select(selector):
                        href = a.get("href")
                        if href:
                            # Chuẩn hóa URL
                            if href.startswith("/"):
                                base_url = category_url.split("/")[0] + "//" + category_url.split("/")[2]
                                href = base_url + href
                            elif not href.startswith("http"):
                                continue
                            
                            # Lọc link hợp lệ
                            if (href not in all_links and 
                                "/video" not in href and 
                                "/multimedia" not in href and
                                ".htm" in href or ".html" in href or self.source_key == "vnexpress"):
                                all_links.append(href)
                
                print(f"  📄 Trang {page}: Tìm thấy {len(all_links)} link")
                time.sleep(1)  # Delay giữa các trang
                
            except Exception as e:
                print(f"  ⚠️ Lỗi trang {page}: {e}")
                continue
        
        return list(set(all_links))  # Loại bỏ trùng lặp
    
    def crawl_article(self, url):
        """Crawl nội dung một bài báo"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Lấy tiêu đề
            title = ""
            title_selector = self.source['selectors']['title']
            title_tag = soup.select_one(title_selector)
            if title_tag:
                title = title_tag.get_text(strip=True)
            
            # Lấy mô tả
            description = ""
            desc_selector = self.source['selectors']['description']
            desc_tag = soup.select_one(desc_selector)
            if desc_tag:
                description = desc_tag.get_text(strip=True)
            
            # Lấy nội dung
            content = ""
            content_selector = self.source['selectors']['content']
            for p in soup.select(content_selector):
                text = p.get_text(strip=True)
                if text and len(text) > 20:  # Lọc đoạn văn ngắn
                    content += text + " "
            
            # Lấy category
            category = ""
            cat_selector = self.source['selectors']['category']
            cat_tags = soup.select(cat_selector)
            if cat_tags and len(cat_tags) > 1:
                category = cat_tags[1].get_text(strip=True)
            elif cat_tags:
                category = cat_tags[0].get_text(strip=True)
            
            # Lấy thời gian
            published_time = ""
            time_selector = self.source['selectors']['time']
            time_tag = soup.select_one(time_selector)
            if time_tag:
                published_time = time_tag.get_text(strip=True)
            
            # Kiểm tra dữ liệu hợp lệ
            if not title or not content or len(content) < 100:
                return None
            
            return {
                "title": title,
                "description": description,
                "content": content.strip(),
                "category": category,
                "published_time": published_time,
                "source": self.source['name']
            }
            
        except Exception as e:
            return None

def save_checkpoint(articles, checkpoint_file="dataset/checkpoint_multi.json"):
    """Lưu checkpoint"""
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def load_checkpoint(checkpoint_file="dataset/checkpoint_multi.json"):
    """Tải checkpoint"""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def display_sources():
    """Hiển thị danh sách nguồn tin"""
    print("\n📰 DANH SÁCH NGUỒN TIN:")
    print("-" * 60)
    for idx, (key, info) in enumerate(NEWS_SOURCES.items(), 1):
        print(f"  {idx}. {info['name']:20s} ({len(info['categories'])} chủ đề)")
    print("-" * 60)

def main():
    """Quy trình crawl đa nguồn"""
    
    print("=" * 70)
    print("🚀 CHƯƠNG TRÌNH CRAWL ĐA NGUỒN - 4 TRANG BÁO LỚN")
    print("=" * 70)
    
    os.makedirs("dataset", exist_ok=True)
    
    # Chọn chế độ
    print("\n🔧 CHỌN CHẾ ĐỘ:")
    print("1. Crawl mới")
    print("2. Tiếp tục từ checkpoint")
    mode = input("Nhập lựa chọn (mặc định 1): ").strip() or "1"
    
    articles = []
    if mode == "2":
        articles = load_checkpoint()
        if articles:
            print(f"✅ Đã tải {len(articles)} bài từ checkpoint")
    
    # Chọn nguồn tin
    display_sources()
    print("\n0. Crawl TẤT CẢ các nguồn")
    source_choice = input("Chọn nguồn tin (0-4, mặc định 0): ").strip() or "0"
    
    # Xác định nguồn cần crawl
    if source_choice == "0":
        selected_sources = list(NEWS_SOURCES.keys())
        print(f"✅ Đã chọn crawl TẤT CẢ {len(selected_sources)} nguồn tin")
    else:
        source_idx = int(source_choice) - 1
        if 0 <= source_idx < len(NEWS_SOURCES):
            selected_sources = [list(NEWS_SOURCES.keys())[source_idx]]
            print(f"✅ Đã chọn nguồn: {NEWS_SOURCES[selected_sources[0]]['name']}")
        else:
            print("❌ Lựa chọn không hợp lệ, sử dụng VnExpress")
            selected_sources = ["vnexpress"]
    
    # Cấu hình
    max_pages = int(input("\n📄 Số trang/chủ đề (mặc định 3): ") or "3")
    max_articles_per_cat = int(input("📊 Giới hạn số bài/chủ đề (0=không giới hạn, mặc định 30): ") or "30")
    
    # Crawl từng nguồn
    for source_key in selected_sources:
        print(f"\n{'='*70}")
        print(f"📰 NGUỒN: {NEWS_SOURCES[source_key]['name'].upper()}")
        print(f"{'='*70}")
        
        crawler = MultiSourceCrawler(source_key)
        categories = NEWS_SOURCES[source_key]['categories']
        
        # Chọn chủ đề
        print(f"\n📋 CHỦ ĐỀ CÓ SẴN ({len(categories)} chủ đề):")
        for key, info in list(categories.items())[:5]:
            print(f"  • {info['name']}")
        print("  • ...")
        
        crawl_all = input("\nCrawl tất cả chủ đề? (y/n, mặc định y): ").strip().lower() or "y"
        
        if crawl_all == "y":
            selected_categories = list(categories.values())
        else:
            # Có thể mở rộng để chọn chủ đề cụ thể
            selected_categories = list(categories.values())[:3]
        
        # Crawl từng chủ đề
        for cat_info in selected_categories:
            print(f"\n{'─'*70}")
            print(f"📂 {cat_info['name']}")
            print(f"{'─'*70}")
            
            # Lấy links
            print(f"🔍 Đang lấy links...")
            links = crawler.get_article_links(cat_info['url'], max_pages)
            
            if max_articles_per_cat > 0 and len(links) > max_articles_per_cat:
                links = links[:max_articles_per_cat]
            
            print(f"✅ Tìm thấy {len(links)} link")
            
            if not links:
                continue
            
            # Crawl content
            print(f"📰 Đang crawl nội dung...")
            success_count = 0
            
            for url in tqdm(links, desc=f"{cat_info['name']}", ncols=100):
                article_data = crawler.crawl_article(url)
                
                if article_data:
                    article_data['url'] = url
                    article_data['crawled_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    articles.append(article_data)
                    success_count += 1
                    
                    # Lưu checkpoint mỗi 10 bài
                    if len(articles) % 10 == 0:
                        save_checkpoint(articles)
                
                time.sleep(1)
            
            print(f"✅ Thành công: {success_count}/{len(links)} bài")
    
    # Lưu kết quả
    print(f"\n{'='*70}")
    print(f"💾 ĐANG LƯU DỮ LIỆU")
    print(f"{'='*70}")
    
    if articles:
        df = pd.DataFrame(articles)
        df = df.drop_duplicates(subset=['url'], keep='first')
        
        filename = "dataset/news_multi_source.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Đã lưu {len(df)} bài vào {filename}")
        
        # Thống kê
        print(f"\n📊 THỐNG KÊ THEO NGUỒN:")
        print("-" * 60)
        if 'source' in df.columns:
            for source, count in df['source'].value_counts().items():
                print(f"  {source:20s}: {count:4d} bài")
        
        print(f"\n📊 THỐNG KÊ THEO CHỦ ĐỀ (TOP 10):")
        print("-" * 60)
        if 'category' in df.columns:
            for cat, count in df['category'].value_counts().head(10).items():
                print(f"  {cat:30s}: {count:4d} bài")
        
        # Xóa checkpoint
        checkpoint_file = "dataset/checkpoint_multi.json"
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)
    else:
        print("\n❌ Không crawl được bài nào!")
    
    print("\n" + "=" * 70)
    print("🎉 HOÀN THÀNH!")
    print("=" * 70)
    print(f"\n📈 Tổng kết:")
    print(f"  • Tổng số bài: {len(articles)}")
    print(f"  • File: dataset/news_multi_source.csv")
    print(f"\n💡 Bước tiếp theo:")
    print(f"  1. Chạy: python preprocess.py")
    print(f"  2. Chạy: python build_ngram.py")

if __name__ == "__main__":
    main()
