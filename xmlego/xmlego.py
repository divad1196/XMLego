from lxml import etree
import igraph
ig = igraph
from .utils import insert_after, insert_before

# etree.fromstring


def to_graph(templates, graph=None):
    if graph is None:
        graph = igraph.Graph(directed=True)
    # Add all template as vertices
    for t in templates:
        id = t.attrib["id"]
        inherits = t.attrib.get("inherits")
        graph.add_vertex(id, id=id, template=t, inherits=inherits)
    # Add the edges
    edges = []
    for v in graph.vs:
        attrs = v.attributes()
        inherits = attrs.get("inherits")
        if inherits:
            edges.append((attrs["id"], inherits))  # child, parent
    graph.add_edges(edges)
    return graph

def plot_graph(graph):
    ig.plot(graph, vertex_label=graph.vs["name"])


def has_cycles(graph):
    return not graph.is_dag()

def split_graph(graph):
    return graph.decompose("weak")  # Split unconnected graphs

def graph_resolve_order(graph):
    # We use the reversed topological order to ensure that the first node is the base
    # We could have used bfs or dfs algorithm instead as long as the first value is the top node of the "tree"
    reverse_topological_order = graph.vs.select(reversed(graph.topological_sorting()))
    templates = (
        v.attributes()["template"]
        for v in reverse_topological_order
    )
    base = next(templates)
    return base, templates

def _get_position_handler(element, position):
    setter = None
    if position == "after":
        setter = insert_after
    elif position == "before":
        setter = insert_before
    
    def handler(children, element=element, setter=setter):
        setter(element, children)
    return handler

def apply_xpath(base, xpath):
    expr = xpath.attrib["expr"]
    position = xpath.attrib["position"]
    elements = base.xpath(expr)
    for el in elements:
        handler = _get_position_handler(el, position)
        handler(xpath.getchildren())
    

def _solve_graph(graph):
    base, templates = graph_resolve_order(graph)
    for t in templates:
        for xpath in t.xpath("xpath"):
            apply_xpath(base, xpath)
    return base


def solve_graph(graph):
    # TODO: add check for cycles
    if has_cycles(graph):
        raise Exception("has cycle")
    return [_solve_graph(g) for g in split_graph(graph)]

# graph = igraph.Graph(directed=True)
# graph.add_vertex   # Add vertex "node"
# graph.bfsiter(0)   # Iter over vertex
# graph.vs.find("test")  # Get vertex by its name