
import dash
from dash import Dash, html,dcc
import plotly.express as px
import pandas as pd
import plotly.express as px


from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
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
df_countries = merged_df_country[merged_df_country['country'].isin(['Egypt', 'Morocco', 'Algeria'])]

app =dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])
server = app.server
d_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in merged_df_country.columns],
    data=merged_df_country.to_dict('records'),
    style_data={'color': 'white', 'backgroundColor': 'black'},
    style_header={'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black', 'fontWeight': 'bold'}
)
# Create figures for demonstration
color_continuous_scale = px.colors.sequential.Plasma
fig_1 = px.choropleth(
    data_frame=df_countries,
    locations="alpha-3",
    color="avg_temp_country",
    locationmode='ISO-3',
    color_continuous_scale=px.colors.sequential.Jet,
    hover_name="country",
    animation_frame="month",
    projection='natural earth',
    title='Yearly Average Temperature Variations in Major Cities'
)
fig_1 = fig_1.update_layout(
    plot_bgcolor="#222222", paper_bgcolor="#222222", geo_bgcolor="#222222", font_color="White", width=1050, height=600,
    coloraxis_colorbar=dict(title='Average Temperature (°C)'),
    coloraxis=dict(cmin=merged_df_country['avg_temp_country'].min(), cmax=merged_df_country['avg_temp_country'].max()),
)
graph1 = dcc.Graph(id='graph1', figure=fig_1, style={'border': '3px solid #636EFA'})
fig_2 = px.line(
    merged_df_country, x='month', y='avg_temp_country', height=300,
    title='Monthly average temperature overview', markers=True
)
fig_2 = fig_2.update_layout(plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="White")
graph2 = dcc.Graph(id='graph2', figure=fig_2, style={'backgroundColor': 'black', 'border': '3px solid #636EFA'})
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
# Create dropdown options from unique cities in the DataFrame
dropdown_options_countries = [{'label': country, 'value': country} for country in merged_df_country['country'].unique()]
app.layout = html.Div([
    html.H1('Yearly Weather Patterns in Major Cities', style={'textAlign': 'center', 'color': '#636EFA'}),
    html.Div(html.P("Overview of Weather fluctuations using Weather API Data"),
             style={'marginLeft': 50, 'marginRight': 25}),
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=dropdown_options_countries,
            value=dropdown_options_countries[0]['value'],
            multi=False,
            style={'width': '50%', 'marginLeft': 'auto', 'marginRight': 'auto'}
        ),
        html.Div(id='selected-country-info'),
        d_table,
        graph1,
        graph2
    ])
])
# Define callback functions to update the table and graphs based on dropdown selection
@app.callback(
    Output('selected-country-info', 'children'),
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Input('dropdown_options_countries', 'value')
)
def update_data(selected_country):
    # Filter the DataFrame based on the selected city
    filtered_data = merged_df_country[merged_df_country['country'] == selected_country]
    # Display selected city information
    info_text = f'Selected Country: {selected_country}'
    # Display filtered table
    table_data = filtered_data.to_dict('records')
    table_columns = [{"name": i, "id": i} for i in filtered_data.columns]
    # Display filtered graphs
    fig_1 = px.choropleth(
        data_frame=filtered_data,
        locations="alpha-3",
        color="avg_temp_country",
        locationmode='ISO-3',
        color_continuous_scale=px.colors.sequential.Jet,
        hover_name="country",
        animation_frame="month",
        projection='natural earth',
        title=f'Yearly Average Temperature Variations in {selected_city}'
    )
    fig_1 = fig_1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", geo_bgcolor="#222222", font_color="White", width=1050, height=600,
        coloraxis_colorbar=dict(title='Average Temperature (°C)'),
        coloraxis=dict(cmin=filtered_data['avg_temp_country'].min(), cmax=filtered_data['avg_temp_country'].max()),
    )
    graph1 = dcc.Graph(id='graph1', figure=fig_1, style={'border': '3px solid #636EFA'})
    fig_2 = px.line(
        filtered_data, x='month', y='avg_temp_country', height=300,
        title=f'{selected_city} monthly average temperature overview', markers=True
    )
    fig_2 = fig_2.update_layout(plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="White")
    graph2 = dcc.Graph(id='graph2', figure=fig_2, style={'backgroundColor': 'black', 'border': '3px solid #636EFA'})
    return info_text, table_data, table_columns, fig_1, fig_2
if __name__ == '__main__':
    app.run_server(port=8097)



















