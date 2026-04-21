document.addEventListener("DOMContentLoaded", () => {
  const imageInput = document.getElementById("imageInput");
  const previewImage = document.getElementById("previewImage");
  const predictButton = document.getElementById("predictButton");
  const loadingMessage = document.getElementById("loadingMessage");
  const errorMessage = document.getElementById("errorMessage");

  imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if (!file) {
      previewImage.classList.add("hidden");
      previewImage.src = "";
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      previewImage.src = reader.result;
      previewImage.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  });

  predictButton.addEventListener("click", async () => {
    const file = imageInput.files[0];

    errorMessage.textContent = "";
    errorMessage.classList.add("hidden");

    if (!file) {
      errorMessage.textContent = "画像を選択してください。";
      errorMessage.classList.remove("hidden");
      return;
    }

    loadingMessage.classList.remove("hidden");
    predictButton.disabled = true;

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const data = {
        prediction: "nobel",
        subprediction: "nobel_peace"
      };

      localStorage.setItem("prediction", data.prediction || "");
      localStorage.setItem("subprediction", data.subprediction || "");

      window.location.href = "./result.html";
    } catch (error) {
      errorMessage.textContent = `エラー: ${error.message}`;
      errorMessage.classList.remove("hidden");
    } finally {
      loadingMessage.classList.add("hidden");
      predictButton.disabled = false;
    }
  });
});