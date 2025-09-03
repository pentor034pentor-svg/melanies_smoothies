# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":watermelon::strawberry: Customize Your Smoothie!:kiwi_fruit::green_apple: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# Input for smoothie name
name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)

# Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert to Python list for multiselect
fruit_options = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect input
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    fruit_options,
    max_selections= 5
)

if ingredients_list:
    # Join ingredients into string
    ingredients_string = ", ".join(ingredients_list)

    st.write("Ingredients selected:", ingredients_string)

    # Prepare insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered! 🥤 Name: {name_on_order}", icon="✅")
        # Debug SQL (optional)
        # st.write(my_insert_stmt)
    st.stop() 
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response)
sf_df = st.dataframe(data = smoothiesfroot_response.json(),use_container_width = True)
