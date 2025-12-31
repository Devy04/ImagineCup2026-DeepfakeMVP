function detect() {
    const fileInput = document.getElementById("fileInput");
    const detectBtn = document.getElementById("detectBtn");
    const progressBar = document.getElementById("progress-bar");
    const verdict = document.getElementById("verdict");
    const confidence = document.getElementById("confidence");
    const explanation = document.getElementById("explanation");

    if (fileInput.files.length === 0) {
        alert("Please select a file before clicking Detect.");
        return;
    }

    const file = fileInput.files[0];
    const mediaType = document.querySelector('input[name="mediaType"]:checked').value;

    if (mediaType === "image" && !file.type.startsWith("image/")) {
        alert("Please upload a valid image file.");
        return;
    }

    if (mediaType === "audio" && !file.type.startsWith("audio/")) {
        alert("Please upload a valid audio file.");
        return;
    }

    detectBtn.disabled = true;
    detectBtn.innerText = "Processing...";

    verdict.innerText = "—";
    confidence.innerText = "—";
    explanation.innerText = "—";

    let progress = 0;
    progressBar.style.width = "0%";
    progressBar.innerText = "0%";

    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + "%";
        progressBar.innerText = progress + "%";

        if (progress >= 100) {
            clearInterval(interval);

            verdict.innerText = "Likely Deepfake";
            confidence.innerText = "82%";
            explanation.innerText = "Detected spectral inconsistencies";

            detectBtn.disabled = false;
            detectBtn.innerText = "Detect";
        }
    }, 300);
}

