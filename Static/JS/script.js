// /Static/JS/script.js

// HTML elements for text input and autocomplete suggestions
const inputField = document.getElementById('autocomplete-input');
const suggestionBox = document.getElementById('suggestion-box');

// Event listener for input changes
inputField.addEventListener('input', function() {
    const prefix = inputField.value;
    if (prefix.length > 0) {
        fetchSuggestions(prefix);
    } else {
        suggestionBox.innerHTML = ''; // Clear suggestions if input is empty
    }
});

// Function to fetch suggestions from the Flask backend
function fetchSuggestions(prefix) {
    fetch('/autocomplete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'prefix': prefix
        })
    })
    .then(response => response.json())
    .then(data => {
        displaySuggestions(data.suggestions);
    })
    .catch(error => {
        console.error('Error fetching suggestions:', error);
    });
}

// Function to display suggestions in the dropdown
function displaySuggestions(suggestions) {
    suggestionBox.innerHTML = ''; // Clear previous suggestions

    suggestions.forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = suggestion;
        suggestionItem.addEventListener('click', () => {
            inputField.value = suggestion; // Set clicked suggestion as input value
            suggestionBox.innerHTML = '';  // Clear suggestions
        });
        suggestionBox.appendChild(suggestionItem);
    });
}
