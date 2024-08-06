# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title("Smoothie Order Form :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col("search_on"))
pd_df = my_dataframe.to_pandas()

name_on_smoothie = st.text_input("Name on Smoothie")

if name_on_smoothie:
    st.write("The name on your smoothie will be " + name_on_smoothie)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients"
    , my_dataframe
    , max_selections=5)


if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    for chosen_fruit in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == chosen_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', chosen_fruit,' is ', search_on, '.')
        
        st.subheader(chosen_fruit+" Nutritional Information");
        fv_df = st.dataframe(data=requests.get("https://fruityvice.com/api/fruit/"+chosen_fruit).json(), use_container_width=True)  
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, order_filled)
            values ('""" + ingredients_string + """','""" + name_on_smoothie + """', FALSE)"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_smoothie}!', icon="✅")
