import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.prodotto_scelto = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dds(self):
        for y in range(2015, 2019):
            self.view.dd_anno.options.append(ft.dropdown.Option(f"{y}"))
        for c in self.model.colors:
            self.view.dd_colore.options.append(ft.dropdown.Option(f"{c}"))

    def handle_crea_grafo(self, e):
        color = self.view.dd_colore.value
        year = int(self.view.dd_anno.value)
        graph = self.model.build_graph(color, year)
        self.fill_dd_prodotti(graph)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {len(graph.nodes)} nodi "
                                                     f"e {len(graph.edges)} archi"))
        archi_pesanti, duplicati = self.model.get_archi_pesanti()
        self.view.txt_result.controls.append(ft.Text(f"I tre archi più pesanti sono:"))
        for a in archi_pesanti:
            self.view.txt_result.controls.append(ft.Text(f"Arco da {a[0]} a {a[1]}, peso = "
                                                         f"{self.model.graph[a[0]][a[1]]['weight']}"))
        self.view.txt_result.controls.append(ft.Text(f"I nodi ripetuti sono: {duplicati}"))
        self.view.update_page()

    def fill_dd_prodotti(self, graph):
        for node in graph.nodes:
            self.view.dd_prodotto.options.append(ft.dropdown.Option(data=node,
                                                                    text=node,
                                                                    on_click=self.read_prodotto))

    def read_prodotto(self, e):
        if e.control.data is None:
            self.prodotto_scelto = None
        self.prodotto_scelto = e.control.data

    def handle_percorso(self, e):
        if self.prodotto_scelto is None:
            self.view.create_alert("Selezionare un prodotto di partenza")
            return
        path = self.model.get_percorso(self.prodotto_scelto)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il percorso trovato include {len(path)} archi: "))
        for p in path:
            self.view.txt_result.controls.append(ft.Text(f"{p[0]} -> {p[1]}: {self.model.graph[p[0]][p[1]]['weight']}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
