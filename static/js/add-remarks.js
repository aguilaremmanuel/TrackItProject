async function getFileUploadQRCodeURL(activityLogNo) {
    console.log("wla remar");
    try {
        const response = await fetch(`/generate-upload-file-qrcode/${activityLogNo}/`);
        if (response.ok) {
            const blob = await response.blob(); // Get the response as a Blob
            const url = URL.createObjectURL(blob); // Create a URL for the QR code blob
            return url; // Return the URL
        } else {
            throw new Error('Failed to generate QR Code');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function fetchPhoneUploadFile() {

    let saveRemarks = document.getElementById('saveRemarks');
    let activityLogNew = saveRemarks.getAttribute('data-activity-log-no');

    fetch(`/fetch-phone-upload-file/${activityLogNew}/`)
    .then(response => response.json())
    .then(data => {
        if(data.filename) {
            const filename = document.getElementById('filenamePhoneUpload');
            filename.textContent = data.filename;
            filename.classList.add('file-name-phone-upload');
            document.getElementById('deletePhoneUploadFile').style.display = "inline-flex";
        }else {
            const filename = document.getElementById('filenamePhoneUpload');
            filename.textContent = "No file uploaded";
            filename.classList.remove('file-name-phone-upload'); 
            document.getElementById('deletePhoneUploadFile').style.display = "none";
            
        }
    })
    .catch(error => console.error('Error', error));
}

function addRemarks() {
    
    const addRemarksBtn = document.getElementById('saveRemarks');
    addRemarksBtn.addEventListener('click', function() {

        const documentNo = addRemarksBtn.getAttribute('data-document-no');
        const remarksNo = addRemarksBtn.getAttribute('data-remarks-no');

        const form = document.getElementById('remarksForm');
        const formData = new FormData(form);

        fetch(`/add-remarks/${documentNo}/${remarksNo}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(), // Ensure CSRF token is included for security
            }
        })
            .then(response => response.json())
            .then(status => {
                document.getElementById('remarks').value = '';
            })
            .catch(error => console.error('Error', error));
    });

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name)).split('=')[1];
        return cookieValue;
    }
}

function clearRemarksAttachmentModal() {
    
    document.getElementById('remarks').value = '';

    const directUpload = document.getElementById('directUpload');
    directUpload.checked = true;
    directUpload.dispatchEvent(new Event('change'));

    document.getElementById('option1').classList.remove('d-none');
    document.getElementById('option2').classList.add('d-none');
    document.getElementById('attachmentFile').value = '';

    document.getElementById('saveRemarks').removeAttribute('data-activity-log-no');
    const filename = document.getElementById('filenamePhoneUpload');
    filename.textContent = "No file uploaded";
    filename.classList.remove('file-name-phone-upload'); 
    document.getElementById('deletePhoneUploadFile').style.display = "none";
}

function deleteEmptyRemarks() {
    fetch(`/delete-empty-remarks/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    addRemarks();
    deleteEmptyRemarks();

    const saveRemarksBtn =  document.getElementById('saveRemarks');
    const directUploadOption = document.getElementById('directUpload');
    const scanQRCodeOption = document.getElementById('scanAttachmentQRCode');
    const fileUploadInput = document.getElementById('attachmentFile');
    const activityLogNo = saveRemarksBtn.getAttribute('data-activity-log-no');
   
    // Function to log selected option
    function logSelectedOption() {
        if (directUploadOption.checked) {
            console.log("Direct Upload Selected");
        } 
    }

    directUploadOption.addEventListener('change', logSelectedOption);

    scanQRCodeOption.addEventListener('change', async function () {

        fileUploadInput.value = '';
        const activityLogNo = saveRemarksBtn.getAttribute('data-activity-log-no');
        console.log(activityLogNo);
        let url = await getFileUploadQRCodeURL(activityLogNo);

        if(url) {
            document.getElementById('uploadFileQr').src = url;
            document.getElementById('qrCodeSpinnerContainer').style.display = 'none';
            document.getElementById('qrCodeUploadContainer').style.display = 'flex';
        } 
        
    });

    document.getElementById('deletePhoneUploadFile').addEventListener('click', function () {
        
        const activityLogNo = saveRemarksBtn.getAttribute('data-activity-log-no');

        fetch(`/delete-phone-upload-file/${activityLogNo}/`)
        .then(response => response.json())
        .then(data => {
            console.log("delete sucess");
        })
        .catch(error => console.error('Error', error));

    });

    const addRemarksCloseBtn = document.getElementById('addRemarksCloseBtn');
    addRemarksCloseBtn.addEventListener('click', function() {
        clearRemarksAttachmentModal();
    });

    const scanAttachmentRadio = document.getElementById('scanAttachmentQRCode');
    const directUploadRadio = document.getElementById('directUpload');
    let activityLogInterval;

    function startInterval() {
        if (!activityLogInterval) { 
            activityLogInterval = setInterval(function() {
                fetchPhoneUploadFile(); // Ensure fetchPhoneUploadFile is defined
            }, 3000);
        }
    }

    function stopInterval() {
        if (activityLogInterval) {
            clearInterval(activityLogInterval);
            activityLogInterval = null; 
        }
    }

    if (scanAttachmentRadio.checked) {
        startInterval();
    }

    scanAttachmentRadio.addEventListener('change', function() {
        if (this.checked) {
            startInterval(); 
        } else {
            stopInterval(); 
        }
    });
    
    directUploadRadio.addEventListener('change', function() {
        if (this.checked) {
            stopInterval();
        }
    });
    
});