// /JS/script.js

const searchInput = document.querySelector('input[name="pattern"]');
const textDisplay1 = document.querySelector('#text-display p:nth-of-type(1)');
const textDisplay2 = document.querySelector('#text-display p:nth-of-type(2)');

let matches = [];  // Array to store all matches in both Text1 and Text2
let currentIndex = -1;
let originalText1 = textDisplay1.innerText;
let originalText2 = textDisplay2.innerText;

// Real-time search listener
searchInput.addEventListener('input', function () {
    const pattern = searchInput.value;
    if (pattern.length > 0) {
        matches = [];  // Reset matches before finding new ones
        findMatches(textDisplay1, pattern, 'Text1');
        findMatches(textDisplay2, pattern, 'Text2');
    } else {
        resetTextDisplay(textDisplay1, 'Text1');
        resetTextDisplay(textDisplay2, 'Text2');
    }
});

// Reset the text display to the original text
function resetTextDisplay(textElement, textId) {
    if (textId === 'Text1') {
        textElement.innerHTML = originalText1;
    } else {
        textElement.innerHTML = originalText2;
    }
}

// Clear All Highlights and Reset State
function clearAllHighlights() {
    resetTextDisplay(textDisplay1, 'Text1');
    resetTextDisplay(textDisplay2, 'Text2');
    matches = [];
    currentIndex = -1;
    searchInput.value = '';  // Clear the search input if necessary
}

// Find all matches in the given text
function findMatches(textElement, pattern, textId) {
    const caseSensitive = document.getElementById('case-sensitive').checked;
    const regex = new RegExp(`(${pattern})`, caseSensitive ? 'g' : 'gi');
    const originalText = textId === 'Text1' ? originalText1 : originalText2;

    // Reset currentIndex
    currentIndex = -1;

    // Search for matches
    let match;
    while ((match = regex.exec(originalText)) !== null) {
        matches.push({
            index: match.index,
            length: match[0].length,
            textId: textId,
        });
    }

    if (matches.length > 0) {
        currentIndex = 0;
        highlightCurrentMatch();  // Highlight the first match
    } else {
        resetTextDisplay(textElement, textId);
    }
}

// Highlight only the current match
function highlightCurrentMatch() {
    if (matches.length === 0 || currentIndex === -1) {
        resetTextDisplay(textDisplay1, 'Text1');
        resetTextDisplay(textDisplay2, 'Text2');
        return;
    }

    const match = matches[currentIndex];
    const textElement = match.textId === 'Text1' ? textDisplay1 : textDisplay2;
    const originalText = match.textId === 'Text1' ? originalText1 : originalText2;

    // Reset both text areas before highlighting
    resetTextDisplay(textDisplay1, 'Text1');
    resetTextDisplay(textDisplay2, 'Text2');

    // Highlight the current match
    const beforeMatch = originalText.slice(0, match.index);
    const matchText = originalText.slice(match.index, match.index + match.length);
    const afterMatch = originalText.slice(match.index + match.length);

    textElement.innerHTML = `${beforeMatch}<span class="highlight">${matchText}</span>${afterMatch}`;
}

// Navigation between matches
function navigateMatches(forward = true) {
    if (matches.length === 0) return;

    if (forward) {
        currentIndex = (currentIndex + 1) % matches.length;  // Move forward
    } else {
        currentIndex = (currentIndex - 1 + matches.length) % matches.length;  // Move backward
    }

    highlightCurrentMatch();
}

// Bind buttons for next/previous match navigation
document.querySelector('#next-match').addEventListener('click', () => navigateMatches(true));
document.querySelector('#prev-match').addEventListener('click', () => navigateMatches(false));

// Bind Clear All button to reset all highlights
document.querySelector('#clear-all-btn').addEventListener('click', function (e) {
    e.preventDefault();
    clearAllHighlights();
});
