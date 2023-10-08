# Importing the necessary modules
import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
import easyocr
import cv2
import re
import pandas as pd
import numpy as np
import time
from PIL import Image

# =======================================Constants======================================================================

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "business_cards",
}


# ========================================Database Connection Function =================================================
# Function to establish a database connection
def connect_to_database():
    # Connect to the MySQL database with the specified credentials
    mydb = mysql.connector.connect(**DATABASE_CONFIG)
    mycursor = mydb.cursor()
    # Create the 'card_data' table if it doesn't already exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS card_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            designation VARCHAR(255),
            company VARCHAR(255),
            contact VARCHAR(255),
            email VARCHAR(255),
            website VARCHAR(255),
            address VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            pincode VARCHAR(255),
            image LONGBLOB,
            UNIQUE KEY unique_name_designation_company (name, designation, company)
        )
    """)
    return mydb, mycursor


# ===================================== Streamlit Page Configuration Function===========================================
# Function to Configure Streamlit Page
def configure_streamlit_page():
    # Load the application icon
    icon = Image.open("C:\\Users\\DIVAHAR\\PycharmProjects\\P18_1\\biz_card\\images\\icon.png")
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="BizCardX",  # Set the page title
        page_icon=icon,  # Set the page icon using the loaded image
        layout="wide"  # Set the layout style to "wide"
    )

    # Display a centered header with a specified title and styling
    st.markdown("<h1 style='text-align: center; color: white;'>BizCardX: Extracting Business Card Data</h1>",
                unsafe_allow_html=True)


# ============================================ Home Section Function====================================================
# Function to Display Home Section Content
def home_section():
    # Create two columns for content layout
    left, right = st.columns(2)
    with left:
        # Display a welcome message and application description
        st.write("### Welcome to the Business Card Application!")
        st.write(
            '#### BizCardX is a Python application crafted to extract information from business cards. It extracts the information in Business Card Image stores it in database,allows user to view records ,card image, update data and delete the records in the database.  ')
        st.write(
            '##### The primary objective of BizCardX is to automate the extraction of critical details from business card images. These details encompass the individuals name, job title, company name, contact information, and other pertinent data. By leveraging the capabilities of Optical Character Recognition (OCR) provided by EasyOCR, BizCardX excels in extracting text from images.')
        st.write("Click on the ****:red[Extract and Upload]**** option to start exploring the Bizard extraction.")
        st.write('### TECHNOLOGIES USED :')
        st.write(
            '##### :red[Python], :red[Streamlit],  :red[EasyOCR],  :red[OpenCV],  :red[MySQL],  :red[RegEx],  :red[OpenCV]')
    with right:
        # Load and display the business card image
        icon_1 = Image.open("C:\\Users\\DIVAHAR\\PycharmProjects\\P18_1\\biz_card\\images\\card.png")
        # Display the business card  image using st.image
        st.image(icon_1, use_column_width=True)


# ================================== Extract and Upload Section Function ===============================================
# Function for the Extract and Upload Section
def extract_and_upload_section(mydb, mycursor):
    # Create two columns for content layout
    file, text = st.columns([2.5, 3])
    with file:
        # Display the "Upload Business Card Image" section
        st.header("Step 1: Upload Business Card Image")
        uploaded_file = st.file_uploader("Upload an Image of a Business Card", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            # Read the uploaded image file
            file_bytes = uploaded_file.read()
            # Display the original image
            np_arr = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            st.image(image, channels='BGR', use_column_width=True)

    # =======================Data Extract and upload to Database ===================================================
    with text:
        # Display the "Business Card Data Extraction" section
        st.header("Step 2: Business Card Data Extraction")
        st.subheader("Data Extraction and Uploading to Database")
        st.markdown(
            "###### *Press below :red[EXTRACT DATA] button to view structured text format & upload the extracted data to the database Using :blue[easyOCR] & :blue[python regular expression]*")
        st.write(
            'Please note: This will work only for :blue[business card image] alone; it will not work with other images')
        # Check if the "EXTRACT DATA" button is clicked
        if st.button('EXTRACT DATA'):
            if uploaded_file is None:
                st.warning(
                    "Please upload an image before extracting data.")  # Display a warning if no image is uploaded
            else:
                with st.spinner('Extracting text...'):
                    # Use EasyOCR to perform text extraction from the image
                    reader = easyocr.Reader(['en'])
                    results = reader.readtext(image)
                    card_info = [i[1] for i in results]
                    demilater = ' '
                    card = demilater.join(card_info)
                    replacement = [
                        (";", ""),
                        (',', ''),
                        ("WWW ", "www."),
                        ("www ", "www."),
                        ('www', 'www.'),
                        ('www.', 'www'),
                        ('wwW', 'www'),
                        ('wWW', 'www'),
                        ('.com', 'com'),
                        ('com', '.com'),
                    ]
                    for old, new in replacement:
                        card = card.replace(old, new)

                    # =========================== Phone Extraction ====================================================
                    ph_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
                    ph = re.findall(ph_pattern, card)
                    Phone = ''
                    for num in ph:
                        Phone = Phone + ' ' + num
                        card = card.replace(num, '')

                    # ========================== Email Extraction ======================================================
                    mail_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
                    mail = re.findall(mail_pattern, card)
                    Email_id = ''
                    for ids in mail:
                        Email_id = Email_id + ids
                        card = card.replace(ids, '')

                    # ============================ Website Extraction===================================================
                    url_pattern = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
                    url = re.findall(url_pattern, card)
                    URL = ''
                    for web in url:
                        URL = URL + web
                        card = card.replace(web, '')

                    # =========================== Pincode Extraction====================================================
                    pin_pattern = r'\d+'
                    match = re.findall(pin_pattern, card)
                    Pincode = ''
                    for code in match:
                        if len(code) == 6 or len(code) == 7:
                            Pincode = Pincode + code
                            card = card.replace(code, '')

                    # =========================== Name, Designation, Company Extraction ================================
                    name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
                    name_data = []
                    for i in card_info:
                        if re.findall(name_pattern, i):
                            if i not in 'WWW':
                                name_data.append(i)
                                card = card.replace(i, '')
                    name = name_data[0]
                    designation = name_data[1]

                    if len(name_data) == 3:
                        company = name_data[2]
                    else:
                        company = name_data[2] + ' ' + name_data[3]
                    card = card.replace(name, '')
                    card = card.replace(designation, '')

                    # ===========================  City, State, Address Extraction =====================================
                    new = card.split()
                    if new[4] == 'St':
                        city = new[2]
                    else:
                        city = new[3]
                    if new[4] == 'St':
                        state = new[3]
                    else:
                        state = new[4]
                    if new[4] == 'St':
                        s = new[2]
                        s1 = new[4]
                        new[2] = s1
                        new[4] = s
                        Address = new[0:3]
                        Address = ' '.join(Address)
                    else:
                        Address = new[0:3]
                        Address = ' '.join(Address)

                    # Display extracted data
                    st.write('')
                    st.write('###### :red[Name]         :', name)
                    st.write('###### :red[Designation]  :', designation)
                    st.write('###### :red[Company name] :', company)
                    st.write('###### :red[Contact]      :', Phone)
                    st.write('###### :red[Email id]     :', Email_id)
                    st.write('###### :red[URL]          :', URL)
                    st.write('###### :red[Address]      :', Address)
                    st.write('###### :red[City]         :', city)
                    st.write('###### :red[State]        :', state)
                    st.write('###### :red[Pincode]      :', Pincode)

                    # ================== Data Checking and insertion into Database =====================================

                    # Check if a record with the same combination of name, designation, and company exists in the
                    # database. This query searches for an existing record in the 'card_data' table with matching
                    # 'name', 'designation', and 'company' values. if extracted and record in database is same it will
                    # skip insertion of data into database

                    # ======================================= Data Checking ============================================
                    # Check if a record with the same combination of name, designation, and company exists in the database.
                    check_query = """
                        SELECT id FROM card_data
                        WHERE name = %s AND designation = %s AND company = %s 
                    """
                    mycursor.execute(check_query, (name, designation, company))
                    existing_record = mycursor.fetchone()

                    # ================== Data insertion into Database===================================================
                    # Insert data into the database if no existing record found
                    if existing_record is None:
                        sql = "INSERT INTO card_data (name,designation,company,contact,email,website,address,city,state,pincode,image) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val = (
                            name, designation, company, Phone, Email_id, URL, Address, city, state, Pincode,
                            file_bytes)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success('Text extracted & successfully uploaded to the database', icon="☑️")
                    else:
                        st.warning("Record with the same combination already exists. Skipping insertion.")


# =================================== Database Navigation Function =====================================================
# Function to Handle Database Navigation
def database_navigation(mydb, mycursor):
    # Add a spinner to indicate connecting to the database
    with st.spinner('Connecting...'):
        time.sleep(1)
    # Create an option menu for database navigation
    with navigation:
        option = option_menu(None, ['Table', 'Image Details', "Update data", "Delete data"],
                             icons=["list-task", "image", "pencil-fill", 'exclamation-diamond'], default_index=0)
    # Based on the selected option, navigate to the corresponding database operation
    if option == 'Table':
        # Display the table containing card data from the database
        database_table_display(mycursor)
    elif option == 'Image Details':
        # Display details of images stored in the database
        database_image_details(mycursor)
    elif option == 'Update data':
        # Allow users to update data in the database
        database_update_data(mydb, mycursor)
    elif option == 'Delete data':
        # Allow users to delete data from the database
        database_delete_data(mydb, mycursor)


# ================================= Display Database Table Function ====================================================
# Function to Display Database Table
def database_table_display(mycursor):
    # Set the header and subheader for the database record display
    st.header("Database Record Display")
    st.subheader("Displaying all the records present in the database")

    # Execute a SQL query to fetch all records from the 'card_data' table
    mycursor.execute("SELECT * FROM card_data")
    myresult = mycursor.fetchall()

    # Convert the fetched records into a DataFrame using pandas
    df = pd.DataFrame(myresult,
                      columns=['id', 'Name', 'Designation', 'Company', 'Contact', 'Email', 'Website', 'Address',
                               'City', 'State', 'Pincode', 'Card Image'])

    # Set the 'id' column as the DataFrame index and drop it from the displayed table
    df.set_index('id', drop=True, inplace=True)

    # Display the DataFrame in Streamlit as a table
    st.dataframe(df, width=0)

    # Provide an option to download the data in CSV format
    # Create a copy of the DataFrame without the 'Card Image' column (only image details in binary)
    df_without_image = df.drop(columns=['Card Image'])

    # Generate a CSV download button with the data from the DataFrame
    download_button_str = df_without_image.to_csv(index=False, encoding='utf-8')
    st.subheader("Bellow button helps to Download the above  Data in CSV format")
    st.write("Please note: :red['Card Image'] column information wont be available in the downloaded file." )
    st.download_button(
        label="Download Data",
        data=download_button_str,
        file_name="bizcard_data.csv",
        key="download_csv",
    )


# ======================== Display Database Image Details Function ====================================================
# Function to Display Image Details
def database_image_details(mycursor):
    # Set the header and subheader for image selection by company and name
    st.header("Image Selection by Company and Name")
    st.subheader("""
                    This feature allows you to view the image of card detail. 
                    Select the company and name to see the image of the selected choice. 
                    Click 'SHOW IMAGE' to view the image.
                """)

    # Create two columns for layout
    left, right = st.columns([1.5, 3])

    with left:
        # Execute a SQL query to fetch distinct company names from the 'card_data' table
        mycursor.execute("SELECT DISTINCT company FROM card_data")
        companies = [row[0] for row in mycursor.fetchall()]

        # Display the selection box for choosing a company
        selected_company = st.selectbox("Select company", companies)

        # Execute a SQL query to fetch names based on the selected company
        mycursor.execute("SELECT name FROM card_data WHERE company = %s", (selected_company,))
        names = [row[0] for row in mycursor.fetchall()]

        # Display the selection box for choosing a name based on the selected company
        selection_name = st.selectbox("Select name", names)

        if st.button('SHOW IMAGE'):
            with right:
                # SQL query to fetch the image data for the selected name and company
                sql = "SELECT image FROM card_data WHERE name = %s AND company = %s"
                mycursor.execute(sql, (selection_name, selected_company))
                result = mycursor.fetchone()

                # Check if image data exists
                if result is not None:
                    # Retrieve the image data from the result
                    image_data = result[0]
                    # Create a file-like object from the image data
                    np_arr = np.frombuffer(image_data, np.uint8)
                    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    # Display the image in Streamlit
                    st.image(image, channels="BGR", use_column_width=True)
                else:
                    st.error("Image not found for the given name and company.")


# ===================================  Update Database Data Function ===================================================
# Function to Update Database Records
def database_update_data(mydb, mycursor):
    # Set the header and subheader for database record modification
    st.header("Database Record Modification")
    st.subheader("""
        This feature allows you to update and modify records present in the database. 
        Select a specific company name and name to update, and enter the new data for the selected record. 
        Click 'UPDATE' to save your changes.
    """)

    # Get the list of distinct companies from the database
    mycursor.execute("SELECT DISTINCT company FROM card_data")
    companies = [row[0] for row in mycursor.fetchall()]

    # Display the selection box for choosing a company
    selected_company = st.selectbox("Select company", companies)

    if selected_company:
        # Get names related to the selected company
        mycursor.execute("SELECT DISTINCT name FROM card_data WHERE company = %s", (selected_company,))
        names = [row[0] for row in mycursor.fetchall()]

        # Display the selection box for choosing a name based on the selected company
        selection_name = st.selectbox("Select name", names)

        if selection_name:
            # Get all available columns for updating
            mycursor.execute("SHOW COLUMNS FROM card_data")
            columns = [i[0] for i in mycursor.fetchall()]

            # Display the selection box for choosing a specific column to update
            selection = st.selectbox("Select specific column to update", columns)

            if selection:
                # Retrieve the current value of the selected column for the chosen name
                mycursor.execute(f"SELECT {selection} FROM card_data WHERE name = %s", (selection_name,))
                current_value = mycursor.fetchone()[0]

                # Display the current value of the selected column
                st.markdown(f"**Current {selection}: {current_value}**")

                # Allow the user to input the new data for the selected column
                new_data = st.text_input(f"Enter the new {selection}")

                if st.button("UPDATE"):
                    # SQL query to update the selected column with the new data
                    sql = f"UPDATE card_data SET {selection} = %s WHERE name = %s"

                    # Execute the SQL query with the new data and name
                    mycursor.execute(sql, (new_data, selection_name,))
                    mydb.commit()
                    st.success("Updated successfully", icon="👆")


# =============================== Delete Database Data Function ========================================================
# Function to Delete Database Records
def database_delete_data(mydb, mycursor):
    # Set the header and subheader for database record deletion
    st.header("Delete Database Records")
    st.subheader("""
                    This feature allows you to delete records present in the database.
                    Select a specific company and name to delete the record. Click 'DELETE' to save your changes.
                """)

    # Get the list of distinct companies from the database
    mycursor.execute("SELECT DISTINCT company FROM card_data")
    companies = [row[0] for row in mycursor.fetchall()]

    # Display the selection box for choosing a company
    selected_company = st.selectbox("Select company", companies)

    if selected_company != "Select an Option":
        # Get names related to the selected company
        mycursor.execute("SELECT DISTINCT name FROM card_data WHERE company = %s", (selected_company,))
        names = [row[0] for row in mycursor.fetchall()]

        # Display the selection box for choosing a name to delete
        selection_name = st.selectbox("Select name to delete", names)

        if selection_name:
            if st.button("DELETE"):
                # Define the SQL query to delete the selected data
                sql = "DELETE FROM card_data WHERE name = %s AND company = %s"
                # Execute the query with the selected name and company
                mycursor.execute(sql, (selection_name, selected_company))
                # Commit the changes to the database
                mydb.commit()
                st.success("Deleted successfully", icon="✅")


# Main Function
if __name__ == "__main__":
    # Connect to the database and obtain a database connection and cursor
    mydb, mycursor = connect_to_database()

    # Configure the Streamlit page settings
    configure_streamlit_page()

    # Create two columns for navigation and text processing
    navigation, text_process = st.columns([1.2, 5])

    with navigation:
        # Create a dropdown menu for selecting the main menu option
        selected = option_menu('Main Menu', ['Home', "Extract and Upload", "Database"],
                               icons=["house", 'cloud-upload', 'gear'], default_index=0)

    with text_process:
        # Based on the selected option, call the appropriate function
        if selected == 'Home':
            home_section()
        elif selected == 'Extract and Upload':
            extract_and_upload_section(mydb, mycursor)
        elif selected == 'Database':
            database_navigation(mydb, mycursor)

# ========================================== End Of Application =======================================================
