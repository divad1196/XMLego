from lxml import etree
from xmlego.xmlego import to_graph, solve_graph
from xmlego.utils import print_xml
from xmlego.templating import eval_xml

# Retrieve all templates
tree = etree.parse("test.xml")
templates = tree.getroot().findall("template")  # use xpath instead?

# Resolve order 
graph = to_graph(templates)
res = solve_graph(graph)[0]
print_xml(res)

res, _ = eval_xml(res)
print_xml(res)
