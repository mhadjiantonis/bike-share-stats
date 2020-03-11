import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input('Select a city [chicago, new york city, washington]: ').lower().strip()
        if city in CITY_DATA.keys():
            print('{} selected.'.format(city.title()))
            break
        else:
            print('Invalid city selection! Try again')

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input('Select a month [january, february, march, april, may, june], or all for no month filter: ').lower().strip()
        if month in MONTHS or month == 'all':
            print('{} selected.'.format(month.title()))
            break
        else:
            print('Invalid month selection! Try again')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Select a day of the week, or all for no day filter: ').lower().strip()
        if day in DAYS or day == 'all':
            print('{} selected.'.format(day.title()))
            break
        else:
            print('Invalid day selection! Try again')


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

    # Load data for given city
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Create month and day of the week columns
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday

    # Filter data by given month
    if month != 'all':
        month_num = MONTHS.index(month) + 1
        df = df.loc[df['Month'] == month_num]

    # Filter data by given day of the week
    if day != 'all':
        day_ind = DAYS.index(day)
        df = df.loc[df['Weekday'] == day_ind]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print('Most common month: {}'.format(MONTHS[most_common_month - 1].title()))

    # Display the most common day of week
    most_common_weekday = df['Weekday'].mode()[0]
    print('Most common weekday: {}'.format(DAYS[most_common_weekday].title()))

    # Display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common start hour: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('Most common start station: {}'.format(most_common_start))

    # Display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(most_common_end))


    # Display most frequent combination of start station and end station trip
    most_common_trip = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('Most common trip: {}'.format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: {0:.2f} minutes'.format(total_time / 60))

    # Display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Total travel time: {0:.2f} minutes'.format(mean_time / 60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User type counts:\n{}\n'.format(user_types.to_string()))


    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print('Gender counts:\n{}\n'.format(genders.to_string()))
    except KeyError:
        print('No gender data available.\n')


    # Display earliest, most recent, and most common year of birth
    try:
        by = df['Birth Year']
        print('Earliest birth year: {0:d}'.format(int(by.min())))
        print('Most recent birth year: {0:d}'.format(int(by.max())))
        print('Most common birth year: {0:d}'.format(int(by.mode()[0])))
    except KeyError:
        print('No birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Shows raw data if reuested
    """
    ind = 0
    show_data = input('Show 5 lines of raw data? Enter yes/no. ')
    while show_data == 'yes':
        if ind + 5 < len(df):
            print(df.iloc[ind:ind + 5])
        else:
            print(df.iloc[ind:])
            print('\nEnd of data stream!')
            break
        ind += 5
        show_data = input('\nShow 5 more lines? Enter  yes/no. ')
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
