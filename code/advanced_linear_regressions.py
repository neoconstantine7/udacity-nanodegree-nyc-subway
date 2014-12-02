import numpy as np
import pandas as pd
import scipy
import statsmodels.api as sm

"""
In this optional exercise, you should complete the function called
predictions(turnstile_weather). This function takes in our pandas
turnstile weather dataframe, and returns a set of predicted ridership values,
based on the other information in the dataframe.

You should attempt to implement another type of linear regression,
that you may have read about, such as ordinary least squares regression:
http://en.wikipedia.org/wiki/Ordinary_least_squares

This is your playground. Go wild!

How does your choice of linear regression compare to linear regression
with gradient descent?

You can look at the information contained in the turnstile_weather dataframe below:
https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
give you a random subset (~15%) of the data contained in turnstile_data_master_with_weather.csv

If you receive a "server has encountered an error" message, that means you are hitting
the 30 second limit that's placed on running your program. See if you can optimize your code so it
runs faster.
"""

def predictions(weather_turnstile):
    #
    # Your implementation goes here. Feel free to write additional
    # helper functions
    #
    y = weather_turnstile['ENTRIESn_hourly']

    # Features
    # Dummy for every hour. Reasoning being that hour variable is incremental, and
    # I expect the relationship
    dummy_units = pd.core.reshape.get_dummies(weather_turnstile['Hour'], prefix='hour')

    # Past hour exits can predict current hour entries.
    past_hour = weather_turnstile['EXITSn_hourly'].shift(1)
    past_hour[0] = 0

    X = weather_turnstile[['rain', 'meandewpti', 'mindewpti', 'maxdewpti', 'fog',
    'maxtempi', 'meantempi', 'mintempi',
    'maxpressurei', 'meanpressurei', 'minpressurei',
    'thunder', 'precipi']].join(dummy_units).join(past_hour)

    model = sm.OLS(y, X)
    results = model.fit()
    prediction = results.predict()

    # Print Results
    print results.summary()

    return prediction

def compute_r_squared(data, predictions):
    SST = ((data-np.mean(data))**2).sum()
    SSReg = ((predictions-np.mean(data))**2).sum()
    r_squared = SSReg / SST

    return r_squared

if __name__ == "__main__":
    input_filename = "turnstile_data_master_with_weather.csv"
    turnstile_master = pd.read_csv(input_filename)
    predicted_values = predictions(turnstile_master)
    r_squared = compute_r_squared(turnstile_master['ENTRIESn_hourly'], predicted_values)

    print r_squared
