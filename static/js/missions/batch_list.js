// UI を更新する関数（取得済み・未取得のバッジを表示）
window.updateUI = function () {
    if (!window.apiData || typeof window.apiData !== "object") return;

    const obtainedBadgesElement = document.getElementById("obtained-badges");
    const unobtainedBadgesElement = document.getElementById("unobtained-badges");

    if (!obtainedBadgesElement || !unobtainedBadgesElement) return;

    // 取得済みバッジのリストを更新
    obtainedBadgesElement.innerHTML =
        window.apiData.obtained_batches.length > 0
            ? window.apiData.obtained_batches.map(badge => `
                <div class="badge-item">
                    <img src="${badge.icon || '/static/images/default_badge.png'}" class="badge-img" alt="${badge.name}">
                    <p class="badge-title">${badge.name}</p>
                </div>
            `).join("")
            : "<p>まだ取得済みのバッジはありません。</p>";

    // 未取得バッジのリストを更新
    unobtainedBadgesElement.innerHTML =
        window.apiData.unobtained_batches.length > 0
            ? window.apiData.unobtained_batches.map(badge => `
                <div class="badge-item badge-unobtained">
                    <img src="${badge.icon || '/static/images/default_badge.png'}" class="badge-img" alt="${badge.name}">
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
        const response = await fetch("/missions/user_batches", {
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
