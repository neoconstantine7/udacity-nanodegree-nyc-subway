from pandas import *
from ggplot import *

import numpy

import datetime

def plot_weather_data(turnstile_weather):
    '''
    Use ggplot to make another data visualization focused on the MTA and weather
    data we used in assignment #3. You should make a type of visualization different
    than you did in exercise #1, and try to use the data in a different way (e.g., if you
    made a lineplot concerning ridership and time of day in exercise #1, maybe look at weather
    and try to make a histogram in exercise #2).

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  Here are some suggestions for things
    to investigate and illustrate:
    * Ridership by time of day or day of week
    * How ridership varies based on Subway station
    * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    To see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we are giving you about 1/3
    of the actual data in the turnstile_weather dataframe
    '''
    df = turnstile_weather.copy()

    #
    df['datetime'] = df.loc[:,'DATEn'].map(lambda x: pandas.to_datetime(x))
    df['dayofweek'] = df.loc[:,'datetime'].map(lambda x: x.strftime('%A'))
    # print df['dayofweek']

    # print df['ENTRIESn_hourly'].describe()
    df['entries_log'] = numpy.log10(df['ENTRIESn_hourly'].fillna(0) + 1)

    # plot = ggplot(turnstile_weather, aes('EXITSn_hourly', 'ENTRIESn_hourly')) \
        # + stat_smooth(span=.15, color='black', se=True)+ geom_point(color='lightblue') \
        # + ggtitle("MTA Entries By The Hour!") \
        # + xlab('Exits') + ylab('Entries')
    # plot = ggplot(df, aes('entries_log')) \
    #     + geom_histogram() \
    #     + facet_wrap('rain') \
    #     + ggtitle("Histogram log10(entries by hour). Rain No-Rain") \
    #     + xlab('Entries per hour') #+ ylab('Entries')
    # df_group = df.groupby('dayofweek', as_index=False).sum()
    # print df_group
    # plot = ggplot(df_group, aes(x='dayofweek', y='ENTRIESn_hourly')) \
    #     + geom_bar(stat='bar') \
    #     + ggtitle("Entries by day of week") \
    #     + xlab('Day of week') + ylab('Entries') #+ scale_x_date(labels = date_format("%d"))

    df_group = df.groupby('Hour', as_index=False).sum()
    # print df_group
    # plot = ggplot(df_group, aes(x='Hour', y='ENTRIESn_hourly')) \
    #     + geom_bar(stat='bar') \
    #     + ggtitle("Entries by hour") \
    #     + xlab('Hour') + ylab('Entries') #+ scale_x_date(labels = date_format("%d"))

    plot = df.describe()
    return plot

if __name__ == "__main__":
    image = "plot.png"
    input_filename = '../exercise_1/turnstile_data_master_with_weather.csv'
    # with open(image, "wb") as f:
    turnstile_weather = pandas.read_csv(input_filename)
    turnstile_weather['datetime'] = turnstile_weather['DATEn'] + ' ' + turnstile_weather['TIMEn']
    gg =  plot_weather_data(turnstile_weather)
    print gg
        # ggsave(f, gg)
