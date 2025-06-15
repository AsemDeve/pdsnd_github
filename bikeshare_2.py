import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def prompt_for_option(options, prompt_label):
    """Generic prompt to select from options by number or name."""
    while True:
        print(f"\nWhich {prompt_label}?")
        for key, value in options.items():
            print(f"{key}. {value.title()}")
        user_input = input(f"Enter the number or name of the {prompt_label}: ").strip().lower()
        if user_input in options:
            return options[user_input]
        elif user_input in [v.lower() for v in options.values()]:
            return user_input
        else:
            print(f"Invalid {prompt_label}. Try again.")


def get_filters():
    """
    Asks user to specify a city, and whether to filter by month, day, both or not at all.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no filter
        (str) day - name of the day of week to filter by, or "all" to apply no filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city_options = {
        '1': 'chicago',
        '2': 'new york city',
        '3': 'washington'
    }
    city_names = {v.lower(): v for v in city_options.values()}

    month_options = {
        '1': 'january',
        '2': 'february',
        '3': 'march',
        '4': 'april',
        '5': 'may',
        '6': 'june'
    }
    month_names = {v.lower(): v for v in month_options.values()}

    day_options = {
        '1': 'saturday',
        '2': 'sunday',
        '3': 'monday',
        '4': 'tuesday',
        '5': 'wednesday',
        '6': 'thursday',
        '7': 'friday'
    }
    day_names = {v.lower(): v for v in day_options.values()}

    # Get city input.
    while True:
        print("\nSelect a city:")
        for key, value in city_options.items():
            print(f"{key}. {value.title()}")

        user_input = input("Enter the number or name of the city: ").strip().lower()

        if user_input in city_options:
            city = city_options[user_input]
            break
        elif user_input in city_names:
            city = city_names[user_input]
            break
        else:
            print("Invalid choice. Please enter a number or valid city name.")

    # Filter options.
    while True:
        print("\nWould you like to filter the data by month, day, both, or not at all?")
        print("1. Month\n2. Day\n3. Both\n4. No filter")
        filter_choice = input("Enter the number or text: ").strip().lower()
        if filter_choice in ['1', 'month']:
            month = prompt_for_option(month_options, "month")
            day = 'all'
            break
        elif filter_choice in ['2', 'day']:
            day = prompt_for_option(day_options, "day")
            month = 'all'
            break
        elif filter_choice in ['3', 'both']:
            month = prompt_for_option(month_options, "month")
            day = prompt_for_option(day_options, "day")
            break

        elif filter_choice in ['4', 'no filter', 'none']:
            month = 'all'
            day = 'all'
            break
        else:
            print("Invalid option. Please choose from 1 to 4 or type the option name.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze (e.g., 'chicago')
        (str) month - name of the month to filter by, or "all" for no filter
        (str) day - name of the day of week to filter by, or "all" for no filter

    Returns:
        df - Pandas DataFrame containing filtered city data
    """
    # map city name to CSV file.
    city_files = {
        'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv'
    }

    # load data file into a dataframe.
    df = pd.read_csv(city_files[city])

    # convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from 'Start Time' to filter
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]
    print("Data for: " + city.title())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel, including counts."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'month' in df.columns:
        common_month = df['month'].mode()[0]
        month_count = df['month'].value_counts()[common_month]
        print(f"Most Common Month: {common_month.title()} (Count: {month_count})")
    else:
        print("Month data is not available in this dataset.")

    # display the most common day of week
    if 'day_of_week' in df.columns:
        common_day = df['day_of_week'].mode()[0]
        day_count = df['day_of_week'].value_counts()[common_day]
        print(f"Most Common Day of Week: {common_day.title()} (Count: {day_count})")
    else:
        print("Day of week data is not available in this dataset.")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    hour_count = df['hour'].value_counts()[common_hour]
    print(f"Most Common Start Hour: {common_hour}:00 (Count: {hour_count})")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip, including counts."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if 'Start Station' in df.columns:
        common_start_station = df['Start Station'].mode()[0]
        start_station_count = df['Start Station'].value_counts()[common_start_station]
        print(f"Most Commonly Used Start Station: {common_start_station} (Count: {start_station_count})")
    else:
        print("Start Station data not available.")

    # display most commonly used end station
    if 'End Station' in df.columns:
        common_end_station = df['End Station'].mode()[0]
        end_station_count = df['End Station'].value_counts()[common_end_station]
        print(f"Most Commonly Used End Station: {common_end_station} (Count: {end_station_count})")
    else:
        print("End Station data not available.")

    # display most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['Trip'] = df['Start Station'] + " → " + df['End Station']
        most_common_trip = df['Trip'].mode()[0]
        trip_count = df['Trip'].value_counts()[most_common_trip]
        print(f"Most Frequent Trip: {most_common_trip} (Count: {trip_count})")
    else:
        print("Trip data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total, average, and count of trip durations."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df.columns:
        total_duration = df['Trip Duration'].sum()
        mean_duration = df['Trip Duration'].mean()
        trip_count = df['Trip Duration'].count()

        print(f"Total Travel Time: {total_duration:,} seconds ({total_duration / 3600:.2f} hours)")
        print(f"Average Travel Time: {mean_duration:.2f} seconds")
        print(f"Number of Trips: {trip_count:,}")
    else:
        print("Trip Duration data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_type_counts = df['User Type'].value_counts()
        print("User Types:")
        print(user_type_counts.to_string())
    else:
        print("User Type data not available.")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts(dropna=True)
        print("\nGender Distribution:")
        print(gender_counts.to_string())
    else:
        print("\nGender data not available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        birth_year_count = df['Birth Year'].value_counts()[most_common]

        print("\nBirth Year Stats:")
        print(f"Earliest Year of Birth: {earliest}")
        print(f"Most Recent Year of Birth: {most_recent}")
        print(f"Most Common Year of Birth: {most_common} (Count: {birth_year_count})")
    else:
        print("\nBirth Year data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Display raw data 5 rows at a time upon user request."""
    i = 0
    pd.set_option('display.max_columns', None)  # Display all columns

    while i < len(df):
        show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
        if show_data != 'yes':
            break
        print(df.iloc[i:i + 5])
        i += 5

    if i >= len(df):
        print("\nAll available data has been displayed.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)  # <-- Add this line

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
