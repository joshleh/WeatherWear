Link to dataset used: https://www.kaggle.com/datasets/ananthr1/weather-prediction/data

# WeatherWear: AI-Powered Outfit Recommendations Based on Weather Predictions

## PEAS / Agent Analysis

Our AI agent is a weather-aware outfit recommender, designed to not only predict the weather but also suggest appropriate clothing based on forecasted conditions. This enhances user convenience by helping them dress comfortably and practically for the day's weather.

### PEAS (Performance Measure, Environment, Actuators, Sensors)

The agent operates as a utility-based AI system, balancing weather prediction accuracy with practical outfit recommendations.

For the **Performance Measure** component, the agent is based on its accuracy in predicting weather conditions and its ability to suggest suitable clothing (e.g., whether the user should wear a jacket, long sleeves, or shorts). Higher accuracy and relevant clothing recommendations improve the overall performance.

For the **Environment** component, the agent interacts with historical and real-time weather data. The dataset used for training consists of Seattle weather records (2012-2015), with attributes like temperature, precipitation, and wind speed. The real-world environment includes daily weather variations that impact what people should wear.

For the **Actuators** component, the agent outputs both weather predictions and clothing recommendations. The clothing suggestions include: <ul><li>Shirt Type: Short sleeve or long sleeve</li><li>Bottom Wear: Shorts or pants</li><li>Outerwear: No jacket, raincoat, windbreaker, or snow jacket</li></ul> The recommendations dynamically change based on predicted weather conditions.

For the **Sensors** component, the model uses historical weather data as input, with features including: <ul><li>Precipitation (mm) - Helps determine if a raincoat is needed.</li><li>Temperature Max (°C) - Influences shirt choice.</li><li>Temperature Min (°C) - Affects whether shorts or pants are recommended.</li><li>Wind Speed (m/s) - Determines if a windbreaker is necessary.</li></ul> These input features allow the agent to make informed weather predictions and clothing recommendations.

## Background & Purpose

This AI agent was built to enhance daily decision-making by automating both weather forecasting and clothing recommendations. Instead of just predicting rain or sunshine, it helps users prepare for the weather in a practical way, reducing the chances of being overdressed or underdressed.

The system was trained using a Random Forest Classifier, optimized with class weighting and manual oversampling, to improve accuracy in predicting both common and rare weather conditions (rain, sun, drizzle, fog, snow). The agent is designed to perform well across all seasons and adapt to different climate conditions.
