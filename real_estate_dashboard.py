import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Generate sample market data
np.random.seed(42)
areas = ["Northside", "Eastville", "South Park", "Lakeshore", "Hillcrest"]
months = pd.date_range(start="2022-01-01", periods=36, freq="M")

records = []
for area in areas:
    base_price = np.random.uniform(220000, 520000)
    base_rent = np.random.uniform(1200, 2800)
    for month_idx, month in enumerate(months):
        price = base_price * (1 + 0.003 * month_idx + np.random.normal(0, 0.01))
        rental_yield = np.clip(np.random.normal(5.4, 0.35), 3.2, 8.0)
        demand = np.clip(100 + 10 * np.sin(month_idx / 4.0) + np.random.normal(0, 8), 60, 150)
        supply = np.clip(70 + 8 * np.cos(month_idx / 5.0) + np.random.normal(0, 7), 40, 120)
        records.append({
            "month": month,
            "area": area,
            "price": round(price, 0),
            "rental_yield": round(rental_yield, 2),
            "demand": round(demand, 0),
            "supply": round(supply, 0),
            "rental_income": round(price * rental_yield / 100 / 12, 0),
        })

market_df = pd.DataFrame(records)

# Geographic sample coordinates for mapping
geo_data = pd.DataFrame([
    {"area": "Northside", "lat": 40.78, "lon": -73.96, "avg_price": market_df.query("area == 'Northside'")["price"].mean()},
    {"area": "Eastville", "lat": 40.70, "lon": -73.88, "avg_price": market_df.query("area == 'Eastville'")["price"].mean()},
    {"area": "South Park", "lat": 40.66, "lon": -73.99, "avg_price": market_df.query("area == 'South Park'")["price"].mean()},
    {"area": "Lakeshore", "lat": 40.75, "lon": -74.05, "avg_price": market_df.query("area == 'Lakeshore'")["price"].mean()},
    {"area": "Hillcrest", "lat": 40.73, "lon": -73.80, "avg_price": market_df.query("area == 'Hillcrest'")["price"].mean()},
])

# Visualizations
price_trend = px.line(
    market_df,
    x="month",
    y="price",
    color="area",
    title="House Price Trends by Area",
    labels={"price": "Average Price (USD)", "month": "Month"},
    template="plotly_white",
)

area_comparison = px.bar(
    market_df[market_df["month"] == market_df["month"].max()],
    x="area",
    y="price",
    color="area",
    title="Latest Area-wise Price Comparison",
    labels={"price": "Latest Average Price (USD)", "area": "Area"},
    template="plotly_white",
)

yield_chart = px.line(
    market_df,
    x="month",
    y="rental_yield",
    color="area",
    title="Rental Yield Trends",
    labels={"rental_yield": "Rental Yield (%)", "month": "Month"},
    template="plotly_white",
)

rental_income_chart = px.bar(
    market_df[market_df["month"] == market_df["month"].max()],
    x="area",
    y="rental_income",
    color="area",
    title="Current Rental Income by Area",
    labels={"rental_income": "Estimated Monthly Rental Income (USD)", "area": "Area"},
    template="plotly_white",
)

supply_demand = px.line(
    market_df,
    x="month",
    y=["demand", "supply"],
    color="area",
    title="Demand and Supply Trends",
    labels={"value": "Units", "month": "Month", "variable": "Series"},
    template="plotly_white",
)

location_map = px.scatter_mapbox(
    geo_data,
    lat="lat",
    lon="lon",
    size="avg_price",
    color="avg_price",
    hover_name="area",
    hover_data={"lat": False, "lon": False, "avg_price": True},
    title="Location Heat Map: Average Property Price",
    color_continuous_scale=px.colors.sequential.OrRd,
    size_max=35,
    zoom=10,
    center={"lat": 40.725, "lon": -73.95},
    mapbox_style="open-street-map",
)

# Build Dash app
app = Dash(__name__)
app.title = "Real Estate Market Trends"

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f5f6fa", "padding": "24px"},
    children=[
        html.H1("Real Estate Market Trends Dashboard", style={"textAlign": "center", "color": "#1f2937"}),
        html.P(
            "Interactive analysis of property prices, rental yields, demand and supply, and geographic heat maps.",
            style={"textAlign": "center", "color": "#4b5563", "maxWidth": "860px", "margin": "0 auto 24px"},
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr", "gap": "24px"},
            children=[
                dcc.Graph(figure=price_trend),
                dcc.Graph(figure=yield_chart),
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px"},
                    children=[dcc.Graph(figure=area_comparison), dcc.Graph(figure=rental_income_chart)],
                ),
                dcc.Graph(figure=supply_demand),
                dcc.Graph(figure=location_map),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
