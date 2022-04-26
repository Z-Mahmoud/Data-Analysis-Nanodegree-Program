import time
import pandas as pd
import os

# Clear The Terminal
if os.name in ('nt', 'dos'):
    os.system('cls')
else:
    os.system('clear')
    
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# auto generate days and months name
# we can change start date and period to auto update the list if needed
months = pd.date_range(start='2022-01', freq='M', periods=6)
days = pd.date_range(start='2022-01-03', freq='D', periods=7) # start with Monday


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (pandas.Series) month - name of the month(s) to filter by, or "all" to apply no month filter
        (pandas.Series) day - name of the day(s) of week to filter by, or "all" to apply no day filter
    """
    city=''; month=pd.Series(dtype='str'); day=pd.Series(dtype='str');
    
    try:
        print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = get_user_input("Which city Would you like to see its data?",
            ['Chicago','New York City','Washington'],['CHI','NYC','WDC'])

        # get user input for month (all, january, february, ... , june)
        month = get_user_input("Would you like to filter the data by month? (type 'all' for no filter)",
                           pd.Index(['all']).append(months.strftime('%B').str.lower()),
                           pd.Index(['all']).append(months.strftime('%b').str.lower()),0,True)
        # changeing month to all if user multiple input include 'all'
        if month.isin(['all']).any():
            month = pd.Series(['all'])

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_user_input("Would you like to filter the data by day? (type 'all' for no filter)",
                             pd.Index(['all']).append(days.strftime('%A').str.lower()),
                             pd.Index(['all']).append(days.strftime('%a').str.lower()),0,True)
        # changeing day to 'all' if user multiple input include 'all'
        if day.isin(['all']).any():
            day = pd.Series(['all'])
    except Exception as e:
        print("Something went wrong: {}".format(e))

    print('-' * 40)
    return city, month, day


def get_user_input(message, acceptable_inputs,abbreviations, index_start=1, multi_filter=False):
    '''
    Asks for user input according to the displayed message,
    allwoing the user to type the complete value, its abbreviation or index
    with multiple input option
    
    Args:
        message - the prompet message
        acceptable_inputs - list of acceptable inputs
        abbreviations - list of the abbreviations for the acceptable inputs list
        index_start (default = 1) - start number for the acceptable inputs index
        multi_filter (default = False) - allow for multiple input seprated by comma
    
    
    Return: 
        string or list of lowercase value from acceptable_inputs list coresponding to user input
    
    '''
    try:
        # Create acceptable inputs DataFrame with complete value and its abbreviation
        # Add index option (Display and accept it) only if there's more than 2 acceptable inputs
        acceptable_inputs_df = pd.DataFrame({'Acceptable Inputs':acceptable_inputs,'Abbreviation':abbreviations})
        if len(acceptable_inputs)>2:
            acceptable_inputs_df.insert(1, 'Index', [str(x) for x in range(index_start,len(acceptable_inputs)+index_start)])
            print('\n'+message,"\nType any of the acceptable inputs, index or abbreviation\n\n", acceptable_inputs_df.to_string(index=False))
            print()
        else:
            print('\n'+message,"Enter",acceptable_inputs," or",abbreviations)
        
        acceptable_inputs_df['Abbreviation']=acceptable_inputs_df['Abbreviation'].str.lower()
        acceptable_inputs_df['Acceptable Inputs']=acceptable_inputs_df['Acceptable Inputs'].str.lower()
        
        extra_message=":"
        if multi_filter: 
            extra_message= "Multiple input are allowed seprated by comma ','\n:"

        while True:
            user_input = input(extra_message).lower()
            if multi_filter:
                user_input = [s.strip() for s in user_input.split(",")]
            else:
                user_input = [user_input]
            user_input = acceptable_inputs_df[acceptable_inputs_df.isin(user_input).any(1)]['Acceptable Inputs']
            if user_input.empty:
                print ("\nIncorrect input, refer to the above acceptable inputs\n" + message)
            else:
                break
        
        if multi_filter:
            return user_input
        else:
            return user_input.to_string(index=False).lower()
    
    except Exception as e:
        print("Something went wrong: {}".format(e))
        return None


def most_common(message, df):
    '''
    Prints the most common element on the DataFrame (df)
    along with the (message) and the number of occurance
    '''
    try:
        most_common = df.value_counts()
        print(message.capitalize(), most_common.index[0])
        print("Number of occurance: ", most_common.values[0], "\n")
    except Exception as e:
        print("Something went wrong: {}".format(e))


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (pandas.Series) month - name of the month(s) to filter by, or "all" to apply no month filter
        (pandas.Series) day - name of the day(s) of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    try:
        df = pd.DataFrame()
        # load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])

        # convert the Birth Year column to int
        if 'Birth Year' in df.columns:
            df['Birth Year']=df['Birth Year'].fillna(0).astype('int')
        
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['Month'] = df['Start Time'].dt.month_name().str.lower()
        df['Week Day'] = df['Start Time'].dt.day_name()  # weekday_name

        # filter by month if applicable
        if month.iloc[0] != 'all':
            # filter by month to create the new dataframe
            df = df[df['Month'].isin(month)]

        # filter by day of week if applicable
        if day.iloc[0] != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['Week Day'].isin(day.str.title())]

    except Exception as e:
        print("Something went wrong: {}".format(e))

    return df


def time_stats(df,month, day):
    """Displays statistics on the most frequent times of travel."""
    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        if (month.size == 1) and (month.iloc[0] != 'all'):
            print("The most common month:\nNot Applicable, we filtered our data for one month only ("+month.iloc[0]+")\n")
        else:
            most_common("The most common month: ", df['Month'])

        # display the most common day of week
        if (day.size == 1) and (day.iloc[0] != 'all'):
            print("The most common day of week:\nNot Applicable, we filtered our data for one day only ("+day.iloc[0]+")\n")
        else:
            most_common("The most common day of week: ", df['Week Day'])

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        most_common("The most common start hour: ", df['hour'])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("Something went wrong: {}".format(e))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        most_common("The most commonly used start station: ", df['Start Station'])

        # display most commonly used end station
        most_common("The most commonly used end station: ", df['End Station'])

        # display most frequent combination of start station and end station trip
        trips = "Start Station: " + df['Start Station'] + " , End Station: " + df['End Station']
        most_common("The most frequent trip: ", trips)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("Something went wrong: {}".format(e))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    try:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display count of trips
        print("Total trips count: ", df['Trip Duration'].count())
        # display total travel time
        print("Total trips duration: ", df['Trip Duration'].sum())
        # display mean travel time
        print("Average trip duration: ", df['Trip Duration'].mean())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("Something went wrong: {}".format(e))


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        print('\nTotal trips count by user types:')
        print('-' * 33)
        print(df['User Type'].groupby(df['User Type']).count().to_string(header=False))

        # Display counts of gender
        print('\nTotal trips count by user gender:')
        print('-' * 33)
        if 'Gender' in df.columns:
            df_gender=df['Gender'].fillna('Unknown')
            print(df_gender.groupby(df_gender).count().to_string(header=False))
        else:
            print('Gender data not available')

        # Display earliest, most recent, and most common year of birth
        print("\nBikeshare users's birth year statistics:")
        print('-' * 33)
        if 'Birth Year' in df.columns and df['Birth Year'].max()>0:
            birth_year_stat =pd.Series([df['Birth Year'][df['Birth Year']>0].min(),df['Birth Year'][df['Birth Year']>0].max(),
                                        df['Birth Year'][df['Birth Year']>0].mode()],
                                        ['Earliest year of birth','Most recent year of birth','Most common year of birth'])
            print(birth_year_stat.astype(int).to_string(header=False))
        else:
            print('Birth Year data not available')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("Something went wrong: {}".format(e))


def show_row_data(df):
    '''
    Raw data is displayed upon request by the user in the following manner:
        1. Prompt the user if they want to see 5 lines of raw data,
        2. Display that data if the answer is 'yes',
        3. Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
        4. Stop the program when the user says 'no' or there is no more raw data to display.
    '''
    try:
        # 
        df.drop(['hour'], axis = 1, errors='ignore', inplace=True)
        message="\nWould you like to see 5 records of trips raw data?"
        start_index = 0
        end_index = 5
        df_index_size = df.index.size

        while start_index <  df_index_size:
            if(start_index==5): 
                message="\nWould you like to see another 5 records of trips raw data?"
            proceed = get_user_input(message, ['yes', 'no'], ['y', 'n'])
            if proceed != 'yes':
                break
            for row in df.iloc[start_index:end_index].iterrows():
                print('-' * 40)
                print(row[1].to_string(dtype=False,name=False))

            start_index += 5
            end_index += 5
    except Exception as e:
        print("Something went wrong: {}".format(e))

        
def main():
    try:
        while True:
            city, month, day = get_filters()
            if not city: 
                break
            else:
                if month.empty: 
                    month = pd.Series(['all'])
                if day.empty:
                    day = pd.Series(['all'])
            print("We Will Apply The Follwoing Filters\nCity:",city,
                  "         Month:", ', '.join(month),
                  "           Day:", ', '.join(day))
            print('-' * 40)
            print("Loading Data ......")
            df = load_data(city, month, day)
            if df.empty: 
                break

            proceed = get_user_input('\nWould you like to see statistics on the most frequent times of travel?', ['yes', 'no'], ['y', 'n'])
            if proceed == 'yes':
                time_stats(df,month, day)

            proceed = get_user_input('\nWould you like to see statistics on the most popular stations and trip?', ['yes', 'no'], ['y', 'n'])
            if proceed == 'yes':
                station_stats(df)

            proceed = get_user_input('\nWould you like to see statistics on the total and average trip duration?', ['yes', 'no'], ['y', 'n'])
            if proceed == 'yes':
                trip_duration_stats(df)

            proceed = get_user_input('\nWould you like to see statistics on bikeshare users?', ['yes', 'no'], ['y', 'n'])
            if proceed == 'yes':
                user_stats(df)

            show_row_data(df)

            restart = get_user_input('\nWould you like to restart?',['yes', 'no'], ['y', 'n'])
            if restart != 'yes':
                break
    except Exception as e:
        print("Something went wrong: {}".format(e))

if __name__ == "__main__":
    main()
