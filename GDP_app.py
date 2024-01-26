import pandas as pd

# Fetch data from Gapminder
import pandas as pd 
import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc

df= px.data.gapminder()

df_countries =df[df['country'].isin(['Japan', 'Brazil', 'India', 'China'])]
df_countries.head()
app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
graph = dcc.Graph()
countries =df_countries['country'].unique().tolist() 

dropdown = dcc.Dropdown(['Japan', 'Brazil', 'India', 'China'], value=['Japan', 'Brazil', 'India', 'China'], 
                        clearable=False, multi=True, style ={'paddingLeft': '30px', 
                                                             "backgroundColor": "#222222", "color": "#222222"})
d_table = dash_table.DataTable(df_countries.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_countries.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })
fig = px.bar(df_countries, 
             x='year', 
             y='gdpPercap',  
             color='country',
             barmode='group',
             height=300, title = "countries",)

fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

graph = dcc.Graph(figure=fig)

fig2 = px.line(df_countries, x='year', y='gdpPercap',color= 'country', height=300, title="GDP per capita ", markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)

fig3 = px.choropleth(df_countries, locations='iso_alpha', 
                    projection='natural earth', animation_frame="year",
                    scope='africa',   #we are adding the scope as europe
                    color='gdpPercap', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.ice)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )


graph3 = dcc.Graph(figure=fig3)

app.layout = html.Div([html.H1('GDP Analysis', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("We take a look at the GDP"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('countries', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 d_table, dropdown, graph,  graph2, graph3])
                      ])
@callback(
    Output(graph, "figure"),
    Output(graph2, "figure"),
    Output(graph3, "figure"),
    Input(dropdown, "value"))

def update_bar_chart(countries): 
    mask = df_countries["country"].isin(countries) # coming from the function parameter
    fig =px.bar(df_countries[mask], 
             x='year', 
             y='gdpPercap',  
             color='country',
             barmode='group',
             height=300, title = "Japan, Brazil, China & India",)
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    fig2 = px.line(df_countries[mask], x='year', y='gdpPercap', color='country', height=300, title="GDP per capita in Japan, Brazil, China & India", markers=True)


    fig2.update_layout(
    plot_bgcolor="#222222", 
    paper_bgcolor="#222222", 
    font_color="white"
    )

    graph2 = dcc.Graph(figure=fig2)

    fig3 = px.choropleth(df_countries[mask], locations='iso_alpha',
                    projection='natural earth', animation_frame="year",
                    scope='world',
                    color='gdpPercap', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.Plasma)

    fig3 = fig3.update_layout(width=1000, height=600,
    coloraxis_colorbar=dict(title='GDP per Capita'),
    coloraxis=dict(cmin=df_countries[mask]['gdpPercap'].min(), cmax=df_countries[mask]['gdpPercap'].max(),
    ))

    fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222")

    graph3 = dcc.Graph(figure=fig3)
    return fig, fig2, fig3

if __name__ == "__main__":
    app.run_server(port=8097)
