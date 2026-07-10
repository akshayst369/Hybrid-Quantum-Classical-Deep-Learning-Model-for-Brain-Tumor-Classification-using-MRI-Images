# Hybrid Quantum-Classical Deep Learning for Brain Tumor Classification

Welcome to the project repository! This project implements a Hybrid Quantum Convolutional Neural Network (HQCNN) combining classical CNN feature extraction layers with a Variational Quantum Circuit (VQC) to classify brain tumors from MRI scans.

---

## 🛠️ Repository Workflow & Git Guidelines

To maintain a stable and clean codebase, our `main` branch is **protected**. You cannot push code directly to `main`. All changes must go through a **Feature-Branch Workflow** and be approved via a Pull Request (PR).

### The Golden Rules
1. **Never work directly on `main`.** Always create a branch for your specific task.
2. **Branch by feature, not by name.** Use naming conventions like `feat/data-pipeline` or `fix/loss-function`.
3. **Keep commits atomic.** Write descriptive commit messages (e.g., `git commit -m "Added normalization to MRI preprocessing"`).

---

## 🚀 Step-by-Step: How to Contribute

Whenever you want to add code, fix a bug, or update documentation, follow these exact steps in your terminal:

### Step 1: Sync with Remote Main
Before starting any new work, switch to main and pull the latest codebase to ensure your environment is fully updated:
```bash
git checkout main
git pull origin main
```

### Step 2: Create Your Feature Branch
Create and switch to a new branch dedicated to the specific task you are working on:
```bash
git checkout -b feat/your-feature-name
```

### Step 3: Develop and Commit
Write your code, stage your modifications, and save your progress locally with a meaningful message:
```bash
git add .
git commit -m "Briefly explain what you changed"
```

### Step 4: Push to GitHub
Upload your local branch and its commits to the remote repository on GitHub:
```bash
git push origin feat/your-feature-name
```

---

## 🔍 How to Open a Pull Request (PR)

Once you have pushed your branch, follow these steps on the web browser:

1. Go to our GitHub repository page. You will see a prominent yellow bar at the top saying: **"Compare & pull request"**. Click it.
2. Title your PR clearly and add a brief description of what you did.
3. On the right-hand side, assign your **Mentor** or a teammate under the **Reviewers** tab.
4. Click **Create pull request**.

> 💡 **Note on Merging:** The repository requires at least 1 approval before code can be merged. If your reviewer leaves line comments, resolve their feedback, push your updates directly to your feature branch, and they will automatically update the PR!

---

## 💻 Tech Stack & Getting Started

Make sure you have your virtual environment set up before installing the dependencies.

* **Core Frameworks:** PyTorch / TensorFlow
* **Quantum Toolkit:** PennyLane (for seamless classical-quantum integration)
* **Data Processing:** OpenCV, NumPy, Scikit-learn

### Initial Environment Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements (once requirements.txt is created)
pip install -r requirements.txt
```
