document.addEventListener('DOMContentLoaded', function () {
    loadPatients();

    // Handle file upload
    const uploadBox = document.querySelector('.upload-box');
    const imageUploadInput = document.getElementById('imageUpload');
    
    uploadBox.addEventListener('click', () => {
        imageUploadInput.click();
    });

    imageUploadInput.addEventListener('change', () => {
        if (imageUploadInput.files.length > 0) {
            uploadBox.textContent = imageUploadInput.files[0].name;
        }
    });

    // Handle prediction
    document.getElementById('predictBtn').addEventListener('click', function () {
        const patientId = document.getElementById('patientSelect').value;
        const disease = document.querySelector('input[name="disease"]:checked').value;

        if (!patientId || !disease || !imageUploadInput.files.length) {
            alert('Please select patient, disease, and upload an image.');
            return;
        }

        // Call prediction API or perform the desired action
        // For example: make a POST request to send the image and get prediction
    });
});

function loadPatients() {
    fetch('/get_patients')
        .then(response => response.json())
        .then(patients => {
            const patientSelect = document.getElementById('patientSelect');
            patients.forEach(patient => {
                const option = document.createElement('option');
                // Display patient name and additional details
                option.value = patient.id;
                option.textContent = `${patient.name} (Age: ${patient.age})`;
                patientSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading patients:', error));
}
