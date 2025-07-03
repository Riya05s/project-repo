from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import networkx as nx
import os
import difflib

app = Flask(__name__, static_folder='.')
CORS(app)  

# —————— Load & build graph ——————
def load_graph(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {csv_path}")
    except pd.errors.ParserError:
        raise RuntimeError(f"Error parsing CSV: {csv_path}")

    G = nx.Graph()

    for _, row in df.iterrows():
        src = row["Source"]
        dst = row["Destination"]
        dist = row["Distance (km)"]
        risk = row["Risk Level"]
        weight = dist + risk * 50

        G.add_edge(src, dst, Distance=dist, Risk=risk, Weight=weight)

        G.nodes[src]["latitude"] = row["Source_Latitude"]
        G.nodes[src]["longitude"] = row["Source_Longitude"]
        G.nodes[src]["state"] = row["Source_State"]

        G.nodes[dst]["latitude"] = row["Destination_Latitude"]
        G.nodes[dst]["longitude"] = row["Destination_Longitude"]
        G.nodes[dst]["state"] = row["Destination_State"]

    return G

def kruskal_mst(G):
    parent = {n: n for n in G.nodes()}
    rank = {n: 0 for n in G.nodes()}

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        if rank[ru] < rank[rv]:
            parent[ru] = rv
        else:
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
        return True

    edges = sorted(G.edges(data=True), key=lambda e: e[2]['Weight'])
    T = nx.Graph()
    for u, v, attr in edges:
        if union(u, v):
            T.add_edge(u, v, **attr)
    return T

def get_real_node_name(G, user_input):
    user_input = user_input.lower()
    for node in G.nodes:
        if node.lower() == user_input:
            return node

    matches = difflib.get_close_matches(user_input, [n.lower() for n in G.nodes], n=1, cutoff=0.8)
    if matches:
        return next((n for n in G.nodes if n.lower() == matches[0]), None)

    return None

# —————— Load graph ——————
CSV_PATH = r"C:\Users\riya5\OneDrive\Documents\ECO_LINK_DAA_PROJECT\Ecolinkdaanew\daa_states_dataset.csv"
G = load_graph(CSV_PATH)

# —————— API: get_corridor ——————
@app.route('/get_corridor')
@app.route('/get_corridor')
def get_corridor():
    src_input = request.args.get('source')
    dst_input = request.args.get('destination')
    if not src_input or not dst_input:
        return jsonify(error="Missing source or destination"), 400

    src = get_real_node_name(G, src_input)
    dst = get_real_node_name(G, dst_input)
    if not src or not dst:
        return jsonify(error="Sanctuary not found. Check spelling."), 404

    mst = kruskal_mst(G)
    if src not in mst or dst not in mst:
        return jsonify(error="No path found"), 404

    try:
        node_list = nx.shortest_path(mst, src, dst, weight='Weight')
    except nx.NetworkXNoPath:
        return jsonify(error="No path found"), 404

    edges = []
    total_distance = 0
    total_risk = 0
    for u, v in zip(node_list, node_list[1:]):
        d = G[u][v]["Distance"]
        r = G[u][v]["Risk"]
        total_distance += d
        total_risk += r
        edges.append({
            "source": u,
            "destination": v,
            "distance": d,
            "risk": r,
            "source_state": G.nodes[u].get("state", "Unknown"),
            "destination_state": G.nodes[v].get("state", "Unknown"),
            "source_full": f"{u} ({G.nodes[u].get('state', 'Unknown')})",
            "destination_full": f"{v} ({G.nodes[v].get('state', 'Unknown')})"
        })

    nodes = {
        n: {
            "latitude": G.nodes[n]["latitude"],
            "longitude": G.nodes[n]["longitude"],
            "state": G.nodes[n].get("state", "Unknown")
        } for n in node_list
    }

    return jsonify({
        "path": edges,
        "nodes": nodes,
        "total_distance": total_distance,
        "total_risk": total_risk
    })

# —————— API: get_risk_info ——————
@app.route('/get_risk_info')
def get_risk_info():
    data = {
        "1": {
            "description": "Very Low Risk – Minimal disturbance and excellent ecological conditions",
            "factors": {
                "Human Disturbance": "Minimal human presence, little to no impact.",
                "Predator Presence": "Low or negligible predator activity.",
                "Environmental Hazard": "No significant hazards detected.",
                "Physical Barrier": "Corridor is open and clear."
            }
        },
        "2": {
            "description": "Low to Moderate Risk – Some environmental concerns but still relatively safe",
            "factors": {
                "Human Disturbance": "Limited human activities causing minor disturbance.",
                "Predator Presence": "Occasional predator sightings.",
                "Environmental Hazard": "Some localized hazards present.",
                "Physical Barrier": "Minor obstacles in the corridor."
            }
        },
        "3": {
            "description": "Moderate to High Risk – Noticeable hazards or disruption in the corridor",
            "factors": {
                "Human Disturbance": "Frequent human activity causing habitat disruption.",
                "Predator Presence": "Regular predator presence posing threat.",
                "Environmental Hazard": "Visible environmental hazards affecting wildlife.",
                "Physical Barrier": "Significant obstacles or partial barriers."
            }
        },
        "4": {
            "description": "High Risk – Significant disturbance or barriers present, risky for animal movement",
            "factors": {
                "Human Disturbance": "High human activity severely disrupting habitats.",
                "Predator Presence": "Predators frequently present, high threat.",
                "Environmental Hazard": "Severe environmental hazards like pollution or fire risk.",
                "Physical Barrier": "Major barriers preventing safe movement."
            }
        }
    }
    return jsonify(data)

# —————— Serve front-end HTML & static ——————
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/map.html')
def serve_map():
    return send_from_directory('.', 'map.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# —————— Run App ——————
if __name__ == '__main__':
    app.run(debug=True)
