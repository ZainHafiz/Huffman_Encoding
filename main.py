import graphviz
import math


class Node:
    def __init__(self, data, left=None, right=None, parent=None):
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
        self.isLeaf = not left and not right

    def __str__(self):
        string = f"{self.data}"
        return string

    def __repr__(self):
        return self.__str__()


# Outputs a dictionary with the frequency of different symbols in a text
def frequency(text):
    if text == "":
        raise ValueError("Content.txt file must contain text")
    freq = {}
    for char in text:
        if char in freq.keys():
            freq[char] += 1
        else:
            freq[char] = 1
    return freq


# function which find the minimum key of any dictionary
def min_key(dictionary):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    return keys[values.index(min(values))]


# Create the tree by inputting in your frequency dictionary
def create_tree(frequency_dict):
    f = frequency_dict
    nodes = {}
    # Create a dictionary called "nodes" where each key represents a character in the text, and each value is the
    # character's corresponding BinTreeNode
    for key, value in f.items():
        nodes[key] = Node((key, value))
    merged = None
    while len(f) > 1:
        minkey = min_key(f)
        del f[minkey]
        next_min = min_key(f)
        del f[next_min]

        # Creates a new key, concatenating the letters from the children nodes
        new_key = nodes[minkey].data[0] + nodes[next_min].data[0]

        # Creates a new value, which is the sum of the frequencies of the child nodes
        new_value = nodes[minkey].data[1] + nodes[next_min].data[1]
        merged = Node((new_key, new_value), nodes[minkey], nodes[next_min])
        merged.left.parent = merged
        merged.right.parent = merged
        del nodes[minkey]
        del nodes[next_min]
        f[new_key] = new_value
        nodes[new_key] = merged

    return nodes[new_key]

def visualise(tree, digraph):
    name = f"{tree.data[0]} - {tree.data[1]}"
    if tree.isLeaf:
        digraph.node(name, name)
    else:
        digraph.node(name, str(tree.data[1]))

    if tree.parent is not None:
        parentName = f"{tree.parent.data[0]} - {tree.parent.data[1]}"
        digraph.edge(parentName, name)

    if not tree.isLeaf:
        visualise(tree.left, digraph)
        visualise(tree.right, digraph)


def generateCodes(tree, code_dict={}, code=""):
    if tree.isLeaf:
        code_dict[tree.data[0]] = code
    else:
        generateCodes(tree.left, code_dict, code + "0")
        generateCodes(tree.right, code_dict, code + "1")
    return code_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = open("Content.txt")

    exampleText = file.read()
    # Colons replaced with rare character to handle error displaying colon in graphviz
    exampleText = exampleText.replace(":", "■")
    f = frequency(exampleText)
    tree = create_tree(f)

    # Render Visualisation
    tree_viz = graphviz.Digraph(comment="Huffman Encoding", format='png')

    visualise(tree, tree_viz)
    tree_viz.render()

    codes = generateCodes(tree)
    codes[":"] = codes["■"]
    del codes["■"]
    exampleText = exampleText.replace("■", ":")

    print(f"Codes: {codes}")
    # Encodes Text
    encoding = "".join([codes[x] for x in exampleText])
    print("Compressed Storage: ", len(encoding), " bits")
    # Storage size using fixed length binary representation
    uncompressed_storage = len(exampleText) * math.ceil(math.log(len(frequency(exampleText)), 2))
    print("Uncompressed Storage: ", uncompressed_storage, " bits")
    efficiency = len(encoding)/uncompressed_storage
    print("Efficiency: ", efficiency)


