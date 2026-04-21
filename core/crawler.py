import os
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from crawler import NEWS_SOURCES, CONFIG, CrawlerCore
from core.managers import crawler_manager


def load_existing_urls(filename="dataset/news.csv") -> set:
    """Đọc toàn bộ URL đã có trong CSV để tránh crawl lại."""
    if not os.path.exists(filename):
        return set()
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig', usecols=['url'])
        return set(df['url'].dropna().tolist())
    except Exception:
        return set()


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
    - Crawl SONG SONG với ThreadPoolExecutor (tăng tốc ~5x).
    - Dùng global seen_urls để loại trùng TRƯỚC khi crawl:
        • Bài đã có trong CSV → bỏ qua (không tốn bandwidth)
        • Bài xuất hiện ở nhiều chuyên mục → chỉ crawl 1 lần
    """
    manager.update(msg="🚀 Bắt đầu crawl dữ liệu mới...")

    os.makedirs("dataset", exist_ok=True)
    articles = []
    start_time = time.time()

    # ── Bước 1: Load toàn bộ URL đã có sẵn ────────────────────────────────
    seen_urls = load_existing_urls()
    manager.update(msg=f"📋 Đã có {len(seen_urls):,} bài trong CSV — sẽ bỏ qua các URL trùng")

    total_categories = sum(len(s['categories']) for s in NEWS_SOURCES.values())
    num_workers = CONFIG.get('max_workers', 3)
    manager.update(
        msg=f"📁 Tổng số nguồn: {len(NEWS_SOURCES)}, "
            f"số chuyên mục: {total_categories} — {num_workers} luồng song song"
    )

    cat_count = 0
    total_skipped = 0  # Đếm tổng URL bị bỏ qua vì trùng

    for source_key, source_config in NEWS_SOURCES.items():
        if manager.stop_event.is_set():
            break

        manager.update(msg=f"📰 Đang lấy nguồn: {source_config['name'].upper()}")
        crawler = CrawlerCore(source_key)

        for category in source_config['categories'].values():
            if manager.stop_event.is_set():
                break

            cat_count += 1
            manager.update(msg=f"📂 Đang xử lý: {category['name']} ({cat_count}/{total_categories})")

            # Lấy toàn bộ links của chuyên mục
            raw_links = crawler.get_article_links(
                category['url'], limit_pages,
                stop_event=manager.stop_event   # ← dừng được giữa chừng khi lấy link
            )

            # ── Bước 2: Filter trùng TRƯỚC khi crawl ───────────────────
            new_links = [url for url in raw_links if url not in seen_urls]
            skipped = len(raw_links) - len(new_links)
            total_skipped += skipped

            if skipped > 0:
                manager.update(
                    msg=f"🔗 {category['name']}: {len(raw_links)} links → "
                        f"bỏ qua {skipped} trùng → còn {len(new_links)} mới"
                )

            if not new_links:
                manager.update(msg=f"⏭️ {category['name']}: Tất cả đã crawl rồi, bỏ qua.")
                continue

            manager.update(
                msg=f"🔍 Crawl {len(new_links)} bài mới ({num_workers} luồng song song)..."
            )
            success_count = 0

            # ── Bước 3: Crawl song song chỉ các URL mới ────────────────
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                future_to_url = {
                    executor.submit(crawler.crawl_article, url): url
                    for url in new_links
                }

                for future in as_completed(future_to_url):
                    if manager.stop_event.is_set():
                        for f in future_to_url:
                            f.cancel()
                        manager.update(msg="⚠️ Đã nhận lệnh dừng crawl!")
                        break

                    url = future_to_url[future]
                    article = future.result()

                    # Đánh dấu URL là đã xử lý dù thành công hay thất bại
                    # → lần kế không crawl lại URL lỗi
                    seen_urls.add(url)

                    if article:
                        articles.append(article)
                        success_count += 1
                        manager.update(
                            progress=len(articles),
                            msg=f"  Tải xong: {article['title']}"
                        )
            # ────────────────────────────────────────────────────────────

            manager.update(
                msg=f"✅ Xong {category['name']}: {success_count}/{len(new_links)} bài thành công."
            )

    if articles:
        manager.update(msg=f"💾 Đang lưu {len(articles)} bài mới vào CSV...")
        save_to_csv(articles, start_time)
        elapsed = time.time() - start_time
        manager.update(
            msg=f"🎉 Hoàn tất! {len(articles)} bài mới | "
                f"Đã bỏ qua {total_skipped} URL trùng | {elapsed:.1f}s"
        )
    else:
        manager.update(
            msg=f"⚠️ Không có bài mới "
                f"(đã bỏ qua {total_skipped} URL trùng — thử tăng số trang)."
        )

    elapsed = time.time() - start_time
    manager.update(msg=f"🏁 Đã hoàn thành tác vụ sau {elapsed:.1f} giây.")
