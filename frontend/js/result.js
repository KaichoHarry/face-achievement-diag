document.addEventListener("DOMContentLoaded", () => {
  const predictionResult = document.getElementById("predictionResult");
  const subpredictionResult = document.getElementById("subpredictionResult");
  const retryButton = document.getElementById("retryButton");
  const backTopButton = document.getElementById("backTopButton");

  if (!predictionResult || !subpredictionResult) {
    console.error("結果表示用のHTML要素が見つかりません。");
    return;
  }

  const prediction = localStorage.getItem("prediction");
  const subprediction = localStorage.getItem("subprediction");

  predictionResult.textContent = prediction || "未取得";
  subpredictionResult.textContent = subprediction || "未取得";

  if (retryButton) {
    retryButton.addEventListener("click", () => {
      window.location.href = "./diagnosis.html";
    });
  }

  if (backTopButton) {
    backTopButton.addEventListener("click", () => {
      window.location.href = "./index.html";
    });
  }
});