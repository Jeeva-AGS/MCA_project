// document.getElementById('predict-btn').addEventListener('click', function (e) {
//     e.preventDefault();
//     let patient_id = document.getElementById('patient-dropdown').value;
//     let disease = document.querySelector('input[name="disease"]:checked');
//     let imageFile = document.getElementById('image').files[0];

//     if (!patient_id) {
//         alert("Please select a patient.");
//         return;
//     }

//     if (!disease) {
//         alert("Please select a disease.");
//         return;
//     }

//     if (!imageFile) {
//         alert("Please upload an image first.");
//         return;
//     }

//     let formData = new FormData();
//     formData.append('patient_id', patient_id);
//     formData.append('disease', disease.value);
//     formData.append('image', imageFile);

//     fetch('/predict', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.result) {
//             document.getElementById('prediction-results').innerText = data.result;
//         } else {
//             alert("Error: Could not get prediction result.");
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert("An error occurred while getting the prediction.");
//     });
// });