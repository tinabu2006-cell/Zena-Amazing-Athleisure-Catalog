# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Zena's Amazing Athleisure Catalog")

cnx = st.connection("snowflake")
session = cnx.session()
view_name = "ZENAS_ATHLEISURE_DB.PRODUCTS.catalog_for_website"
sql_query = f"select * from {view_name}"
try:
    data_df = session.sql(sql_query).to_pandas()
    # st.dataframe(data_df)
    selected_option = st.selectbox(
        "Pick a sweatsuit color or style:"
        , data_df
    )
    
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.write("Please ensure the view name is correct and your role has the necessary privileges.")

if selected_option:
    filtered_df = data_df[data_df["COLOR_OR_STYLE"] == selected_option]
    st.subheader(f"Details for: {selected_option}")
    # st.dataframe(filtered_df)
    
    if not filtered_df.empty:
        details = filtered_df.iloc[0]
        st.image(details['FILE_URL'])
        st.markdown(f"Price: ${details['PRICE']:.2f}")
        st.markdown(f"Sizes available: {details['SIZE_LIST']}")
        st.markdown(f"BONUS: {details['UPSELL_PRODUCT_DESC']}")
        
