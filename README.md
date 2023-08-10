# Example of importing a file and simply querying in the terminal
This example is based on the examples from Llama index's docs: https://gpt-index.readthedocs.io/en/latest/getting_started/installation.html


Example video for example 0
![Example video](media/example-0.gif)

## Setup
### 0) Install needed tools
``````
sudo apt install build-essential python3.10-dev -y # For some pip installs

sudo apt install pandoc -y # Needed for document processing
```


### 1) Create pyenv and install reqs
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirnments.txt -U
```

### 2) Configure API key
Create a `key.txt` file with your OpenAI API key

### 3) Optional: Configure data
The data directory has a txt with a copy of a Roman cookbook I downloaded from Gutenburg. Feel free to replace this text document with any document/


## Example 0 - Simple CLI query of the Roman Cookbook
NOTE: All commands are run from the root of the repo, if you cd into any directories the paths will need to be changed.

Example video
![Example video](media/example-0.gif)

### Step 1: Build your data store
```
python3 00-simple-cli-query-roman-cookbook/load_data.py 
```

### Step 1: Query the data with a chat interface
```
python3 00-simple-cli-query-roman-cookbook/query.py
```

### Notes:
This simple example isn't doesn't have very high accuracy, but it does work. I will work on improving this in the next examples.