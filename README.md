# Sakshi_30170
My DBDW assistant
Custom Gem
Financial Portfolio Tracker
A personal financial portfolio tracker that allows an individual to track their investments, monitor portfolio performance, and analyze asset allocation.

Key Features
User & Asset Management: A single-user application to manage profiles and link multiple financial accounts.

Portfolio Tracking: Users can view the real-time value, gains, and losses for individual assets and the entire portfolio.

Analysis & Reporting: Provides a breakdown of holdings by asset class and generates performance reports over time.

Transactions: Logs transactions such as buying, selling, and dividend payouts.

Database Schema
The application's data is stored in a PostgreSQL database. The schema is designed to support the functional requirements and includes the following tables:

users: Stores user profile information.

accounts: Links financial accounts to a user.

assets: Stores details of all assets held in various accounts.

transactions: Logs all financial transactions, such as buys and sells.

market_data: Records historical and current market prices for each asset.

Code Structure
The application code is split into a frontend and a backend file, promoting a clear separation of concerns.

frontend_fin.py: Manages the user interface and interactions using the Streamlit library. It displays data, forms for input, and triggers backend functions.

backend_fin.py: Contains the core logic for database operations using the psycopg2 library. This file includes functions for Create, Read, Update, and Delete (CRUD) operations, as well as business insights queries.

Getting Started
Set up the PostgreSQL database: Execute the provided SQL script to create the necessary tables.

Configure the backend: Update the database connection details (DB_NAME, DB_USER, DB_PASS, DB_HOST) in backend_fin.py.

Install dependencies:

Bash

pip install streamlit psycopg2-binary pandas
Run the application:

Bash

streamlit run frontend_fin.py
Business Insights
The application includes a dedicated section for business insights, powered by SQL aggregate functions like COUNT, SUM, AVERAGE, MIN, and MAX. This allows users to gain a deeper understanding of their portfolio's performance and asset allocation.
