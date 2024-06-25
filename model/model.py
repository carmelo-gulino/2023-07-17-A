import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_sol = None
        self.colors = DAO.get_all_colors()
        self.graph = None

    def build_graph(self, color, year):
        self.graph = nx.Graph()
        products = DAO.get_nodes(color)
        self.graph.add_nodes_from(products)
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if u != v:
                    peso = DAO.get_n_sales(year, u.Product_number, v.Product_number)
                    if peso > 0:
                        self.graph.add_edge(u, v, weight=peso)
        return self.graph

    def get_archi_pesanti(self):
        sorted_edges = list(self.graph.edges)
        sorted_edges.sort(key=lambda x: self.graph[x[0]][x[1]]['weight'], reverse=True)
        duplicati = self.get_archi_duplicati(sorted_edges[:3])
        return sorted_edges[:3], duplicati

    def get_archi_duplicati(self, sorted_edges):
        duplicati = set()
        for edge in sorted_edges:
            for node in edge:
                c = 0
                for e in sorted_edges:
                    if node == e[0] or node == e[1]:
                        c += 1
                if c > 1:
                    duplicati.add(node)
        return duplicati

    def get_percorso(self, partenza):
        self.best_sol = []
        sorted_neighbors = list(self.graph.neighbors(partenza))
        sorted_neighbors.sort(key=lambda x: self.graph[x][partenza]['weight'])
        parziale = [(partenza, sorted_neighbors[0])]
        pesi_aggiunti = [self.graph[partenza][sorted_neighbors[0]]['weight']]
        self.ricorsione(parziale, pesi_aggiunti)
        return self.best_sol

    def ricorsione(self, parziale, pesi_aggiunti):
        ultimo = parziale[-1][1]
        if len(parziale) > len(self.best_sol):
            self.best_sol = copy.deepcopy(parziale)
            print(len(parziale))
        sorted_neighbors = [n for n in self.graph.neighbors(ultimo) if self.graph[n][ultimo]['weight'] >= pesi_aggiunti[-1]]
        sorted_neighbors.sort(key=lambda x: self.graph[x][ultimo]['weight'])
        for neighbor in sorted_neighbors:
            if (ultimo, neighbor) not in parziale and (neighbor, ultimo) not in parziale:
                parziale.append((ultimo, neighbor))
                pesi_aggiunti.append(self.graph[neighbor][ultimo]['weight'])
                self.ricorsione(parziale, pesi_aggiunti)
                parziale.pop()
                pesi_aggiunti.pop()
