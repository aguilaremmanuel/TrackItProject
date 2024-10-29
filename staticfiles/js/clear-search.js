const searchInput = document.querySelector('.form-search');
const clearIcon = document.querySelector('.clear-icon');

searchInput.addEventListener('input', function() {
    if (this.value) {
        clearIcon.style.display = 'block'; // Show the clear icon when there's input
    } else {
        clearIcon.style.display = 'none'; // Hide the clear icon when input is empty
    }
});

clearIcon.addEventListener('click', function() {
    searchInput.value = ''; // Clear the input value
    clearIcon.style.display = 'none'; // Hide the clear icon after clearing
    searchInput.focus(); // Refocus the input after clearing
});
