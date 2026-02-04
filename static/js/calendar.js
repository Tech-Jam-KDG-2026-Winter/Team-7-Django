const now = new Date();
// 英語(US)ロケールで、月(short: Feb)と曜日(short: Mon)を取得して表示
document.getElementById('display-month').textContent = now.toLocaleString('en-US', { month: 'short' });
document.getElementById('display-weekday').textContent = now.toLocaleString('en-US', { weekday: 'short' });

// --- モーダル表示機能 ---
const modal = document.getElementById('calorie-modal');
const modalDate = document.getElementById('modal-date');
const modalCalories = document.getElementById('modal-calories');
const closeButton = document.querySelector('.close-button');

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('grid-item')) {
        const day = event.target.getAttribute('data-day');
        const calories = event.target.getAttribute('data-calories');

        // 日付情報がある場合のみモーダルを表示
        if (day) {
            modalDate.textContent = `${day}日`;
            modalCalories.textContent = `消費カロリー: ${calories} kcal`;
            modal.style.display = 'block';
        }
    }
});

// 閉じるボタンまたは背景クリックでモーダルを閉じる
window.addEventListener('click', function(event) {
    if (event.target === modal || (closeButton && event.target === closeButton)) {
        modal.style.display = 'none';
    }
});

// --- 無限スクロールカレンダー機能 ---
const scrollArea = document.getElementById('calendar-scroll-area');
let prevMonthDate = new Date(now.getFullYear(), now.getMonth(), 1); // 先月の基準日
let nextMonthDate = new Date(now.getFullYear(), now.getMonth(), 1); // 来月の基準日
let isLoading = false;
let isDown = false;
let startX;
let scrollLeft;

// カレンダーグリッドを生成する関数
function createMonthHTML(year, month) {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startDayOfWeek = firstDay.getDay();

    let html = `<div class="month-container">`;
    html += `<div class="month-label">${year} / ${month + 1}</div>`;
    html += '<div class="calendar-grid">';

    // 月初めの空白セル（曜日合わせ）
    for (let i = 0; i < startDayOfWeek; i++) {
        html += '<div class="grid-item color-gray" style="opacity: 0.3;"></div>';
    }

    // 日付セル
    for (let d = 1; d <= daysInMonth; d++) {
        html += `<div class="grid-item color-gray" data-day="${d}" data-calories="0"></div>`;
    }

    html += '</div>';
    html += '</div>';
    return html;
}

// 先月を追加ロード
function loadPrevMonth() {
    scrollArea.style.scrollSnapType = 'none';

    prevMonthDate.setMonth(prevMonthDate.getMonth() - 1);
    
    const year = prevMonthDate.getFullYear();
    const month = prevMonthDate.getMonth();
    const html = createMonthHTML(year, month);
    
    const oldScrollWidth = scrollArea.scrollWidth;
    const oldScrollLeft = scrollArea.scrollLeft;

    scrollArea.insertAdjacentHTML('afterbegin', html);

    // 要素追加分だけスクロール位置を戻す（見た目の位置を維持し、連続ロードを防ぐ）
    const newScrollWidth = scrollArea.scrollWidth;
    scrollArea.scrollLeft = oldScrollLeft + (newScrollWidth - oldScrollWidth);

    setTimeout(() => {
        scrollArea.style.scrollSnapType = 'x mandatory';
    }, 50);
}

// 来月を追加ロード
function loadNextMonth() {
    nextMonthDate.setMonth(nextMonthDate.getMonth() + 1);
    
    const year = nextMonthDate.getFullYear();
    const month = nextMonthDate.getMonth();
    const html = createMonthHTML(year, month);
    
    scrollArea.insertAdjacentHTML('beforeend', html);
}

// スクロール位置をチェックしてロードする関数
function checkScrollAndLoad() {
    if (isLoading || isDown) return; // ロード中またはドラッグ中は処理しない

    const scrollLeft = scrollArea.scrollLeft;
    const scrollWidth = scrollArea.scrollWidth;
    const clientWidth = scrollArea.clientWidth;

    // 左端に近づいたら先月をロード (閾値: 50px)
    if (scrollLeft < 50) {
        isLoading = true;
        loadPrevMonth();
        setTimeout(() => { isLoading = false; }, 500); // 待機時間を少し延長
    }

    // 右端に近づいたら来月をロード (閾値: 50px)
    if (scrollLeft + clientWidth > scrollWidth - 50) {
        isLoading = true;
        loadNextMonth();
        setTimeout(() => { isLoading = false; }, 500);
    }
}

// スクロールイベントの監視
scrollArea.addEventListener('scroll', checkScrollAndLoad);

// --- ドラッグスクロール機能 ---
scrollArea.addEventListener('mousedown', (e) => {
    isDown = true;
    scrollArea.classList.add('active');
    startX = e.pageX - scrollArea.offsetLeft;
    scrollLeft = scrollArea.scrollLeft;
});

scrollArea.addEventListener('mouseleave', () => {
    isDown = false;
    scrollArea.classList.remove('active');
});

scrollArea.addEventListener('mouseup', () => {
    isDown = false;
    scrollArea.classList.remove('active');
    checkScrollAndLoad();
});

scrollArea.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - scrollArea.offsetLeft;
    const walk = (x - startX) * 2; 
    scrollArea.scrollLeft = scrollLeft - walk;
});

loadPrevMonth();
loadNextMonth();

const currentContainer = document.getElementById('current-month-container');
if (currentContainer) {
    currentContainer.scrollIntoView({ inline: 'center' });
}