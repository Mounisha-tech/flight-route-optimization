import streamlit as st
import networkx as nx

from backend import (load_data,
                     build_graph,
                     find_best_route,
                     draw_graph,
                     build_visual_graph_from_route,
                     format_time
                    )

# Page design 
st.set_page_config(page_title="⌯⌲ Flight Route Optimizer",layout="centered")

st.title("🛫 Flight Route Optimizer")
st.subheader("Student-friendly domestic flight route planner")

st.caption("Prices and durations are based on historical data and are for comaparision purposes only")


# Logic building 

original_df=load_data("data/Flight Data.xlsx")

# # criteria=selected_criteria
# filtered_df=original_df.loc[original_df.groupby(["source","destination"])[criteria].idxmin()]
# G=build_graph(filtered_df)

# path,cost=find_best_route(G,source,destination,criteria)

# Airports list
# airports=sorted(set(original_df["source"].tolist()+original_df["destination"].tolist()))

source_airports=sorted(original_df["source"].unique())
destination_airports=sorted(original_df["destination"].unique())

airport_code_map={
    "DEL":"Delhi",
    "BOM":"Mumbai",
    "MAA":"Chennai",
    "BLR":"Banglore",
    "CCU":"Kolkata",
    "COK":"Cochin",
    "HYD":"Hyderaabd",
    "LKO":"Lucknow"
}

with st.container():

    source=st.selectbox("Source City",source_airports)
    destination=st.selectbox("Destination City",destination_airports)

    criteria=st.radio(
        "Optimize by",
        ["price","time","distance"],
        horizontal=True
    )

    
    vacation_mode=st.toggle("Student Vacation Mode")

if st.button(" ✈ Find Best Route"):

    if source==destination:
        st.warning("Source and destination cannot be the same.")

    else:

        with st.spinner("Finding best route..."):


            # Apply vacation filter 
            working_df=original_df.copy()

            if vacation_mode:

                st.info("Showing routes based on historical student vacation months.")
                vacation_months=[5,6,12]
                working_df=working_df[working_df["month"].isin(vacation_months)]

            
            # building filtered data frame based on selected criteria
            filtered_df=working_df.loc[
                                        working_df.groupby(["source","destination"])[criteria].idxmin()
                                        ]
            
            G=build_graph(filtered_df)

            path,cost=find_best_route(G,source,destination,criteria)

            # selected_row=filtered_df[(filtered_df["source"]==source) & (filtered_df["destination"]==destination)].iloc[0]

            # route_str=selected_row["route"]

            
        
        if path:
            st.success("Best route found!")

            # Showing the flights that a passanger need to change 
            st.subheader("Optimal Travel Route (Cities) ")
            st.write(" ➡️ ".join(path))
            
            # Trip Summary 
            st.subheader("Trip Summary")

            if criteria=="price":
                st.write(f"💰 **Total Price:** ₹{cost:,}")
            elif criteria=="time":
                st.write(f" ⏱ **Total Travel Time:** {format_time(cost)} ")
            else:
                st.write(f"📏 **Total Distance:** {cost} km")


            st.write(f"🛑 **Stops:** {len(path)-2 if len(path)>2 else 0}")
            st.write(f"🧭 **Optimization Criteria:** {criteria.capitalize()}")

            st.divider()

            # Airport level visualization 

            vis_G=nx.DiGraph()

            for i in range(len(path)-1):

                segment_source=path[i]
                segment_dest=path[i+1]

                segment_rows=filtered_df[
                                (filtered_df["source"]==segment_source)
                                & (filtered_df["destination"]==segment_dest)
                ]

                if not segment_rows.empty:

                    route_str=segment_rows.iloc[0]["route"]
                    segment_graph=build_visual_graph_from_route(route_str)

                    vis_G=nx.compose(vis_G,segment_graph)
            
            airport_nodes=list(vis_G.nodes())

            # Airport route formatting 

            st.subheader("Actual Flight Path (Airports)")
            st.write(" ✈ ".join(airport_nodes))

            st.write("**Airport Codes:**")

            for code in airport_nodes:
                city=airport_code_map.get(code,"Unknown")
                st.write(f"{code} - {city}")
            st.caption(
                "Airport route shows the actual flight legs including intermediate stops."
            )

            st.divider()

            # Graph visualization 

            st.subheader("Flight Route Visualization")


            fig=draw_graph(vis_G)
            st.pyplot(fig)

            # fig=draw_graph(G,path)

            # selected_row=filtered_df[
            #     (filtered_df["source"]==source) &
            #     (filtered_df["destination"]==destination)
            # ].iloc[0]

            # route_str=selected_row["route"]

            # vis_G=build_visual_graph_from_route(route_str)

        
        else:
            st.error("No route found between selected cities")
