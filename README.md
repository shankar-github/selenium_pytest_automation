### Automated Testing with Selenium and pytest

This project contains automated tests for testing the functionality of a web application using Selenium and pytest. 
It includes test cases for the Contact Us page of the web application.

### Prerequisites

Before running the tests, ensure you have the following installed:

- Python 3.x
- Pip (Python package manager)

### Installation

1. Clone this repository to your local machine:

    ```bash
    
    git clone <repository-url>

    ```

2. Navigate to the project directory:

    ```bash
    
    cd <project-directory>

    ```

3. Install the required Python packages using pip:

    ```bash
    
    pip install -r requirements.txt

    ```

### Running all tests and generating reports using Allure

To run all tests and generate reports using Allure, you can follow these steps:

1. Ensure you have installed Allure command-line tool by following the instructions [here](https://docs.qameta.io/allure/).

2. Navigate to the project directory in your terminal.

3. Run the following command:

    ```bash
    
    python -m pytest --alluredir allure-results

    ```

This command will execute all tests and generate XML files in the allure-report directory, which is the default output directory for Allure reports.

4. After the tests have finished running, generate the HTML report by running the following command:

    ```bash
    
    serve allure-results

    ```
Replace allure-results with the path to the directory specified in the outputFolder setting of the reporter.This command will generate and serve an HTML report based on the XML files generated in the allure-report directory. You can view the report in your web browser by clicking on the provided URL.

### Running a single test file

5. To run a specific test file using pytest, you can use the following command:

    ```bash
    
    pytest path/to/test_file.py

    ```

Replace `path/to/test_file.py` with the actual path to your test file. This command will execute only the tests defined in the specified file.

