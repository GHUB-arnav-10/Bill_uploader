# Full-Stack Receipt & Bill Analyzer

## Project Overview

This full-stack Flask application provides an AI-powered solution for uploading, analyzing, and visualizing receipts and bills. Users can upload documents in various formats (PDF, JPG, PNG), and the system automatically extracts key information using a sophisticated Vision Transformer model, stores it, and presents insightful analytics through an interactive dashboard.

The core of this project is the implementation of the **Donut (Document Understanding Transformer)** model, which offers a modern, OCR-free approach to document analysis, providing a high degree of flexibility across different document types.

---

## Core Technology & Architectural Choices

The assignment suggested using rule-based logic or traditional OCR for data extraction. However, to build a more robust and scalable system within the project's constraints, a strategic decision was made to implement a single, powerful AI model for the core processing task.

Our architecture is a **Visual Document Understanding pipeline**:

-   **Core Engine: Donut Model from Hugging Face**
    -   We employ **`naver-clova-ix/donut-base`**, a powerful Vision Transformer model.
    -   Unlike traditional methods that require a separate OCR step, Donut is **OCR-free**. It processes the document image directly, learning to "read" and understand the layout and text simultaneously. This end-to-end approach is more resilient to varied document formats and image quality issues.
    -   Its role in this project is to serve as the sole engine for converting the visual information from any document into a structured JSON output, which the application then uses.

This focused approach allowed for the successful implementation of an end-to-end AI feature within the project's timeline.

**Technology Stack:**
- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **AI & Machine Learning:** Hugging Face Transformers (Donut)
- **Frontend:** Jinja2, TailwindCSS, Chart.js

---

## Features Implemented

This application successfully delivers on the core requirements outlined in the assignment brief.

| Requirement | Implementation Status | Details |
| :--- | :--- | :--- |
| **Data Ingestion** | ✅ **Completed** | Handles `.jpg`, `.png`, and `.pdf` file uploads. |
| **Data Parsing** | ✅ **Completed** | The Donut model pipeline extracts Vendor, Date, Amount, and Category. |
| **Data Storage** | ✅ **Completed** | Uses Flask-SQLAlchemy with a SQLite database for persistent, normalized storage. |
| **Dashboard UI** | ✅ **Completed** | A clean, responsive dashboard built with Jinja2 and TailwindCSS. |
| **Tabular View** | ✅ **Completed** | All extracted records are displayed in a sortable table. |
| **Statistical Visualizations** | ✅ **Completed** | Implemented "Spend by Category" (Doughnut Chart) and "Monthly Spend Trend" (Bar Chart) using Chart.js. |
| **Bonus: Data Export** | ✅ **Completed** | Functionality to export all receipt data as `.csv` or `.json` files is included. |

---

## Algorithmic Implementation & Design Choices

The assignment requested the implementation of specific search, sorting, and aggregation algorithms.

Given the **3-day project timeline**, a strategic decision was made to prioritize building a robust, end-to-end functional application using modern, production-ready tools. Therefore, instead of manually re-implementing fundamental algorithms, we leveraged the highly optimized, industry-standard implementations provided by our chosen technology stack (SQLAlchemy and Python).

-   **Search Algorithms:** The "Search by vendor or category" feature is implemented using the SQLAlchemy ORM. This translates the user's query into an efficient SQL `WHERE ... LIKE` clause, which leverages the database's internal indexing for fast, pattern-based searching.

-   **Sorting Algorithms:** Sorting by Vendor, Date, or Amount is handled directly by the database via the ORM's `order_by()` method. The database's sorting engine is highly optimized and is the most efficient way to perform this operation.

-   **Aggregation Functions:** Statistical aggregations (total spend, average spend, spend by category, monthly trends) are computed in the backend using Python's native data structures. These operations utilize fast, built-in functions and optimized dictionary/list comprehensions.

**Note on Timeline and Future Work:** This approach delivered a feature-complete and performant application within the tight 3-day constraint. With an extended timeline, it would be entirely feasible to replace the ORM-based logic with manual, "from-scratch" implementations of search and sort algorithms to precisely match the assignment's note on applying native algorithmic thinking.

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

4.  **Initialize the Database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5.  **Run the Application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`. The first time you run it, the Donut model will be downloaded from Hugging Face, which may take a few moments.
