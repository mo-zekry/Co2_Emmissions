// Event listener for form submission using Fetch API
document
  .getElementById("predictionForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const formData = new FormData(event.target);

    // Send POST request to Flask server
    fetch("/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json()) // Parse response as JSON
      .then((data) => {
        // Update result element with prediction
        document.getElementById("result").textContent = data.prediction;
      });
  });

// Event listener for DOMContentLoaded event
document.addEventListener("DOMContentLoaded", function () {
  // Form submission event listener
  document
    .getElementById("predictionForm")
    .addEventListener("submit", handlePredictionFormSubmit);
});

// Function to handle form submission
function handlePredictionFormSubmit(event) {
  event.preventDefault(); // Prevent form submission

  // Get form inputs
  var model = document.getElementById("model").value;
  var year = document.getElementById("year").value;
  var month = document.getElementById("month").value;

  // Validation
  if (model === "" || year === "" || month === "") {
    alert("Please fill in all fields.");
    return;
  }

  if (
    isNaN(parseInt(year)) ||
    isNaN(parseInt(month)) ||
    parseInt(month) < 1 ||
    parseInt(month) > 12
  ) {
    alert("Please enter a valid year and month.");
    return;
  }

  // Display loading message
  document.getElementById("result").innerHTML = "Loading...";

  // Send AJAX request to Flask server
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/predict", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Parse JSON response
        var response = JSON.parse(xhr.responseText);
        // Display prediction result
        document.getElementById("result").innerHTML =
          `Predicted CO2 Emissions at ${year} / ${month}: ${response.prediction.toFixed(2)} T_CO2E`;
      } else {
        // Display error message if request fails
        document.getElementById("result").innerHTML =
          "Error: Failed to make prediction.";
      }
    }
  };
  // Send form data in the request body
  xhr.send("model=" + model + "&year=" + year + "&month=" + month);
}
