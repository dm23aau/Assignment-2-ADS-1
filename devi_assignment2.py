# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Read the world bank data
def read_worldbank_data(filename, selected_rows):
    # Read CSV file into a python dataframe.
    # Skipping the first 4 rows of the data file as they are empty.
    df = pd.read_csv(filename, skiprows=4)

    # Select relevant columns (Country Name and columns P to BM)
    df_selected = df.iloc[:, [0] + list(range(35, 65))]
    df_selected = df_selected.iloc[selected_rows]

    # Transpose the dataframe
    df_transposed = df_selected.transpose()

    # Clean the transposed dataframe
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed[1:]
    
    # Set the name of the first column to 'Year'
    df_transposed.columns.name = 'Year'
    
    df_transposed = df_transposed.astype(float)

    return df_selected, df_transposed



def plot_side_by_side_boxplots_matplotlib(df_list1, df_list2, years, titles):
    # Create subplots
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    # Plot boxplots for each dataframe in 1991
    for i in range(3):
        axes[0, i].boxplot(df_list1[i].values.T)
        axes[0, i].set_title(f'{titles[i]} - {years[0]}')
        axes[0, i].set_ylabel('Value')

    # Plot boxplots for each dataframe in 2020
    for i in range(3):
        axes[1, i].boxplot(df_list2[i].values.T)
        axes[1, i].set_title(f'{titles[i]} - {years[1]}')
        axes[1, i].set_ylabel('Value')

    plt.show()


def plot_time_series(df, title):
    # Set the first column as the index
    df.set_index(df.columns[0], inplace=True)

    # Transpose the dataframe for proper plotting
    df_transposed = df.transpose()

    # Plot the time series
    plt.figure(figsize=(12, 8))
    df_transposed.plot(kind='line', marker='o')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
    

def calculate_indicator_correlations(df1, df2, df3):
    # Extract country names and numerical values
    country_names = df1.index
    data1 = df1.iloc[:, :].astype(float)
    data2 = df2.iloc[:, 1:].astype(float)
    data3 = df3.iloc[:, 1:].astype(float)

    columns = ['Country Name', 'Access to Electricity vs Agricultural Land', 
               'Access to Electricity vs CO2 Emissions', 'Agricultural Land vs CO2 Emissions']
    # Initialize an empty dataframe to store correlations
    result_df = pd.DataFrame(columns = columns)

    # Loop through each row and calculate correlations
    for i in range(len(data1)):
        row1 = df1.iloc[i, :]
        row2 = df2.iloc[i, :]
        row3 = df3.iloc[i, :]

        correlation1_2 = row1.corr(row2)
        correlation1_3 = row1.corr(row3)
        correlation2_3 = row2.corr(row3)

        # Append the correlations to the result dataframe
        result_df = result_df.append({'Country Name': country_names[i],
                          'Access to Electricity vs Agricultural Land': correlation1_2,
                          'Access to Electricity vs CO2 Emissions': correlation1_3,
                          'Agricultural Land vs CO2 Emissions': correlation2_3}, ignore_index=True)
        
    return result_df


# Data files
access_to_electricity_filename = 'access_to_electricity.csv'
agricultural_land_filename = 'agricultural_land.csv'
co2_emissions_filename = 'co2_emissions.csv'

# Select a few countries for the analysis.
selected_countries = [20, 26, 117, 174, 185]

df_access_to_electricity, df_access_to_electricity_transpose = read_worldbank_data(access_to_electricity_filename, selected_countries)
df_agricultural_land, df_agricultural_land_transpose = read_worldbank_data(agricultural_land_filename, selected_countries)
df_co2_emissions, df_co2_emissions_transpose = read_worldbank_data(co2_emissions_filename, selected_countries)

# Explore statistical properties
print("Statistical Properties of Access to Electricity:")
print(df_access_to_electricity_transpose.describe())

print("\nStatistical Properties of Agricultural Land:")
print(df_agricultural_land_transpose.describe())

print("\nStatistical Properties of CO2 Emissions:")
print(df_co2_emissions_transpose.describe())

# Plot Box-Plot
plot_side_by_side_boxplots_matplotlib([df_access_to_electricity.iloc[:, 1], 
                                       df_agricultural_land.iloc[:, 1], 
                                       df_co2_emissions.iloc[:, 1]],
                                      [df_access_to_electricity.iloc[:, -1], 
                                       df_agricultural_land.iloc[:, -1], 
                                       df_co2_emissions.iloc[:, -1]],
                                      ['1991', '2020'],
                                      ['Access to Electricity', 
                                       'Agricultural Land', 
                                       'CO2 Emissions'])

# Plot Time-series
plot_time_series(df_access_to_electricity, '% of population having access to electricity')
plot_time_series(df_agricultural_land, 'Agricultural land (% of land area)')
plot_time_series(df_co2_emissions, 'CO2 Emission level')



# Compute and display pair-wise correlations
correlation_results = calculate_indicator_correlations(
    df_access_to_electricity,
    df_agricultural_land,
    df_co2_emissions
)

# Display the results
print(correlation_results)


