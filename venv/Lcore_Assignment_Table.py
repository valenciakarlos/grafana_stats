# Creates and Lcore assignment table
# INPUTs:
# 1. -p <name> PATH where Stats are located
# 2. -f <name> FILENAME for CSV file
# 3. -h <hostname> Name of the host we want to extract

import argparse
import os


def validate_arguments():
    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-p", "--path", help="PATH where Stats are located", required=True)
    parser.add_argument("-f", "--filename", help="FILENAME for CSV file", required=True)
    parser.add_argument("-n", "--name", help="HOSTNAME to parse stats for", required=True)
    parser.add_argument("-w", "--worker", help="Worker node to parse stats for", required=True)



    args = parser.parse_args()

    # Further validate the arguments

    # Check if the path exists
    if not os.path.exists(args.path):
        parser.error(f"The provided path '{args.path}' does not exist.")

    # Check with the file exists
    file_path = os.path.join(args.path, args.filename)
    if not os.path.exists(file_path):
        parser.error(f"The specified file '{file_path}' does not exist in the provided path.")
    print(type(args))
    return args

#### End of method
# Sample invocation:
#  python Lcore_Assignment_Table.py -p "/Users/vcarlos/Library/CloudStorage/Box-Box/Partners/Ericsson/PCG TCP Core 3.0 Perf numbers/Work with Rosa/TCP 3.0 PCG Perf Test/n294_1dp_16vcpu_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_0920" -f n294_1dp_16vcpu_6lcore_pnicrsson_netqrss_5gudp_cpu_ctx3_20230929_0920_pm.csv -n n294-esxi-ht-04.sc.sero.gic.ericsson.se -w standard5gc-htnp-b9f7d6d9b-hcczp


