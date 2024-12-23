import streamlit as st
import pickle
import numpy as np

with open('casual.pkl', 'rb') as f:
    casual_model = pickle.load(f)

with open('registered.pkl', 'rb') as f:
    registered_model = pickle.load(f)

st.title('Casual User and Registered User Prediction')

hum = float(st.text_input('Humidity (0 to 1)', '0.5'))
season = st.selectbox('Season', ['winter', 'spring', 'summer', 'fall'])
temp = float(st.text_input('Temperature (0 to 1)', '0.5'))
hr = int(st.text_input('Hour of the Day (0-23)', '12'))

season_mapping = {'winter': 0, 'spring': 1, 'summer': 2, 'fall': 3}

season_encoded = season_mapping[season]

if hr >= 18:
    hr_converted = [False, False, True]  # Evening
elif hr >= 12:
    hr_converted = [True, False, False]  # Afternoon
elif hr >= 6:
    hr_converted = [False, True, False]  # Morning
else:
    hr_converted = [False, True, False]  # Early morning

season_converted = [0, 0, 0]
if season == 'winter':
    season_converted = [1, 0, 0]
elif season == 'spring':
    season_converted = [0, 1, 0]
elif season == 'summer':
    season_converted = [0, 0, 1]
elif season == 'fall':
    season_converted = [0, 0, 0]

# Prepare the input features in the correct format for the model
input_features = np.array([[hum, temp, *hr_converted, *season_converted]])

# Predict with both models
casual_prediction = casual_model.predict(input_features)
registered_prediction = registered_model.predict(input_features)

# Display the predictions
st.write("### Predictions")
st.write(f"Predicted Casual: {round(casual_prediction[0] - 15, 0)}") 
st.write(f"Predicted Registered: {round(registered_prediction[0] - 25, 0)}")
st.write("Predicted Total:", round(registered_prediction[0] + casual_prediction[0] - 40, 0))
