import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def graph_flights(df):
    if df.empty:
        st.info("No data to display for the current filters.")
        return

    df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'], errors='coerce')
    df['day_of_week'] = df['departure_scheduled'].dt.day_name()
    df['flight_date'] = df['departure_scheduled'].dt.date
    df['route'] = df['departure_airport'] + " → " + df['arrival_airport']

    # Top 10 delayed airports
    top_airports = df.groupby('departure_airport')['total_delay'].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_airports.values, y=top_airports.index, color="red", ax=ax1)
    ax1.set_title("Top 10 Delayed Airports (Average Delay in Minutes)")
    ax1.set_xlabel("Average Total Delay")
    ax1.set_ylabel("Airport")
    st.pyplot(fig1)

    # Average delays by day
    daily_delays = df.groupby('day_of_week')['total_delay'].mean()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=daily_delays.index, y=daily_delays.values, color="blue", ax=ax2)
    ax2.set_title("Average Delay by Day of Week")
    ax2.set_xlabel("Day of Week")
    ax2.set_ylabel("Average Total Delay")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

    # Top 10 airlines by number of flights
    top_airlines = df['airline_name'].value_counts().head(10)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_airlines.values, y=top_airlines.index, color="green", ax=ax3)
    ax3.set_title("Top 10 Airlines by Number of Flights")
    ax3.set_xlabel("Number of Flights")
    ax3.set_ylabel("Airline")
    st.pyplot(fig3)

    # Top 10 busiest departure airports
    busiest_airports = df['departure_airport'].value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=busiest_airports.values, y=busiest_airports.index, color="purple", ax=ax4)
    ax4.set_title("Top 10 Busiest Departure Airports")
    ax4.set_xlabel("Number of Flights")
    ax4.set_ylabel("Airport")
    st.pyplot(fig4)

    # Top 10 most common routes
    popular_routes = df['route'].value_counts().head(10)
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=popular_routes.values, y=popular_routes.index, color="orange", ax=ax5)
    ax5.set_title("Top 10 Most Common Routes")
    ax5.set_xlabel("Number of Flights")
    ax5.set_ylabel("Route")
    st.pyplot(fig5)

    # Flights per day
    flights_per_day = df.groupby('flight_date').size()
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=flights_per_day.index, y=flights_per_day.values, marker='o', ax=ax6)
    ax6.set_title("Flights per Day")
    ax6.set_xlabel("Date")
    ax6.set_ylabel("Number of Flights")
    ax6.tick_params(axis='x', rotation=45)
    st.pyplot(fig6)