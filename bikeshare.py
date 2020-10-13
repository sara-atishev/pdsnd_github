import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('\nWhich city would you like to see data for: Chicago, New York City, or Washington?\n').lower()

        if city in cities:
            print('\nWe will be looking at data for {}.\n'.format(city.title()))
            break
        else:
            print('\nI\'m sorry, I don\'t recognize that city. Remember, I only have data for Chicago, New York City, and Washington. Please try again.\n')
            city = input('\nWhich city would you like to see data for: Chicago, New York City, or Washington?\n').lower()

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month = input('\nWhat month would you like to see data for: January, February, March, April, May, June, or All?\n').lower()

        if month in months:
            print('\nYou\'ve requested data for {}.\n'.format(month.title()))
            break
        else:
            print('\nI\'m sorry, that\'s not a valid month. Please request data from January, February, March, April, May, June, or All.\n')
            month = input('\nWhat month would you like to see data for: January, February, March, April, May, June, or All?\n').lower

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('\nWhat day of the week would you like to see data for: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All?\n').lower()

        if day in days:
            print('\nWe\'ll look at data on {}.\n'.format(day.title()))
            break
        else:
            print('\nI\'m sorry, that\'s not a valid day. Please enter a day of the week or all to see data from all days.\n')
            day = input('\nWhat day of the week would you like to see data for: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All?\n').lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost Common Month:\n', months[popular_month-1].title())

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost Common Day of the Week:\n', popular_day.title())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Common Start Hour:\n',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:\n',popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station:\n',popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('\nMost Popular Start Station to End Station Combination:\n',popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def convert(seconds):
        seconds_per_day = 60 * 60 * 24
        if seconds < seconds_per_day:
            return time.strftime("%H:%M:%S", time.gmtime(seconds))
        days = seconds // seconds_per_day
        seconds_without_days = seconds % seconds_per_day
        return str(days) + " day(s), " + time.strftime("%H:%M:%S", time.gmtime(seconds_without_days))
    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('\nTotal Trip Time, in Seconds:\n', convert(total_travel_time))

    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean()

    print('\nAverage Trip Time:\n', convert(average_travel_time))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe number of users of each user type:\n',user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        user_genders = df['Gender'].value_counts()
        print('\nThe number of users of each gender:\n',user_genders)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        common_birth_year = df['Birth Year'].mode()[0]
        print ('\nMost Common Birth Year:\n',int(common_birth_year))
        earliest_birth_year = df['Birth Year'].min()
        print ('\nEarliest Birth Year:\n',int(earliest_birth_year))
        latest_birth_year = df['Birth Year'].max()
        print ('\nLatest Birth Year:\n',int(latest_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        start_index = 0
        end_index = 5
        while True:
            raw_data = input('\nWould you like to see 5 lines of raw data?\n')
            if raw_data.lower() == "yes":
                if end_index >= len(df):
                    print("You reached the end of the dataframe. Stopping")
                    break
                print(df[start_index:end_index])
                start_index +=5
                end_index += 5
            elif raw_data.lower() == "no":
                break
            else:
                print('\nI didn\'t understand your input, please input "yes" or "no" \n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
