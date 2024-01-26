import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html,dcc
import plotly.express as px
import pandas as pd
import plotly.express as px

import pandas as pd 
import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dash_table
import dash_bootstrap_components as dbc

df= pd.read_csv('climate.csv')
df_2 =pd.read_csv('iso_codes.csv')
merged_df = df.merge( df_2, on= 'country', how = 'left')
merged_df['date'] = pd.to_datetime(merged_df['date'])

merged_df['day'] = merged_df['date'].dt.day
merged_df['month'] = merged_df['date'].dt.month
merged_df['year'] = merged_df['date'].dt.year
merged_df_country = merged_df.sort_values(by='month', ascending=True)
merged_df_country
merged_df_country['avg_temp_country']=merged_df_country.groupby(['country', 'month'])['avg_temp'].transform('mean')
merged_df_country =merged_df_country[merged_df_country['date'].dt.year == 2023]
df_egypt= merged_df_country[merged_df_country['country']=='Egypt']
d_table = dash_table.DataTable(df_egypt.to_dict('records'),
                                  [{"name": i, "id": i} for i in df.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })
df_countries = merged_df_country[merged_df_country['country'].isin(['Egypt', 'Morocco', 'Algeria', 'Italy'])]
df_countries = df_countries[['country','alpha-3','month', 'avg_temp_country', 'avg_max_temp', 'avg_min_temp', 'lat', 'lon']]
df_countries_monthly = df_countries.groupby(['country', 'month']).agg({
    'avg_temp_country': 'mean', 'avg_temp_country': 'max','avg_min_temp':'min'
}).reset_index()
app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
graph = dcc.Graph()
countries =df_countries['country'].unique().tolist() 

dropdown = dcc.Dropdown(['Morocco', 'Egypt', 'Algeria', 'Italy'], value=['Morocco', 'Egypt', 'Algeria','Italy'], 
                        clearable=False, multi=True, style ={'paddingLeft': '30px', 
                                                             "backgroundColor": "#222222", "color": "#222222"})
d_table = dash_table.DataTable(df_countries_monthly.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_countries_monthly.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })
fig = px.bar(df_countries, 
             x='month', 
             y='avg_temp_country',  
             color='country',
             barmode='group',
             height=300, title = "Egypt",)

fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

graph = dcc.Graph(figure=fig)

fig2 = px.line(df_countries, x='month', y='avg_temp_country',color= 'country', height=300, title="Average temperature in Egypt", markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)

fig3 = px.choropleth(df_countries, locations='alpha-3', 
                    projection='natural earth', animation_frame="month",
                    scope='africa',   #we are adding the scope as europe
                    color='avg_temp_country', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.ice)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )


graph3 = dcc.Graph(figure=fig3)

app.layout = html.Div([html.H1('Weather Analysis', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("We take a look at the weather"), 
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
             x='month', 
             y='avg_temp_country',  
             color='country',
             barmode='group',
             height=300, title = "Morocco vs Egypt & Algeria",)
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    fig2 = px.line(df_countries[mask], x='month', y='avg_temp_country', color='country', height=300, title="Average Temperature in Morocco, Egypt  & Algeria", markers=True)


    fig2.update_layout(
    plot_bgcolor="#222222", 
    paper_bgcolor="#222222", 
    font_color="white"
    )

    graph2 = dcc.Graph(figure=fig2)

    fig3 = px.choropleth(df_countries[mask], locations='alpha-3', 
                    projection='natural earth', animation_frame="month",
                    scope='africa',
                    color='avg_temp_country', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.Plasma)

    fig3 = fig3.update_layout(width=1000, height=600,
    coloraxis_colorbar=dict(title='Average Temperature (°C)'),
    coloraxis=dict(cmin=df_countries[mask]['avg_temp_country'].min(), cmax=df_countries[mask]['avg_temp_country'].max(),
    ))

    fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222")

    graph3 = dcc.Graph(figure=fig3)
    return fig, fig2, fig3

if __name__ == "__main__":
    app.run_server(port=8099)
