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
