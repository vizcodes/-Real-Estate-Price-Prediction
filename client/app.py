import streamlit as st
import util
from numerize import numerize
import pandas as pd

util.load_saved_artifacts()
st.header('Real Estate Price Prediction 🏠')
st.markdown('The App helps you get price estimate of real estate properties in and around **Bengaluru**')

with st.sidebar:
    st.caption('Please select the below options to get the price estimate ')

    locations = util.get_location_names()
    location = st.selectbox('What area are you looking for?',options=locations)

    area_list = ['Carpet  Area','Super built-up  Area','Built-up  Area','Plot  Area']
    area_type = st.selectbox('Plot type',area_list)

    total_sqft = st.number_input('Total Sqft.',min_value=300.00,max_value = 30000.00)

    bhk = st.slider('No. of Bedrooms',min_value =1,max_value = 9,step = 1)
    bath = st.slider('No. of Bathrooms',min_value =1,max_value = 9,step = 1)
    balcony = st.slider('No. of Balconys',min_value =0,max_value = 3,step = 1)

    ready_to_move = st.radio('Looking for Ready to move in properties?',['Yes','No'])

    est_button = st.button(label='Get Estimate!')
if est_button == True:
    pred_val = util.get_estimated_price(location,area_type,total_sqft,bhk,bath,balcony,ready_to_move)
    st.write('Estimated price of the Property :')
    st.metric('Price in Rupees ₹ :',value = numerize.numerize(pred_val,3))
    try:
        lat,long =util.get_lat_long(location)
        loc_df = pd.DataFrame({'lat':lat,'lon':long},index = [0])
        st.map(loc_df,zoom = 12)
    except:
        None