# Project Overview

## Introduction
This project is a comprehensive solution that includes a backend for statistical extraction, language correction and detection, validation of results, and a frontend with a chatbot for text input and specific result requests, as well as a dashboard for visualizing results with appropriate graphs.

## Backend

### Statistical Extraction
- **Tool Used**: Claude
- **Description**: Claude is used for extracting statistical data from various sources. It processes raw data and extracts meaningful statistics that are used in the project.

### Language Correction and Detection
- **Tool Used**: Llama
- **Description**: Llama is employed for language correction and detection. It ensures that the input text is grammatically correct and identifies the language of the input text.
- **Weakness**: Llama sometimes does not provide accurate results, which can affect the overall quality of the language correction and detection.

### Validation of Results
- **Description**: The results obtained from Claude and Llama are validated to ensure accuracy and reliability. This step is crucial to maintain the integrity of the data and the results presented to the users.

### Weakness of SpaCy
- **Description**: SpaCy is a powerful NLP tool, but it struggles with extracting complex information from text, which can limit its effectiveness in certain applications.

## Frontend

### Chatbot
- **Description**: The chatbot allows users to input text and request specific results. It interacts with the backend to process the input and retrieve the necessary information.
- **Screenshot**:
  ![Chatbot Screenshot](path/to/chatbot_screenshot.png)

### Dashboard
- **Description**: The dashboard provides a visual representation of the results. It includes various graphs and charts to help users understand the data better.
- **Screenshot**:
  ![Dashboard Screenshot](path/to/dashboard_screenshot.png)

## Steps to Run the Project

1. **Clone the Repository**
    ```bash
    git clone https://github.com/ayman-fdl/french-grammar-stats.git
    cd french-grammar-stats
    ```

2. **Set Up a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Django Project**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Contributors

This project was developed by:
- Ait Mouhamed Firdaous
- Fadili Aymane
- Bouragaa Hamza

Supervised by:
- Mohamed Amine Chadi

## Conclusion
This project integrates advanced tools and technologies to provide a seamless experience for users. The backend ensures accurate data processing and validation, while the frontend offers an interactive and user-friendly interface for data input and visualization.