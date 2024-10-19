// Function to open the modal and display the image
function openModal(imageSrc) {
    var modal = document.getElementById("imageModal");
    var modalImage = document.getElementById("modalImage");
    modal.style.display = "block";
    modalImage.src = imageSrc;
}

// Function to close the modal
function closeModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
