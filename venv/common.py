# Common modules that can be used by my script

def decide_format(number):
    # Decides the format of a number with following criteria
    # floats format with 2 decimal points
    # Integers format with commas
    # Usage: formatted_data = decide_format(DATA) Returns a float better formatted with 2 decimal points
    #
    if isinstance(number, float):
        format=f"{number:,.2f}"
    else:
        format=f"{number:,.2f}"
        # Alternative formatting for integers
        #format=f"{number:,}"
    return format

def single_axis_plot(x_axis, data1, x_label, y1_label):
    # Receives a list with three DFs, one for x asis and the two remaining for the two axis
    import matplotlib.pyplot as plt

    first_column = data1.name

    TITLE = first_column



    # Create a dual-axis plot
    fig, ax1 = plt.subplots()

    # Set Max and Mean labels for DATA 1
    DATA1_MAX = data1.max()
    # formatted_data1_max=f"{DATA1_MAX:.2f}"
    formatted_data1_max = decide_format(DATA1_MAX)
    DATA1_MEAN = data1.mean()
    # formatted_data1_mean=f"{DATA1_MEAN:.2f}"
    formatted_data1_mean = decide_format(DATA1_MEAN)
    first_max_data1 = data1.idxmax()
    FIRST_MAX_DATA1 = x_axis[first_max_data1]

    DATA1_LEGEND = "Max :" + formatted_data1_max + "\n" + "Mean:" + formatted_data1_mean+"\n"+"First Max:"+FIRST_MAX_DATA1




    # Plot the data from the first DataFrame on the left-y axis
    ax1.plot(x_axis, data1, color='tab:blue', label=DATA1_LEGEND)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color='tab:blue')

    # Draw the labels
    ax1.legend(loc="lower left")
    ax2.legend(loc="lower right")

    # Time doesnt show well. Not readable fixed with the tick_interval below
    tick_interval = 10
    plt.xticks(x_axis[::tick_interval], rotation=90)

    # Set the title and show the plot
    plt.title(TITLE)
    plt.show()
    return 0



def dual_axis_plot(x_axis, data1, data2, x_label, y1_label, y2_label):
    # Receives a list with three DFs, one for x asis and the two remaining for the two axis
    import matplotlib.pyplot as plt

    first_column = data1.name
    second_column = data2.name
    TITLE = first_column + " and " + second_column



    # Create a dual-axis plot
    fig, ax1 = plt.subplots()

    # Set Max and Mean labels for DATA 1
    DATA1_MAX = data1.max()
    # formatted_data1_max=f"{DATA1_MAX:.2f}"
    formatted_data1_max = decide_format(DATA1_MAX)
    DATA1_MEAN = data1.mean()
    # formatted_data1_mean=f"{DATA1_MEAN:.2f}"
    formatted_data1_mean = decide_format(DATA1_MEAN)
    first_max_data1 = data1.idxmax()
    FIRST_MAX_DATA1 = x_axis[first_max_data1]

    DATA1_LEGEND = "Max :" + formatted_data1_max + "\n" + "Mean:" + formatted_data1_mean+"\n"+"First Max:"+FIRST_MAX_DATA1
    # Set Max and Mean labels for DATA 2
    DATA2_MAX = data2.max()
    # formatted_data2_max=f"{DATA2_MAX:,}"
    formatted_data2_max = decide_format(DATA2_MAX)
    DATA2_MEAN = data2.mean()
    # formatted_data2_mean=f"{DATA2_MEAN:,}"
    formatted_data2_mean = decide_format(DATA2_MEAN)
    first_max_data2 = data2.idxmax()
    FIRST_MAX_DATA2 = x_axis[first_max_data2]

    DATA2_LEGEND = "Max :" + formatted_data2_max + "\n" + "Mean:" + formatted_data2_mean+"\n"+"First Max:"+FIRST_MAX_DATA2

    # Plot the data from the first DataFrame on the left-y axis
    ax1.plot(x_axis, data1, color='tab:blue', label=DATA1_LEGEND)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color='tab:blue')

    # Create a second y-axis on the right
    ax2 = ax1.twinx()

    # Plot the data from the second DataFrame on the second axis
    ax2.plot(x_axis, data2, color='tab:red', label=DATA2_LEGEND)
    ax2.set_ylabel(y2_label, color='tab:red')

    # Draw the labels
    ax1.legend(loc="lower left")
    ax2.legend(loc="lower right")

    # Time doesnt show well. Not readable fixed with the tick_interval below
    tick_interval = 10
    plt.xticks(x_axis[::tick_interval], rotation=90)

    # Set the title and show the plot
    plt.title(TITLE)
    plt.show()
    return 0


