import os
import time
import pandas as pd
from crawler import NEWS_SOURCES, CONFIG, CrawlerCore
from core.managers import crawler_manager


def save_to_csv(articles, start_time):
    """Lưu danh sách bài báo vào file CSV, tự động gộp với dữ liệu cũ nếu tồn tại."""
    filename = "dataset/news.csv"
    df_new = pd.DataFrame(articles)

    if os.path.exists(filename):
        try:
            df_old = pd.read_csv(filename, encoding='utf-8-sig')
            df = pd.concat([df_old, df_new], ignore_index=True)
            df = df.drop_duplicates(subset=['url'], keep='first')
        except Exception:
            df = df_new.drop_duplicates(subset=['url'], keep='first')
    else:
        df = df_new.drop_duplicates(subset=['url'], keep='first')

    df.to_csv(filename, index=False, encoding='utf-8-sig')


def run_crawler(manager, limit_pages=1):
    """
    Hàm crawler chạy ở background thread.
    Sử dụng manager để cập nhật tiến độ.
    manager.stop_event được kiểm tra để có thể dừng sớm.
    """
    manager.update(msg="🚀 Bắt đầu crawl dữ liệu mới...")

    os.makedirs("dataset", exist_ok=True)
    articles = []

    start_time = time.time()

    # Ước tính số lượng
    total_categories = sum(len(s['categories']) for s in NEWS_SOURCES.values())
    manager.update(msg=f"📁 Tổng số nguồn: {len(NEWS_SOURCES)}, số chuyên mục: {total_categories}")

    cat_count = 0
    max_articles = CONFIG.get('max_articles_per_category', 0)

    for source_key, source_config in NEWS_SOURCES.items():
        if manager.stop_event.is_set():
            break

        manager.update(msg=f"📰 Đang lấy nguồn: {source_config['name'].upper()}")

        # Tạo CrawlerCore cho từng nguồn
        crawler = CrawlerCore(source_key)

        # categories là dict {key: {name, url}}, cần lấy .values()
        for category in source_config['categories'].values():
            if manager.stop_event.is_set():
                break

            cat_count += 1
            manager.update(msg=f"📂 Đang xử lý: {category['name']} ({cat_count}/{total_categories})")

            # Lấy links qua CrawlerCore instance method
            links = crawler.get_article_links(category['url'], limit_pages)
            if max_articles > 0:
                links = links[:max_articles]

            if not links:
                manager.update(msg=f"⚠️ Không tìm thấy bài nào trong {category['name']}")
                continue

            manager.update(msg=f"🔍 Tìm thấy {len(links)} links, đang tải từng bài...")
            success_count = 0

            for url in links:
                if manager.stop_event.is_set():
                    manager.update(msg="⚠️ Đã nhận lệnh dừng crawl!")
                    break

                article = crawler.crawl_article(url)
                if article:
                    articles.append(article)
                    success_count += 1

                # Cập nhật progress số bài crawl được
                manager.update(
                    progress=len(articles),
                    msg=f"  Tải xong: {article['title'] if article else 'Lỗi'}"
                )
                time.sleep(CONFIG['delay_between_requests'] / 2.0)

            manager.update(msg=f"✅ Xong {category['name']}: {success_count} bài thành công.")

    if articles:
        manager.update(msg=f"💾 Đang lưu {len(articles)} bài vào CSV...")
        save_to_csv(articles, start_time)
        manager.update(msg="🎉 Đã lưu thành công dữ liệu!")
    else:
        manager.update(msg="⚠️ Không crawl được bài nào (có thể do đã dừng hoặc lỗi).")

    elapsed = time.time() - start_time
    manager.update(msg=f"🏁 Đã hoàn thành tác vụ sau {elapsed:.1f} giây.")

