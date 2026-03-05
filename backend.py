import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

def convert_duration_to_minutes(duration):

    """Converts flight duration like '2h 50m' to total mintutes"""

    if pd.isna(duration):
        return None
    
    hours=0 
    minutes=0

    h=re.search(r"(\d+)h",duration)
    m=re.search(r"(\d+)m",duration)

    if h:
        hours=int(h.group(1))
    if m:
        minutes=int(m.group(1))
    
    return hours*60+minutes

def load_data(filepath):

    """Loads data and cleans it in required format"""

    df=pd.read_excel(filepath)

    df.columns=df.columns.str.strip().str.lower()

    df=df.rename(columns={
                          "duration":"time",
                          "price":"price",
                          "route":"route"})
    
    df["date_of_journey"]=pd.to_datetime(df["date_of_journey"],dayfirst=True)

    df["month"]=df["date_of_journey"].dt.month

    df=df[["source","destination","time","price","route","date_of_journey","month"]]

    airport_mapping={"New Delhi":"Delhi"}

    df["source"]=df["source"].replace(airport_mapping)
    df["destination"]=df["destination"].replace(airport_mapping)

    df["time"]=df["time"].apply(convert_duration_to_minutes)

    df=df.dropna()

    df["price"]=df["price"].astype(int)
    df["time"]=df["time"].astype(int)

    # approximate distance
    df["distance"]=((df["time"]/60)*750).astype(int) #avg flight speed=750 kmph

    return df

def build_graph(df):

    """Builds graph with the cleaned data"""

    G=nx.DiGraph()

    for _,row in df.iterrows():
        G.add_edge(row["source"],
                   row["destination"],
                   time=row["time"],
                   price=row["price"],
                   distance=row["distance"])

    return G

def find_best_route(G,source,destination,criteria):

    """Finds best route based on the given criteria from the given source to destination"""
    
    try:
        path=nx.shortest_path(G,source=source,target=destination,weight=criteria)

        total_cost=nx.shortest_path_length(G,source=source,target=destination,weight=criteria)
        
        return path,total_cost
    
    except nx.NetworkXNoPath:
        return None,None
    
def draw_graph(G,path=None):

    """Draw graph as a flight path"""

    plt.figure(figsize=(10,4))

    nodes=list(G.nodes())

    pos={node:(i,0) for i,node in enumerate(nodes)}

    nx.draw(G,pos,with_labels=True,node_color="lightblue",edge_color="lightgray",node_size=1800,font_size=10,font_weight="bold") 

    # if path:
    #     path_edges=list(zip(path,path[1:]))
    #     nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color="red",width=3)
    
    return plt


def build_visual_graph_from_route(route_str):
    """
    Builds a temporary graph using airport codes from route column.
    Example: 'DEK → LKO → BOM → COK'
    """

    route_nodes=route_str.split("→")
    route_nodes=[node.strip() for node in route_nodes]

    vis_G=nx.DiGraph()

    for i in range(len(route_nodes)-1):
        vis_G.add_edge(route_nodes[i],route_nodes[i+1])
    
    return vis_G

def format_time(minutes):
    hours=minutes//60
    mins=minutes%60

    if hours >0:
        return f"{hours} hr {mins} min"
    else:
        return f"{mins} min"

if __name__=="__main__":
     df=load_data("data/Flight Data.xlsx")
     
     G=build_graph(df)
     source="Mumbai"
     destination="Hyderabad"
     criteria="price"

     path,cost=find_best_route(G,source,destination,criteria)

     print("Path:",path)
     print("Cost",cost)

     if path:
         fig=draw_graph(G,path)
         fig.show()

     
         
