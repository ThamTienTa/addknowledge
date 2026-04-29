# UnFail — AI Training Data Collector

A simple web app where contributors can submit conversation training data, and the owner can **approve** or **delete** each submission before using it to train an AI.

---

## 📁 Project Structure

```
unfail-training-collector/
├── app.py
├── requirements.txt
├── README.md
├── data.json           ← auto-created on first run
└── templates/
    └── index.html
```

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/unfail-training-collector.git
cd unfail-training-collector
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## 🧠 How to Submit Training Data

Use this format — each conversation pair is one `User:` line followed by one `AI:` line:

```
User: hi
AI: hello! how are you today?

User: hi
AI: hey! nice to talk to you

User: how are you
AI: i'm doing well, thanks for asking. how about you?

User: what is your name
AI: i am a simple ai chatbot created to talk with you.
```

- Each line starts with either `User:` or `AI:`
- You can include multiple pairs in one submission
- Enter your name so the owner knows who submitted it

---

## ✅ Owner Workflow

1. Open `http://localhost:5000`
2. See all **Pending** submissions at the top
3. Click **Approve** to move a submission to the Approved list
4. Click **Delete** to reject and remove it
5. Copy approved data from the Approved section to use for training

---

## 💾 Data Storage

All data is saved in `data.json` automatically. No database setup needed.

---

## 📄 License

MIT — free to use and modify.