# Prints all Columns on a dataframe
def print_df_cols(dataframe):


    columns_list = dataframe.columns.tolist()
    print("Number of columns=" + str(dataframe.shape[1]))
    columns_list = dataframe.columns.tolist()
    for index, col in enumerate(columns_list):
        print(f'Index {index}: {col}')

def lcore_insight(dataframe):
    # Takes a dataframe with lcores and their stats and produces a table with
    # ['Lcore', 'AverageUsage', 'MaxValue', 'Position', 'Time']
    # Ideally want to add the most allocated queue but need to think about that

    from prettytable import PrettyTable
    from prettytable import MSWORD_FRIENDLY
    print("The data frame is:")
    print(dataframe)

    import pandas as pd

    # Creating a table to store all information
    lcores_table = PrettyTable(['Lcore', 'AverageUsage', 'MaxValue', 'Position','Time'])
    lcores_table.set_style(MSWORD_FRIENDLY)


    columns_list = dataframe.columns.tolist()
    print("Number of columns=" + str(dataframe.shape[1]))
    columns_list = dataframe.columns.tolist()
    for index, col in enumerate(columns_list):
        print(f'Index {index}: {col}')
        position = (dataframe[col].idxmax())


        max_value=dataframe[col].max()
        # Add non-zero values to a table
        import numbers
        if (isinstance(max_value,numbers.Number)):
            lcores_table.add_row([col,decide_format(dataframe[col].mean()),decide_format(max_value),position, dataframe['Time'][position]])
            #print(f'Lcore: {col} Max: {max_value} Position: {position} Average: {decide_format(dataframe[col].mean())}')


    lcores_table.float_format = '.1'

    print("Lcores Inventory")
    lcores_table.sortby="AverageUsage"
    print(lcores_table)




# Finds the max values of columns of a df

def analyze_df_cols(dataframe):
    from prettytable import PrettyTable
    from prettytable import MSWORD_FRIENDLY
    print("The data frame is:")
    print(dataframe)

    import pandas as pd

    # Melt the DataFrame to convert columns into rows
    melted_df = pd.melt(dataframe, id_vars=['Time'], var_name='Variable', value_name='Value')

    # Filter out non-zero values
    non_zero_values = melted_df[melted_df['Value'] != 0]

    # Display the result grouped by Variable name

    for variable, group_df in non_zero_values.groupby('Variable'):
        print(f"Variable {variable} non-zero values are:")
        print(group_df[['Time', 'Value']])
        print("\n")

    # Creating a table with ALL the values
    all_table = PrettyTable(['Index','Name', 'Max Value','Position','Time'])
    all_table.set_style(MSWORD_FRIENDLY)
    # Table for non-zero values
    nonzero_table = PrettyTable(['Index','Name', 'Nax Value','Position','Time'])
    nonzero_table.set_style(MSWORD_FRIENDLY)

    columns_list = dataframe.columns.tolist()
    print("Number of columns=" + str(dataframe.shape[1]))
    columns_list = dataframe.columns.tolist()
    for index, col in enumerate(columns_list):
        print(f'Index {index}: {col}')
        position = (dataframe[col].idxmax())

        #print("Max:"+str(dataframe[col].max())+" position:"+str(position)+" At time :"+dataframe['Time'][position])
        max_value=dataframe[col].max()
        # Add non-zero values to a table
        import numbers
        if (isinstance(max_value,numbers.Number)):
            all_table.add_row([index,col,max_value,position,dataframe['Time'][position]])
            if (max_value>0):
               nonzero_table.add_row([index,col,max_value,position,dataframe['Time'][position]])

    nonzero_table.float_format = '.1'

    print("All values")
    print(all_table)

    print("Non zero values")
    print(nonzero_table)

