pip install geopy
import json
import pickle as pkl
import numpy as np

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="real_estate_app")

__locations = None
__features = None
__model = None
__scaler = None

def get_location_names():
    return __locations

def get_estimated_price(location,area_type,sqft,bhk,bath,balcony,ready_to_move):
    ref_dict = {
        'area_type':{'Carpet  Area':1,'Super built-up  Area':2,'Built-up  Area':3,'Plot  Area':4},
        'ready_to_move':{'Yes':1,'No':0}
    }
    try:
        loc_index = __features.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__features))
    x[0] = ref_dict.get('area_type').get(area_type)
    x[1] = sqft
    x[2] = bath
    x[3] = balcony
    x[4] = bhk
    x[5] = ref_dict.get('ready_to_move').get(ready_to_move)
    if loc_index >=0:
        x[loc_index] = 1
    
    x = x.reshape(1,-1)
    x_sc = __scaler.transform(x)
    pred = __model.predict(x_sc)[0] * 100000

    return pred

def get_lat_long(location):
    fin_address = location + ', Bengaluru'
    geo_locate = geolocator.geocode(fin_address)
    return(geo_locate.latitude, geo_locate.longitude)


def load_saved_artifacts():
    print('loading artifacts...')

    global __features
    global __locations
    global __model
    global __scaler

    with open('artifacts/features.json','r') as f:
        __features = json.load(f)['features']
        __locations = __features[6:]

    with open('artifacts/bng_price_model.pkl','rb') as f:
        __model = pkl.load(f)
    
    with open('artifacts/bng_price_scaler.pkl','rb') as f:
         __scaler = pkl.load(f)


    print('Loading artifacts complete :)')

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Vijayanagar','Super built-up  Area',2000, 4,1,1,'no'))
    
    

