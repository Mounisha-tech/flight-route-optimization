import streamlit as st
import networkx as nx
import time

from backend import (
    load_data,
    build_graph,
    find_best_route,
    draw_graph,
    build_visual_graph_from_route,
    draw_route_map,
    format_time
)

# PAGE CONFIG

st.set_page_config(page_title="✈️ Flight Route Optimizer", layout="centered")

# Side bar section 

st.sidebar.title("✈ Flight Route Optimizer")

st.sidebar.markdown(
    """
### About 
 This application helps users find the **best flight route between Indian cities** using graph algorithms.
 
 It optimizes routes based on:
 
- 💰 **Price**
- ⏱ **Travel Time**
- 📏 **Distance**

The system analyzes historical flight data and computes the **optimal route using shortest path algorithms**.

---

### How to use 
1️⃣ Select **Source City**

2️⃣ Select **Destination City**

3️⃣ Choose optimization criteria  
- Price  
- Time  
- Distance

4️⃣ (Optional) Enable **Student Vacation Mode**

5️⃣ Click **Find Best Route**

The app will display:

✔ Optimal city route  
✔ Airport-level flight path  
✔ Trip summary  
✔ Route visualization
"""
)

st.sidebar.divider()

st.sidebar.markdown(
"""
### 🎓 Student Vacation Mode
Filters flights to those that operate during major **student travel periods**, specifically the **summer and winter vacation months (May, June, and December)**. This helps provide route suggestions that better reflect typical holiday travel patterns.
"""
)

st.markdown("""
<style>

.route-card{
padding:12px;
border-radius:8px;
font-size:18px;
text-align:center;
font-weight:600;
border:1px solid #E5E7E9;
}

.airport-card{
border:1px solid #E5E7E9;
padding:10px;
border-radius:6px;
text-align:center;
font-size:15px;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.title("✈ Flight Route Optimizer")

st.caption("Student-friendly domestic flight planner")

st.divider()

# LOAD DATA

original_df = load_data("data/Flight Data.xlsx")

source_airports = sorted(original_df["source"].unique())
destination_airports = sorted(original_df["destination"].unique())

airport_code_map = {
    "DEL":"Delhi",
    "BOM":"Mumbai",
    "MAA":"Chennai",
    "BLR":"Bangalore",
    "CCU":"Kolkata",
    "COK":"Cochin",
    "HYD":"Hyderabad",
    "LKO":"Lucknow"
}

# INPUT SECTION

col1,col2 = st.columns(2)

with col1:
    source = st.selectbox("Source City", source_airports)

with col2:
    destination = st.selectbox("Destination City", destination_airports)

criteria = st.radio(
    "Optimize by",
    ["price","time","distance"],
    horizontal=True
)

vacation_mode = st.toggle("Student Vacation Mode")

# ROUTE COMPUTATION

if st.button("Find Best Route"):

    if source == destination:
        st.warning("Source and destination cannot be the same.")

    else:

        loader = st.empty()

        loader.info("Finding the best route...")

        time.sleep(0.8)

        # Vacation filtering
        working_df = original_df.copy()

        if vacation_mode:

            st.info("Showing routes based on historical student vacation months.")

            vacation_months = [5,6,12]

            working_df = working_df[
                working_df["month"].isin(vacation_months)
            ]

        # Select best rows
        filtered_df = working_df.loc[
            working_df.groupby(["source","destination"])[criteria].idxmin()
        ]

        G = build_graph(filtered_df)

        path, cost = find_best_route(G, source, destination, criteria)

        loader.empty()

        if path:

            st.success("Best route found!")

            # CITY ROUTE

            st.subheader("Optimal Travel Route")

            route_text = " ✈ ".join(path)

            st.markdown(
                f"<div class='route-card'>{route_text}</div>",
                unsafe_allow_html=True
            )

            # TRIP SUMMARY

            st.subheader("Trip Summary")

            col1,col2,col3 = st.columns(3)

            with col1:

                if criteria == "price":
                    st.metric("Total Price", f"₹{cost:,}")

                elif criteria == "time":
                    st.metric("Travel Time", format_time(cost))

                else:
                    st.metric("Distance", f"{cost} km")

            with col2:

                stops = len(path)-2 if len(path)>2 else 0
                st.metric("Stops", stops)

            with col3:

                st.metric("Optimization", criteria.capitalize())

            st.divider()

            # BUILD VISUAL GRAPH

            vis_G = nx.DiGraph()

            for i in range(len(path)-1):

                segment_source = path[i]
                segment_dest = path[i+1]

                segment_rows = filtered_df[
                    (filtered_df["source"]==segment_source) &
                    (filtered_df["destination"]==segment_dest)
                ]

                if not segment_rows.empty:

                    route_str = segment_rows.iloc[0]["route"]

                    segment_graph = build_visual_graph_from_route(route_str)

                    vis_G = nx.compose(vis_G, segment_graph)

            airport_nodes = list(vis_G.nodes())

            # AIRPORT ROUTE

            st.subheader("Actual Flight Path")

            airport_route = " ✈ ".join(airport_nodes)

            st.markdown(
                f"<div class='route-card'>{airport_route}</div>",
                unsafe_allow_html=True
            )

            st.caption("Airport route shows intermediate stops taken by flights.")

            # AIRPORT CODE MEANING

            st.subheader("Airport Codes")

            cols = st.columns(len(airport_nodes))

            for i, code in enumerate(airport_nodes):

                city = airport_code_map.get(code,"Unknown")

                cols[i].markdown(
                    f"""
                    <div class='airport-card'>
                    <b>{code}</b><br>
                    {city}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

            # GRAPH VISUALIZATION

            st.subheader("Flight Route Visualization")

            map_fig=draw_route_map(airport_nodes)

            st.plotly_chart(map_fig)

        else:

            st.error("No route found between selected cities.")