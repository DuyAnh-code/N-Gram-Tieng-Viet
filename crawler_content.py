import requests
from bs4 import BeautifulSoup

def crawl_article(url):
    """Crawl nội dung một bài báo từ URL"""
    try:
        # Thêm headers để tránh bị chặn
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Lấy tiêu đề
        title_tag = soup.find("h1", class_="title-detail")
        title = title_tag.text.strip() if title_tag else "Không tìm thấy tiêu đề"
        
        # Lấy nội dung
        content = ""
        article = soup.find("article", class_="fck_detail")
        if article:
            for p in article.find_all("p", class_="Normal"):
                content += p.text.strip() + "\n"
        
        if not content:
            content = "Không tìm thấy nội dung"
        
        return title, content
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi crawl {url}: {e}")
        return None, None

# Test với URL mẫu
if __name__ == "__main__":
    url = "https://vnexpress.net/thi-the-nam-sinh-vien-cung-xe-may-duoi-vuc-5048666.html"
    
    print("🔍 Đang crawl bài báo...")
    title, content = crawl_article(url)
    
    if title and content:
        print(f"\n📰 Tiêu đề: {title}")
        print(f"\n📝 Nội dung:\n{content[:500]}...")  # Hiển thị 500 ký tự đầu
        print(f"\n✅ Crawl thành công!")
    else:
        print("\n❌ Crawl thất bại!")