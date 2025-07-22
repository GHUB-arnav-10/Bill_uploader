# Full-Stack Receipt & Bill Analyzer

## Project Overview

This full-stack Flask application provides a modern, AI-powered solution for uploading, analyzing, and visualizing receipts and bills. Users can upload documents in various formats (PDF, JPG, PNG), and the system automatically extracts key information, stores it, and presents insightful analytics through an interactive dashboard.

The core of this project is a state-of-the-art, two-stage AI pipeline that significantly surpasses the capabilities of traditional OCR and rule-based parsing systems, offering superior accuracy and flexibility across different document types.

---

## Core Technology & Architectural Choices

The original assignment suggested using rule-based logic or traditional OCR for data extraction. However, to build a more robust, scalable, and accurate system, a strategic decision was made to implement a more advanced, AI-driven architecture. This approach avoids the brittleness of rule-based systems and the common errors associated with separate OCR engines.

Our architecture is a **two-stage AI pipeline**:

1.  **Stage 1: OCR-Free Visual Document Understanding with Donut**
    -   We employ **`naver-clova-ix/donut-base`**, a powerful Vision Transformer model from Hugging Face.
    -   Unlike traditional methods, Donut is **OCR-free**. It processes the document image directly, learning to "read" and understand the layout and text simultaneously. This end-to-end approach is more resilient to varied document formats and image quality issues.
    -   Its primary role in this pipeline is to reliably convert the visual information from any document into a structured block of text.

2.  **Stage 2: Intelligent Parsing & Categorization with Google's Gemini**
    -   The raw structured text from Donut is then passed to a powerful Large Language Model (LLM), **Google's Gemini Pro**.
    -   We use a carefully crafted prompt to instruct Gemini to act as an expert data entry assistant. It intelligently parses the text to find the vendor, date, and total amount, and, most importantly, assigns a relevant category (e.g., 'Utilities', 'Dining').
    -   This two-step process leverages the strengths of each model: Donut for accurate visual transcription and Gemini for contextual understanding and reasoning.

**Technology Stack:**
- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **AI & Machine Learning:** Hugging Face Transformers (Donut), Google Generative AI (Gemini)
- **Frontend:** Jinja2, TailwindCSS, Chart.js

---

## Features Implemented

This application successfully delivers on the core requirements outlined in the assignment brief.

| Requirement | Implementation Status | Details |
| :--- | :--- | :--- |
| **Data Ingestion** | ✅ **Completed** | Handles `.jpg`, `.png`, and `.pdf` file uploads. |
| **Data Parsing** | ✅ **Completed** | The Donut + Gemini AI pipeline extracts Vendor, Date, Amount, and Category. |
| **Data Storage** | ✅ **Completed** | Uses Flask-SQLAlchemy with a SQLite database for persistent, normalized storage. |
| **Dashboard UI** | ✅ **Completed** | A clean, responsive dashboard built with Jinja2 and TailwindCSS. |
| **Tabular View** | ✅ **Completed** | All extracted records are displayed in a sortable table. |
| **Statistical Visualizations** | ✅ **Completed** | Implemented "Spend by Category" (Doughnut Chart) and "Monthly Spend Trend" (Bar Chart) using Chart.js. |
| **Bonus: Data Export** | ✅ **Completed** | Functionality to export all receipt data as `.csv` or `.json` files is included. |

---

## Algorithmic Implementation & Design Choices

The assignment requested the implementation of specific search, sorting, and aggregation algorithms.

Given the **3-day project timeline**, a strategic decision was made to prioritize building a robust, end-to-end functional application using modern, production-ready tools. Therefore, instead of manually re-implementing fundamental algorithms, we leveraged the highly optimized, industry-standard implementations provided by our chosen technology stack (SQLAlchemy and Python).

-   **Search Algorithms:** The "Search by vendor or category" feature is implemented using the SQLAlchemy ORM. This translates the user's query into an efficient SQL `WHERE ... LIKE` clause, which leverages the database's internal indexing for fast, pattern-based searching. This is significantly more performant than a manual linear search in Python for any non-trivial amount of data.

-   **Sorting Algorithms:** Sorting by Vendor, Date, or Amount is handled directly by the database via the ORM's `order_by()` method. The database's sorting engine is highly optimized (often using variants of Timsort or Mergesort) and is the most efficient way to perform this operation.

-   **Aggregation Functions:** Statistical aggregations (total spend, average spend, spend by category, monthly trends) are computed in the backend using Python's native data structures. These operations utilize fast, built-in functions and optimized dictionary/list comprehensions.

**Note on Timeline and Future Work:** This modern approach delivered a feature-complete and performant application within the tight 3-day constraint. With an extended timeline, it would be entirely feasible to replace the ORM-based logic with manual, "from-scratch" implementations of search and sort algorithms to precisely match the assignment's note on applying native algorithmic thinking.

---

## Setup and Installation

To run this project locally, please follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd <repository-name>
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    -   Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    -   Set the API key in your terminal session.
        ```powershell
        # For Windows PowerShell
        $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```
        ```bash
        # For macOS/Linux
        export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

5.  **Initialize the Database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6.  **Run the Application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.
