import pandas as pd
import networkx as nx

df=pd.read_csv("data/flights.csv")
print("Dataset:")
print(df)

G=nx.DiGraph()

for _ ,row in df.iterrows():
    G.add_edge(row["source"],
               row["destination"],
               distance=row["distance"],
               time=row["time"],
               price=row["price"])


print("\nNodes in graph:")
print(G.nodes())

print("\nEdges with weights:")
for u,v,data in G.edges(data=True):
    print(f"{u} -> {v} | {data} ")


# Trying to take the below as input 
source="Delhi"
destination="London"
criteria="price"

try:
    path=nx.shortest_path(G,source=source,
                          target=destination,weight=criteria)
    total_cost=0
    for i in range(len(path)-1):
        total_cost+=G[path[i]][path[i+1]][criteria]
    
    print(f"\nBest route based on {criteria}")
    print(" -> ".join(path))
    print(f"Total {criteria}:{total_cost}")
except nx.NetworkXNoPath:
    print("No path exists between the selected airports")


