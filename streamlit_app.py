# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title("Smoothie Order Form :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_on_smoothie = st.text_input("Name on Smoothie")

if name_on_smoothie:
    st.write("The name on your smoothie will be " + name_on_smoothie)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients"
    , my_dataframe
    , max_selections=5)


if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    ing_dfs = [st.dataframe(data=requests.get("https://fruityvice.com/api/fruit/watermelon").json(), use_container_width=True) for x in ingredients_list]
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, order_filled)
            values ('""" + ingredients_string + """','""" + name_on_smoothie + """', FALSE)"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_smoothie}!', icon="✅")
