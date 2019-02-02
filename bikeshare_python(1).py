import time
import pandas as pd
import numpy as np

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

"""
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by.
        (str) day - name of the day of week to filter by.
"""
# get user input for city (chicago, new york city, washington). 
def get_city():
    '''Asks the user for a city and returns the filename for 
    that city's bike share data.
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    start_time = time.time()    
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 '\nWould you like to see data for Chicago(c), New York(n), or Washington(w)?\n')

    city = city.lower()

    while True: 
        if city == "new york" or city == "n":
            return new_york_city
        if city == "chicago" or city == "c":
            return chicago
        elif city == "washington" or city == "w":
            return washington
        city = input("Please choose between Chicago (c), New York (n), or Washington (w)")
        city = city.lower()
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Used to take input from user for which specfic date/dates it requires the data for.    
def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (str) Time period information.
    '''
    start_time = time.time()    
    time_period = input('\nWould you like to filter the data by month(m) or day of the week(d) or by none(n)\n') 
    time_period = time_period.lower()

    while True: 
        if time_period == "month" or time_period == "m":

            while True:
                filterByDayOfMonth = input("\n Do you wish to filter by day of the month too? Type 'YES' or 'NO'\n").lower()

                if filterByDayOfMonth == "no":
                    print('\n Data will be filtered by month\n')

                    return 'month'

                elif filterByDayOfMonth == "yes":
                   print ('\n Data will be filtered by month and day of the month\n')
                   return 'day_of_month'
                
        if time_period == "day" or time_period == "d":
            print('\n Data will be filtered by day of the week.\n')
            return 'day_of_week'
        elif time_period == "none" or time_period == "n":
            print('\n No filter will be applied\n')
            return "none"
        time_period = input("\n Please choose a time filter option between month(m), day of the week(d) or by none(n) \n").lower()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        
# get user input for month (all, january, february, ... , june)
def get_month(month_):
    '''Asks the user for a month and returns the specified month.
    Args:
        month_ - the output from get_time_period()
    Returns:
        (str) Month information.
    '''
    start_time = time.time()    
    if month_ == 'month' or month_ == "m":

        month = input('\nWhich month? January, February, March, April, May, or June? Please type the full month name.\n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June? Please type the full month name.\n')
        return month.strip().lower()         
    else:
        return 'none'
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)      
 
# get user input for day of week (all, monday, tuesday, ... sunday)      
def get_day_of_month(df, dayOfMonth_):
    """Asks the user for a month and a day of month, and returns both
    Args: 
        dayOfMonth_ - the ouput of get_time_period()
        df - the dataframe with all bikedata
    Returns:
        list with Month and day information
    """
    monthAndDay = []
    
    if dayOfMonth_ == "day_of_month":
        
        month = get_month("month")
        monthAndDay.append(month)

        maxDayOfMonth = get_max_day_of_month(df, month)
        
        while (True):

            promptString = """\n Which day of the month? \n
            Please type your response as an integer between 1 and """
                            
            #used to find the last date of inputed month by user
            promptString  = promptString + str(maxDayOfMonth) + "\n" 

            dayOfMonth = input(promptString)

            try: 

                dayOfMonth = int(dayOfMonth)

                if 1 <= dayOfMonth <= maxDayOfMonth:
                    monthAndDay.append(dayOfMonth)
                    return monthAndDay

            except ValueError:
                print("That's not an integer")
    else:
        return 'none'        

#Function used to select a specfic day of the week
def get_day(day_):
    '''Asks the user for a day and returns the specified day.
    Args:
        day_ - string - should data be filtered by day
    Returns:
        (str) Day information.
    '''
    start_time = time.time()    
    if day_ == 'day_of_week' or day_ == "d":
        day = input('\nWhich day of the week? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        while day.lower().strip() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease type a day as a choice from M, Tu, W, Th, F, Sa, Su. \n')
        return day.lower().strip()
    else:
        return 'none'
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Loads the csv according to user specified city input     
def load_data(city):
    """
    Reads the city file name and loads it to a dataframe
    """
    print('\nLoading the data...\n')
    df = pd.read_csv(city)
    
    #add datetime format to permit easy filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #add auxiliary columns to aid filtering 
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.weekday_name.html
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    return df

