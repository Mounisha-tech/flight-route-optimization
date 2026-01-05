import pandas as pd
import networkx as nx

def load_data(filepath):
    """Load and clean flight dataset"""
    df=pd.read_csv(filepath)
    # df.columns=df.columns.str.strip().str.lower()
    # print("Dataset:")
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

    # print("\nNodes in graph:")
    # print(G.nodes())

    # print("\nEdges with weights:")
    # for u,v,data in G.edges(data=True):
    #     print(f"{u} -> {v} | {data} ")

    return G
    


# Trying to take the below as input 
def find_best_route(G,source,destination,criteria):
    """Find shortest path based on selected criteria"""
# source="Delhi"
# destination="London"
# criteria="price"

    try:
        path=nx.shortest_path(G,source=source,
                            target=destination,weight=criteria)
        total_cost=0
        for i in range(len(path)-1):
            total_cost+=G[path[i]][path[i+1]][criteria]
        
        return path,total_cost
    
        # print(f"\nBest route based on {criteria}")
        # print(" -> ".join(path))
        # print(f"Total {criteria}:{total_cost}")

    except nx.NetworkXNoPath:
        return None,None
        # print("No path exists between the selected airports")


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