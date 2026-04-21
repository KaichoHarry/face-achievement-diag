document.addEventListener("DOMContentLoaded", () => {
  const predictionResult = document.getElementById("predictionResult");
  const subpredictionResult = document.getElementById("subpredictionResult");
  const retryButton = document.getElementById("retryButton");
  const backTopButton = document.getElementById("backTopButton");

  const prediction = localStorage.getItem("prediction");
  const subprediction = localStorage.getItem("subprediction");

  predictionResult.textContent = prediction || "大分類の結果がありません。";
  subpredictionResult.textContent = subprediction || "小分類の結果がありません。";

  retryButton.addEventListener("click", () => {
    window.location.href = "./diagnosis.html";
  });

  backTopButton.addEventListener("click", () => {
    window.location.href = "./index.html";
  });
});