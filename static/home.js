// Function to show the dialog box
function showDialog() {
    document.getElementById('addPatientDialog').style.display = 'flex';
}

// Function to hide the dialog box
function hideDialog() {
    document.getElementById('addPatientDialog').style.display = 'none';
}

// // Function to add patient details to the list and send to the server
// function addPatient() {
//     const name = document.getElementById('name').value;
//     const age = document.getElementById('age').value;

//     if (name && age) {
//         // Sending data to the server
//         fetch('/add_patient', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ name, age }),
//         }).then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 displayPatient(name, age); // Add new patient to the page
//                 hideDialog(); // Hide the dialog box after adding the patient
//             }
//         });
//     }
// }

// // Function to display a new patient card on the page
// function displayPatient(name, age) {
//     const patientList = document.getElementById('patient-list');
//     const patientCard = document.createElement('div');
//     patientCard.classList.add('patient-card');
//     patientCard.innerHTML = `<p><strong>Name:</strong> ${name}</p><p><strong>Age:</strong> ${age}</p>`;
//     patientList.appendChild(patientCard); // Append the new patient card to the list
// }

function addPatient() {
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const contact = document.getElementById('contact').value;
    const address = document.getElementById('address').value;
    const email = document.getElementById('email').value;
    const profileImage = document.getElementById('profileImage').files[0];
    
    if (name && age && contact && address && email && profileImage) {
        // Create a FormData object to send file and text data
        const formData = new FormData();
        formData.append('name', name);
        formData.append('age', age);
        formData.append('contact', contact);
        formData.append('address', address);
        formData.append('email', email);
        formData.append('profileImage', profileImage);
        
        // Send the data to the server using a POST request
        fetch('/add_patient', {
            method: 'POST',
            body: formData,
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                displayPatient(data.patient); // Display new patient on the page
                hideDialog(); // Hide the dialog box after adding the patient
            } else {
                alert('Error adding patient. Please try again.');
            }
        });
    } else {
        alert('Please fill all fields and upload a profile image.');
    }
}

function displayPatient(patient) {
    const patientList = document.getElementById('patient-list');
    const patientCard = document.createElement('div');
    patientCard.classList.add('patient-card');

    // Display patient information and profile image
    patientCard.innerHTML = `
        <img src="${patient.profileImageUrl}" alt="${patient.name}'s Profile Image" class="profile-img">
        <div class="patient-info">
            <p><strong>Name:</strong> ${patient.name}</p>
            <p><strong>Age:</strong> ${patient.age}</p>
            <p><strong>Contact:</strong> ${patient.contact}</p>
            <p><strong>Address:</strong> ${patient.address}</p>
            <p><strong>Email:</strong> ${patient.email}</p>
        </div>
    `;

    patientList.appendChild(patientCard); // Append the new patient card to the list
}


// Function to display a new patient card on the page
function displayPatient(patient) {
    const patientList = document.getElementById('patient-list');
    const patientCard = document.createElement('div');
    patientCard.classList.add('patient-card');

    // Display patient information and profile image
    patientCard.innerHTML = `
        <img src="${patient.profileImageUrl}" alt="${patient.name}'s Profile Image" class="profile-img">
        <p><strong>Name:</strong> ${patient.name}</p>
        <p><strong>Age:</strong> ${patient.age}</p>
        <p><strong>Contact:</strong> ${patient.contact}</p>
        <p><strong>Address:</strong> ${patient.address}</p>
        <p><strong>Email:</strong> ${patient.email}</p>
    `;

    patientList.appendChild(patientCard); // Append the new patient card to the list
}



// Function to display a new patient card on the page
function displayPatient(patient) {
    const patientList = document.getElementById('patient-list');
    const patientCard = document.createElement('div');
    patientCard.classList.add('patient-card');

    // Display patient information and profile image
    patientCard.innerHTML = `
        <img src="${patient.profileImageUrl}" alt="${patient.name}'s Profile Image" class="profile-img">
        <p><strong>Name:</strong> ${patient.name}</p>
        <p><strong>Age:</strong> ${patient.age}</p>
        <p><strong>Contact:</strong> ${patient.contact}</p>
        <p><strong>Address:</strong> ${patient.address}</p>
        <p><strong>Email:</strong> ${patient.email}</p>
    `;

    patientList.appendChild(patientCard); // Append the new patient card to the list
}



// Function to fetch and display all patients on page load
window.onload = function() {
    fetch('/get_patients')
    .then(response => response.json())
    .then(data => {
        data.forEach(patient => {
            displayPatient(patient[0], patient[1]); // Display each patient
        });
    });
};


// Show Predict Disease Dialog
function showPredictDialog() {
    document.getElementById('predictDiseaseDialog').style.display = 'flex';
}

// Hide Predict Disease Dialog
function hidePredictDialog() {
    document.getElementById('predictDiseaseDialog').style.display = 'none';
}

// Handle Image Upload
function uploadImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (file) {
        // Display file name or do additional processing if needed
        console.log('Image uploaded:', file.name);
    } else {
        alert('Please select an image to upload.');
    }
}

// Handle Prediction Request
function getPrediction() {
    // Mockup prediction logic. Replace with actual API call.
    const predictionResult = document.getElementById('prediction-result');
    predictionResult.innerHTML = "Processing..."; // Show loading message
    
    // Simulate a delay for the prediction process
    setTimeout(() => {
        predictionResult.innerHTML = "Prediction: Disease B";
    }, 2000);
}


// Show patient details in dialog
function showPatientDetails(name, age, contact, email, address, imagePath) {
    // Populate dialog with patient details
    document.getElementById('dialogPatientName').textContent = name;
    document.getElementById('dialogPatientAge').textContent = age;
    document.getElementById('dialogPatientContact').textContent = contact;
    document.getElementById('dialogPatientEmail').textContent = email;
    document.getElementById('dialogPatientAddress').textContent = address;
    document.getElementById('patientDialogImage').src = imagePath;

    // Display the dialog
    document.getElementById('patientDetailsDialog').style.display = 'block';
}

// Hide patient details dialog
function hidePatientDetails() {
    document.getElementById('patientDetailsDialog').style.display = 'none';
}
