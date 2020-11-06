import pandas as pd
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, WheelZoomTool, Div
from bokeh.io import curdoc
from bokeh.transform import cumsum
from bokeh.layouts import gridplot

# Output to file
output_file('result.html', 
            title='result')

# 3a: What was the number of new coronavirus cases in California on a particular day in August
# Import state data for 3a
state_total = pd.read_csv("latimes-state-totals.csv", parse_dates=['date'])
#state_total.info(verbose=True)

# Filter out August for 3a
start_date = "2020-08-01"
end_date = "2020-08-31"
after_start_date = state_total["date"] >= start_date
before_end_date = state_total["date"] <= end_date
between_two_dates = after_start_date & before_end_date
filtered_month = state_total.loc[between_two_dates]
# New cases in August
new_cases = filtered_month[["date","new_confirmed_cases"]]

new_case_fig = figure(x_axis_type='datetime',toolbar_location="below",
             title='New Cases in August in California',
             plot_width=1200, plot_height=800,
             x_axis_label='Date', y_axis_label='New Cases in August in California')

# Render the new cases as line with dot
new_case_fig.line('date', 'new_confirmed_cases', 
         color='orange', legend='New Cases', 
         source=new_cases)
new_case_fig.circle('date', 'new_confirmed_cases', 
           fill_color="orange", legend='New Cases',
           size=12, source=new_cases)

new_case_fig.add_tools(HoverTool(tooltips=[
    ("Date: ","@date{%m-%d-%Y}"),
    ("New Cases: ", "@new_confirmed_cases")],
    formatters = {'@date': 'datetime'}))

new_case_fig.toolbar.active_scroll = new_case_fig.select_one(WheelZoomTool)

# Move the legend to the upper left corner
new_case_fig.legend.location = 'top_left'
new_case_fig.title.text_font_size = "25px"
# Add to tab
new_case_tab = Panel(child=new_case_fig, title="New Cases in August in California")


# 3b: For a particular day, what is the %percent cases by race 
#    compared to their representation in the general population

# Import race data for 3 b and 3 c
race = pd.read_csv("cdph-race-ethnicity.csv", parse_dates=['date'])
race = race[race['age']=="all"]
race = race[["date", "race", "confirmed_cases_total", "confirmed_cases_percent",
             "deaths_total", "deaths_percent", "population_percent"]]

# Isolate the data for the different race
asian_df = race[race["race"] == "asian"]
black_df = race[race["race"] == "black"]
cdph_other_df = race[race["race"] == "cdph-other"]
latino_df = race[race["race"] == "latino"]
other_df = race[race["race"] == "other"]
white_df = race[race["race"] == "white"]

# Create a ColumnDataSource object for each race
asian = ColumnDataSource(asian_df)
black = ColumnDataSource(black_df)
cdph_other = ColumnDataSource(cdph_other_df)
latino = ColumnDataSource(latino_df)
other = ColumnDataSource(other_df)
white = ColumnDataSource(white_df)

# Create and configure the figure
race_fig = figure(x_axis_type='datetime',toolbar_location="below",
             title='Confirmed Case Percentage by Race',
             plot_width=1200, plot_height=800,
             x_axis_label='Date', y_axis_label='Cases Percentage')

# Render the race as line with dot
def plot_race(data,color_it,legend_it):
    race_fig.line('date', 'confirmed_cases_percent', line_width= 3,
         color=color_it, legend=legend_it, 
         source=data)
    race_fig.circle('date', 'confirmed_cases_percent', 
           fill_color=color_it, legend=legend_it, 
           size=12, source=data)
plot_race(asian,'#FFC300','Asian')
plot_race(black,'#98947E','Black')
plot_race(cdph_other,'#FFBDF9','cdph_other')
plot_race(latino,'#FF6666','Latino')
plot_race(other,'#58E6BF','Other')
plot_race(white,'#77B1FF','White')

race_fig.add_tools(HoverTool(tooltips=[
    ("Race: ","@race"),
    ("Date: ","@date{%m-%d-%Y}"),
    ("Confirmed cases: ", "@confirmed_cases_total"),
    ("Confirmed cases percentage: ", "@confirmed_cases_percent{0.000} %"),
    ("Race percentage of the population: ", "@population_percent{0.000} %")
    ],
    formatters = {'@date': 'datetime'}))

race_fig.toolbar.active_scroll = race_fig.select_one(WheelZoomTool)

