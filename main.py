import graphviz
import math


class BinTreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.isLeaf = not (left) and not (right)

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
        nodes[key] = BinTreeNode((key, value))
    while len(f) > 1:
        minkey = min_key(f)
        del f[minkey]
        next_min = min_key(f)
        del f[next_min]
        new_key = nodes[minkey].data[0] + nodes[next_min].data[
            0]  # Creates a new key, concatenating the letters from the children nodes
        new_value = nodes[minkey].data[1] + nodes[next_min].data[
            1]  # Creates a new value, which is the sum of the frequencies of the child nodes
        merged = BinTreeNode((new_key, new_value), nodes[minkey], nodes[next_min])
        del nodes[minkey]
        del nodes[next_min]
        f[new_key] = new_value
        nodes[new_key] = merged
    return nodes[new_key]


def visualise(tree, digraph):
    if tree.isLeaf:
        return "Complete"
    else:
        parent = str(tree.data)
        if tree.left.isLeaf:
            L = f"{tree.left.data[0]} - {tree.left.data[1]}"
            L_label = L
        else:
            L = str(tree.left.data)
            L_label = str(tree.left.data[1])
        if tree.right.isLeaf:
            R = f"{tree.right.data[0]} - {tree.right.data[1]}"
            R_label = R
        else:
            R = str(tree.right.data)
            R_label = str(tree.right.data[1])

        digraph.node(L, L_label)
        digraph.node(R, R_label)
        digraph.edge(parent, L)
        digraph.edge(parent, R)
        visualise(tree.left, digraph)
        visualise(tree.right, digraph)


def generateCodes(tree, code_dict = {}, code=""):
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
    exampleText = exampleText.replace(":", "■")
    f = frequency(exampleText)
    tree = create_tree(f)
    # Render Visualisation
    tree_viz = graphviz.Digraph(comment="Huffman Encoding", format='png')

    tree_viz.node(name=str(tree.data), label=str(tree.data[1]))
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


