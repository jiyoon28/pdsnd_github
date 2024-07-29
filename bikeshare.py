import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input("PLease enter the name of the city for Chicago, New York City, or Washington > ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. please choose from Chicago, New York City, or Washington.")

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Please enter the name of the month > ").lower()
        if month in months:
            break
        else: 
            print("Invalid input. Please choose a month from January to June or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day =  input("Please enter the name of the day of week > ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose a day from Monday to Sunday or 'all'.")

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most Common Month: {most_common_month}")

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day: {most_common_day}")

    # Extract the hour from the 'Start Time' column to create the 'hour' column
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {most_common_start_hour}")

    # Display the time taken to perform the calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {most_common_start_station}")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Frequent Combination of Start Station and End Station Trip: {most_common_trip}")

    # Display the time taken to perform the calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time}")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of User Type: {user_types}")

    # Display counts of gender
    if "Gender" in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"Counts of Gender: {gender_counts}")
 
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest Year of Birth: {earliest_year}")
        print(f"Most Recent Year of Birth: {most_recent_year}")
        print(f"Most Common Year of Birth: {most_common_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays raw data in increments of 5 rows based on user input.

    Args:
        df - Pandas DataFrame containing city data
    """
    start_loc = 0
    while True:
        display_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no.\n")
        if display_data.lower() != 'yes':
            break
        else:
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5

def main():
    """
    The main function to run the bikeshare data analysis.

    This function repeatedly asks the user to specify a city, month, and day to analyze.
    It then loads the corresponding data and displays various statistics on the most
    frequent times of travel, the most popular stations and trips, trip durations, and user information.
    Additionally, it offers the user the option to view the raw data in increments of 5 rows.
    
    The function continues to restart and run the analysis until the user chooses to exit.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    """
    Entry point of the bikeshare data analysis program.

    When the script is run directly, this block ensures that the main function is called,
    starting the interactive bikeshare data analysis process.
    """
main()