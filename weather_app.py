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
df_countries = merged_df_country[merged_df_country['country'].isin(['Egypt', 'Morocco', 'Algeria', 'Italy'])]
df_countries = df_countries[['country','alpha-3','month', 'avg_temp_country', 'avg_max_temp', 'avg_min_temp', 'lat', 'lon']]
df_countries_monthly = df_countries.groupby(['country', 'month']).agg({
    'avg_temp_country': 'mean', 'avg_temp_country': 'max','avg_min_temp':'min'
}).reset_index()
app =dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

d_table = dash_table.DataTable(df_countries.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_countries.columns],
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

fig4= px.scatter_mapbox(df_countries, 
                        lat="lat", lon="lon", 
                        hover_name="country", 
                        # start location and zoom level
                        zoom=4, 
                        mapbox_style='carto-positron')
fig4.update_layout(width=1000, height=600,
coloraxis_colorbar=dict(title='Average Temperature (°C)'),
coloraxis=dict(cmin=df_countries['avg_temp_country'].min(), cmax=df_countries['avg_temp_country'].max()),
)
fig4 = fig4.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )
graph4 = dcc.Graph(figure=fig4)


app.layout = html.Div([html.H1('Weather', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                       html.Div([html.Div('Egypt', style={'backgroundColor': 'coral', 'color': 'white', 'width': "Germany"}),d_table, graph, graph2, graph3, graph4])
])

color_continuous_scale=px.colors.sequential.Plasma
fig5 = px.choropleth(
    data_frame= df_countries,
    locations="alpha-3",
    color="avg_temp_country",
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



if __name__ == '__main__':
     app.run_server(port= 8090)

















