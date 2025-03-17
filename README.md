# WeatherWear: AI-Powered Outfit Recommendations Based on Weather Predictions

## PEAS / Agent Analysis

We’ve all had those days where we step outside and immediately regret our outfit choice—maybe you wore a hoodie on a hot day or forgot a raincoat when it started pouring. That’s exactly what this AI agent is here to solve!

This smart assistant doesn’t just predict the weather—it also tells you what to wear so you can stay comfortable and prepared, no matter what the forecast brings.

### PEAS (Performance Measure, Environment, Actuators, Sensors)

| Component | How It Works in Our AI |
|------|----------------------|
| Performance Measure | The agent is judged by how accurately it predicts the weather and how well it recommends clothing based on that prediction. If the weather forecast is right but the clothing suggestion is off (e.g., recommending shorts on a freezing day), that’s a failure. The goal is to keep users comfortable while ensuring accurate weather forecasts. |                 |
| Environment | The AI operates using Seattle’s historical weather data (2012-2015) and would ideally integrate with real-time weather updates in the future. It considers things like rain, temperature, and wind speed to make both forecasts and outfit suggestions. |
| Actuators (Outputs) | Instead of just predicting “Rain” or “Sunny,” the AI recommends what you should wear based on the weather, including: <ul><li>Shirt: Short sleeves or long sleeves?</li><li>Bottoms: Shorts or pants?</li><li>Outerwear: No jacket, raincoat, windbreaker, or snow jacket?</li></ul> The goal is to remove the guesswork from getting dressed each day. |                |
| Sensors (Inputs) | The model takes in key weather factors to make predictions: <ul><li>Precipitation (mm): Helps determine if a raincoat is needed.</li><li>Temperature Max (°C): Influences shirt choice.</li><li>Temperature Min (°C): Affects whether shorts or pants are recommended.</li><li>Wind Speed (m/s): Determines if a windbreaker is necessary.</li></ul> These factors work together to ensure the AI makes weather-appropriate outfit choices. |
## Background & Purpose

The whole idea behind this agent is simple: knowing the weather isn’t enough—people need to know how to dress for it. Instead of just giving you a generic weather forecast, this AI helps you make smarter clothing choices, so you’re always prepared.

We built this system using a Random Forest Classifier, carefully optimizing it to accurately predict both common and rare weather conditions (like fog or drizzle, which are often misclassified in other models). With this approach, the AI is better at handling real-world weather variations and giving more reliable recommendations.

So next time you’re wondering, *“Should I bring a jacket?”*—just ask the AI. It’s got you covered!

## Agent Setup, Data Preprocessing, Training setup

