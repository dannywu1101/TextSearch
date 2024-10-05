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
@app.route('/search', methods=['POST'])
def search_pattern():
    pattern = request.form['pattern']
    text1 = request.form['text1']  # Retrieve Text1 that was uploaded
    text2 = request.form['text2']  # Retrieve Text2 that was uploaded

    # Remove any existing <span class="highlight"> tags from both texts
    text1 = re.sub(r'<span class="highlight">(.*?)</span>', r'\1', text1)
    text2 = re.sub(r'<span class="highlight">(.*?)</span>', r'\1', text2)

    # Define a helper function to highlight all occurrences of the pattern
    def highlight_all_occurrences(text, pattern):
        return re.sub(f'({re.escape(pattern)})', r'<span class="highlight">\1</span>', text)

    # Highlight the pattern in both Text1 and Text2
    highlighted_text1 = highlight_all_occurrences(text1, pattern)
    highlighted_text2 = highlight_all_occurrences(text2, pattern)

    # Render the template with the updated text content
    return render_template('index.html', text1=highlighted_text1, text2=highlighted_text2, pattern=pattern)







# Find LCS
@app.route('/similarity', methods=['POST'])
def similarity():
    text1 = request.form.get('text1', '')  # Get Text1 from the form
    text2 = request.form.get('text2', '')  # Get Text2 from the form

    # Ensure both texts are available
    if not text1 or not text2:
        return "Error: Both Text1 and Text2 are required.", 400

    # Clear any existing palindrome highlights before applying similarity highlights
    text1 = re.sub(r'<span class="highlight-green">(.*?)</span>', r'\1', text1)
    text2 = re.sub(r'<span class="highlight-green">(.*?)</span>', r'\1', text2)

    # Find the longest common substrings (LCS)
    lcs_result = find_lcs(text1, text2)

    # Highlight all LCS occurrences in both texts with the "highlight-blue" class
    highlighted_text1 = text1
    highlighted_text2 = text2
    for lcs in lcs_result:
        highlighted_text1 = re.sub(f'({lcs})', r'<span class="highlight-blue">\1</span>', highlighted_text1)
        highlighted_text2 = re.sub(f'({lcs})', r'<span class="highlight-blue">\1</span>', highlighted_text2)

    # Render the template with the highlighted LCS
    return render_template('index.html', text1=highlighted_text1, text2=highlighted_text2, lcs=lcs_result)



# Find Palindrome
@app.route('/palindrome', methods=['POST'])
def palindrome():
    # Check which text is selected
    text_id = request.form['text_id']

    # Get the appropriate text based on the selection
    if text_id == "Text1":
        text = request.form['text1']
        other_text = request.form['text2']  # Get the other text without modification
    else:
        text = request.form['text2']
        other_text = request.form['text1']  # Get the other text without modification

    # Ensure text is provided
    if not text:
        return "Error: No text provided for palindrome search.", 400

    # Clear any existing highlights from both texts
    text = re.sub(r'<span class="highlight.*?">(.*?)<\/span>', r'\1', text)
    other_text = re.sub(r'<span class="highlight.*?">(.*?)<\/span>', r'\1', other_text)

    # Debugging: Print the cleaned text to check if it's correct
    print(f"Cleaned text for palindrome search in {text_id}: {text}")

    # Find the longest palindrome using Manacher's algorithm
    longest_pal = longest_palindrome(text)

    # Debugging: Print the longest palindrome found
    print(f"Longest palindrome in {text_id}: {longest_pal}")

    # Highlight the found palindrome in the selected text with the "highlight-green" class
    if longest_pal:
        highlighted_text = text.replace(longest_pal, f'<span class="highlight-green">{longest_pal}</span>')
    else:
        highlighted_text = text

    # Render the template with the highlighted palindrome and unmodified other text
    if text_id == "Text1":
        return render_template('index.html', text1=highlighted_text, text2=other_text, palindrome=longest_pal)
    else:
        return render_template('index.html', text1=other_text, text2=highlighted_text, palindrome=longest_pal)


# Clear All Highlights
@app.route('/clear', methods=['POST'])
def clear():
    # Retrieve text1 and text2 without any highlights
    text1 = request.form.get('text1', '')
    text2 = request.form.get('text2', '')
    
    # Render the page with the original text, clearing any highlights
    return render_template('index.html', text1=text1, text2=text2)

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
