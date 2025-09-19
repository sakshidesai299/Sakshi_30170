import psycopg2
import pandas as pd
from datetime import date
from decimal import Decimal

# Database connection details
DB_NAME = "Financial Portfolio Tracker"
DB_USER = "postgres"
DB_PASS = "Sakshi@299"
DB_HOST = "localhost"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn

# === CRUD Operations ===

# --- CREATE ---
def create_user(first_name, last_name, email):
    """Creates a new user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING user_id;", 
                    (first_name, last_name, email))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def create_account(user_id, account_name, account_type):
    """Creates a new financial account for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO accounts (user_id, account_name, account_type) VALUES (%s, %s, %s) RETURNING account_id;", 
                    (user_id, account_name, account_type))
        account_id = cur.fetchone()[0]
        conn.commit()
        return account_id
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating account: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def create_asset(account_id, ticker, name, asset_class):
    """Adds a new asset to an account."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO assets (account_id, ticker_symbol, asset_name, asset_class) VALUES (%s, %s, %s, %s) RETURNING asset_id;", 
                    (account_id, ticker, name, asset_class))
        asset_id = cur.fetchone()[0]
        conn.commit()
        return asset_id
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating asset: {e}")
        return None
    finally:
        cur.close()
        conn.close()
    
# --- READ ---
def get_user(user_id):
    """Retrieves a user's details."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_all_assets_for_user(user_id):
    """Retrieves all assets for a given user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.asset_id, a.ticker_symbol, a.asset_name, a.asset_class, ac.account_name
        FROM assets a
        JOIN accounts ac ON a.account_id = ac.account_id
        WHERE ac.user_id = %s;
    """, (user_id,))
    assets = cur.fetchall()
    cur.close()
    conn.close()
    return assets

# --- UPDATE ---
def update_user_email(user_id, new_email):
    """Updates a user's email address."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET email = %s WHERE user_id = %s;", (new_email, user_id))
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error updating email: {e}")
        return False
    finally:
        cur.close()
        conn.close()

# --- DELETE ---
def delete_asset(asset_id):
    """Deletes an asset and all associated transactions."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM assets WHERE asset_id = %s;", (asset_id,))
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error deleting asset: {e}")
        return False
    finally:
        cur.close()
        conn.close()

# === Business Insights ===
def get_total_portfolio_value(user_id):
    """Calculates the total market value of a user's portfolio."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(t.shares_quantity * md.closing_price)
        FROM transactions t
        JOIN assets a ON t.asset_id = a.asset_id
        JOIN accounts ac ON a.account_id = ac.account_id
        JOIN market_data md ON a.asset_id = md.asset_id
        WHERE ac.user_id = %s;
    """, (user_id,))
    total_value = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total_value if total_value is not None else Decimal('0.00')

def get_asset_allocation(user_id):
    """Provides a breakdown of a user's portfolio by asset class."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.asset_class, SUM(t.shares_quantity * md.closing_price) as total_value
        FROM assets a
        JOIN accounts ac ON a.account_id = ac.account_id
        JOIN transactions t ON a.asset_id = t.asset_id
        JOIN market_data md ON a.asset_id = md.asset_id
        WHERE ac.user_id = %s
        GROUP BY a.asset_class
        ORDER BY total_value DESC;
    """, (user_id,))
    allocation_data = cur.fetchall()
    cur.close()
    conn.close()
    return allocation_data

def get_performance_insights(user_id):
    """Provides insights using COUNT, SUM, AVG, MIN, and MAX."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Total number of assets
    cur.execute("""
        SELECT COUNT(a.asset_id)
        FROM assets a
        JOIN accounts ac ON a.account_id = ac.account_id
        WHERE ac.user_id = %s;
    """, (user_id,))
    num_assets = cur.fetchone()[0]
    
    # Total shares, avg price, min/max cost basis for all assets
    cur.execute("""
        SELECT SUM(shares_quantity), AVG(price), MIN(cost_basis), MAX(cost_basis)
        FROM transactions t
        JOIN assets a ON t.asset_id = a.asset_id
        JOIN accounts ac ON a.account_id = ac.account_id
        WHERE ac.user_id = %s;
    """, (user_id,))
    insights = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if insights[0] is None:
        return {
            'num_assets': num_assets,
            'total_shares': 0,
            'avg_price': 0,
            'min_cost_basis': 0,
            'max_cost_basis': 0
        }
    
    return {
        'num_assets': num_assets,
        'total_shares': insights[0],
        'avg_price': insights[1],
        'min_cost_basis': insights[2],
        'max_cost_basis': insights[3]
    }