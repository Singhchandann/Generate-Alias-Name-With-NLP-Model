# Generate Alias Name with NLP Model

This project generates alias names from full names using an NLP model based on transliteration and fairseq.  


Generate-alias-name-with-NLP-Model/  
│  
├── alias_generator.py  # Your main Python code  
├── requirements.txt    # Dependencies  
├── README.md           # Project overview and instructions  
└── .gitignore          # Files to ignore (like virtual environments)  

  
## How to Run

1. Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

2. Add your data in `total_members.xlsx`.

3. Run the code:

    ```
    python alias_generator.py
    ```

## Project Overview

This project uses the ai4bharat transliteration engine and a IndicTrans2 fairseq model to generate combinations of alias names for a list of full names.
