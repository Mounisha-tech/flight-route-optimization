import streamlit as st
from backend import load_data,build_graph,find_best_route,draw_graph

st.set_page_config(page_title="⌯⌲ Flight Route Optimizer",layout="centered")

st.title("🛫 Flight Route Optimizer")

df=load_data("data/flights.csv")
G=build_graph(df)

Source_airports=sorted(set(df["source"]).union(set(df["destination"])))
Destination_airports=sorted(set(df["destination"]).union(set(df["source"])))

source=st.selectbox("Select Source Airport",Source_airports)
destination=st.selectbox("Select destination airport",Destination_airports)

criteria=st.selectbox("Optimization Criteria",["distance","time","price"])

if st.button("Find Best Route"):
    if source==destination:
        st.warning("Source and Destination cannot be the same.")
    else:
        path,cost=find_best_route(G,source=source,destination=destination,criteria=criteria)

        if path:
            st.success("Best Route Found!")
            st.write("➡️".join(path))
            st.write(f"**Total {criteria} :** {cost}")

            fig=draw_graph(G,path)
            st.pyplot(fig)

        else:
            st.error("No route exists between selected airports")
