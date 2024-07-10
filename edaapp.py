import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Get the directory of the current script
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'webapp/nycAirBnb.csv')

# Load the CSV file
df = pd.read_csv(file_path)


# Sidebar widgets
st.sidebar.header('NYC AirBnb Dashboard')
borough = st.sidebar.radio('Select Borough:', 
    ('Bronx', "Brooklyn", "Queens", "Manhattan", "Staten Island"))

st.sidebar.header('About This Dashboard')
st.sidebar.write("Welcome to the NYC Airbnb Dashboard! This tool provides insights into Airbnb listings across New York City for the year 2019. Explore data by borough and neighborhood, analyze price distributions, review trends, and visualize listings on an interactive map. Discover detailed information to better understand the NYC Airbnb market.")

if borough == "Bronx":
    st.title('Bronx')
    data = df[df['borough'] == 'Bronx']
elif borough == 'Brooklyn':
    st.title('Brooklyn')
    data = df[df['borough'] == 'Brooklyn']
elif borough == 'Queens':
    st.title('Queens')
    data = df[df['borough'] == 'Queens']
elif borough == 'Manhattan':
    st.title('Manhattan')
    data = df[df['borough'] == 'Manhattan']
elif borough == 'Staten Island':
    st.title('Staten Island')
    data = df[df['borough'] == 'Staten Island']  

st.subheader("Explore Detailed Analysis Below: Insights on Prices, Room Types, and More for Your Selected Neighborhood")

# Extract unique neighborhoods
neighborhoods = data['neighborhood'].unique()

# Populate the selectbox with neighborhood names
selected_neighborhood = st.selectbox('Select a neighborhood:', options=neighborhoods) 

# Filter data based on the selected neighborhood
filtered_data = data[data['neighborhood'] == selected_neighborhood]

# Calculate the center of the neighborhood
neighborhood_center = filtered_data[['latitude', 'longitude']].mean()

# Create map
fig_map = px.scatter_mapbox(filtered_data, lat="latitude", lon="longitude", color="room_type",
                            size="price", hover_name="name", hover_data=["neighborhood", "price"],
                            title=f"Airbnb Listings in {selected_neighborhood}", 
                            mapbox_style="carto-positron", 
                            center={"lat": neighborhood_center['latitude'], "lon": neighborhood_center['longitude']},
                            zoom=12)  # Adjust zoom level as needed

st.plotly_chart(fig_map)



# Create histogram for room types in the selected neighborhood
fig = px.histogram(
    filtered_data, 
    x='price',
    title=f'Price Distribution in {selected_neighborhood}',
    labels={'price': 'Price (USD)', 'room_type': 'Room Type'},  # Axis labels
    nbins=30  # Adjust number of bins as needed
)

# Add black lines to histogram bars
fig.update_traces(marker_line_color='black', marker_line_width=1.5)

# Calculate the mean price of the selected neighborhood
mean_price = filtered_data['price'].mean()

# Add annotation for the mean
fig.add_annotation(
    x=mean_price,
    y=filtered_data['price'].value_counts().max(),
    text=f'Mean: {mean_price:.2f}',
    showarrow=False,
    bgcolor="rgba(255,255,255,0.8)",
    font=dict(size=12, color="black")
)

fig.update_layout(
    title={'text': f'Price Distribution in {selected_neighborhood}', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Price (USD)',
    yaxis_title='Count',
    legend_title='Room Type',
    template='plotly_white'
)
#st.plotly_chart(fig)

# Calculate mean price by room type for the selected neighborhood
mean_prices_room_type = filtered_data.groupby('room_type')['price'].mean().reset_index().round()

# Create bar chart for mean price by room type in the selected neighborhood
fig3 = px.bar(mean_prices_room_type, x='room_type', 
    y='price', 
    color = "room_type",
    labels={'room_type': 'Room Type', 'price': f'Mean Price in {selected_neighborhood}'},
    title=f'Mean Price by Room Type in {selected_neighborhood}')
#st.plotly_chart(fig3)

fig3.update_layout(
    title={'text': f'Mean Price by Room Type in {selected_neighborhood}', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Room Type',
    yaxis_title='Price',
    legend_title='Room Type',
    template='plotly_white'
)

#Room Type Distribution
fig_room_type_dist = px.pie(filtered_data, names='room_type', title= f'Room Type Distribution in {selected_neighborhood}')
#st.plotly_chart(fig_room_type_dist)


fig_room_type_dist.update_traces(textfont=dict(color='white', size=10, family='Arial'), textposition='inside')

fig_room_type_dist.update_layout(
    title={'text': f'Room Type Distribution in {selected_neighborhood}', 'x': 0.4, 'xanchor': 'center'},
    legend_title='Room Type'
)

#Tabs
tab3, tab4, tab5 = st.tabs(["Price Distrubution", "Room Type Distribution", "Avg Price by Room Type"])

with tab3:
    st.plotly_chart(fig, theme = "streamlit")
with tab4:
    st.plotly_chart(fig_room_type_dist, theme = "streamlit")
with tab5:
    st.plotly_chart(fig3, theme = "streamlit")


#Scatter Plot
fig2 = px.scatter(filtered_data, x="number_of_reviews", y="reviews_per_month", color = "room_type",
    title = f"Relationship Between Number of Reviews and Reviews Per Month by Room Type in {selected_neighborhood}")


fig2.update_layout(
    title={'text': f"Relationship Between Number of Reviews and Reviews Per Month by Room Type in {selected_neighborhood}", 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Number of Reviews',
    yaxis_title='Reviews Per Month',
    legend_title='Room Type'
)

st.plotly_chart(fig2)
