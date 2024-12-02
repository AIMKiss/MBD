from flask import Flask, Response, render_template, request, redirect, url_for, session
from typing import Union, List, Dict

import networkx as nx

from components.graph import DatabaseGraph
from components.cluster.factory.cluster_factory import ClusterFactory
from components.facade.database_facade import DatabaseFacade
from components.helpers import estimate_clusters
from components.cluster.utils import ClusterUtils

import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index() -> Union[str, Response]:
    if request.method == 'POST':
        user: str = request.form['user']
        password: str = request.form['password']
        host: str = request.form['host']
        database: str = request.form['database']

        # Store credentials in session
        session['user'] = user
        session['password'] = password
        session['host'] = host
        session['database'] = database

        # Confirm connection
        db_facade: DatabaseFacade = DatabaseFacade(user, password, host, database)
        if db_facade.test_connection():
            return redirect(url_for('form_graph'))
        else:
            return render_template('index.html', error="Connection failed. Please check your credentials.")
    return render_template('index.html')

@app.route('/form_graph', methods=['GET', 'POST'])
def form_graph() -> Union[str, Response]:
    if request.method == 'POST':
        if 'action' in request.form and request.form['action'] == 'confirm':
            return redirect(url_for('identify_clusters'))
        elif request.form['action'] == 'form' or request.form['action'] == 'recreate':
            db_facade: DatabaseFacade = DatabaseFacade(session['user'], session['password'], session['host'], session['database'])
            db_facade.fetch_table_dependencies()
            db_facade.create_graph()

            image_path: str = os.path.join('static', 'images', 'graph.png')
            db_facade.visualize_graph_without_clustering(image_path)

            session['graph_data'] = json.dumps(list(db_facade.graph.graph.edges()))

            return render_template('form_graph.html', image_url=image_path)
    return render_template('form_graph.html')

@app.route('/identify_clusters', methods=['GET', 'POST'])
def identify_clusters() -> Union[str, Response]:
    if request.method == 'POST':
        if 'action' in request.form and request.form['action'] == 'confirm':
            return redirect(url_for('perform_clustering'))
        elif request.form['action'] == 'identify' or request.form['action'] == 'reidentify':

            graph_data: List[tuple] = json.loads(session['graph_data'])
            G: nx.Graph = nx.Graph()
            G.add_edges_from(graph_data)

            n_clusters: int = estimate_clusters(G)

            session['n_clusters'] = n_clusters

            return render_template('identify_clusters.html', n_clusters=n_clusters)
    return render_template('identify_clusters.html')

@app.route('/perform_clustering', methods=['GET', 'POST'])
def perform_clustering() -> Union[str, Response]:
    methods: List[str] = ClusterUtils.clustering_options()
    if request.method == 'POST':
        method: str = request.form.get('method', 'spectral')
        session['method'] = method

        # Recreate the graph from session data
        graph_data: List[tuple] = json.loads(session['graph_data'])
        G: nx.Graph = nx.Graph()
        G.add_edges_from(graph_data)

        # Run clustering
        cluster = ClusterFactory.create_cluster(method)
        n_clusters: int = session.get('n_clusters')
        G, labels = cluster.perform_clustering(G, n_clusters)

        # Visualize the table schema
        image_path: str = os.path.join('static', 'images', 'table_schema')
        graph: DatabaseGraph = DatabaseGraph(session['user'], session['password'], session['host'], session['database'])
        graph.load_graph(G)
        graph.fetch_table_details()
        graph.visualize_table_schema(image_path, labels)

        return render_template('perform_clustering.html', methods=methods, image_url=url_for('static', filename='images/table_schema.png'))
    return render_template('perform_clustering.html', methods=methods)

if __name__ == '__main__':
    app.run(debug=True)
