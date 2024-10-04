# /app.py

from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from palindromo import longest_palindrome
from z import find_substring
from lcs import find_lcs
from trie import Trie, load_text_into_trie
import re

app = Flask(__name__)

# Ensure that the UPLOAD_FOLDER exists
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
trie = Trie()  # Create a global Trie instance

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    file1 = request.files.get('file1')  # Get the first file for Text1
    file2 = request.files.get('file2')  # Get the second file for Text2
    text1 = ''
    text2 = ''
    
    if file1 and allowed_file(file1.filename):
        filename1 = secure_filename(file1.filename)
        t1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'T1.txt')
        file1.save(t1_path)
        with open(t1_path, 'r', encoding='utf-8') as f:
            text1 = f.read()  # Store T1 content

    if file2 and allowed_file(file2.filename):
        filename2 = secure_filename(file2.filename)
        t2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'T2.txt')
        file2.save(t2_path)
        with open(t2_path, 'r', encoding='utf-8') as f:
            text2 = f.read()  # Store T2 content
    
    return render_template('index.html', text1=text1, text2=text2)

# Search pattern using Z-algorithm
import re

@app.route('/search', methods=['POST'])
def search_pattern():
    pattern = request.form['pattern']
    text = request.form['text']  # Retrieve the text that was uploaded
    text_id = request.form['text_id']  # Identify which text is being searched

    # Remove any existing <span class="highlight"> tags
    text = re.sub(r'<span class="highlight">(.*?)</span>', r'\1', text)

    # Find the position of the pattern
    position = find_substring(text, pattern)

    # If the pattern is found, wrap it with a <span> tag for highlighting
    if position != -1:
        highlighted_text = (text[:position] +
                            f'<span class="highlight">{pattern}</span>' +
                            text[position+len(pattern):])
    else:
        highlighted_text = text

    # Keep the original texts and only highlight for this request
    text1 = highlighted_text if text_id == "Text1" else request.form.get('text1', '')
    text2 = highlighted_text if text_id == "Text2" else request.form.get('text2', '')

    # Render the template with the search result and preserved text content
    return render_template('index.html', text1=text1, text2=text2, 
                           pattern=pattern, position=position)


# Longest Common Substring (LCS)
@app.route('/similarity', methods=['POST'])
def similarity():
    text1 = request.form.get('text1', '')  # Get Text1 from the form
    text2 = request.form.get('text2', '')  # Get Text2 from the form

    # Ensure both texts are available
    if not text1 or not text2:
        return "Error: Both Text1 and Text2 are required.", 400

    # Find the longest common substrings (LCS)
    lcs_result = find_lcs(text1, text2)

    # Highlight all LCS occurrences in both texts
    highlighted_text1 = text1
    highlighted_text2 = text2
    for lcs in lcs_result:
        highlighted_text1 = highlighted_text1.replace(lcs, f'<span class="highlight">{lcs}</span>')
        highlighted_text2 = highlighted_text2.replace(lcs, f'<span class="highlight">{lcs}</span>')

    # Render the template with the highlighted LCS
    return render_template('index.html', text1=highlighted_text1, text2=highlighted_text2, lcs=lcs_result)


# Longest Palindrome
@app.route('/palindrome', methods=['POST'])
def palindrome():
    # Check which text is selected
    text_id = request.form['text_id']
    
    # Get the appropriate text based on the selection
    if text_id == "Text1":
        text = request.form['text1']
    else:
        text = request.form['text2']

    # Ensure text is provided
    if not text:
        return "Error: No text provided for palindrome search.", 400

    # Find the longest palindrome using your Manacher's algorithm or any other method
    longest_pal = longest_palindrome(text)

    # Highlight the found palindrome in the text
    highlighted_text = text.replace(longest_pal, f'<span class="highlight-green">{longest_pal}</span>')

    # Render the template with the highlighted palindrome
    if text_id == "Text1":
        return render_template('index.html', text1=highlighted_text, text2=request.form['text2'], palindrome=longest_pal)
    else:
        return render_template('index.html', text1=request.form['text1'], text2=highlighted_text, palindrome=longest_pal)

# Clear highlights
@app.route('/clear', methods=['POST'])
def clear():
    # Get the current text1 and text2 from the form
    text1 = request.form.get('text1', '')
    text2 = request.form.get('text2', '')

    # Remove all highlight tags from the text
    clean_text1 = re.sub(r'<span class="highlight.*?">(.*?)</span>', r'\1', text1)
    clean_text2 = re.sub(r'<span class="highlight.*?">(.*?)</span>', r'\1', text2)

    # Re-render the template with the cleaned text (no highlights)
    return render_template('index.html', text1=clean_text1, text2=clean_text2)


# Autocomplete logic
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    prefix = request.form.get('prefix')
    suggestions = trie.search(prefix)
    return jsonify(suggestions=suggestions)

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt'}

if __name__ == '__main__':
    app.run(debug=True)
