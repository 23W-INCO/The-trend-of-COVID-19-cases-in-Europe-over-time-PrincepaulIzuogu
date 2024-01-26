### The Distribution of Vaccines Across Countries in Europe between 2021-2023


### Description:

This repository contains static files like Index.html, styles.css and script.js which contains D3.js code for visualizing the distribution of vaccines across all the countries in Europe from 2021 to 2023 and it's trend. The data is sourced from [https://ourworldindata.org/covid-cases] which came in CSV format, i had to change it to json format and then convert it further to FHIR bundle (Immunization) which can be streamed by the user on the url generated from **test_fhir.py** but these data will not be saved because it is a very large dataset. Then my visualization uses a bar chart created with **D3.js** codes, with each country's flag on the tip of the bar providing an interactive and dynamic representation of the vaccination distributions across European countries and over time. i also use **GUNICORN** to export my port.

![Screenshot 2024-01-25 212958](https://github.com/PrincepaulIzuogu/The-Vaccine-Distributions-in-Europe/assets/123191250/387d1726-2a64-427e-b91b-1a000c48d4a5)

![Screenshot 2024-01-25 212628](https://github.com/PrincepaulIzuogu/The-Vaccine-Distributions-in-Europe/assets/123191250/968b43ab-cef9-44f0-bbc5-a5a20b0a8335)

![Screenshot 2024-01-25 213032](https://github.com/PrincepaulIzuogu/The-Vaccine-Distributions-in-Europe/assets/123191250/57560de5-a59b-4f43-bd61-90eafd27a88f)



## Key User Group
**The Director of European Centre for Disease Prevention and Control:** The Director of ECDC is responsible for leading the ECDC’s work in strengthening Europe’s defence against infectious disease.

## A Problem the The Director of ECDC Encouters
To specifically compare the distribution of covid-19 vaccinations of all the European countries between 2021-2023 in order TO HOWEVER; DETERMINE THE AMOUNT OF VACCINES THAT WILL BE DISTRIBUTED TO EACH EUROPEAN COUNTRIES IN JANUARY 2024.

## My Solution

This app is the solution to this problem, The Director of ECDC can use this interactive bar chart to easily understand the distribution of vaccines across different European countries within the specified period of time, she can choose any country she wants to view their statistics for the past years, she can compare 2 or more countries to not only compare there distributions over the past years, but also to check if the amount distributed to the countries matches their population and total cases there, so she can make ammendments for the next distribution in january 2024.
Due to the data i selected for this visualization, it is easier for the Director of ECDC to identify the following: 
    countries,
    date,
    total_cases,
    population,
    total_vaccinations,
    people_vaccinated,
    people_fully_vaccinated,
    total_vaccinations_per_hundred,
    people_vaccinated_per_hundred, and
    people_fully_vaccinated_per_hundred for each and every European countries.


## Speedup video of my App
https://github.com/PrincepaulIzuogu/The-Vaccine-Distributions-in-Europe/assets/123191250/01aaaeae-378a-4d3d-b728-2581c7b8fa6d

https://github.com/PrincepaulIzuogu/The-Vaccine-Distributions-in-Europe/assets/123191250/1939016c-32cf-4425-a06a-62e6f3957f72


## User Objectives

Users aim to:

- To identify or rather, calculate how the next distribution would be done.
- To compare and view the statistics of each European country and make changes for the next distribution in january 2024.
- Understand the overall distribution of vaccines in Europe.
- Compare the total cases to the amount of vaccine distributed across different countries or regions.
- To compare the vaccines distributed to each European countries to their population.
- compare the distributed vaccines to the total people fully vacinated.
- To compare and view the statistics of each European country and make changes for the next distribution in january 2024.

## Visualization Strategy and how the users can achieve task with this app effectively and efficiently

**1. Dashboard Overview:**

**Interactive Charts:** Explore the data visually with interactive charts that represent the total vaccinations across different locations.

**Summary Table:** The app displays a summary table showcasing crucial vaccination data such as total cases, population, total vaccinations, and more

**2. Navigating the Summary Table:**

The Summary Data Table provides an overview of critical vaccination metrics categorized by different locations.
Each row represents a location, and the columns show various vaccination statistics.
You can see the total number of cases, population, total vaccinations, people vaccinated, people fully vaccinated, and vaccination rates per hundred.

**3. Using the Interactive Charts:**

The interactive chart visualizes the total vaccinations across various locations.
Hover over each bar to see detailed information about the location, date range, and specific vaccination statistics.
Use the checkboxes to select specific locations for comparative analysis.

**4. How to Interact with the Date Slider:**

The date slider allows you to select a specific date range for viewing the vaccination data.
Move the slider to a particular date to visualize the vaccination statistics for that specific period.
Play or pause the slider to view the data as it progresses through time.

**5. Searching Specific Dates:**

Use the date range picker to specify start and end dates for a precise period.
Click the "Search" button to view the vaccination data within the selected date range.
6. Tips for Optimal Use:

To focus on specific locations, use the checkboxes to select or deselect locations in the charts for a clearer representation.
Experiment with the date slider and date range picker to explore data variations over time.

## Additional Features

- **Filtering Options:** Users can customize the timeframe for a more focused view.
- **Hover Information:** Interactive tooltips provide detailed information about each country's total cases.

## How to Use

1. Clone the repository.
2. Run in github codespaces
3. Explore the interactive choropleth map and customize it as needed.
