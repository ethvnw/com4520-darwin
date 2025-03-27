from transitions.extensions import GraphMachine

class Machine(GraphMachine):
    style_attributes = {
        "node": {
            "default": {
                "style": "rounded,filled",
                "shape": "circle",
                "fillcolor": "white",
                "color": "black",
                "peripheries": "1",
            },
            "inactive": {"fillcolor": "white", "color": "black", "peripheries": "1"},
            "parallel": {
                "shape": "circle",
                "color": "black",
                "fillcolor": "white",
                "style": "dashed, rounded, filled",
                "peripheries": "1",
            },
            "active": {"color": "red", "fillcolor": "darksalmon", "peripheries": "2"},
            "previous": {"color": "blue", "fillcolor": "azure", "peripheries": "1"},
        },
        "edge": {"default": {"color": "black"}, "previous": {"color": "blue"}},
        "graph": {
            "default": {"color": "black", "fillcolor": "white", "style": "solid"},
            "previous": {"color": "blue", "fillcolor": "azure", "style": "filled"},
            "active": {"color": "red", "fillcolor": "darksalmon", "style": "filled"},
            "parallel": {"color": "black", "fillcolor": "white", "style": "dotted"},
        },
    }

    def draw_graph(self, title=None):
        graph = self.get_graph(title=title)
        self._add_initial_state_arrow(graph)
        graph.graph_attr['label'] = title if title else ""
        return graph
    
    def _add_initial_state_arrow(self, graph):
        graph.add_node('initial', style='invis', width='0', shape='point')
        graph.add_edge('initial', self.initial, style='solid')
