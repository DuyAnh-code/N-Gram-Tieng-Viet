/* =====================================================
   VN N-gram Studio — app.js v2.0
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboardStats();
    initCrawler();
    initPreprocess();
    initNgramBuilder();
    initPredictor();
    initEvaluator();
    initVisualize();
    initRippleButtons();
});

// ────────────────────────────────────────────────────
// NAVIGATION
// ────────────────────────────────────────────────────
function initNavigation() {
    const allTabs   = document.querySelectorAll('.nav-links li[data-tab]');
    const sections  = document.querySelectorAll('.tab-pane');
    const pageTitle = document.getElementById('page-title');
    const breadcrumb = document.getElementById('breadcrumb-page');

    const tabLabels = {
        dashboard:  'Tổng quan hệ thống',
        crawler:    'Thu thập dữ liệu',
        preprocess: 'Tiền xử lý văn bản',
        ngram:      'Xây dựng mô hình N-gram',
        predict:    'Dự đoán từ & Sinh văn bản',
        evaluate:   'Đánh giá mô hình',
        visualize:  'Trực quan hóa',
    };

    allTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active from all tabs in all nav-links
            document.querySelectorAll('.nav-links li').forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.classList.add('hidden'));

            tab.classList.add('active');
            const targetId = tab.getAttribute('data-tab');
            const section = document.getElementById(targetId);
            if (section) {
                section.classList.remove('hidden');
                section.classList.remove('fade-in');
                void section.offsetWidth; // force reflow
                section.classList.add('fade-in');
            }

            const label = tabLabels[targetId] || targetId;
            pageTitle.textContent  = label;
            breadcrumb.textContent = label;

            if (targetId === 'dashboard') loadDashboardStats();
            if (targetId === 'ngram')     loadTopNgram(1);
        });
    });
}

// ────────────────────────────────────────────────────
// RIPPLE EFFECT (auto-apply to all .btn)
// ────────────────────────────────────────────────────
function initRippleButtons() {
    document.addEventListener('click', e => {
        const btn = e.target.closest('.btn');
        if (!btn) return;
        const circle = document.createElement('span');
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        circle.style.cssText = `
            position:absolute;
            width:${size}px; height:${size}px;
            border-radius:50%;
            background:rgba(255,255,255,0.25);
            left:${e.clientX - rect.left - size/2}px;
            top:${e.clientY - rect.top  - size/2}px;
            transform: scale(0);
            animation: ripple-anim 0.55s linear;
            pointer-events:none;
        `;
        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(circle);
        circle.addEventListener('animationend', () => circle.remove());
    });

    const style = document.createElement('style');
    style.textContent = `
    @keyframes ripple-anim {
        to { transform: scale(3); opacity: 0; }
    }`;
    document.head.appendChild(style);
}

// ────────────────────────────────────────────────────
// UTILS
// ────────────────────────────────────────────────────
async function fetchAPI(endpoint, method = 'GET', body = null) {
    const options = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);
    try {
        const res = await fetch(`/api${endpoint}`, options);
        return await res.json();
    } catch (err) {
        console.error('API Error:', err);
        return { error: 'Lỗi kết nối server' };
    }
}

function clearLog(id) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = '';
}

function appendLog(id, text) {
    const el = document.getElementById(id);
    if (!el) return;
    const now = new Date();
    const ts  = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;
    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerHTML = `<span class="log-time">[${ts}]</span><span class="log-text">${escHtml(text)}</span>`;
    el.appendChild(line);
    el.scrollTop = el.scrollHeight;
}

function escHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function animateCount(el, target) {
    const start = parseInt(el.textContent.replace(/[^0-9]/g,'')) || 0;
    const duration = 800;
    const step = (timestamp, startTime) => {
        const pct = Math.min((timestamp - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - pct, 3);
        el.textContent = Math.round(start + (target - start) * eased).toLocaleString('vi-VN');
        if (pct < 1) requestAnimationFrame(ts => step(ts, startTime));
    };
    requestAnimationFrame(ts => step(ts, ts));
}

// ────────────────────────────────────────────────────
// PROCESS UI — shared updater
// ────────────────────────────────────────────────────
function updateProcessUI(prefix, status) {
    const btnStart  = document.getElementById(`btn-start-${prefix}`);
    const btnStop   = document.getElementById(`btn-stop-${prefix}`);
    const msg       = document.getElementById(`${prefix}-msg`);
    const bar       = document.getElementById(`${prefix}-progress`);
    const pctLabel  = document.getElementById(`${prefix}-pct`);
    const logBox    = document.getElementById(`${prefix}-logs`);

    // Buttons
    if (status.is_running) {
        btnStart?.classList.add('hidden');
        btnStop?.classList.remove('hidden');
    } else {
        btnStart?.classList.remove('hidden');
        btnStop?.classList.add('hidden');
    }

    // Progress
    let pct = 0;
    if (status.total > 0) {
        pct = Math.min((status.progress / status.total) * 100, 100);
    }
    if (bar)      bar.style.width = pct + '%';
    if (pctLabel) pctLabel.textContent = Math.round(pct) + '%';

    // Message
    if (msg && status.message) {
        msg.classList.remove('hidden');
        msg.textContent = status.message;
    }

    // Logs — append only new lines
    if (status.logs && status.logs.length > 0 && logBox) {
        const existing = logBox.querySelectorAll('.log-line').length;
        for (let i = existing; i < status.logs.length; i++) {
            appendLog(`${prefix}-logs`, status.logs[i]);
        }
    }
}

function pollStatus(prefix, endpoint) {
    const interval = setInterval(async () => {
        const status = await fetchAPI(endpoint);
        updateProcessUI(prefix, status);
        if (!status.is_running) {
            clearInterval(interval);
        }
    }, 1000);
}

// ────────────────────────────────────────────────────
// DASHBOARD
// ────────────────────────────────────────────────────
async function loadDashboardStats() {
    const stats = await fetchAPI('/dashboard/stats');
    if (stats.error) return;

    const totalEl   = document.getElementById('dash-total-articles');
    const procEl    = document.getElementById('dash-processed-articles');
    const vocabEl   = document.getElementById('dash-vocab-size');

    if (totalEl) animateCount(totalEl, stats.dataset_size || 0);
    if (procEl)  animateCount(procEl,  stats.processed_size || 0);
    if (vocabEl) animateCount(vocabEl, stats.vocab_size || 0);

    const tbody = document.querySelector('#models-table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    [1, 2, 3, 4].forEach((n, idx) => {
        const model = stats.models?.find(m => m.n === n);
        const delay = idx * 60;
        if (model) {
            tbody.innerHTML += `
            <tr style="animation: fadeIn 0.4s ease ${delay}ms both">
                <td><strong style="color:var(--text-bright)">${n}-gram</strong></td>
                <td><span class="badge success"><i class="fa-solid fa-circle-check"></i> Sẵn sàng</span></td>
                <td><span style="font-family:'JetBrains Mono',monospace;color:var(--accent)">${model.size_mb} MB</span></td>
                <td>
                    <button class="btn ghost" style="padding:6px 14px;font-size:0.8rem"
                        onclick="switchToNgramTab()">
                        <i class="fa-solid fa-eye"></i> Xem
                    </button>
                </td>
            </tr>`;
        } else {
            tbody.innerHTML += `
            <tr style="animation: fadeIn 0.4s ease ${delay}ms both">
                <td><strong style="color:var(--text-bright)">${n}-gram</strong></td>
                <td><span class="badge muted"><i class="fa-solid fa-circle-xmark"></i> Chưa tạo</span></td>
                <td><span style="color:var(--text-muted)">—</span></td>
                <td><span style="color:var(--text-muted);font-size:0.85rem">Chưa có mô hình</span></td>
            </tr>`;
        }
    });
}

function switchToNgramTab() {
    document.getElementById('nav-ngram')?.click();
}

// ────────────────────────────────────────────────────
// CRAWLER
// ────────────────────────────────────────────────────
function initCrawler() {
    document.getElementById('btn-start-crawl')?.addEventListener('click', async () => {
        const limit = parseInt(document.getElementById('crawl-limit').value) || 1;
        clearLog('crawl-logs');
        await fetchAPI('/crawler/start', 'POST', { limit });
        pollStatus('crawl', '/crawler/status');
    });

    document.getElementById('btn-stop-crawl')?.addEventListener('click', async () => {
        await fetchAPI('/crawler/stop', 'POST');
    });

    fetchAPI('/crawler/status').then(res => {
        if (res.is_running) pollStatus('crawl', '/crawler/status');
    });
}

// ────────────────────────────────────────────────────
// PREPROCESS
// ────────────────────────────────────────────────────
function initPreprocess() {
    document.getElementById('btn-start-prep')?.addEventListener('click', async () => {
        const removeStopwords = document.getElementById('prep-stopwords').checked;
        const fieldChoice     = document.getElementById('prep-field').value;
        clearLog('prep-logs');
        await fetchAPI('/preprocess/run', 'POST', { remove_stopwords: removeStopwords, field_choice: fieldChoice });
        pollStatus('prep', '/preprocess/status');
    });

    document.getElementById('btn-stop-prep')?.addEventListener('click', async () => {
        await fetchAPI('/preprocess/stop', 'POST');
    });

    fetchAPI('/preprocess/status').then(res => {
        if (res.is_running) pollStatus('prep', '/preprocess/status');
    });
}

// ────────────────────────────────────────────────────
// N-GRAM BUILDER
// ────────────────────────────────────────────────────
function initNgramBuilder() {
    document.getElementById('btn-start-build')?.addEventListener('click', async () => {
        const checks   = document.querySelectorAll('.ngram-check:checked');
        const n_values = Array.from(checks).map(cb => parseInt(cb.value));
        if (n_values.length === 0) {
            showToast('Vui lòng chọn ít nhất 1 mô hình!', 'danger');
            return;
        }
        clearLog('build-logs');
        await fetchAPI('/ngram/build', 'POST', { n_values });
        pollStatus('build', '/ngram/status');
    });

    document.getElementById('btn-stop-build')?.addEventListener('click', async () => {
        await fetchAPI('/ngram/stop', 'POST');
    });

    fetchAPI('/ngram/status').then(res => {
        if (res.is_running) pollStatus('build', '/ngram/status');
    });

    // Tab switch for top N-gram
    document.querySelectorAll('#ngram .tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#ngram .tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadTopNgram(parseInt(btn.getAttribute('data-n')));
        });
    });

    loadTopNgram(1);
}

async function loadTopNgram(n) {
    const tbody = document.querySelector('#top-ngram-table tbody');
    if (!tbody) return;
    tbody.innerHTML = `<tr><td colspan="4" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Đang tải...</td></tr>`;

    const res = await fetchAPI(`/ngram/top?n=${n}&limit=30`);
    if (res.error) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger"><i class="fa-solid fa-triangle-exclamation"></i> ${res.error}</td></tr>`;
        return;
    }

    const colors = ['var(--primary-light)', 'var(--accent)', 'var(--green)'];
    tbody.innerHTML = '';
    res.top?.forEach((item, index) => {
        const rank = index + 1;
        const rankStyle = rank <= 3
            ? `style="color:${colors[index]};font-weight:800;font-size:1rem"`
            : '';
        tbody.innerHTML += `
        <tr style="animation:fadeIn 0.3s ease ${index * 30}ms both">
            <td><span ${rankStyle}>${rank}</span></td>
            <td><strong style="color:var(--text-bright)">${escHtml(item.ngram)}</strong></td>
            <td style="font-family:'JetBrains Mono',monospace">${item.count.toLocaleString('vi-VN')}</td>
            <td>
                <span style="color:var(--accent);font-family:'JetBrains Mono',monospace">
                    ${(item.probability * 100).toFixed(4)}%
                </span>
            </td>
        </tr>`;
    });
}

// ────────────────────────────────────────────────────
// PREDICTOR
// ────────────────────────────────────────────────────
function initPredictor() {
    const ctxInput  = document.getElementById('pred-context');
    const resBox    = document.getElementById('pred-results');
    const nSelect   = document.getElementById('pred-n');
    const nBadge    = document.getElementById('pred-n-badge');

    const nLabels = { '2': 'Bigram', '3': 'Trigram', '4': '4-gram' };

    nSelect?.addEventListener('change', () => {
        if (nBadge) nBadge.textContent = nLabels[nSelect.value] || 'N-gram';
        if (ctxInput?.value.trim()) ctxInput.dispatchEvent(new Event('input'));
    });

    let timer;
    ctxInput?.addEventListener('input', () => {
        clearTimeout(timer);
        timer = setTimeout(async () => {
            const context = ctxInput.value.trim();
            if (!context) {
                resBox.innerHTML = `<span style="color:var(--text-muted);font-size:0.85rem">Nhập văn bản để xem gợi ý...</span>`;
                return;
            }

            const n   = nSelect?.value || '3';
            const res = await fetchAPI('/predict/next_word', 'POST', { context, n, top_k: 7 });

            if (res.error) {
                resBox.innerHTML = `<span style="color:var(--danger)"><i class="fa-solid fa-triangle-exclamation"></i> ${escHtml(res.error)}</span>`;
            } else if (res.predictions?.length > 0) {
                resBox.innerHTML = res.predictions.map(p =>
                    `<div class="pred-chip"
                        onclick="appendPrediction('${escHtml(p.word)}')">
                        ${escHtml(p.word)}
                        <span class="pred-prob">${(p.prob * 100).toFixed(1)}%</span>
                    </div>`
                ).join('');
            } else {
                resBox.innerHTML = `<span style="color:var(--text-muted)">Không tìm thấy dự đoán phù hợp.</span>`;
            }
        }, 280);
    });

    // Generate text
    document.getElementById('btn-generate')?.addEventListener('click', async () => {
        const seed   = document.getElementById('gen-seed')?.value || '';
        const n      = nSelect?.value || '3';
        const num    = document.getElementById('gen-length')?.value || '15';
        const outBox = document.getElementById('gen-output');

        if (outBox) {
            outBox.innerHTML = `<span style="color:var(--text-muted)"><i class="fa-solid fa-spinner fa-spin"></i> Đang sinh văn bản...</span>`;
            outBox.classList.remove('has-content');
        }

        const res = await fetchAPI('/predict/generate', 'POST', { seed, n, num_words: parseInt(num) });

        if (!outBox) return;
        if (res.error) {
            outBox.innerHTML = `<span style="color:var(--danger)"><i class="fa-solid fa-triangle-exclamation"></i> ${escHtml(res.error)}</span>`;
        } else {
            outBox.textContent = res.generated_text;
            outBox.classList.add('has-content');
        }
    });
}

function appendPrediction(word) {
    const input = document.getElementById('pred-context');
    if (!input) return;
    input.value += ' ' + word;
    input.dispatchEvent(new Event('input'));
    input.focus();
}

// ────────────────────────────────────────────────────
// EVALUATOR
// ────────────────────────────────────────────────────
function initEvaluator() {
    document.getElementById('btn-run-eval')?.addEventListener('click', async () => {
        const btn   = document.getElementById('btn-run-eval');
        const tbody = document.querySelector('#eval-table tbody');

        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Đang đánh giá...`;
        btn.disabled  = true;
        tbody.innerHTML = `<tr><td colspan="6" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Đang chạy đánh giá — vui lòng đợi...</td></tr>`;

        const res = await fetchAPI('/evaluate/run', 'POST', { n_values: [1, 2, 3] });

        btn.innerHTML = `<i class="fa-solid fa-calculator"></i> Bắt đầu đánh giá`;
        btn.disabled  = false;

        if (res.error) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger"><i class="fa-solid fa-triangle-exclamation"></i> ${escHtml(res.error)}</td></tr>`;
            return;
        }

        tbody.innerHTML = '';
        res.results?.forEach((r, idx) => {
            if (r.error) {
                tbody.innerHTML += `<tr style="animation:fadeIn 0.4s ease ${idx*60}ms both">
                    <td><strong>${escHtml(r.model_name)}</strong></td>
                    <td colspan="5" class="text-danger">${escHtml(r.error)}</td>
                </tr>`;
            } else {
                const ppColor = r.perplexity < 100
                    ? 'var(--green)'
                    : r.perplexity < 1000 ? 'var(--accent)' : 'var(--danger)';
                const ppVal   = r.perplexity === -1 ? '∞' : r.perplexity;

                tbody.innerHTML += `
                <tr style="animation:fadeIn 0.4s ease ${idx*60}ms both">
                    <td><strong style="color:var(--text-bright)">${escHtml(r.model_name)}</strong></td>
                    <td>
                        <span style="color:${ppColor};font-weight:700;font-family:'JetBrains Mono',monospace">
                            ${ppVal}
                        </span>
                    </td>
                    <td>${r.n === 1 ? '<span class="text-muted">—</span>' : `<span style="color:var(--accent)">${r.accuracy_top1}%</span>`}</td>
                    <td>${r.n === 1 ? '<span class="text-muted">—</span>' : `<span style="color:var(--green)">${r.accuracy_top5}%</span>`}</td>
                    <td>${r.coverage}%</td>
                    <td style="font-family:'JetBrains Mono',monospace">${Number(r.unique_ngrams).toLocaleString('vi-VN')}</td>
                </tr>`;
            }
        });
    });
}

// ────────────────────────────────────────────────────
// VISUALIZE
// ────────────────────────────────────────────────────
function initVisualize() {
    const btn    = document.getElementById('btn-run-vis');
    const msg    = document.getElementById('vis-msg');
    const imgBox = document.getElementById('vis-images');

    // Try loading existing images
    const ts = Date.now();
    const imgCompare = document.getElementById('img-compare');
    const imgVocab   = document.getElementById('img-vocab');

    if (imgCompare) {
        imgCompare.src = `/dataset/model_comparison_detailed.png?t=${ts}`;
        imgCompare.onload = () => { if (imgBox) imgBox.style.display = 'block'; };
    }
    if (imgVocab) {
        imgVocab.src = `/dataset/vocabulary_analysis.png?t=${ts}`;
    }

    btn?.addEventListener('click', async () => {
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Đang vẽ biểu đồ...`;
        btn.disabled  = true;
        if (msg) { msg.classList.remove('hidden'); msg.textContent = 'Đang khởi tạo...'; }
        if (imgBox) imgBox.style.display = 'none';

        await fetchAPI('/visualize/generate', 'POST');

        const interval = setInterval(async () => {
            const status = await fetchAPI('/visualize/status');
            if (msg) msg.textContent = status.message || '...';

            if (!status.is_running) {
                clearInterval(interval);
                btn.innerHTML = `<i class="fa-solid fa-palette"></i> Tạo biểu đồ mới`;
                btn.disabled  = false;

                if (status.message?.includes('hoàn tất')) {
                    const newTs = Date.now();
                    if (imgCompare) imgCompare.src = `/dataset/model_comparison_detailed.png?t=${newTs}`;
                    if (imgVocab)   imgVocab.src   = `/dataset/vocabulary_analysis.png?t=${newTs}`;
                    if (imgBox)     imgBox.style.display = 'block';
                    msg?.classList.add('hidden');
                } else {
                    if (msg) msg.style.color = 'var(--danger)';
                }
            }
        }, 1000);
    });
}

// ────────────────────────────────────────────────────
// TOAST NOTIFICATION
// ────────────────────────────────────────────────────
function showToast(message, type = 'info') {
    const colors = {
        info:    { bg: 'var(--primary-dark)', border: 'var(--primary)', icon: 'fa-circle-info',      color: 'var(--primary-light)' },
        success: { bg: 'rgba(35,209,139,0.1)', border: 'var(--green)', icon: 'fa-circle-check',      color: 'var(--green)' },
        danger:  { bg: 'var(--danger-glow)',   border: 'var(--danger)', icon: 'fa-triangle-exclamation', color: 'var(--danger)' },
    };
    const c = colors[type] || colors.info;

    const toast = document.createElement('div');
    toast.style.cssText = `
        position:fixed; bottom:24px; right:24px; z-index:9999;
        background:${c.bg}; border:1px solid ${c.border};
        color:${c.color}; border-radius:10px;
        padding:12px 20px; font-size:0.88rem; font-weight:600;
        display:flex; align-items:center; gap:10px;
        box-shadow:0 8px 30px rgba(0,0,0,0.4);
        animation: slideUp 0.3s cubic-bezier(0.4,0,0.2,1);
        font-family:'Inter',sans-serif;
        max-width:340px;
    `;
    toast.innerHTML = `<i class="fa-solid ${c.icon}"></i> ${escHtml(message)}`;
    document.body.appendChild(toast);

    const style = document.createElement('style');
    style.textContent = `@keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }`;
    document.head.appendChild(style);

    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s';
        toast.style.opacity    = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
