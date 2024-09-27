from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from lcs import find_lcs
from palindromo import find_longest_palindrome
from z import find_pattern

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files[]')
    text1 = ''
    text2 = ''
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                if text1 == '':
                    text1 = f.read()
                else:
                    text2 = f.read()

    return render_template('index.html', text1=text1, text2=text2)

# Search pattern using KMP/Z
@app.route('/search', methods=['POST'])
def search_pattern():
    pattern = request.form['pattern']
    text = request.form['text']
    
    matches = find_pattern(pattern, text)  # Using your Z algorithm or KMP
    return render_template('index.html', text=text, pattern=pattern, matches=matches)

# Longest Common Substring
@app.route('/similarity', methods=['POST'])
def similarity():
    text1 = request.form['text1']
    text2 = request.form['text2']
    
    lcs = find_lcs(text1, text2)  # Longest Common Substring logic
    return render_template('index.html', text1=text1, text2=text2, lcs=lcs)

# Longest Palindrome
@app.route('/palindrome', methods=['POST'])
def palindrome():
    text = request.form['text']
    
    palindrome = find_longest_palindrome(text)  # Manacher's algorithm for palindrome
    return render_template('index.html', text=text, palindrome=palindrome)

# Autocomplete logic
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    text = request.form['text']
    prefix = request.form['prefix']
    
    # Logic for generating autocomplete suggestions using Tries
    # You can implement this in the `script.js` file or here
    suggestions = generate_autocomplete_suggestions(text, prefix)
    
    return render_template('index.html', text=text, suggestions=suggestions)

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt'}

if __name__ == '__main__':
    app.run(debug=True)
