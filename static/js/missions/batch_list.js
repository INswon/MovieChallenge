// UI を更新する関数（取得済み・未取得のバッジを表示）
window.updateUI = function () {
    if (!window.apiData || typeof window.apiData !== "object") return;

    const obtainedBadgesElement = document.getElementById("obtained-badges");
    const unobtainedBadgesElement = document.getElementById("unobtained-badges");

    if (!obtainedBadgesElement || !unobtainedBadgesElement) return;

    const resolveIcon = (badge) => {
        if (badge.icon) return badge.icon;

        const name = badge.name || "";

        if (name.includes("1日3") || name.includes("1日に3本")) {
            return "/static/images/missions/badges/daily_three_movie_badge.jpg";
        }
        if (name.includes("3本の映画視聴達成") || name.includes("3本の映画") || name.includes("3作品")) {
            return "/static/images/missions/badges/three_watch_movie_badge.jpg";
        }
        if (name.includes("3ジャンル制覇") || name.includes("3ジャンル制覇バッジ")) {
            return "/static/images/missions/badges/three_genres_watch_badge.jpg";
        }

        return "/static/images/missions/badges/three_watch_movie_badge.jpg";
    };

    // 取得済みバッジのリストを更新
    obtainedBadgesElement.innerHTML =
        window.apiData.obtained_batches.length > 0
            ? window.apiData.obtained_batches.map(badge => `
                <div class="badge-item">
                    <img src="${resolveIcon(badge)}" class="badge-img" alt="${badge.name}">
                    <p class="badge-title">${badge.name}</p>
                </div>
            `).join("")
            : "<p>まだ取得済みのバッジはありません。</p>";

    // 未取得バッジのリストを更新
    unobtainedBadgesElement.innerHTML =
        window.apiData.unobtained_batches.length > 0
            ? window.apiData.unobtained_batches.map(badge => `
                <div class="badge-item badge-unobtained">
                    <img src="${resolveIcon(badge)}" class="badge-img" alt="${badge.name}">
                    <p class="badge-title">${badge.name}</p>
                </div>
            `).join("")
            : "<p>未取得のバッジはありません。</p>";
};

// バッジデータ取得に失敗した場合、エラーメッセージを表示
function showError(message) {
    document.getElementById("obtained-badges").innerHTML = `<p class='text-danger'>${message}</p>`;
    document.getElementById("unobtained-badges").innerHTML = `<p class='text-danger'>${message}</p>`;
}

// APIからバッジデータを取得する関数
async function loadBatches() {
    try {
        const response = await fetch("/missons/user_batches/", {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        });

        if (!response.ok) throw new Error(`API エラー: ${response.status} ${response.statusText}`);

        window.apiData = await response.json();
        updateUI();

    } catch (error) {
        showError("バッジデータの取得に失敗しました。");
    }
}

// ページロード時にバッジデータを取得
document.addEventListener("DOMContentLoaded", loadBatches);
