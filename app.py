from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from palindromo import longest_palindrome
from z import find_substring
from lcs import find_lcs
from trie import Trie, load_text_into_trie

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
    text = request.form['text']  # Now we receive the text content from the form

    # Perform the search using the pattern and the provided text
    position = find_substring(text, pattern)
    
    # Render the template with the search result (you can add more info like position)
    return render_template('index.html', text=text, pattern=pattern, position=position)


# Longest Common Substring (LCS)
@app.route('/similarity', methods=['POST'])
def similarity():
    text1 = request.form['text1']
    text2 = request.form['text2']
    
    lcs = find_lcs(text1, text2)
    return render_template('index.html', text1=text1, text2=text2, lcs=lcs)

# Longest Palindrome
@app.route('/palindrome', methods=['POST'])
def palindrome():
    text = request.form['text']
    
    longest_pal = longest_palindrome(text)
    return render_template('index.html', text=text, palindrome=longest_pal)

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
