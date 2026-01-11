import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def load_data(filepath):
    """Load and clean flight dataset"""
    df=pd.read_csv(filepath)
    return df


def build_graph(df):
    """Build directed graph from flight data"""
    G=nx.DiGraph()

    for _ ,row in df.iterrows():
        G.add_edge(row["source"],
                row["destination"],
                distance=row["distance"],
                time=row["time"],
                price=row["price"])
    return G
    

def find_best_route(G,source,destination,criteria):
    """Find shortest path based on selected criteria"""

    try:
        path=nx.shortest_path(G,source=source,
                            target=destination,weight=criteria)
        total_cost=0
        for i in range(len(path)-1):
            total_cost+=G[path[i]][path[i+1]][criteria]
        
        return path,total_cost
    
    except nx.NetworkXNoPath:
        return None,None


def draw_graph(G,path=None):
    """Draw graph and highlight best path"""
    plt.figure(figsize=(10,6))

    pos=nx.spring_layout(G,seed=42)
    
    nx.draw_networkx(G,pos,with_labels=True,node_color="lightblue",edge_color="gray",node_size=2000,font_size=9)

    if path:
        path_edges=list(zip(path,path[1:]))
        nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color="red",width=3)

    return plt


if __name__=="__main__":
     df=load_data("data/flights.csv")
     G=build_graph(df)

     source="Delhi"
     destination="New York"
     criteria="distance"

     path,cost=find_best_route(G,source,destination,criteria)

     if path:
        print(f"\nBest route based on {criteria}")
        print(" -> ".join(path))
        print(f"Total {criteria}:{cost}")
     else:
        print("No path exists.")