import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os
import json
import gzip
import pickle
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import threading
import sys

# Cấu hình crawler nâng cao
CONFIG = {
    "max_workers": 5,
    "timeout": 15,  # Tăng timeout lên 15s
    "delay_between_requests": 0.5,  # Giảm delay để nhanh hơn
    "checkpoint_interval": 50,
    "enable_compression": True,
    "max_retries": 3,  # Tăng lên 3 retry
    "max_links_per_category": 1000,  # TĂNG LÊN 1000 links/chủ đề
    "user_agents": [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    ]
}

NEWS_SOURCES = {
    "tuoitre": {
        "name": "Tuổi Trẻ",
        "base_url": "https://tuoitre.vn",
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
            "links": [
                "a.box-category-link-title",
                "h3.title-news a",
                "h2.box-title-text a",
                "div.box-category-content a",
                "a[href*='.htm']",
            ],
            "title": ["h1.detail-title", "h1.article-title", "h1"],
            "description": ["h2.detail-sapo", "div.sapo", "p.sapo"],
            "content": ["div.detail-content p", "div.article-content p", "div.content p"],
            "category": ["ul.detail-breadcrumb li a", "div.breadcrumb a"],
            "time": ["div.detail-time", "span.date-time"]
        },
        "pagination_patterns": ["-trang-{page}.htm", "?page={page}"]
    },
    "thanhnien": {
        "name": "Thanh Niên",
        "base_url": "https://thanhnien.vn",
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
            "links": [
                "h2.story__title a",
                "h3.story__title a",
                "a.story__thumb",
                "article a[title]",
            ],
            "title": ["h1.detail__title", "h1.article-title", "h1"],
            "description": ["div.detail__sapo", "div.sapo"],
            "content": ["div#main-detail-content p", "div.detail-content p"],
            "category": ["ul.detail__breadcrumb li a", "div.breadcrumb a"],
            "time": ["div.detail__meta time", "time"]
        },
        "pagination_patterns": ["?trang={page}", "?page={page}"]
    },
    "dantri": {
        "name": "Dân Trí",
        "base_url": "https://dantri.com.vn",
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
            "links": [
                "h3.article-title a",
                "h2.article-title a",
                "a.article-thumb",
                "article a[title]",
            ],
            "title": ["h1.title-page", "h1.article-title", "h1"],
            "description": ["h2.singular-sapo", "div.sapo"],
            "content": ["div.singular-content p", "div.article-content p"],
            "category": ["ul.breadcrumb li a", "div.breadcrumb a"],
            "time": ["span.author-time", "time"]
        },
        "pagination_patterns": ["/trang-{page}.htm", "?page={page}"]
    },
    "vnexpress": {
        "name": "VnExpress",
        "base_url": "https://vnexpress.net",
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
            "11": {"name": "Du lịch", "url": "https://vnexpress.net/du-lich"},
            "12": {"name": "Khoa học", "url": "https://vnexpress.net/khoa-hoc"},
            "13": {"name": "Số hóa", "url": "https://vnexpress.net/so-hoa"},
            "14": {"name": "Xe", "url": "https://vnexpress.net/oto-xe-may"},
        },
        "selectors": {
            "links": [
                "article.item-news a.thumb",  # Selector chính
                "h3.title-news a",
                "h2.title-news a", 
                "h3 a.thumb-art",
                "article a[title]",  # Fallback
                "div.list-news-subfolder article a",
                "a[href*='/thoi-su/']",  # By URL pattern
                "a[href*='/goc-nhin/']",
                "a[href*='/the-gioi/']",
            ],
            "title": ["h1.title-detail", "h1.title_news_detail", "h1"],
            "description": ["p.description", "p.lead-detail", "div.description"],
            "content": [
                "article.fck_detail p.Normal",
                "article.content_detail p",
                "div.fck_detail p",
                "div.Normal"
            ],
            "category": ["ul.breadcrumb li", "div.breadcrumb li"],
            "time": ["span.date", "span.time"]
        },
        "pagination_patterns": ["-p{page}", "?page={page}", "/p{page}"]  # Thử nhiều pattern
    },
    "vietnamnet": {
        "name": "Vietnamnet",
        "base_url": "https://vietnamnet.vn",
        "categories": {
            "1": {"name": "Thời sự", "url": "https://vietnamnet.vn/thoi-su"},
            "2": {"name": "Thế giới", "url": "https://vietnamnet.vn/the-gioi"},
            "3": {"name": "Kinh doanh", "url": "https://vietnamnet.vn/kinh-doanh"},
            "4": {"name": "Giải trí", "url": "https://vietnamnet.vn/giai-tri"},
            "5": {"name": "Thể thao", "url": "https://vietnamnet.vn/the-thao"},
            "6": {"name": "Pháp luật", "url": "https://vietnamnet.vn/phap-luat"},
            "7": {"name": "Giáo dục", "url": "https://vietnamnet.vn/giao-duc"},
            "8": {"name": "Sức khỏe", "url": "https://vietnamnet.vn/suc-khoe"},
            "9": {"name": "Đời sống", "url": "https://vietnamnet.vn/doi-song"},
        },
        "selectors": {
            "links": [
                "h3.vnn-title a",
                "div.vnn-title a",
                "a.vnn-title"
            ],
            "title": ["h1.content-detail-title", "h1.title", "h1"],
            "description": ["h2.content-detail-sapo", "h2.sapo", "div.sapo"],
            "content": ["div.maincontent p", "div.article-content p"],
            "category": ["div.bread-crumb-detail a", "div.breadcrumb a"],
            "time": ["span.date", "div.bread-crumb-detail span"]
        },
        "pagination_patterns": ["-page{page}"]
    },
    "nld": {
        "name": "Người Lao Động",
        "base_url": "https://nld.com.vn",
        "categories": {
            "1": {"name": "Thời sự", "url": "https://nld.com.vn/thoi-su.htm"},
            "2": {"name": "Quốc tế", "url": "https://nld.com.vn/quoc-te.htm"},
            "3": {"name": "Kinh tế", "url": "https://nld.com.vn/kinh-te.htm"},
            "4": {"name": "Giáo dục", "url": "https://nld.com.vn/giao-duc.htm"},
            "5": {"name": "Pháp luật", "url": "https://nld.com.vn/phap-luat.htm"},
            "6": {"name": "Giải trí", "url": "https://nld.com.vn/giai-tri.htm"},
            "7": {"name": "Thể thao", "url": "https://nld.com.vn/the-thao.htm"},
            "8": {"name": "Sức khỏe", "url": "https://nld.com.vn/suc-khoe.htm"},
        },
        "selectors": {
            "links": [
                "h3.title-news a",
                "h2.title-news a",
                "a.link-title",
                "a[href*='.htm']"
            ],
            "title": ["h1.title-detail", "h1"],
            "description": ["h2.sapo-detail", "h2.sapo", "div.sapo"],
            "content": ["div.content-detail p", "div.detail-content p"],
            "category": ["div.bread-crumbs a", "ul.breadcrumb li a"],
            "time": ["span.date", "span.date-time"]
        },
        "pagination_patterns": ["-trang-{page}.htm"]
    }
}

