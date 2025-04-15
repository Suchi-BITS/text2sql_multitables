from dotenv import load_dotenv
import os
import streamlit as st
from groq import Groq

load_dotenv()
api = os.getenv("GROQ_API_KEY")

# --- Streamlit Setup ---
st.set_page_config(page_title="SQL Query Generator", layout="centered")
st.title("Natural Language to SQL Generator")
print("reloading...")

st.markdown("""
There are four tables in the database:

- **Customer Table**: Customer_ID, First_Name, Last_Name, Email_ID, Age, Phone, Created_At  
- **Flights Table**: Flight_ID, Origin, Destination, Departure_Date, Arrival_Date, Carrier, Price  
- **Reservations Table**: Reservations_ID, Customer_ID, Flight_ID, Reservation_DateTime, Status  
- **Transactions Table**: Transaction_ID, Reservation_ID, Amount, Transaction_DateTime  
""")

# --- Table Metadata Descriptions ---
Customer = """
Table: Customer
Columns:
- Customer_ID: an integer representing the unique ID of a customer.
- First_Name: a string containing the first name of the customer.
- Last_Name: a string containing the last name of the customer.
- Email_ID: a string representing the customer's email id.
- Age: an integer containing customer's age.
- Phone: a string for the customer's contact number.
- Created_At: a date representing the creation date of the customer.
"""

Flights = """
Table: Flights
Columns:
- Flight_ID: an integer representing the unique ID of a Flight.
- Origin: a string containing the origin of the flight.
- Destination: a string containing the destination of the flight.
- Departure_Date: a date representing the flight's departure.
- Arrival_Date: a date representing the flight's arrival.
- Carrier: a string representing the airline carrier.
- Price: a float representing the ticket price.
"""

Reservations = """
Table: Reservations
Columns:
- Reservations_ID: an integer representing the unique ID of the reservation.
- Customer_ID: a string referencing the Customer_ID from the Customer table.
- Flight_ID: a string referencing the Flight_ID from the Flights table.
- Reservation_DateTime: a datetime for when the reservation was made.
- Status: a string representing the reservation status.
"""

Transactions = """
Table: Transactions
Columns:
- Transaction_ID: an integer representing the unique ID of the transaction.
- Reservation_ID: a string referencing the Reservations_ID from the Reservations table.
- Amount: a float representing the payment amount.
- Transaction_DateTime: a datetime for when the transaction occurred.
"""

# --- Combine Metadata ---
def get_combined_metadata():
    return "\n\n".join([Customer, Flights, Reservations, Transactions])

# --- Prompt Creator for Multi-table SQL ---
def create_prompt(user_query, full_metadata):
    system_prompt = """
    You are a SQL query generator that can handle multiple tables.

    Your task is to:
    - Interpret the user's intent
    - Use the provided metadata
    - Perform JOIN operations across tables where necessary
    - Generate correct and optimized SQL
    - Use standard SQL syntax

    Rules:
    - Use only the tables and columns defined in metadata.
    - Include JOINs only when needed.
    - Filter, sort, or aggregate as per user intent.
    - Return the output in ONE single-line SQL query.
    - Do NOT return anything other than the SQL query.
    """

    user_prompt = f"""
    User Query: {user_query}
    Table Metadata:
    {full_metadata}
    """
    return system_prompt, user_prompt

# --- SQL Generator using Groq ---
def generate_output(system_prompt, user_prompt):
    client = Groq(api_key=api)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama3-70b-8192",
    )
    res = chat_completion.choices[0].message.content.strip()
    return res if res.lower().startswith("select") else "❌ Couldn't generate a valid SQL query."

# --- Main UI ---
st.markdown("### Enter your natural language query below:")

user_query = st.text_input("Natural Language Query", placeholder="e.g., Show all customers who booked a flight to New York")

if st.button("Generate SQL"):
    if not user_query:
        st.warning("Please enter a query first.")
    else:
        with st.spinner("🔄 Generating SQL query..."):
            metadata = get_combined_metadata()
            system_prompt, user_prompt = create_prompt(user_query, metadata)
            output = generate_output(system_prompt, user_prompt)
            st.success("✅ SQL Query Generated:")
            st.code(output, language="sql")