def get_filters(df, time_period, month, dayOfWeek, monthAndDay):
    '''
    Filters the data according to the criteria specified by the user.
    '''
    #Filter by Month if required
    if time_period == 'month' or time_period == 'm':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week if required
    if time_period == 'day_of_week' or time_period == 'd':
        days = ['Monday', 'Tuesday', 
        'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if dayOfWeek.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time_period == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = monthAndDay[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = monthAndDay[1]
        df = df[df['day_of_month'] == day]
    return df

def pop_month(df):
    start_time = time.time()  
    '''Finds and prints the most popular month for start time.
        Args:
        bikeshare dataframe
    Returns:
        none
    '''
    print('\n * What is the most popular month for bike traveling?')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_pop_month = months[m - 1].capitalize()
    return most_pop_month
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def pop_day(df):
    start_time = time.time()  
    '''Finds and prints the most popular day of week (Monday, Tuesday, etc.) for start time.
    Args:
        bikeshare dataframe
    Returns:
        none    
    '''
    print('\n * What is the most popular day of the week for bike traveling?')
    
    return df['day_of_week'].value_counts().reset_index()['index'][0]
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  
def pop_hour(df):
    start_time = time.time()  
    '''Finds and prints the most popular hour of day for start time.
    Args:
        bikeshare dataframe
    Returns:
        none    
    '''
    print('\n * What is the most popular hour of the day for bike traveling?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration(df):
    start_time = time.time()  
    '''Finds and prints the total trip duration and average trip duration.
    '''
    print('\n * What was the total traveling done , and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
 
    total_travel_time = np.sum(df['Travel Time'])
    totalDays = str(total_travel_time).split()[0]

    average_travel_time = np.mean(df['Travel Time'])
    averageDays = str(average_travel_time).split()[0]
    print ("\nThe total travel time was {} days and the average travel time was {} days\n.".format(totalDays, averageDays)) 
                    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def popular_stations(df):
    start_time = time.time()  
    '''Finds and prints the most popular start station and most popular end station.
    '''
    print("\n* What is the most popular start station?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n* What is the most popular end station?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def popular_trip(df):
    start_time = time.time()  
    '''Finds and prints the most popular trip.
    '''
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n* What was the most popular trip from start to end?')
    return result
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def users(df):
    start_time = time.time()  
    '''Finds and prints the counts of each user type.
    '''
    print('\n* Are users subscribers or customers.\n')
    
    return df['User Type'].value_counts()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def gender(df):
    start_time = time.time()  
    '''Finds and prints the counts of gender.
    '''
    print('\n* What is the breakdown of gender among users?\n')

    return df['Gender'].value_counts()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def birth_years(df): 
    ''' Finds and prints the earliest (i.e. oldest user), most recent (i.e. 
        youngest user), and most popular birth years.
    '''
    start_time = time.time()    
    print('\n* What is the earliest, latest, and most frequent year of birth, respectively?')
    earliest = np.min(df['Birth Year'])
    latest = np.max(df['Birth Year'])
    most_pop_birth= df['Birth Year'].mode()[0]
    print('The oldest users are born in {}.\nThe youngest users are born in {}.'

          '\nThe most popular birth year is {}.'.format(earliest, latest, most_pop_birth))
    return earliest, latest, most_pop_birth
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.
    Args:
        data frame
    Returns:
        none
    '''
    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print("Sorry, I do not understand your input. Please type 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes':
        # prints every column except the 'journey' column created in statistics()
        print(df[df.columns[0:-1]].iloc[head:tail])
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_ = False
            while valid_input_ == False:
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_ = is_valid(display_more)
                if valid_input_ == True:
                    break
                else:
                    print("Sorry, I do not understand your input. Please type "
                          "'yes' or 'no'.")
            if display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display_more.lower() == 'no':
                break  

    
def compute_func(f, df):
    """
    Computes the function using the data available
    """ 
    statToCompute = f(df)
    print(statToCompute)
                
def main():
    '''Calculates and prints out the descriptive statistics about a city
    and time period specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    city = get_city()

    df = load_data(city)
    time_period = get_time_period()
    month = get_month(time_period)
    day = get_day(time_period)
    monthAndDay = get_day_of_month(df, time_period)

    df = get_filters(df, time_period, month, day, monthAndDay)
    
    # Display five lines of data at a time if user specifies that they would like to
    display_data(df)    
    
    stat_function_list = [pop_month,
     pop_day, pop_hour, 
     trip_duration, popular_trip, 
     popular_stations, users, birth_years, gender]
    for x in stat_function_list:
        compute_func(x, df)

    # Restart?
    restart = input("\n * Would you like to restart and perform another analysis? Type \'yes\' or \'no\'.\n")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        main()

if __name__ == '__main__':
   main()