# Move the legend to the upper left corner
race_fig.legend.location = 'top_left'
race_fig.title.text_font_size = "25px"
# Add to tab
race_tab = Panel(child=race_fig, title="Cases by Race in California")

# 3c: For a particular day, what is the %percent deaths by race
#    compared to their representation in the general population

# Create and configure the figure
death_fig = figure(x_axis_type='datetime',toolbar_location="below",
             title='Death Percentage by Race',
             plot_width=1200, plot_height=800,
             x_axis_label='Date', y_axis_label='Deaths Percentage')

def plot_race(data,color_it,legend_it):
    death_fig.line('date', 'deaths_percent', line_width= 3,
         color=color_it, legend=legend_it, 
         source=data)
    death_fig.circle('date', 'deaths_percent', 
           fill_color=color_it, legend=legend_it, 
           size=12, source=data)
plot_race(asian,'#FFC300','Asian')
plot_race(black,'#98947E','Black')
plot_race(cdph_other,'#FFBDF9','cdph_other')
plot_race(latino,'#FF6666','Latino')
plot_race(other,'#58E6BF','Other')
plot_race(white,'#77B1FF','White')

death_fig.add_tools(HoverTool(tooltips=[
    ("Race: ","@race"),
    ("Date: ","@date{%m-%d-%Y}"),
    ("Deaths: ", "@deaths_total"),
    ("Death totals percentage: ", "@deaths_percent{0.000} %"),
    ("Race percentage of the population: ", "@population_percent{0.000} %")
    ],
    formatters = {'@date': 'datetime'}))
death_fig.toolbar.active_scroll = death_fig.select_one(WheelZoomTool)

# Move the legend to the upper left corner
death_fig.legend.location = 'top_left'
death_fig.title.text_font_size = "25px"
# Add to tab
death_tab = Panel(child=death_fig, title="Deaths by Race in California")

div1 = Div(text="""
<p><strong>Name: </strong>Junbo Sheng</p>
<h1>Source for the data</h1>
<p><strong>Source Link: </strong><a target="_blank" href="https://github.com/datadesk/california-coronavirus-data">The Los Angeles Times' independent tally of coronavirus cases in California.</a></p>
<p><strong>Files used:</strong></p>
    <ol>
        <strong><li><a target="_blank" href="https://github.com/datadesk/california-coronavirus-data/blob/master/cdph-race-ethnicity.csv">latimes-state-totals.csv</a></strong></li>
        <p>The statewide total of cases and deaths logged by local public health agencies each day</p>
        <p><strong>Columns used: </strong></pi>
        <p><strong>new_confirmed_cases: </strong>the net change in confirmed cases over the previous date.</p>
        <strong><li><a target="_blank" href="https://github.com/datadesk/california-coronavirus-data/blob/master/latimes-state-totals.csv">cdph-race-ethnicity.csv</a></strong></li>
        <p>Statewide demographic data tallying race totals by age for both cases and deaths.</p>
        <p>Provided by the <a target="_blank" href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx">California Department of Public Health.</a></p>
        <p><strong>Columns used: </strong></pi>
        <p><strong>race: </strong>The race being tallied</pi>
        <p><strong>age: </strong>The age bracket being tallied, 0-17, 18+, 18-34, 35-49, 50-64, 65-79, 80+, all, I used "all" for the graph.</p>       
        <p><strong>confirmed_cases_total: </strong>The cumulative number of confirmed coronavirus case amoung this race and age at that time.</p>
        <p><strong>confirmed_cases_percent: </strong>The case totals percentage of the total in this age bracket.</p>
        <p><strong>deaths_total: </strong>The cumulative number of deaths case amoung this race and age at that time.</p>
        <p><strong>deaths_percent: </strong>The death totals percentage of the total in this age bracket.</p>
        <p><strong>population_percent: </strong>The race's percentage of the overall state population in this age bracket.</p>
    </ol>
<h1>Date of last update</h1>
<p>I downloaded the data from the source on <strong>November 5, 2020</strong>.</p>
<h1>Click tab to view different chart</h1>
<p><strong>Scroll the wheel on the chart to zoom</strong></p>
<p><strong>Hover over the dot to see the detailed data</strong></p>
<p><strong>No record if there is no dot on that day</strong></p>
""")

# Tabs
tabs = Tabs(tabs=[ new_case_tab, race_tab, death_tab ])
layout = gridplot([[div1],[tabs]])
#show(layout)
curdoc().add_root(layout)