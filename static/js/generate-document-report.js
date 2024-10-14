function openDocumentReportPDF() {

    console.log("ewan;");
    const documentNo = document.getElementById('generateDocumentReportBtn').getAttribute('data-document-no');
    window.open(`/generate-document-report/${documentNo}`, '_blank');
}