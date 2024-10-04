// /Static/JS/script.js
const searchInput = document.querySelector('input[name="pattern"]');
const textDisplay1 = document.querySelector('#text-display p:nth-of-type(1)');
const textDisplay2 = document.querySelector('#text-display p:nth-of-type(2)');

let currentIndex = -1;
let matches = [];
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
    textElement.innerHTML = textId === 'Text1' ? originalText1 : originalText2;
}

// Clear All Highlights
function clearAllHighlights() {
    // Remove only the highlight spans without resetting the content
    textDisplay1.innerHTML = textDisplay1.innerHTML.replace(/<span class="highlight.*?">(.*?)<\/span>/g, '$1');
    textDisplay2.innerHTML = textDisplay2.innerHTML.replace(/<span class="highlight.*?">(.*?)<\/span>/g, '$1');
}

// Find all matches and store their positions
function findMatches(textElement, pattern, textId) {
    const caseSensitive = document.getElementById('case-sensitive').checked;
    const regex = new RegExp(`(${pattern})`, caseSensitive ? 'g' : 'gi');
    const originalText = textId === 'Text1' ? originalText1 : originalText2;

    // Reset matches array
    let match;
    while ((match = regex.exec(originalText)) !== null) {
        matches.push({
            index: match.index,
            length: match[0].length,
            textId: textId,
        });
    }

    if (matches.length > 0) {
        currentIndex = 0;  // Start with the first match
        highlightCurrentMatch();  // Highlight the first match
    } else {
        resetTextDisplay(textElement, textId);  // No matches, reset text
    }
}

// Highlight only the current match and reset the other text
function highlightCurrentMatch() {
    if (matches.length === 0 || currentIndex === -1) {
        resetTextDisplay(textDisplay1, 'Text1');
        resetTextDisplay(textDisplay2, 'Text2');
        return;
    }

    const match = matches[currentIndex];
    const textElement = match.textId === 'Text1' ? textDisplay1 : textDisplay2;
    const otherTextElement = match.textId === 'Text1' ? textDisplay2 : textDisplay1;
    const originalText = match.textId === 'Text1' ? originalText1 : originalText2;

    // Reset the other text to remove any highlights
    resetTextDisplay(otherTextElement, match.textId === 'Text1' ? 'Text2' : 'Text1');

    // Now highlight the current match in the relevant text element
    const beforeMatch = originalText.slice(0, match.index);
    const matchText = originalText.slice(match.index, match.index + match.length);
    const afterMatch = originalText.slice(match.index + match.length);

    textElement.innerHTML = `${beforeMatch}<span class="highlight">${matchText}</span>${afterMatch}`;
}

// Navigation between matches
function navigateMatches(forward = true) {
    if (matches.length === 0) return;

    // Navigate through matches
    if (forward) {
        currentIndex = (currentIndex + 1) % matches.length;
    } else {
        currentIndex = (currentIndex - 1 + matches.length) % matches.length;
    }

    // Update the highlighting
    highlightCurrentMatch();
}

// Bind buttons for next/previous navigation
document.querySelector('#next-match').addEventListener('click', () => navigateMatches(true));
document.querySelector('#prev-match').addEventListener('click', () => navigateMatches(false));

// Bind Clear All Button
document.querySelector('#clear-all-btn').addEventListener('click', function (e) {
    e.preventDefault();  // Prevent the form from submitting
    clearAllHighlights();  // Clear all highlights
});
