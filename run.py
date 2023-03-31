from pandas import read_csv
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

df_g = read_csv("graph.csv")
df_v = read_csv("nodes.csv")

G = nx.Graph()

pos = {}
for row in df_v.iloc:
    v, x, y = list(row)
    pos[int(v)] = (x, y)
    G.add_node(v, x=x, y=y)

for row in df_g.iloc:
    u, v, w = list(row)
    w = max(1, round(100 / w))
    G.add_edge(int(v), int(u), weight=w)


gravity = sum(df_v.x) / len(df_v.x), sum(df_v.y) / len(df_v.y)


def dist(p1, p2):
    from math import hypot

    x1, y1 = p1
    x2, y2 = p2
    return hypot(x1 - x2, y1 - y2)


def draw_mid(G, d):
    mid = [v.source for v in df_v.iloc if dist(gravity, (v.x, v.y)) < d]
    H = nx.induced_subgraph(G, mid)
    nx.draw(H, nodelist=mid, pos=pos, node_size=5, node_color="black")
    plt.show()


def remove_pendants(X):
    print(len(X.nodes()))
    changed = True
    while changed:
        changed = False
        for v in X.nodes():
            if nx.degree(X, v) <= 1:
                X.remove_node(v)
                print(len(X.nodes()))
                changed = True
                break
    return X


DIST = 800

mid = [v.source for v in df_v.iloc if dist(gravity, (v.x, v.y)) < DIST]
H = remove_pendants(nx.induced_subgraph(G, mid).copy())
assert min([nx.degree(H, v) for v in H.nodes()]) >= 2
nx.write_gml(H, "city.gml")
