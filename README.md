Link to dataset used: https://www.kaggle.com/datasets/ananthr1/weather-prediction/data

Questions for this milestone are answered below and are also included in the jupyter notebook weather-predictor:

The AI agent for this project is a weather predictor. This weather predcitor is a utility-based agent, which can be explained in terms of PEAS (Performance measure, Environment, Actuators, Sensors).
- The performance measure for this agent is to accurately predict the weather (e.g. whether it's raining or not) while minimizing the incorrect classifications. 
- The environment for this agent is the dataset that includees Seattle's weather conditions from the year 2012 to the year 2015, as well as the real-world environment which includes precipitation, temperature fluctuatoins, and season effects. 
- The actuators for this agent are the output predictions about the weather based on the input conditions.
- The sensors for this agent are the inputs from previous weather data: preciptation, temperature, wind, and speed

The weather prediction agent is built using a Naive Bayes Classifier, which is a probablistic model that estimates the likelihood of different weather conditions based on the given features. 

In this dataset, there are 1461 observations.

Column Descriptions:
- date: the specific date of the observation, in a YYYY-MM-DD format
- preciptation: the total rainfall or snowfall received during the day (millimeters)
- temp_max: maximum temperature recorded that day (Degrees Celsius)
- temp_min: minimum temperature recorded on that day 
- wind: average daily wind speed (meters per second)
- weather: represents weather conditions of that day (e.g. rain, sun, drizzle, fog, snow)

Thankfully, there is no data missing, so no adjustments need there. 

Conclusion
Although the model accuracy is high (82.94%), there is zero precision and recall for some cases. This is due to the severe class imbalance, as the weather types drizzle, fog, and snow have very few examples in the test set compared to the weather types sun and rain. In order to improve it, the class weights need to be taken into consideration.  