[Data Exploration and Preprocessing](https://nbviewer.org/github/joshleh/WeatherWear/blob/Milestone3/weather-predictor.ipynb#data-exploration-and-preprocessing)

### Exploring the Dataset & Why It Matters

Ever stepped outside and instantly regretted your outfit choice? Maybe you didn’t check the forecast, or maybe the forecast wasn’t detailed enough to tell you what to actually wear. That’s exactly what this AI is built to fix.

Instead of just saying, "It’s going to rain today," our model helps you decide:

<ul><li>Should you wear a jacket? If so, what kind?</li>
<li>Is it warm enough for shorts, or should you stick with pants?</li>
<li>Will the wind make it feel colder than it actually is?</li></ul>

To do this, we trained the AI on Seattle’s historical weather data (2012-2015), which includes everything from temperature to wind speed.

### What's in the Dataset?

Each row in the dataset represents one day of weather, giving the AI key details to make smart predictions.

| Feature | What It Represents | Why It's Important |
|------|----------------------| ------------------- |
| Date | 	The specific day (YYYY-MM-DD). | Not directly used, but seasonal patterns matter. |
| Precipitation | Rain or snowfall that day (mm). | Helps decide if a raincoat or snow jacket is needed. |
| Temp Max | The highest temperature that day (°C). | Determines if short vs. long sleeves are best. |
| Temp Min | The lowest temperature that day (°C). | Helps pick between shorts or pants. | Determines if a windbreaker is necessary. |
| Wind Speed | How strong the wind was (m/s). | Determines if a windbreaker is necessary. |
| Weather | The overall condition (rain, sun, drizzle, fog, snow). | This is what the AI predicts! |

### Why Does the AI Choose Shirt Type Based on Max Temperature and Bottom Wear Based on Min Temperature?

Imagine getting dressed in the morning. You’re trying to decide what to wear for the entire day, but here’s the tricky part:

- Mornings and nights are often much colder than the afternoon.
- Your upper body is easier to adjust (you can layer shirts or take off a jacket), but your lower body? Not so much.

That’s why our AI makes clothing recommendations the way most people naturally do—by basing shirt choice on the warmest part of the day (max temp) and pants vs. shorts on the coldest part of the day (min temp).

#### 1. Why is Shirt Type Based on Max Temperature?

- You dress for the heat, not the cold, when picking a shirt.
    - The hottest part of the day is when you feel the most discomfort from wearing something too warm.
    - If it’s hot in the afternoon (e.g., 25°C/77°F+), you’re going to want a short-sleeve shirt, even if the morning started a little chilly.
    - If it never warms up (e.g., max temp = 15°C/59°F), then a long-sleeve shirt is a better choice.
- Shirts are easy to adjust.
    - If it’s chilly in the morning but warms up later, you can layer a jacket or sweater over a short-sleeve shirt and take it off when it gets hot.
    - Your arms are more sensitive to heat—so even on a cold morning, if it gets hot later, you’ll want a breathable short sleeve option.

#### 2. Why is Bottom Wear Based on Min Temperature?
- Legs don’t adjust as easily as your upper body.
    - Unlike shirts, you can’t easily change your pants during the day—so you want to be comfortable from morning to night.
    - If the morning or night is too cold, wearing shorts might not be comfortable, even if the afternoon warms up.
- People tend to dress their legs for the coldest part of the day.
    - If the morning is below 10°C (50°F) → Most people will wear pants, even if it warms up later.
    - If the lowest temperature is still above 18°C (64°F) → Shorts are comfortable all day long.

#### How This Helps You Dress Smarter
- You won’t overheat in the afternoon because your shirt is chosen for the hottest part of the day.
- You won’t freeze in the morning because your pants/shorts are picked based on the coldest part of the day.

### How These Features Help the AI Make Better Clothing Recommendations
- Temperature (`temp_max`, `temp_min`) → Affects shirt choice and bottom wear
    - Hot day? → Short sleeves & shorts
    - Chilly morning? → Long sleeves & pants

- Precipitation (`precipitation`) → Tells us if a raincoat or snow jacket is needed
    - Light rain? → Raincoat, but no need for extra layers
    - Heavy snow? → Snow jacket & extra warmth

- Wind Speed (`wind`) → Helps decide if a windbreaker is necessary
    - Breezy but warm? → No jacket needed
    - Strong winds? → Windbreaker, even if it's sunny

- Weather Type (`weather`) → The AI’s main prediction
    - This is the final decision that determines all clothing recommendations.

### How It All Comes Together

Instead of making generic weather predictions, the AI looks at multiple factors to give recommendations that actually make sense.

For instance:
<ul><li>Cold + Rainy + Windy? → The AI suggests a long-sleeve shirt, pants, and a raincoat or windbreaker.</li>
<li>Warm + Sunny? → The AI suggests a short-sleeve shirt and shorts—no jacket needed.</li>
<li>Cold + Snowing? → The AI suggests a snow jacket, long-sleeve shirt, and pants.</li></ul>

This means no more standing in front of your closet, wondering if you’ll freeze or sweat through your clothes. The AI does the thinking for you.

## Training the model

[Training the model](https://nbviewer.org/github/joshleh/WeatherWear/blob/Milestone3/weather-predictor.ipynb#training-the-model)

### Why We Chose Random Forest (And How It Works)

In this project, we used a Random Forest Classifier—a powerful machine learning algorithm that helps predict weather conditions and recommend clothing based on temperature, wind, and precipitation.

Even though Random Forest might not have been explicitly covered in class, it’s a widely used model that balances accuracy, interpretability, and robustness—making it perfect for this task. So, let’s break it down in a simple, human-friendly way.

#### What is a Random Forest Classifier?
Think of Random Forest as a team of decision trees working together to make predictions. Each tree is like a mini-expert, and instead of relying on a single tree, we let many trees vote on the best answer.

Here’s how it works:
- The forest is made up of many individual decision trees.
- Each tree is trained on a random portion of the data.
- Each tree makes a prediction (Rain? Sun? Snow?).
- The final prediction is based on majority voting.

This method makes Random Forest much stronger than a single Decision Tree, because it:
- Reduces overfitting (no single tree dominates the prediction).
- Handles missing or noisy data well (because multiple trees vote).
- Works with both numerical and categorical data.

##### How is Random Forest Different from a Single Decision Tree?

A Decision Tree is like a simple flowchart that asks a series of yes/no questions:

For instance:
- Is the temperature above 20°C? → If yes, wear a short-sleeve shirt.
- Is it raining? → If yes, bring a raincoat.

While a single Decision Tree is easy to understand, it can be too simple and might overfit the data.
- Random Forest solves this by training multiple decision trees and averaging their results.
- Instead of relying on just one tree, we get opinions from many trees and take the majority vote.
- This makes the model more accurate and reliable in different weather scenarios.

#### How Does Random Forest Perform Inference? (How It Makes Predictions)

After training, the model makes predictions using this simple 3-step process:
1. A new weather input (temperature, precipitation, wind) is passed into the model.
2. Each tree in the forest makes its own prediction (e.g., one tree says "Rain", another says "Sun").
3. The final prediction is determined by majority vote (e.g., if most trees say "Rain", the model predicts "Rain").

Why is this better than a single tree?
- If one tree makes a mistake, it won’t ruin the whole prediction.
- The model is more robust to weird or unusual weather patterns.

#### Final Thoughts: Why Random Forest Was the Best Choice
- Handles multiple weather factors well (temperature, wind, precipitation).
- Balances accuracy and interpretability (not too simple, not too complex).
- Improves predictions for rare weather events (Drizzle, Fog, Snow) by combining multiple decision trees.
- More reliable than a single tree (less chance of overfitting).

Instead of making one big decision, Random Forest lets multiple trees work together to make smarter predictions—just like how multiple meteorologists would give a better weather forecast than one person alone.

## Conclusion / Results

Now that we’ve trained our model, it’s time to answer the big question: How well does it actually work?

Our AI’s goal wasn’t just to predict the weather—it also needed to give practical outfit recommendations so people could dress appropriately. Let’s break down how well it performed, what worked, what didn’t, and what could be improved.

### 1. How did the AI Perform?

We evaluated the model using accuracy, precision, recall, and F1-score, and here’s what we found:
- Strong overall accuracy – The model successfully predicts common weather conditions (Rain, Sun) and significantly improved its ability to detect rare ones (Drizzle, Fog, Snow).
- Balanced precision & recall – After manually oversampling rare weather types, the model was much better at detecting them while still maintaining strong performance for common ones.
- Practical clothing recommendations – The AI reliably suggested jackets on rainy days, shorts on warm days, and windbreakers when it’s windy.

| Weather Condition | Precision | Recall | F1-Score |
|------|------| ------ | ------ |
| Rain | 0.98 | 0.88 | 0.93 |
| Sun | 0.86 | 0.88 | 0.87 |
| Drizzle | 0.82 | 0.91 | 0.86 | 
| Fog | 0.87 | 0.96 | 0.91 |
| Snow | 0.89 | 0.89 | 0.89 | 

### 2. What the AI Got Right
- Rain & Sun were predicted very accurately. These are the most common weather types, so the model had plenty of data to learn from.
- Rare weather types (Drizzle, Fog, Snow) improved significantly after balancing the dataset. Originally, the model struggled with these, but now they are detected far more reliably.
- Realistic clothing recommendations. Instead of just predicting the weather, the AI connected the forecast to actual human decisions—choosing short vs. long sleeves, jackets vs. no jackets, and shorts vs. pants.

### 3. Where the AI Struggled

- Handling Edge Cases (e.g., Light Rain vs. Drizzle) – Some borderline cases were tricky, especially between Drizzle and Rain or Fog and Cloudy conditions. The AI sometimes misclassified these because there isn’t always a clear distinction in the dataset.
- Wind-Based Recommendations – The AI could detect when it was windy, but deciding when wind speed actually makes someone feel cold was a bit more complicated. Right now, the windbreaker recommendation is based only on speed, but humidity and temperature might play a role too.
- Better Seasonal Adjustments – The model doesn't currently factor in seasonality (e.g., Seattle winters are colder than summer). This means that some temperature-based clothing recommendations could be improved by understanding seasonal trends.

### 4. How Can We Make It Even Better?
1. Improve Drizzle & Fog Predictions with More Context
- The AI could use humidity levels or visibility data to better distinguish Fog from Cloudy days.
- Adding rain intensity measurements could help separate Drizzle from Rain more accurately.

2. Tune Windbreaker Recommendations
- Instead of recommending a windbreaker based only on wind speed, the model could factor in feels-like temperature (wind chill).
- We could also look at how wind speed affects temperature perception—a 10°C day with strong wind feels much colder than one without wind.

3. Introduce Seasonal Awareness
- Right now, the AI treats a 10°C day the same way in summer and winter, but in reality, people dress differently in different seasons.
- Adding month-based adjustments (e.g., people wear jackets earlier in fall than in spring) could improve clothing recommendations.

4. Try a More Advanced Model
- While Random Forest worked well, we could try Gradient Boosting (XGBoost) to see if a more refined model improves predictions.
- This could be useful for subtle differences between weather types that Random Forest sometimes struggles with.

### 5. Final Thoughts: Is This AI Ready for the Real World?
- Yes! This AI is already a big step up from just checking the weather—it actually helps people decide what to wear based on the forecast.
- It gets common weather types right, and now it also performs well on rarer conditions like drizzle, fog, and snow.
- There’s still room for improvement, especially in edge cases, wind handling, and seasonal adjustments, but overall, the AI does exactly what it was designed to do—help people dress smarter for the weather.
- With some additional refinements, this AI could be integrated into real-world weather apps to make dressing for the day effortless!

## Addtional Notes
Throughout this project, various tools, datasets, and AI assistance were used to develop, refine, and improve the weather prediction and outfit recommendation model. Below is a detailed list of resources used, ensuring full transparency and proper attribution.
### 1. Dataset Used
- Seattle Weather Dataset (2012 - 2015), source: https://www.kaggle.com/datasets/ananthr1/weather-prediction/data
  - This dataset provided historical weather data, including precipitation, temperature, wind speed, and overall weather conditions

### 2. Libraries & Tools
Several open-source Python libraries were used to preprocess the data, build the machine learning model, and generate visualizations:
- Data Processing & Analysis:
    - `pandas` — Data handling and manipulation
    - `numpy` — Numerical computations
- Machine Learning & Model Training:
    - `scikit-learn` — Used for Random Forest classification, model evaluation, and train-test splitting
- Data Visualization
    - `matplotlib` — Used for generating plots and heatmaps
    - `seaborn` — Enhanced data visualization for feature relationships
- Class Imbalance Handling:
    - sklearn.utils.resample — Used for manual oversampling of underrepresented weather classes

### 3. Generative AI Assistance (ChatGPT - OpenAI)
Role: ChatGPT was used throughout the project to:
<ul><li>optimize model choices and parameter tuning</li>
<li>assist in debugging and evaluating model performance</li></ul>

### 4. Other References & Research
- Standard machine learning documentation and resources were consulted, including:
  - Scikit-learn Documentation, source: https://scikit-learn.org/0.21/documentation.html
  - Matplotlib Documentation, source: https://matplotlib.org/stable/index.html
