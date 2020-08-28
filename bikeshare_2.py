import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
valid_months = ['january','february','march','april','may','june']
valid_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def valid_city(city):
    return city == 'chicago' or city == 'new york city' or city == 'washington'

def valid_month(month):
    return month in valid_months or month == 'all'

def valid_day(day):
    return day in valid_days or day == 'all'

def get_user_input(message):
    return input(message).strip().lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input('Would you like to see data for Chicago, New York City, or Washington?')
    month = "all"
    day = "all"
    while  not(valid_city(city)):
        print('Incorrect city provided. Lets try again...')
        city = get_user_input('Please provide name of the city. You can enter \'Chicago\', \'New York City\' or \'Washington\': ')
   
    
    filter_type = get_user_input('Would you like to filter the data by month, day, or not at all?')
    if filter_type == "month":
        # get user input for month (all, january, february, ... , june)
        month = get_user_input('Which month - January, February, March, April, May, or June?')
        while  not(valid_month(month)):
            print('Incorrect month provided. Lets try again...')
            month = get_user_input('Please provide month to analyze. You can enter January, February, March, April, May, or June:')

    elif filter_type == "day":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_user_input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
        while  not(valid_day(day)):
            print('Incorrect day provided. Lets try again...')
            day = get_user_input('Please provide the day of the week to analyze. You can enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ')
    else:
        print('Ok lets apply no filter at all!')
        month = "all"
        day = "all"

    print('Following filters were selected for month = {}, day = {}'.format(month, day))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    if month != 'all':
        df = df[df['Start Time'].dt.month == (valid_months.index(month) + 1)]
    if day != 'all':
        df = df[df['Start Time'].dt.dayofweek == (valid_days.index(day) + 1)]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Month'] = df['Start Time'].dt.month
    most_common_month = df['Month'].mode()[0]
    print('The most common month is: ', valid_months[most_common_month - 1])

    # display the most common day of week
    df['Day of Week'] = df['Start Time'].dt.dayofweek
    most_common_day_of_week = df['Day of Week'].mode()[0]
    print('The most common day of week is: ', valid_days[most_common_day_of_week - 1])


    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Hour'].mode()[0]
    print('The most common hour is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #start_station = df.groupby('Start Station')['Start Time'].count().sort_values(ascending=False).reset_index()
    start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is: ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most common End Station is: ', end_station)

    # display most frequent combination of start station and end station trip
    df['Combined Start and End Stations'] = df['Start Station'] + ' and ' + df['End Station']
    start_end_combined =  end_station = df['Combined Start and End Stations'].mode()[0]
    print('The most common combination of Start and End Stations is: ', start_end_combined)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total trip duration is: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: {}'.format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('User type count: ', user_type_count)

    print()
    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('Gender count: ', gender_count)

    print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_years = np.sort(df.dropna(axis=0)['Birth Year'].unique())
        earliest_birth_year = birth_years[0]
        print('Earliest birth year is: ', earliest_birth_year)
     
        most_recent_birth_year = birth_years[len(birth_years) - 1]
        print('Most recent birth year is: ', most_recent_birth_year)

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year is: ', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    show_raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
    position = 0
    
    if show_raw_data.lower() == 'yes':
        for label, row in df.iterrows() :
            print(label, row)
            position = position + 1
            if position == 5:
                show_raw_data = input('\nWould you like to see 5 more raws of data? Enter yes or no.\n')
                if show_raw_data.lower() == 'yes':
                    position = 0
                else:
                    break
           


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
