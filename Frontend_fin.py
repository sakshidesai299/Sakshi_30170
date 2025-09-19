import streamlit as st
import Backend_fin as db
from decimal import Decimal

# --- User Management ---
st.sidebar.header("User Selection")
user_id = st.sidebar.number_input("Enter User ID", min_value=1, value=1)
if st.sidebar.button("Fetch User"):
    user = db.get_user(user_id)
    if user:
        st.sidebar.success(f"Fetched user: {user[1]} {user[2]}")
    else:
        st.sidebar.error("User not found.")

st.title("Financial Portfolio Tracker")

# --- CRUD Section ---
st.header("CRUD Operations")

# CREATE
with st.expander("Create New Data"):
    st.subheader("Add New User")
    with st.form("new_user_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        if st.form_submit_button("Create User"):
            new_user_id = db.create_user(first_name, last_name, email)
            if new_user_id:
                st.success(f"User created with ID: {new_user_id}")
            else:
                st.error("Failed to create user.")

# READ
with st.expander("View Assets"):
    st.subheader("View All Assets for User")
    if st.button("Refresh Asset List"):
        assets = db.get_all_assets_for_user(user_id)
        if assets:
            st.table(assets)
        else:
            st.info("No assets found for this user.")

# UPDATE
with st.expander("Update Data"):
    st.subheader("Update User Email")
    with st.form("update_email_form"):
        update_user_id = st.number_input("User ID to Update", min_value=1, value=user_id)
        new_email = st.text_input("New Email")
        if st.form_submit_button("Update Email"):
            if db.update_user_email(update_user_id, new_email):
                st.success(f"Email for User {update_user_id} updated.")
            else:
                st.error("Failed to update email.")

# DELETE
with st.expander("Delete Data"):
    st.subheader("Delete an Asset")
    with st.form("delete_asset_form"):
        asset_id_to_delete = st.number_input("Asset ID to Delete", min_value=1)
        if st.form_submit_button("Delete Asset"):
            if db.delete_asset(asset_id_to_delete):
                st.success(f"Asset ID {asset_id_to_delete} deleted.")
            else:
                st.error("Failed to delete asset. It may not exist.")

# --- Business Insights Section ---
st.header("Business Insights")

if st.button("Generate Insights"):
    total_value = db.get_total_portfolio_value(user_id)
    allocation = db.get_asset_allocation(user_id)
    performance = db.get_performance_insights(user_id)
    
    st.subheader("Portfolio Summary")
    st.metric(label="Total Portfolio Value", value=f"${total_value:,.2f}")
    
    st.subheader("Asset Allocation by Class")
    if allocation:
        # Convert to DataFrame for better visualization
        df_allocation = pd.DataFrame(allocation, columns=['Asset Class', 'Total Value'])
        st.bar_chart(df_allocation.set_index('Asset Class'))
    else:
        st.info("No allocation data available. Add some assets and market data.")
    
    st.subheader("Portfolio Performance Metrics")
    st.markdown(f"**Number of Assets:** {performance['num_assets']}")
    st.markdown(f"**Total Shares Owned:** {performance['total_shares']:,.2f}")
    st.markdown(f"**Average Transaction Price:** ${performance['avg_price']:,.2f}")
    st.markdown(f"**Minimum Cost Basis:** ${performance['min_cost_basis']:,.2f}")
    st.markdown(f"**Maximum Cost Basis:** ${performance['max_cost_basis']:,.2f}")