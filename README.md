# FILTERS OPTION
#### Demonstração em vídeo: <URL AQUI>
#### Descrição:

# 'Filters Option' - Web Application for Filtering and Analyzing Financial Options

## Market Context for Derivatives in Brazil
The derivatives market, particularly options, is one of the most complex and important in Brazil. Trading options requires analyzing large volumes of data quickly, involving underlying assets, expiration dates, exercise prices, and other variables. The platform developed by Adriana and Jober serves as a solution for professionals and investors seeking agility and precision in this environment. This project was designed to optimize a process that once took about 3 hours of manual work, reducing it to just a few seconds, saving valuable time and transforming the analysis and decision-making workflow.

## About the Application
This application focuses on filtering market data from options based on a spreadsheet provided by B3 (Brazilian Stock Exchange). The system automates data collection, pre-filtering, and provides this data to the end user, enhancing efficiency in analysis and preparation for financial operations.
This project was developed as part of the final submission for HarvardX’s CS50 course and meets all the complexity, functionality, and documentation requirements of the course.

## Key Features

### User Registration:
Users need to create a free account using email and password to access the platform.
The system ensures security with authentication managed by Werkzeug.

### Data Filtering:
Users can filter assets based on various criteria, including:
- Option type (Call or Put).
- Assets listed in IBOVESPA.
- Specific expiration dates.
- Weekly options.
Results can be downloaded in spreadsheet format for use in their financial operation platform.

### Automated Data Collection:
An automated routine uses Selenium and WebdriverEdge to fetch the initial spreadsheet directly from the B3 website.
This spreadsheet is pre-filtered by an internal system, not accessible to the end user, and stored locally for processing.

### User-Friendly Interface:
Developed with Flask, HTML, CSS, JavaScript, and Bootstrap, the front-end offers an intuitive and responsive experience.
The design incorporates technology and financial elements for an effective and streamlined user experience.

## Project Motivation
The application was designed to meet the needs of professionals like Jober, who operates in the derivatives market. His direct experience inspired the creation of a tool that solves real problems, saving time and reducing the need for intensive manual work. This system delivers fast and reliable results, significantly enhancing workflow efficiency.

## Project Architecture
The application was built using various technologies and libraries, each playing a crucial role:
- Python and Flask: Business logic and web application development.
- SQL and SQLite: Database management for storing user information.
- Jinja: Dynamic HTML page generation.
- HTML, CSS, Bootstrap: Creation of a responsive and user-friendly interface.
- JavaScript: Interactive features on the user interface.
- Selenium and WebdriverEdge: Automation for data collection directly from B3’s website.
- Werkzeug: Secure authentication and session management.

## File Structure
- app.py: The main file containing Flask business logic and endpoints.
- templates/: Contains dynamically rendered HTML files with Jinja.
- static/: Directory for CSS files and images.
- users.db: SQLite file for managing user data and settings.
- extract_b3_data.py: Script that automates downloading the B3 spreadsheet.
- data_processing.py: Script for pre-filtering the B3 spreadsheet.
- downloads/: Contains downloaded spreadsheets.
- requirements.txt: List of project dependencies.
- README.md: This document explaining the project.

## Design Decisions

### Local Spreadsheet Storage:
Since the system is not hosted on a server, the initial B3 spreadsheet is stored locally. This decision was made to facilitate development and testing.

### Secure Registration:
Basic authentication using email and password ensures that only registered users have access to filtered data.

### Separated Data Filtering:
The pre-filtering routine is kept separate from user access, prioritizing simplicity in the front-end and efficiency in the back-end.

### Git Utilization:
The entire development process was managed using Git, facilitating information sharing among developers and ensuring efficient version control.

### Support from ChatGPT:
ChatGPT was used to correct errors and explore alternatives, contributing to the overall quality of the final project.

## How to Run the Project

- Clone the repository:
git clone <repository-link>

- Install dependencies:
pip install -r requirements.txt

- Adjust local machine paths.

- Run the application:
flask run

- Access the system via your web browser.

## Conclusion
This project demonstrates the application of advanced programming and automation concepts to solve real-world problems in the financial market. Developed with a focus on performance, security, and user-friendliness, the application meets all the requirements of the CS50 course and reflects the team’s learning and dedication throughout the process. We are confident that this solution can have a positive impact on the workflows of professionals in the derivatives sector.
