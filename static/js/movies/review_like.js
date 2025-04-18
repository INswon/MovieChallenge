document.addEventListener("DOMContentLoaded", function () {

  // .like-buttonが複数あることを想定して全取得
  const buttons = document.querySelectorAll(".like-button")
  buttons.forEach(button => {
    button.addEventListener("click", async function (e) {
      e.preventDefault();
      
      const reviewId = button.dataset.reviewId;

      try {
        const response = await fetch(`/movies/review_like/${reviewId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({}),
        });

        if (!response.ok) {
          throw new Error(`レスポンスステータス: ${response.status}`);
        }

        const data = await response.json();
        console.log("サーバーからのレスポンス:", data);
        

        // DOM更新処理（❤️↔🤍 切り替え + カウント更新）
        if (data.liked) {
          button.querySelector(".icon").textContent = "❤️";
        } else {
          button.querySelector(".icon").textContent = "🤍";
        }
        button.querySelector(".count").textContent = data.count;
        
        } catch (error) {
        console.error("fetchエラー:", error.message);
      }
    });
  });
});

// DjangoのCSRFトークンを取得する関数
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
