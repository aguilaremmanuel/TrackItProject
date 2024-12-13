function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

document.addEventListener('DOMContentLoaded', function() {

    const selectAllBtn = document.getElementById('selectAllBtn');
    const table = document.querySelector('#recordsTable');

    document.addEventListener('change', function (e) {

        if (e.target.type === 'checkbox') {

            const value = e.target.value;
            const numericValue = Number(value);

            if(!isNaN(numericValue) && Number.isInteger(numericValue) && value != "") {

                let action;

                if (e.target.checked) {
                    action = "checked";
                } else {
                    action = "unchecked";
                    selectAllBtn.innerHTML = 'Select All';
                }

                fetch(`/select-document/${action}/${numericValue}/`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("success");
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                
            }

        }
    });

    selectAllBtn.addEventListener('click', function(e) {
        e.preventDefault();

        const checkboxes = table.querySelectorAll('input[type="checkbox"]');

        const allSelected = Array.from(checkboxes).every(checkbox => checkbox.checked);

        let documents_no = [];
        let action = "";

        checkboxes.forEach(checkbox => {
            checkbox.checked = !allSelected;
            documents_no.push(checkbox.value);
        });

        if(allSelected) {
            selectAllBtn.innerHTML = 'Select All';
            action = 'deselect-all';
        }else{
            selectAllBtn.innerHTML = 'Deselect All';
            action = 'select-all';
        }

        fetch(`/select-all-documents/${action}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() 
            },
            body: JSON.stringify({ documents_no }) 
        })
            .then(response => response.json())
            .then(data => {
                console.log("Success");
            })
            .catch(error => {
                console.error('Error:', error);
            });

    });

});