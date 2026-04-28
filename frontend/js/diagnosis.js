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

  // =========================
  // エラー表示
  // =========================
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

  // =========================
  // ローディング表示
  // =========================
  function setLoading(isLoading) {
    if (loadingMessage) {
      loadingMessage.classList.toggle("hidden", !isLoading);
    }

    predictButton.disabled = isLoading;
    predictButton.innerHTML = isLoading
      ? "診断中..."
      : '診断する <span>›</span>';
  }

  // =========================
  // ファイルチェック
  // =========================
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

  // =========================
  // プレビュー表示
  // =========================
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

  // =========================
  // ファイル選択時
  // =========================
  imageInput.addEventListener("change", () => {
    clearError();

    const file = imageInput.files[0];
    const error = validateFile(file);

    if (error) {
      selectedFile = null;
      previewImage.src = "";
      previewImage.classList.add("hidden");

      if (previewPlaceholder) {
        previewPlaceholder.classList.remove("hidden");
      }

      showError(error);
      return;
    }

    selectedFile = file;
    showPreview(file);
  });

  // =========================
  // ドラッグ＆ドロップ対応
  // =========================
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

  // =========================
  // 診断ボタン
  // =========================
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
      /*
        ===============================
        仮実装版
        ===============================
        現在はバックエンド接続なしで動くようにしています。
        1秒後に仮の診断結果を保存して result.html に移動します。
      */
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const data = {
        prediction: "nobel",
        subprediction: "nobel_peace"
      };

      localStorage.setItem("prediction", data.prediction || "");
      localStorage.setItem("subprediction", data.subprediction || "");

      window.location.href = "./result.html";

      /*
        ===============================
        本番接続版にする場合
        ===============================
        FastAPIなどのバックエンドに画像を送る場合は、
        上の仮実装を消して、下のコードを使ってください。

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://127.0.0.1:8000/predict", {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          throw new Error("診断に失敗しました。");
        }

        const data = await response.json();

        localStorage.setItem("prediction", data.prediction || "");
        localStorage.setItem("subprediction", data.subprediction || "");

        window.location.href = "./result.html";
      */
    } catch (error) {
      showError(`エラー: ${error.message}`);
    } finally {
      setLoading(false);
    }
  });
});