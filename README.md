# BizCardX: Extracting Business Card Data

Welcome to the **BizCardX** repository! This Python application is designed to extract information from business cards using various technologies such as Streamlit, EasyOCR, OpenCV, Regular Expressions (RegEx), and MySQL database integration.

# Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Workflow and Execution Overview](#project-workflow-and-execution-overview)
  - [Step 1: Upload Business Card Image](#step-1-upload-business-card-image)
  - [Step 2: Business Card Data Extraction](#step-2-business-card-data-extraction)
  - [Step 3: Data Checking and Database Upload (Optional)](#step-3-data-checking-and-database-upload-optional)
- [Database Navigation](#database-navigation)
  - [Database Record Display](#database-record-display)
  - [Image Selection by Company and Name](#image-selection-by-company-and-name)
  - [Update Database Data](#update-database-data)
  - [Delete Database Data](#delete-database-data)
- [Contact](#contact)
- [License](#license)

## Overview

The primary goal of BizCardX is to automate the extraction of critical details from business card images. These details include the individual's name, job title, company name, contact information, email, website, address, city, state, and pincode. The application leverages Optical Character Recognition (OCR) provided by EasyOCR to extract text from images.

## Features

- **Upload Business Card Image**: Upload a business card image (JPG, JPEG, or PNG).
- **Business Card Data Extraction**: Extract information from the uploaded image.
- **Database Integration**: Store extracted data in a MySQL database.
- **Database Navigation**: View, update, or delete records in the database.
- **Image Details**: View card details by selecting a specific company and name.
- **Data Modification**: Modify and update database records.
- **Data Deletion**: Delete records from the database.

# Project Workflow and Execution Overview
## Step 1: Upload Business Card Image
- Upload Business Card Image
- Click the Upload Business Card Image section.
- Upload an image of a business card in JPG, JPEG, or PNG format.
- The uploaded image will be displayed.
## Step 2: Business Card Data Extraction
- Click the EXTRACT DATA button to initiate text extraction.
- The application will use EasyOCR to extract text from the uploaded image.
- Extracted data will include Name, Designation, Company Name, Contact Information, Email, Website, Address, City, State, and Pincode.
- The extracted data will be displayed.
## Step 3: Data Checking and Database Upload (Optional)
- The application checks if the same combination of Name, Designation, and Company already exists in the database.
- If it's a new combination, the data is inserted into the database.
- If the combination already exists, the insertion is skipped.
## Database Navigation
- You can navigate to the Database section to view, update, or delete records in the database.
- Select the option from the menu to perform database operations.
## Database Record Display
- The Table option displays all the records present in the database.
- You can also download the data in CSV format.
## Image Selection by Company and Name
- The Image Details option allows you to view the image of card details.
- Select a specific company and name, then click SHOW IMAGE to view the image.
## Update Database Data
- In the Update data section, you can modify records present in the database.
- Select a company, name, and the specific column you want to update.
- Enter the new data and click UPDATE to save changes.
## Delete Database Data
- In the Delete data section, you can delete records from the database.
- Select a company, name, and click DELETE to remove the record.

# Contact
For any inquiries or support, please contact us at:
Email: divahar2896@gmail.com

# License
- Feel free to contribute, report issues, or provide suggestions to improve this project.


