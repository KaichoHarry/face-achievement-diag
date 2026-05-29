document.addEventListener("DOMContentLoaded", () => {
  const imageInput = document.getElementById("imageInput");
  const previewImage = document.getElementById("previewImage");
  const predictButton = document.getElementById("predictButton");
  const loadingMessage = document.getElementById("loadingMessage");
  const errorMessage = document.getElementById("errorMessage");

  const uploadBox = document.querySelector(".upload-box");
  const uploadHelp = document.querySelector(".upload-help");
  const previewPlaceholder = document.querySelector(".preview-placeholder");

  if (!imageInput || !previewImage || !predictButton) {
    console.error("必要なHTML要素が見つかりません。");
    return;
  }

  let selectedFile = null;

  function showError(message) {
    if (!errorMessage) return;

    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");
  }

  function clearError() {
    if (!errorMessage) return;

    errorMessage.textContent = "";
    errorMessage.classList.add("hidden");
  }

  function setLoading(isLoading) {
    if (loadingMessage) {
      loadingMessage.classList.toggle("hidden", !isLoading);
    }

    predictButton.disabled = isLoading;

    if (isLoading) {
      predictButton.textContent = "診断中...";
    } else {
      predictButton.innerHTML = '診断する <span>›</span>';
    }
  }

  function validateFile(file) {
    if (!file) {
      return "画像を選択してください。";
    }

    if (!file.type.startsWith("image/")) {
      return "画像ファイルを選択してください。";
    }

    const maxSize = 5 * 1024 * 1024;

    if (file.size > maxSize) {
      return "画像サイズは5MB以内にしてください。";
    }

    return "";
  }

  function resetPreview() {
    selectedFile = null;
    previewImage.src = "";
    previewImage.classList.add("hidden");

    if (previewPlaceholder) {
      previewPlaceholder.classList.remove("hidden");
    }

    if (uploadBox) {
      uploadBox.classList.remove("is-selected");
    }

    if (uploadHelp) {
      uploadHelp.innerHTML = `
        またはドラッグ＆ドロップ<br />
        <small>JPG / PNG に対応</small>
      `;
    }
  }

  function showPreview(file) {
    const reader = new FileReader();

    reader.onload = () => {
      previewImage.src = reader.result;
      previewImage.classList.remove("hidden");

      if (previewPlaceholder) {
        previewPlaceholder.classList.add("hidden");
      }

      if (uploadBox) {
        uploadBox.classList.add("is-selected");
      }

      if (uploadHelp) {
        uploadHelp.innerHTML = `
          選択中：${file.name}<br />
          <small>別の画像に変更できます</small>
        `;
      }
    };

    reader.readAsDataURL(file);
  }

  imageInput.addEventListener("change", () => {
    clearError();

    const file = imageInput.files[0];
    const error = validateFile(file);

    if (error) {
      resetPreview();
      showError(error);
      return;
    }

    selectedFile = file;
    showPreview(file);
  });

  if (uploadBox) {
    uploadBox.addEventListener("dragover", (event) => {
      event.preventDefault();
      uploadBox.classList.add("is-dragover");
    });

    uploadBox.addEventListener("dragleave", () => {
      uploadBox.classList.remove("is-dragover");
    });

    uploadBox.addEventListener("drop", (event) => {
      event.preventDefault();
      uploadBox.classList.remove("is-dragover");

      const file = event.dataTransfer.files[0];
      const error = validateFile(file);

      clearError();

      if (error) {
        resetPreview();
        showError(error);
        return;
      }

      selectedFile = file;

      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      imageInput.files = dataTransfer.files;

      showPreview(file);
    });
  }

  predictButton.addEventListener("click", async () => {
    clearError();

    const file = selectedFile || imageInput.files[0];
    const error = validateFile(file);

    if (error) {
      showError(error);
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      // 同一ドメインから配信するため相対パスで指定可能
      // Hugging Face SpacesのAPIエンドポイント（絶対パス）に修正
      const API_URL = "https://kaichoharry-backend-face-achievement.hf.space/predict";

      const response = await fetch(API_URL, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("診断に失敗しました。");
      }

      const data = await response.json();

      // APIのレスポンスに合わせてlocalStorageに保存
      localStorage.setItem("prediction", data.prediction);
      localStorage.setItem("subprediction", `${(data.probability * 100).toFixed(1)}%`);

      window.location.href = "./result.html";
    } catch (error) {
      showError(`エラー: ${error.message}`);
    } finally {
      setLoading(false);
    }
  });
});