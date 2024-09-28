document.addEventListener('DOMContentLoaded', function() {
            
    document.getElementById('printQR').addEventListener('click', async function() {

        let routesInitials = document.getElementById('routesInitials').textContent;
        let routesTitles = document.getElementById('routesTitles').textContent;
        let trackingNo = document.getElementById('documentTrackingNumber').textContent;
        let documentNo = document.getElementById('documentTitleLink').getAttribute('data-document-no');
        let url = await getQRCodeURL(documentNo);

        const printWindow = window.open('', '', 'height=600,width=700');
        printWindow.document.write('<html><head><title>Print QR Code</title>');
        printWindow.document.write('<style>');
        printWindow.document.write('body, html { font-family: Inter, sans-serif; text-align: center; margin: 0; padding: 0; }');
        printWindow.document.write('img { max-width: 45mm;}'); // Limit QR code width to 45mm
        printWindow.document.write('p { font-size: 18px; font-weight: bold; margin: 0; padding: 0; }'); // Adjust font size
        printWindow.document.write('@media print { body, html { margin: 0; padding: 0; } }'); // Additional print-specific styles
        printWindow.document.write('</style>');
        printWindow.document.write('</head><body>');;    
        printWindow.document.write('<div style="width: 165px; display: flex; flex-direction: column; align-items: center;">'); // Centering div
        printWindow.document.write('<p>' + routesInitials + '</p>');
        printWindow.document.write('<p style="font-size: 9px; font-weight: 400">('+ routesTitles +')</p>');
        printWindow.document.write('<img id="qrCodeImage" src="' + url + '" />');
        printWindow.document.write('<p style="font-size: 13px;">' + trackingNo + '</p>');
        printWindow.document.write('<p style="font-size: 8px; font-weight: 400">(Document Tracking Number)</p>');
        printWindow.document.write('</div>');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
         // Wait for the image to load before printing
        const qrCodeImage = printWindow.document.getElementById('qrCodeImage');
        qrCodeImage.onload = function() {
            printWindow.focus();
            printWindow.print();
        };
    });
});