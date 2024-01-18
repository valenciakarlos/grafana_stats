# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    import pandas as pd

    data = {'Time': ['10:00', '10:01', '10:02', '10:03'],
            'lcore-q1': [1, 1, 2, 1],
            'lcore-q2': [0, 2, 1, 4]}
    df = pd.DataFrame(data)
    print(df.describe())


    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Sample DataFrame
    data = {'Time': ['10:00', '10:01', '10:02', '10:03'],
            'lcore-q1': [1, 1, 2, 1],
            'lcore-q2': [0, 2, 1, 4]}

    df = pd.DataFrame(data)

    # Convert 'Time' column to datetime
    df['Time'] = pd.to_datetime(df['Time'])

    # Melt the DataFrame to have a 'variable' column and a 'value' column
    melted_df = pd.melt(df, id_vars=['Time'], var_name='lcore', value_name='value')

    # Create a heatmap using seaborn
    plt.figure(figsize=(10, 6))
    sns.heatmap(data=melted_df.pivot('Time', 'lcore', 'value'), cmap='viridis', annot=True, fmt='d')
    plt.title('Values of lcores over Time')
    plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
