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

    df=df.rename(columns={"source":"source",
                          "destination":"destination",
                          "duration":"time","price":"price"})

    df=df[["source","destination","time","price"]]

    df["time"]=df["time"].apply(convert_duration_to_minutes)
    df=df.dropna()

    df["price"]=df["price"].astype(int)
    df["time"]=df["time"].astype(int)
    df["distance"]=((df["time"]/60)*750).astype(int) #avg flight speed=750kmph

    return df

def build_graph(df):
    """Builds graph with the cleaned data"""
    G=nx.DiGraph()

    for _,row in df.iterrows():
        G.add_edge(row["source"],row["destination"],time=row["time"],price=row["price"],distance=row["distance"])

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
    """Plot the given route"""
    plt.figure(figsize=(10,6))

    pos=nx.spring_layout(G,seed=42)

    nx.draw(G,pos,with_labels=True,node_color="lightblue",edge_color="lightgray",node_size=1200,font_size=9)

    if path:
        path_edges=list(zip(path,path[1:]))
        nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color="red",width=3)
    
    return plt

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

     
         