if __name__ == "__main__":
    args = validate_arguments()
    FILE_PATH = os.path.join(args.path, args.filename)
    HOSTNAME = args.name
    WORKER= args.worker

    # Now you can use the validated arguments in your code.
    print("Processing")
    print("Filename:", FILE_PATH)
    print("Hostname:", HOSTNAME)
    print("Worker: ", WORKER)

    import pandas as pd

    df = pd.read_csv(FILE_PATH)

    #queue_match = r'Time|.*n294-esxi-ht-04\.sc\.sero\.gic\.ericsson\.se-standard5gc-htnp-b9f7d6d9b-z574b.eth[0-9]-[t|r]x'
    queue_match = r'Time|.*'+HOSTNAME+'-'+WORKER+'.eth[0-9]-[t|r]x'

    filteredqueue_df = df.filter(regex=queue_match)

    columns_list = filteredqueue_df.columns.tolist()

    print("Filtered df:")
    print(filteredqueue_df.keys())
    print("Columns")
    print(columns_list)

    # Get the mode of each column
    mode_result = filteredqueue_df.mode()

    for index in filteredqueue_df.keys():
        most_common_value = filteredqueue_df[index].mode()
        print(f"Most common value for {index} is : {most_common_value}")
        occurrences = filteredqueue_df[index].value_counts()
        print(f"Number of ocurrences for {index}:")
        print(occurrences)


    filteredqueue_df.set_index('Time')
    first_time = 1
    time_dict = {}  # Dictionary with keys being the time. Could really be a list but trying with a dictionary to see if we can later on use as a DF
    # indices is just the row counter at the beginning. row is the full row.
    # individual rows can be accessed with row['Time'] for example
    for indices, row in filteredqueue_df.iterrows():

        for col in columns_list:
            if col == 'Time':
                # Found the Time column. Use it as the index and create a new entry on the dictionary
                curr_time = row['Time']
                # A dictionary with lcores, each pointing to a list of port associated to said lcore
                lcores_dict = {}  # Dictionary on which I will be indexing lcores observed for that Time
                time_dict[curr_time] = lcores_dict
            else:  # It's not the 'Time' Column therefore it should be a port column associated to an lcore value
                lcore_key = row[col]
                if lcore_key in lcores_dict:
                    # Lcore is already part of the dictionary. Need to append to it
                    lcores_dict[lcore_key].append(col)
                else:  # Lcore entry is new create new one
                    lcores_dict[lcore_key] = [col]
                # print("Other Column, but I took the whole row on previous step. Column name="+col)



    # Some validations. Observe how things are print differently depending on dictionary vs data frame

    # print("Entry at 12:07")
    # print(dict['12:07'])
    # newdf=pd.DataFrame(dict)
    # print("The new dictionary is ")
    # print(time_dict)

    # Printing keys and values separately
    # print("Keys:", list(time_dict.keys()))
    # print("Values:", list(time_dict.values()))

    # Printing a dictionary using a loop and the items() method
    '''
    for key, value in time_dict.items():
        print(key, ":", value)
    '''

    # Below is code to compare some of those samples
    # print("Let's compare some samples")

    '''
    print("First Entry DF")
    row=filteredqueue_df[filteredqueue_df['Time'] == '12:07:00']
    for indices, row in row.iterrows():
        for col in columns_list:
            print(col +"="+str(row[col]))


    print("First Entry Dict")
    print(time_dict['12:07:00'])

    print("In between Entry DF")
    row=filteredqueue_df[filteredqueue_df['Time'] == '13:07:00']
    for indices, row in row.iterrows():
        for col in columns_list:
            print(col +"="+str(row[col]))

    print("Last between Dict")
    print(time_dict['13:07:00'])


    print("Last Entry DF")
    row=filteredqueue_df[filteredqueue_df['Time'] == '14:50:00']
    for indices, row in row.iterrows():
        for col in columns_list:
            print(col +"="+str(row[col]))

    print("Last Entry Dict")
    print(time_dict['14:50:00'])


    print("Whole dictionary")
    print(time_dict)
    #print("Specific Value")
    #print(dict['14:50:00'])

    '''

    lcores_df = pd.DataFrame.from_dict(time_dict, orient='index')
    '''
    The above provides the following result with lcores on the colums and time on the rows.

    Resulting DF:
                                                              1  ...                                                  4
    12:07:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...                                                NaN
    12:08:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...                                                NaN
    12:09:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...                                                NaN
    12:10:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    12:11:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    ...                                                     ...  ...                                                ...
    14:46:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    14:47:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    14:48:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    14:49:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    14:50:00  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....


 



    for lcore in lcores_df.columns:  # Here the colums are the lcores and time is on rows
        print("-----------------------")
        print("Cheking lcore:" + str(lcore))

        prev_entry = []
        for entry in lcores_df[lcore]:
            new_entry = entry

            if new_entry != prev_entry:
                print("Entry changed:")
                separator = "\n"
                print(separator.join(entry))
                prev_entry = new_entry

   '''

    '''
    The below yields a result like so with lcores on the rows and time on the columns
    Resulting DF:
                                                12:07:00  ...                                           14:50:00
    1  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    0  [EDP queue lcore assigment:n294-esxi-ht-04.sc....  ...                                                NaN
    3                                                NaN  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    5                                                NaN  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....
    4                                                NaN  ...  [EDP queue lcore assigment:n294-esxi-ht-04.sc....

    '''

    lcores_in_row_df = pd.DataFrame.from_dict(time_dict)

    '''
    print("Lcores in rows:")
    print(lcores_in_row_df)
    '''

    time_columns = lcores_in_row_df.columns
    START_OF_RUN = time_columns[0]
    END_OF_RUN = time_columns[-1]
    for lcore, time_rows in lcores_in_row_df.iterrows():
        print("---------------Lcore " + str(lcore) + " ------------------------------")
        prev_entry = []
        for time_col in time_columns:
            new_entry = lcores_in_row_df.loc[
                lcore, time_col]  # This is the way to access the actual value based on index (lcore number) AND column
            if time_col == START_OF_RUN:
                print("Starting Time ", end="")
                print("Lcore " + str(lcore) + " at " + time_col)
                separator = "\n"
                print(separator.join(new_entry))
                prev_entry = new_entry
            elif new_entry != prev_entry:
                print("Entry Changed for lcore " + str(lcore) + " at " + time_col)
                separator = "\n"
                print(separator.join(new_entry))
                prev_entry = new_entry

            if time_col == END_OF_RUN:
                print("Ending Time ", end="")
                print("Lcore " + str(lcore) + " at " + time_col)
                separator = "\n"
                print(separator.join(new_entry))


