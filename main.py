from flask import Flask, render_template
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
# Dash with a custom route to pointing to '/import.html/'
dash_app = Dash(__name__, server=app, url_base_pathname='/import.html/')
dash_app.title = 'DVI - Datasets' #custom title

# Sample data for demonstration
afri_data = px.data.gapminder().query("year==2007").query("continent=='Africa'")
asia_data = px.data.gapminder().query("year==2007").query("continent=='Asia'")

# Initial figures
fig_afri = px.scatter(afri_data, x="lifeExp", y="gdpPercap", size="pop", color="lifeExp", hover_name="country",
                      title="Africa's GDP & Life Expectancy.")
fig_asia = px.scatter(asia_data, x="lifeExp", y="gdpPercap", size="pop", color="lifeExp", hover_name="country",
                      title="Asia's GDP & Life Expectancy.")

# Initial slider values
initial_year = 2007

dash_app.layout = html.Div([

    dcc.Graph(id='graph-afri', figure=fig_afri),
    dcc.Slider(
        id='slider-afri',
        min=2000,
        max=2007,
        step=1,
        marks={year: str(year) for year in range(2000, 2024)},
        value=initial_year
    ),

    dcc.Graph(id='graph-asia', figure=fig_asia),
    dcc.Slider(
        id='slider-asia',
        min=2000,
        max=2007,
        step=1,
        marks={year: str(year) for year in range(2000, 2008)},
        value=initial_year
    )
])

# Define callback to update the Africa plot
@dash_app.callback(
    Output('graph-afri', 'figure'),
    [Input('slider-afri', 'value')]
)
def update_afri_plot(selected_year):
    filtered_data = px.data.gapminder().query(f"year=={selected_year}").query("continent=='Africa'")
    fig = px.scatter(filtered_data, x="lifeExp", y="gdpPercap", size="pop", color="lifeExp", hover_name="country",
                     title=f"Africa's GDP & Life Expectancy ({selected_year})")
    return fig

# Define callback to update the Asia plot
@dash_app.callback(
    Output('graph-asia', 'figure'),
    [Input('slider-asia', 'value')]
)
def update_asia_plot(selected_year):
    filtered_data = px.data.gapminder().query(f"year=={selected_year}").query("continent=='Asia'")
    fig = px.scatter(filtered_data, x="lifeExp", y="gdpPercap", size="pop", color="lifeExp", hover_name="country",
                     title=f"Asia's GDP & Life Expectancy ({selected_year})")
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
    app.run(host='0.0.0.0', port=5000, debug=True)
