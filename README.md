## CBC_CLI Complete Blood Count CLI Application

   Heres' how the sample looks like in the terminal:
   ![Sample CBC Output](screenshots/Screenshot%20from%202025-06-01%2018-03-31.png)
    
   A python based Command Linr Interface application for managing Diagnostic Data. THis project supports structured Sample Entry,
   Result Flagging and persistend DataBase storage using SQLite.


## Features

 > User can view Detailed CBC Reports by SAmple_ID
 > User can Add a new Sample Interactively
 > Auto Analysis of results using Refference test data ('Low',
      'Normal','High')
 > Built in Refferrence Data for common CBC Paraneters

 ## Project Structure
     CBC_CLI/
├── cli/
│ └── main.py # CLI commands using Click
├── database/
│ ├── db_session.py # Session creation logic
│ ├── seed_data.py # Seeds reference CBC test data and sample
│ └── setup.py # SQLAlchemy engine setup
├── models/
│ └── db_models.py # ORM models: Sample, CBCResult, CBCTest, AnalysisLog
├── utils/
│ └── unit_map.py # Units mapping (for future use)
├── cbc_analysis.db # SQLite database file
└── README.md # Project documentation


##  CBC Tests Supported

Reference data seeded includes:

- WBC
- RBC
- Hemoglobin
- Hematocrit
- Platelets
- MCV
- MCH
- MCHC

Each test includes:
- Units (e.g., `x10^9/l`, `g/dl`, etc.)
- Normal ranges
- Automatic flag assignment (`Low`, `Normal`, `High`)

---

##  Technologies Used

- **Python 3.11+**
- **SQLAlchemy** - ORM for modeling and database operations
- **SQLite** - Lightweight relational database
- **Click** - Beautiful command-line interfaces
- **Datetime** - For timestamping logs and sample entries

---

##  How to Use

###  Step 1: Seed Reference Data

```bash
python -m database.seed_data
Seeds:

Reference test ranges

One default sample (DG-001) if not already present

###   Step 2: Add a Sample
bash:
python -m cli.main add-sample
Prompts you to:

Enter sample ID and patient name

Enter CBC test names and values

Flags each result based on reference ranges

### Step 3: View a Sample
bash:
python -m cli.main view-sample <SAMPLE_ID>
Example:

bash:
python -m cli.main view-sample DG-004
Output:

text
Copy
Edit
🧾 Sample ID: DG-004
👤 Patient: Albert
📅 Collected: 2025-05-31 14:45:43.869154

🧪 CBC Results:
- WBC: 7.0 x10^9/l (Normal: 4.0–11.0) ➤ [Normal]
- RBC: 3.8 x10^12/l (Normal: 4.7–6.1) ➤ [Low]
...
✅ Progress So Far
 Setup clean project structure

 Created SQLAlchemy models for CBC data

 Built a working CLI using Click

 Implemented sample entry and analysis logic

 Designed output format with clear flags

 Seeded reference test data

 View detailed reports per sample ID

###  Future Enhancements
Export sample results as PDF or CSV

Support for CSV batch uploads

Add authentication for sensitive data

Improve test name normalization and auto-suggestions



Created by: Arnold Kiprop Korir
Student at Moringa School | Learning Python, SQLAlchemy & CLI Development


 License
This project is for educational purposes and not intended for clinical or medical use.

---









