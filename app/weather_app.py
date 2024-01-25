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

df= pd.read_csv('../data/climate.csv')
df_2 =pd.read_csv('../data/iso_codes.csv')
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
app =dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

# set app layout

app.layout = html.Div([html.H1('Weather', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                       html.Div(d_table),
])


d_table = dash_table.DataTable(df_egypt.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_egypt.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })
app.layout = html.Div([html.H1('Weather', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                       html.Div([html.Div('Egypt', style={'backgroundColor': 'coral', 'color': 'white', 'width': "Germany"}),d_table])
])


df_countries = merged_df_country[merged_df_country['country'].isin(['Egypt', 'Morocco', 'Algeria'])]
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

app.layout = html.Div([html.H1('Weather', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                       html.Div([html.Div('Egypt', 
                                          style={'backgroundColor': 'coral', 'color': 'white', 'width': "Egypt"}),d_table, graph])

                    
])


    
fig2 = px.line(df_egypt, x='month', y='avg_temp_country', height=300, title="Average temperature in Egypt", markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)
app.layout = html.Div([html.H1('Analysis of Egypt', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H3("Using the gapminder data we take a look at Germany's profile"),
                       html.Div([html.Div('Egypt', 
                                          style={'backgroundColor': 'coral', 'color': 'white',
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 d_table, graph2, graph])

                    
])



fig3 = px.choropleth(df_countries, locations='alpha-3', 
                    projection='natural earth', animation_frame="month",
                    scope='africa',   #we are adding the scope as europe
                    color='avg_temp_country', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.ice)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )

# here we needed to change the geo color also to make the world black

graph3 = dcc.Graph(figure=fig3)
app.layout = html.Div([html.H1('Temperature Analysis of Egypt', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("We take a look at Egypt's profile"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('Egypt', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 d_table, graph,  graph2, graph3])

                    
])



fig4= px.scatter_mapbox(df_countries, 
                        lat="lat", lon="lon", 
                        hover_name="country", 
                        # start location and zoom level
                        zoom=4, 
                        mapbox_style='carto-positron')
fig4.update_layout(width=1000, height=600,
coloraxis_colorbar=dict(title='Average Temperature (°C)'),
coloraxis=dict(cmin=df_countries['avg_temp'].min(), cmax=df_countries['avg_temp'].max()),
)
fig4 = fig4.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
graph4 = dcc.Graph(figure=fig4)
app.layout = html.Div([html.H1('Temperature Analysis of Egypt', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("We take a look at Egypt's profile"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('Egypt', 
                                          style={'backgroundColor': '#636EFA', 'color': 'black', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 d_table, graph,  graph2, graph3, graph4])

                    
])



color_continuous_scale=px.colors.sequential.Plasma
fig5 = px.choropleth(
    data_frame= df_countries,
    locations="alpha-3",
    color="avg_temp",
    hover_name="alpha-3",
    animation_frame="month",
    projection='natural earth',
    title='Temperature Over Time'
)
fig5.update_layout(width=1000, height=600,
coloraxis_colorbar=dict(title='Average Temperature (°C)'),
coloraxis=dict(cmin=merged_df_country['avg_temp'].min(), cmax=merged_df_country['avg_temp'].max()),
)
fig5.write_html('temperature1.html', include_plotlyjs='cdn')
graph5 = dcc.Graph(figure=fig5)

fig5 = fig5.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
app.layout = html.Div([html.H1('Temperature Analysis of Egypt', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("We take a look at Egypt's profile"), 
                                style={'marginLeft': 50, 'marginRight': 25,'color': '#636EFA'}),
                       html.Div([html.Div('Egypt', 
                                          style={'backgroundColor': '#636EFA', 'color': 'black', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 d_table, graph,  graph2, graph3, graph4, graph5])

                    
])


raph = dcc.Graph()


app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

radio= dcc.RadioItems(id="countries",options=['Egypt', 'Morocco', 'Algeria'], value="Egypt", 
                      inline=True, style ={'paddingLeft': '30px'})


app.layout = html.Div([html.H1(' Analysis of Egypt', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("We take a look at Egypt's profile"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('Egypt', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 d_table, radio, graph,  graph2, graph3])
                      ])


@callback(
    Output(graph, "figure"), 
    Input("countries", "value"))

#let's also define discrete colors for each bar, so we can distinguish them easily, everytime we change our selection

def update_bar_chart(countries): 
    mask =merged_df_countries["country"]==(countries)
    fig =px.bar(merged_df_countries[mask], 
             x='month', 
             y='avg_temp_country',  
             color='country',
             color_discrete_map = {'Egypt': '#7FD4C1', 'Morocco': '#8690FF', 'Algeria': '#F7C0BB'},
             barmode='group',
             height=300, title = "Egypt vs Morocco & Algeria",)
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

    return fig 



if __name__ == "__main__":
    app.run_server()