class CrawlerCore:
    """Crawler lõi đã hợp nhất với parallel processing và compression"""
    
    def __init__(self, source_key: str):
        self.source = NEWS_SOURCES.get(source_key)
        self.source_key = source_key
        self.lock = threading.Lock()
        self.success_count = 0
        self.fail_count = 0
        
    def get_headers(self):
        """Random User-Agent để tránh bị chặn"""
        import random
        return {
            'User-Agent': random.choice(CONFIG['user_agents']),
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
        }
    
    def get_article_links(self, category_url: str, max_pages: int = 50) -> List[str]:
        """Lấy links với SMART PAGINATION và FLEXIBLE SELECTORS"""
        all_links = set()  # Dùng set để tự động loại trùng
        consecutive_failures = 0
        max_consecutive_failures = 3
        
        print(f"   🎯 Mục tiêu: {CONFIG['max_links_per_category']} links")
        
        for page in range(1, max_pages + 1):
            # DỪNG nếu đủ links
            if len(all_links) >= CONFIG['max_links_per_category']:
                print(f"   ✅ Đã đủ {CONFIG['max_links_per_category']} links!")
                break
            
            # DỪNG nếu liên tục thất bại
            if consecutive_failures >= max_consecutive_failures:
                print(f"   ⛔ Dừng sau {consecutive_failures} lần thất bại liên tiếp")
                break
            
            try:
                # XÂY DỰNG URL với smart pagination
                if page == 1:
                    url = category_url
                else:
                    url = self._build_pagination_url(category_url, page)
                
                if page <= 5 or page % 10 == 0:  # In log định kỳ
                    print(f"   📄 Trang {page}: {url[:80]}...")
                
                response = requests.get(url, headers=self.get_headers(), timeout=CONFIG['timeout'])
                
                if response.status_code != 200:
                    print(f"   ⚠️ HTTP {response.status_code} - Trang {page}")
                    consecutive_failures += 1
                    if page > 5:
                        break
                    continue
                
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, "html.parser")
                
                # THỬ TẤT CẢ SELECTORS cho đến khi có kết quả
                page_links = self._extract_links_flexible(soup, category_url)
                
                if not page_links:
                    consecutive_failures += 1
                    if page <= 5:
                        print(f"   ⚠️ Trang {page}: Không tìm thấy link (thử selector khác...)")
                    if page > 3:
                        break
                    continue
                
                # THÀNH CÔNG - reset failure counter
                consecutive_failures = 0
                new_links = [link for link in page_links if link not in all_links]
                all_links.update(new_links)
                
                if page <= 10 or page % 10 == 0:
                    print(f"   ✅ Trang {page}: +{len(new_links)} links (tổng: {len(all_links)})")
                
                # Delay
                time.sleep(CONFIG['delay_between_requests'])
                
            except requests.Timeout:
                print(f"   ⏱️ Timeout trang {page}")
                consecutive_failures += 1
                if page > 5:
                    break
            except Exception as e:
                print(f"   ❌ Lỗi trang {page}: {str(e)[:50]}")
                consecutive_failures += 1
                if page > 5:
                    break
        
        print(f"   🎉 Hoàn thành: {len(all_links)} links từ {page} trang")
        return list(all_links)
    
    def _build_pagination_url(self, base_url: str, page: int) -> str:
        """Xây dựng URL phân trang thông minh"""
        patterns = self.source.get('pagination_patterns', ["-p{page}"])
        
        for pattern in patterns:
            if ".htm" in base_url:
                # Format: /category.htm -> /category-trang-2.htm
                url = base_url.replace(".htm", pattern.replace("{page}", str(page)))
            else:
                # Format: /category/ -> /category/?page=2
                url = base_url.rstrip('/') + pattern.replace("{page}", str(page))
            
            # Chỉ return URL đầu tiên (có thể mở rộng để test nhiều pattern)
            return url
        
        return base_url + f"?page={page}"  # Fallback
    
    def _extract_links_flexible(self, soup, base_url: str) -> List[str]:
        """Trích xuất links với NHIỀU SELECTOR DỰ PHÒNG"""
        links = []
        base_domain = '/'.join(base_url.split('/')[:3])
        
        # THỬ TẤT CẢ SELECTORS
        selectors = self.source['selectors']['links']
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            for a in soup.select(selector):
                href = a.get("href")
                if not href:
                    continue
                
                # Chuẩn hóa URL
                if href.startswith("/"):
                    href = base_domain + href
                elif not href.startswith("http"):
                    continue
                
                # Lọc URL không hợp lệ
                if any(x in href for x in ["/video", "/multimedia", "/podcast", "#", "javascript:"]):
                    continue
                
                # Kiểm tra có phải bài báo không
                if self._is_valid_article_url(href):
                    links.append(href)
        
        return list(set(links))  # Loại trùng
    
    def _is_valid_article_url(self, url: str) -> bool:
        """Kiểm tra URL có phải bài báo hợp lệ"""
        # Phải có ít nhất 1 số (ID bài báo)
        if not any(char.isdigit() for char in url):
            return False
        
        # Loại các URL không phải bài báo
        invalid_patterns = [
            '/category/', '/tag/', '/search', '/rss', 
            '.jpg', '.png', '.gif', '.pdf',
            '/page/', '/archive/'
        ]
        
        return not any(pattern in url.lower() for pattern in invalid_patterns)
    
    def crawl_article(self, url: str) -> Optional[Dict]:
        """Crawl một bài báo với FLEXIBLE SELECTORS"""
        for attempt in range(CONFIG['max_retries']):
            try:
                response = requests.get(url, headers=self.get_headers(), timeout=CONFIG['timeout'])
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Lấy dữ liệu với NHIỀU SELECTOR
                title = self._extract_text(soup, self.source['selectors']['title'])
                description = self._extract_text(soup, self.source['selectors']['description'])
                content = self._extract_content(soup, self.source['selectors']['content'])
                category = self._extract_category(soup, self.source['selectors']['category'])
                published_time = self._extract_text(soup, self.source['selectors']['time'])
                
                # Validate
                if not title or not content or len(content) < 100:
                    return None
                
                with self.lock:
                    self.success_count += 1
                
                return {
                    "title": title,
                    "description": description,
                    "content": content.strip(),
                    "category": category,
                    "published_time": published_time,
                    "source": self.source['name'],
                    "url": url,
                    "crawled_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
            except Exception as e:
                if attempt == CONFIG['max_retries'] - 1:
                    with self.lock:
                        self.fail_count += 1
                    return None
                time.sleep(1)
        
        return None
    
    def _extract_text(self, soup, selectors) -> str:
        """Trích xuất text với nhiều selector"""
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            tag = soup.select_one(selector)
            if tag:
                return tag.get_text(strip=True)
        
        return ""
    
    def _extract_content(self, soup, selectors) -> str:
        """Trích xuất nội dung với nhiều selector"""
        if isinstance(selectors, str):
            selectors = [selectors]
        
        content = ""
        for selector in selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:
                        content += text + " "
                if content:
                    break
        
        return content
    
    def _extract_category(self, soup, selectors) -> str:
        """Trích xuất category"""
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            tags = soup.select(selector)
            if tags and len(tags) > 1:
                return tags[1].get_text(strip=True)
            elif tags:
                return tags[0].get_text(strip=True)
        
        return ""
    
    def crawl_parallel(self, urls: List[str]) -> List[Dict]:
        """Crawl song song nhiều URL"""
        articles = []
        
        with ThreadPoolExecutor(max_workers=CONFIG['max_workers']) as executor:
            future_to_url = {executor.submit(self.crawl_article, url): url for url in urls}
            
            for future in tqdm(as_completed(future_to_url), total=len(urls), desc=f"Crawling {self.source['name']}"):
                result = future.result()
                if result:
                    articles.append(result)
                time.sleep(CONFIG['delay_between_requests'])
        
        return articles

def save_checkpoint_compressed(articles: List[Dict], filepath: str):
    """Lưu checkpoint với nén"""
    if CONFIG['enable_compression']:
        with gzip.open(filepath + '.gz', 'wb') as f:
            pickle.dump(articles, f)
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

def load_checkpoint_compressed(filepath: str) -> List[Dict]:
    """Tải checkpoint đã nén"""
    if os.path.exists(filepath + '.gz'):
        with gzip.open(filepath + '.gz', 'rb') as f:
            return pickle.load(f)
    elif os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def estimate_data_size(num_articles: int) -> str:
    """Ước tính kích thước dữ liệu"""
    avg_size_kb = 2.5  # Trung bình 2.5KB/bài
    total_mb = (num_articles * avg_size_kb) / 1024
    if total_mb < 1024:
        return f"{total_mb:.1f} MB"
    else:
        return f"{total_mb/1024:.2f} GB"

def main():
    """Chương trình Crawler chính đã hợp nhất"""
    
    print("=" * 80)
    print("🚀 N-GRAM CRAWLER - THU THẬP DỮ LIỆU BÁO CHÍ ĐA LUỒNG TỐI ƯU")
    print("=" * 80)
    
    os.makedirs("dataset", exist_ok=True)
    
    # Kiểm tra tham số tự động
    auto_mode = "--auto" in sys.argv or "-a" in sys.argv
    
    # Chọn chế độ
    if auto_mode:
        mode = "1"
        print("\n🔧 CHẾ ĐỘ: Tự động - Crawl mới")
    else:
        print("\n🔧 CHỌN CHẾ ĐỘ:")
        print("1. Crawl mới")
        print("2. Tiếp tục từ checkpoint")
        mode = input("Nhập lựa chọn (mặc định 1): ").strip() or "1"
    
    checkpoint_file = "dataset/checkpoint_crawler.pkl"
    articles = []
    all_collected_links = []
    
    if mode == "2":
        articles = load_checkpoint_compressed(checkpoint_file)
        if articles:
            print(f"✅ Đã tải {len(articles)} bài từ checkpoint (~{estimate_data_size(len(articles))})")
    
    # Chọn nguồn
    if auto_mode:
        source_choice = "0"
        selected_sources = list(NEWS_SOURCES.keys())
        print(f"\n📰 NGUỒN: Tất cả {len(selected_sources)} nguồn")
    else:
        print("\n📰 CHỌN NGUỒN TIN:")
        for idx, (key, info) in enumerate(NEWS_SOURCES.items(), 1):
            print(f"  {idx}. {info['name']:20s} ({len(info['categories'])} chủ đề)")
        print("  0. Crawl TẤT CẢ TỰ ĐỘNG")
        
        source_choice = input("\nChọn (0-6, mặc định 0): ").strip() or "0"
        
        if source_choice == "0":
            selected_sources = list(NEWS_SOURCES.keys())
            print(f"✅ Chọn tất cả {len(selected_sources)} nguồn")
        else:
            source_idx = int(source_choice) - 1
            selected_sources = [list(NEWS_SOURCES.keys())[source_idx]]
    
    # Cấu hình crawl
    if auto_mode:
        max_pages = 5  # Số trang rút ngắn để chạy liên tục qua các nguồn
        target_articles = 0  # Không giới hạn số bài
        duration_hours = None  # KHÔNG GIỚI HẠN THỜI GIAN
        print(f"\n⚙️ CẤU HÌNH TỰ ĐỘNG:")
        print(f"  • Số trang/chủ đề: {max_pages}")
        print(f"  • Số luồng song song: {CONFIG['max_workers']}")
    else:
        print("\n⚙️ CẤU HÌNH CRAWL:")
        print(f"Hiện tại: {CONFIG['max_workers']} luồng song song")
        
        max_pages = int(input("\n📄 Số trang/chủ đề (khuyến nghị 5-20): ").strip() or "5")
        target_articles = int(input("🎯 Mục tiêu số bài (0=không giới hạn): ").strip() or "0")
        duration_hours = None
    
    if not auto_mode:
        confirm = input("\n⚠️ Bắt đầu crawl? (y/n, mặc định y): ").strip().lower() or 'y'
        if confirm != 'y':
            print("❌ Hủy bỏ!")
            return
    else:
        print("\n⚠️ Bắt đầu crawl tự động...")
    
    # Bắt đầu crawl
    start_time = time.time()
    
    for source_key in selected_sources:
        print(f"\n{'='*80}")
        print(f"📰 NGUỒN: {NEWS_SOURCES[source_key]['name'].upper()}")
        print(f"{'='*80}")
        
        crawler = CrawlerCore(source_key)
        categories = NEWS_SOURCES[source_key]['categories']
        
        for cat_info in categories.values():
            if target_articles > 0 and len(articles) >= target_articles:
                print(f"\n🎯 Đã đạt mục tiêu {target_articles:,} bài!")
                break
            
            print(f"\n{'─'*80}")
            print(f"📂 {cat_info['name']}")
            
            # Lấy links
            print(f"🔍 Đang lấy links từ {max_pages} trang...")
            links = crawler.get_article_links(cat_info['url'], max_pages)
            print(f"✅ Tìm thấy {len(links)} link")
            
            if not links:
                continue
            
            # Lưu lại links ra Excel
            for link in links:
                all_collected_links.append({
                    "Nguồn báo": NEWS_SOURCES[source_key]['name'],
                    "Chuyên mục": cat_info['name'],
                    "Đường dẫn URL": link,
                    "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            try:
                df_links = pd.DataFrame(all_collected_links)
                df_links.to_excel("dataset/crawled_links.xlsx", index=False)
            except Exception as e:
                print(f"⚠️ Không thể lưu links ra Excel: {e}")
            
            # Crawl parallel
            print(f"📰 Đang crawl với {CONFIG['max_workers']} luồng...")
            new_articles = crawler.crawl_parallel(links)
            articles.extend(new_articles)
            
            print(f"✅ Thành công: {len(new_articles)}/{len(links)} bài")
            print(f"📊 Tổng đợt này hiện có: {len(articles):,} bài (~{estimate_data_size(len(articles))})")
            
            # Lưu checkpoint
            if len(articles) % CONFIG['checkpoint_interval'] == 0:
                save_checkpoint_compressed(articles, checkpoint_file)
        
        if target_articles > 0 and len(articles) >= target_articles:
            break
    
    # LƯU VÀ GỘP DỮ LIỆU
    print(f"\n{'='*80}")
    print(f"💾 ĐANG LƯU VÀ GHI NỐI TIẾP VÀO CSV (Chống mất dữ liệu trũ)")
    print(f"{'='*80}")
    
    if articles:
        df_new = pd.DataFrame(articles)
        filename = "dataset/news.csv"
        
        # KIỂM TRA VÀ GỘP VỚI FILE CŨ NẾU CÓ
        if os.path.exists(filename):
            print(f"\n📂 Phát hiện file CSV gốc đã tồn tại: {filename}")
            try:
                df_old = pd.read_csv(filename, encoding='utf-8-sig')
                print(f"  • Số lượng bài trong file cũ: {len(df_old):,} bài")
                print(f"  • Số lượng bài mới cào được: {len(df_new):,} bài")
                
                # Nối ghép, loại bỏ bài trùng
                df = pd.concat([df_old, df_new], ignore_index=True)
                original_count = len(df)
                df = df.drop_duplicates(subset=['url'], keep='first')
                duplicate_count = original_count - len(df)
                
                if duplicate_count > 0:
                    print(f"  • Đã loại bỏ {duplicate_count:,} bài bị trùng lặp!")
                    
                print(f"  • Tổng bài sau khi gộp: {len(df):,} bài")
            except Exception as e:
                print(f"⚠️ Không thể đọc file cũ, tiến hành thay thế mới toàn bộ: {e}")
                df = df_new.drop_duplicates(subset=['url'], keep='first')
        else:
            print(f"\n📂 Tạo file dữ liệu mới: {filename}")
            df = df_new.drop_duplicates(subset=['url'], keep='first')
            
        # Ghi file
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        # Lưu bản nén dự phòng (tuỳ chọn backup)
        if CONFIG['enable_compression']:
            with gzip.open(filename + '.gz', 'wt', encoding='utf-8') as f:
                df.to_csv(f, index=False)
            compressed_size = os.path.getsize(filename + '.gz') / (1024*1024)
            print(f"✅ Đã tạo file Backup nén: {filename}.gz ({compressed_size:.1f} MB)")
        
        # Thống kê hiệu suất
        raw_size = os.path.getsize(filename) / (1024*1024)
        elapsed = (time.time() - start_time) / 60
        
        print(f"\n✅ TIẾN TRÌNH HOÀN TẤT THÀNH CÔNG!")
        print(f"\n📊 THỐNG KÊ CHI TIẾT:")
        print(f"  • Tổng dung lượng kho tin bài: {len(df):,} bài")
        print(f"  • Kích thước tệp tin: {raw_size:.1f} MB")
        print(f"  • Tổng thời gian chạy: {elapsed:.2f} phút")
        if elapsed > 0:
            print(f"  • Tốc độ quét: {len(df_new)/elapsed:.0f} bài/phút")
        
        # Xóa file tạm checkpoint
        if os.path.exists(checkpoint_file + '.gz'):
            os.remove(checkpoint_file + '.gz')
            
        print(f"\n💡 BƯỚC TIẾP THEO MỖI KHI CRAWL XONG:")
        print(f"  1. Chạy 'python preprocess.py'")
        print(f"  2. Chạy 'python build_ngram.py'")
        
    else:
        print("\n❌ Lần thu thập này không bắt được bài nào mới, hoặc đã bị ngắt sớm!")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Bạn vừa ngắt tiến trình! Toàn bộ tiến độ hiện tại đã lưu tạm vào checkpoint.")
    except Exception as e:
        print(f"\n❌ Lỗi hệ thống: {e}")
        import traceback
        traceback.print_exc()
