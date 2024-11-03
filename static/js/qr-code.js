async function getQRCodeURL(documentNo) {
    try {
        const response = await fetch(`/generate-qrcode/${documentNo}/`);
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

function displayRoutes(documentNo) {
    fetch(`/get-routes/${documentNo}/`) // Adjust the endpoint to match your view
        .then(response => response.json())
        .then(data => {
            document.getElementById('routesInitials').textContent = data.str_routes;
            document.getElementById('routesTitles').textContent = "(" + data.str_routes_titles + ")";
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {

    const documentQRCodeLink = document.getElementById('documentTitleLink');

    documentQRCodeLink.addEventListener('click', async function () {
        documentNo = documentQRCodeLink.getAttribute('data-document-no');
        console.log("emns" + documentNo);
        let url = await getQRCodeURL(documentNo);
        if(url) {
            document.getElementById('qrCodeImage').src = url;
        }
        displayRoutes(documentNo);
        let trackingNo = document.getElementById('documentTrackingNumber').textContent;
        document.getElementById('qrModalTrackingNo').textContent = trackingNo;
    });

    document.getElementById('saveQR').addEventListener('click', async function() {

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const strRoutes = document.getElementById('routesInitials').textContent;
        const routesTitles = document.getElementById('routesTitles').textContent;
        const strTrackingNo = document.getElementById('documentTrackingNumber').textContent;
        const documentNo = document.getElementById('documentTitleLink').getAttribute('data-document-no');
        let url = await getQRCodeURL(documentNo);
        const qrCodeImg = new Image();
        qrCodeImg.src = url;
        qrCodeImg.onload = function () {
            canvas.width = qrCodeImg.width;
            canvas.height = qrCodeImg.height + 110; // Extra space for text
            // Fill the canvas with a white background
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            // Draw the QR code image
            ctx.drawImage(qrCodeImg, 0, 50); // Adjust y position for QR code
            // Set font for the text
            ctx.font = 'bold 31px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillStyle = 'black'; 
            ctx.fillText(strRoutes, canvas.width / 2, 43);
            ctx.font = '16px Inter, sans-serif';
            ctx.fillText(routesTitles, canvas.width / 2, 65);
            ctx.font = 'bold 20px Inter, sans-serif';
            ctx.fillText(strTrackingNo, canvas.width / 2, canvas.height - 54);
            ctx.font = '16px Inter, sans-serif';
            ctx.fillText("(Document Tracking Number)", canvas.width / 2, canvas.height - 35);
            // Trigger download
            const link = document.createElement('a');
            link.href = canvas.toDataURL('image/png');
            link.download = 'doc_' + documentNo + '_qr_code.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };
    });

});