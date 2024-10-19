# Flask Application Setup

This guide will walk you through setting up a virtual environment and running a Flask application.

## Prerequisites

- Python 3 installed
- pip (Python package installer) installed
- You need to have cloned this repository

## How to Clone a Repository

In case you do not know how to clone a repository, all you need to do is have git installed on your computer and use the following command.

```bash
git clone https://github.com/dannywu1101/TextSearch.git
```


## Steps

### 1. Navigate to the project directory

Make sure you are in the folder where your `app.py` file is located.

### 2. Create a virtual environment

Run the following command to create a virtual environment:

```bash
python3 -m venv <name_of_virtual_environment>
```

### 3. Activate your virrtual environment:

Run the following command to activate your virtual environment:

```bash
source <name_of_virtual_environment>/bin/activate
```

### 4. Install Flask

Install Flask so you have no problems running the app and using all its functionalities.

```bash
pip3 install flask
```

or

```bash
pip install flask
```

### 5. Run the App

Finally, run the app.py file to start the Flask application: (make sure you´re on the right path).

```bash
python3 app.py
```
or

```bash
python app.py
```

### 6. Deactivate the virtual environment

Once you are done, you can deactivate the virtual environment with:

```bash
deactivate
```

