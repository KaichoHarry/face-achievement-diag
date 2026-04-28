document.addEventListener("DOMContentLoaded", () => {
  const startButton = document.getElementById("startButton");

  if (!startButton) return;

  startButton.addEventListener("click", () => {
    window.location.href = "./diagnosis.html";
  });
});