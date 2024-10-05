// Smooth scrolling for anchor links
document.addEventListener("DOMContentLoaded", function() {
  // Select all links with hashes
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener("click", function(e) {
          e.preventDefault();
          const target = document.querySelector(this.getAttribute("href"));
          if (target) {
              target.scrollIntoView({
                  behavior: "smooth",
                  block: "start"
              });
          }
      });
  });
});

// File upload validation (checks if a file is selected)
document.addEventListener("DOMContentLoaded", function() {
  const uploadForms = document.querySelectorAll("form");

  uploadForms.forEach(form => {
      form.addEventListener("submit", function(event) {
          const fileInput = form.querySelector('input[type="file"]');
          if (!fileInput.files.length) {
              alert("Please select an audio file before submitting.");
              event.preventDefault();  // Prevent form submission if no file is selected
          } else {
              const file = fileInput.files[0];
              const allowedExtensions = ['audio/wav', 'audio/mp3', 'audio/ogg'];
              if (!allowedExtensions.includes(file.type)) {
                  alert("Unsupported file format. Please upload a .wav, .mp3, or .ogg file.");
                  event.preventDefault();  // Prevent form submission if file format is incorrect
              }
          }
      });
  });
});

// Placeholder for real-time audio processing
function startRealTimeAnalysis() {
  alert("Real-time audio analysis feature is under development. Stay tuned!");
}

// Placeholder function to demonstrate keyword detection (can be updated with real logic)
function demoKeywordDetection() {
  alert("Keyword detection is currently in demo mode. This will soon be connected with our backend.");
}

// Placeholder for future interactive exercises
function demoAudioClassification() {
  alert("Audio classification is currently in demo mode. Real-time classification coming soon!");
}

// Attach the placeholder functions to buttons (if needed)
document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll('.tool button').forEach(button => {
      button.addEventListener('click', function(event) {
          const toolType = event.target.getAttribute('data-tool');
          switch (toolType) {
              case 'realTimeAnalysis':
                  startRealTimeAnalysis();
                  break;
              case 'keywordDetection':
                  demoKeywordDetection();
                  break;
              case 'audioClassification':
                  demoAudioClassification();
                  break;
              default:
                  alert("Feature under development!");
          }
      });
  });
});
