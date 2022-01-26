from lxml import etree
import copy


def print_xml(xml):
    print(etree.tostring(xml, pretty_print=True).decode())
    
def copy_element(xml):
    return copy.deepcopy(xml)

def insert_after(xml, elements):
    for el in reversed(elements):
        xml.addnext(el)

def insert_before(xml, elements):
    for el in elements:
        xml.addprevious(el)

def remove_element(xml):
    xml.getparent().remove(xml)

def clear_element(xml):
    children = xml.getchildren()
    insert_after(xml, children)
    remove_element(xml)