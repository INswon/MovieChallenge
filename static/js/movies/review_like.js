document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMが読み込まれました");
  
    const buttons = document.querySelectorAll(".like-button");
    console.log("ボタンの数:", buttons.length);  // ← ここで0ならセレクタが間違い
  
    buttons.forEach(button => {
      button.addEventListener("click", function(e) {
        e.preventDefault();
        const reviewId = button.dataset.reviewId;
        console.log("レビューID:", reviewId);
      });
    });
  });
  