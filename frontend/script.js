function detect() {
    
    const fileInput = document.getElementById("fileInput");      
    const detectBtn = document.getElementById("detectBtn");      
    const progressBar = document.getElementById("progress-bar"); 
    const verdict = document.getElementById("verdict");          
    const confidence = document.getElementById("confidence");    
    const explanation = document.getElementById("explanation");  
    if (fileInput.files.length === 0) {
        alert("Please select an image file first.");
        return;
    }

    const file = fileInput.files[0];

    if (!file.type.startsWith("image/")) {
        alert("Only image files are supported right now.");
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
        if (progress < 90) {
            progress += 10;
            progressBar.style.width = progress + "%";
            progressBar.innerText = progress + "%";
        }
    }, 200);

    const formData = new FormData();
    formData.append("file", file); 

    
    fetch("http://127.0.0.1:5000/detect", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Backend error");
        }
        return response.json();
    })
    .then(data => {
        
        clearInterval(interval);

        
        progressBar.style.width = "100%";
        progressBar.innerText = "100%";

        
        verdict.innerText = data.verdict;
        confidence.innerText = (data.confidence * 100).toFixed(2) + "%";
        explanation.innerText = data.explanation;

        detectBtn.disabled = false;
        detectBtn.innerText = "Detect";
    })
    .catch(error => {
        clearInterval(interval);

        verdict.innerText = "Error";
        confidence.innerText = "—";
        explanation.innerText = "Could not connect to backend";

        detectBtn.disabled = false;
        detectBtn.innerText = "Detect";

        console.error("Detection failed:", error);
    });
}
