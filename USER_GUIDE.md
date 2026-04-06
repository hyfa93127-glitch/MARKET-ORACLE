# 🟢 User Guide: How to Run the Stock Predictor

This guide is designed for users who want to use the dashboard without needing to write code. Follow these **3 simple steps** to get started.

---

## Step 1: Install Python (First Time Only)
To run this project, your computer needs **Python**.
1.  Go to [python.org/downloads](https://www.python.org/downloads/).
2.  Download the latest version for Windows.
3.  **IMPORTANT**: During installation, make sure to check the box: **"Add Python to PATH"**.
4.  Click **"Install Now"** and wait for it to finish.

---

## Step 2: One-Click Start
I have included a file called `run_app.bat` in the project folder. This file automates everything for you.

1.  Open the project folder on your computer.
2.  Find the file named **`run_app.bat`**.
3.  **Double-click it**.
4.  A black window (Command Prompt) will open. It will automatically:
    -   Install the required software libraries.
    -   Fetch the latest stock market prices.
    -   Train the AI models.
    -   Launch the Dashboard.

---

## Step 3: Using the Dashboard
Once the process finishes, your web browser will automatically open to a page like **`http://localhost:8501`**.

-   **Sidebar (Left)**: Choose which stock you want to see (e.g., Apple, NVIDIA).
-   **Investment Budget**: Type in how much money you want to invest and click **"Calculate Portfolio"**.
-   **Tabs**:
    -   **Technical Data**: See the raw numbers.
    -   **Upcoming Events**: See when the next earnings report is due.
    -   **Portfolio Allocator**: See exactly how many shares the AI suggests you buy.

---

### ⚠️ Troubleshooting
- **Black window closes immediately?** Right-click `run_app.bat`, select "Edit", and ensure Python was installed correctly in Step 1.
- **Data looks old?** Close the dashboard and run `run_app.bat` again to fetch the latest market prices.
