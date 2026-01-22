import streamlit as st
from backend import load_data,build_graph,find_best_route,draw_graph

st.set_page_config(page_title="⌯⌲ Flight Route Optimizer",layout="centered")

st.title("🛫 Flight Route Optimizer")
st.subheader("Student-friendly domestic flight route planner")

st.caption("Prices and durations are based on historical data and are for comaparision purposes only")

df=load_data("data/Flight Data.xlsx")
G=build_graph(df)

airports=sorted(set(df["source"].tolist()+df["destination"].tolist()))

with st.container():
    source=st.selectbox("Source City",airports)
    destination=st.selectbox("Destination City",airports)
    criteria=st.radio(
        "Optimize by",
        ["price","time","distance"],
        horizontal=True
    )

if st.button("Find Best Route"):
    if source==destination:
        st.warning("Source and destination cannot be the same.")
    else:
        with st.spinner("Finding best route..."):
            path,cost=find_best_route(G,source,destination,criteria)
        
        if path:
            st.success("Best route found!")
            st.write("➡️".join(path))
            st.write(f"**Total {criteria}:** {cost}")

            fig=draw_graph(G,path)
            st.pyplot(fig)
        
        else:
            st.error("No route found between selected cities")







