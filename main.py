from flask import Flask, render_template
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
# Dash with a custom route to pointing to '/import.html/'
dash_app = Dash(__name__, server=app, url_base_pathname='/import.html/')
dash_app.title = 'DVI - Datasets' #custom title

# Sample data for demonstration
afri_gdp_data = px.data.gapminder().query("year==2007").query("continent=='Africa'")
afri_pop_data = px.data.gapminder().query("continent == 'Africa' and year == 2007 and pop > 2.e6")
euro_pop_data = px.data.gapminder().query("year==2007").query("continent=='Europe'")
trajectory = px.data.gapminder().query("country in ['Nigeria', 'Egypt']")


# Initial figures !!!!!
# African GDP
fig_afri_gdp = px.scatter(afri_gdp_data, x="lifeExp", y="gdpPercap", size="pop", color="lifeExp", hover_name="country",
                      title="Africa's GDP & Life Expectancy.")

# African population with update
fig_afri_pop = px.bar(afri_pop_data, x="country", y="pop", text_auto=".2s", hover_name="country",
                      title="Africa's population (2007)")
fig_afri_pop.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)

# European population
fig_euro_pop = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
fig_euro_pop.loc[fig_euro_pop['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig_euro_pop = px.pie(fig_euro_pop, values='pop', names='country', title='Population of European continent')

# trajectory of Nigeria to Egypt
fig_nig_egy = px.line(trajectory, x="lifeExp", y="gdpPercap", color="country", text="year")
fig_nig_egy.update_traces(textposition="bottom right")

# Initial slider values
initial_year = 2007

dash_app.layout = html.Div([

    dcc.Graph(id='graph-afri-gdp', figure=fig_afri_gdp),
    dcc.Slider(
        id='slider-afri-gdp',
        min=2000,
        max=2007,
        step=1,
        marks={year: str(year) for year in range(2000, 2008)},
        value=initial_year
    ),

    dcc.Graph(id='graph-afri-pop', figure=fig_afri_pop),
    dcc.Slider(
        id='slider-afri-pop',
        min=2000,
        max=2007,
        step=1,
        marks={year: str(year) for year in range(2000, 2008)},
        value=initial_year
    ),

    dcc.Graph(id='graph-euro-pop', figure=fig_euro_pop),
    dcc.Slider(
        id='slider-euro-pop',
        min=2000,
        max=2007,
        step=1,
        marks={year: str(year) for year in range(2000, 2008)},
        value=initial_year
    ),

    dcc.Graph(id='graph-nig-egy', figure=fig_euro_pop),
    dcc.Slider(
        id='slider-nig-egy',
        min=2000,
        max=2007,
        step=1,
        marks={year: str(year) for year in range(2000, 2008)},
        value=initial_year
    )
])

# Define callback to update the Africa plot
@dash_app.callback(
    Output('graph-afri-gdp', 'figure'),
    [Input('slider-afri-gdp', 'value')]
)
def update_afri_gdp_plot(selected_year):
    filtered_data = px.data.gapminder().query(f"year=={selected_year}").query("continent=='Africa'")
    fig = px.scatter(filtered_data, x="lifeExp", y="gdpPercap", size="pop", color="lifeExp", hover_name="country",
                     title=f"Africa's GDP & Life Expectancy ({selected_year})")
    return fig

# Define callback to update the Africa pop plot
@dash_app.callback(
    Output('graph-afri-pop', 'figure'),
    [Input('slider-afri-pop', 'value')]
)
def update_africa_pop_plot(selected_year):
    filtered_data = px.data.gapminder().query(f"year=={selected_year}").query("continent=='Africa'")
    fig = px.bar(filtered_data, x="country", y="pop", text_auto=".2s", hover_name="country", title=f"Africa's population ({selected_year})")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

# Define callback to update the Europe pop plot
@dash_app.callback(
    Output('graph-euro-pop', 'figure'),
    [Input('slider-euro-pop', 'value')]
)
def update_europe_pop_plot(selected_year):
    filtered_data = px.data.gapminder().query(f"year=={selected_year}").query("continent=='Europe'")
    fig = px.pie(filtered_data, x="country", y="pop", text_auto=".2s", hover_name="country", title=f"Population of "
                                                                          f"European continent ({selected_year})")
    return fig

# Define callback to update the trajectory of Nigeria to Egypt
@dash_app.callback(
    Output('graph-nig-egy', 'figure'),
    [Input('slider-nig-egy', 'value')]
)
def update_europe_pop_plot(selected_year):
    filtered_data = px.data.gapminder().query(f"year=={selected_year}").query("continent in ['Nigeria', 'Egypt']")
    fig = px.line(trajectory, x="lifeExp", y="gdpPercap", color="country", text="year", title=f"European continent ({selected_year})")
    fig.update_traces(textposition="bottom right")
    return fig





# Flask route
@app.route('/')
def index():
    return render_template('index.html')


# Dash route for the Dash application
@dash_app.server.route('/import.html/')
def render_dashboard():
    return dash_app.index()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
