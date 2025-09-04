# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
from snowflake.snowpark.exceptions import SnowparkSQLException
# Write directly to the app
st.title(f":watermelon::strawberry: Customize Your Smoothie!:kiwi_fruit::green_apple: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
# Input for smoothie name
name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)
# st.dataframe(data=my_dataframe,use_container_width = True)
# st.stop()


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
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
      ingredients_string += fruit_chosen + ' '
      st.subheader(fruit_chosen + ' Nutrition information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
      sf_df = st.dataframe(data = smoothiefroot_response.json(),use_container_width = True)
    # Join ingredients into string
    ingredients_string = ", ".join(ingredients_list)

    st.write("Ingredients selected:", ingredients_string)

    # Prepare insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
  # Submit button
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
      try:
          session.sql(
              "INSERT INTO orders (ingredients, name_on_order) VALUES (?, ?)",
              params=[ingredients_string, name_on_order]
          ).collect()
          st.success(f"Your Smoothie is ordered! 🥤 Name: {name_on_order}", icon="✅")
      except Exception as e:
          st.error(f"Insert failed: {e}")
      st.stop()
    # time_to_insert = st.button('Submit Order')
    # if time_to_insert:
    #     session.sql(my_insert_stmt).collect()
    #     st.success(f"Your Smoothie is ordered! 🥤 Name: {name_on_order}", icon="✅")
    #     # Debug SQL (optional)
    #     # st.write(my_insert_stmt)
    # st.stop() 




