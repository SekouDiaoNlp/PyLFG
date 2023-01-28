"""
This module provides classes to represent and visualize LFG parse trees.
The LFGParseTree class provides a visualization of the tree structure of the sentence,
as well as functional annotations in the lexical items.
"""

import networkx as nx
import matplotlib.pyplot as plt


class LFGParseTreeNode:
    def __init__(self, label: str, token: str, functional_labels: dict = None, children=None):
        """
        Construct a new LFG parse tree node.
        Parameters:
        - label (str): The label of the node, typically a non-terminal symbol or a terminal symbol.
        - token (str): The token the node represents, if any.
        - functional_labels (Dict[str, str]): functional labels of the lexical item in the XLFG standard format, where keys are the functional labels and values are the corresponding label values
        - children (List[LFGParseTreeNode]): The children of the node.
        """
        self.label = label
        self.token = token
        self.functional_labels = functional_labels if functional_labels is not None else {}
        self.children = children or []
        self.e_structure = None

    def add_child(self, child):
        self.children.append(child)

    def add_functional_label(self, label: str, value: str):
        """
        Add a new functional label
        :param label: (str) functional label
        :param value: (str) corresponding label value
        """
        self.functional_labels[label] = value

    def get_functional_label(self, label: str):
        """
        get the value of the functional label specified
        :param label: (str) functional label
        :return: (str) corresponding label value
        """
        return self.functional_labels.get(label)

    def remove_functional_label(self, label: str):
        """
        remove the specified functional label from the functional_labels
        :param label: (str) functional label
        """
        self.functional_labels.pop(label, None)

    def get_all_functional_labels(self):
        """
        get all functional labels
        :return: dict of functional labels in the XLFG standard format
        """
        return self.functional_labels
    
   def calculate_e_structure(self):
        e_structure = {}
        if self.label in e_structure:
            e_structure[self.label] = (self.f_structure, [])
        for child in self.children:
            child.calculate_e_structure()
            e_structure[self.label][1].append(child.e_structure)
        self.e_structure = e_structure 
    
    def is_leaf(self):
        """
        Determine if the node is a leaf node (i.e., has no children).
        Returns:
        - bool: True if the node is a leaf node, False otherwise.
        """
        return not self.children

    def __repr__(self):
        """
        Return a string representation of the node.
        Returns:
        - str: A string representation of the node.
        """
        return f"LFGParseTreeNode(label={self.label}, token={self.token}, functional_labels={self.functional_labels}, children={self.children})"


class LFGParseTreeNodeF(LFGParseTreeNode):
    def __init__(self, label: str, token: str, functional_labels=None, children=None):
        super().__init__(label, token, functional_labels, children)
        self.f_structure = FStructure()
        self.path_stm = path_stm
        
    def add_to_f_structure(self, attribute: str, value: str):
        self.f_structure.add(attribute, value)
        
    def set_in_f_structure(self, attribute: str, value: str):
        self.f_structure.set(attribute, value)
        
    def get_from_f_structure(self, attribute: str):
        return self.f_structure.get(attribute)
        
    def remove_from_f_structure(self, attribute: str):
        self.f_structure.remove(attribute)
        
    def get_all_f_structure(self):
        return self.f_structure.get_all()
        
    def has_in_f_structure(self, attribute: str):
        return self.f_structure.has(attribute)

    def display_f_structure(self):
        return self.f_structure.display()
    
    def set_path_stm(self, path_stm):
        self.path_stm = path_stm

    def get_path_stm(self):
        return self.path_stm

class LFGParseTreeNodeE(LFGParseTreeNode):
    def __init__(self, label: str, token: str, children=None):
        super().__init__(label, token, children)
        self.syntactic_category = None
        self.tense = None
        self.aspect = None
        self.semantic_role = None
        self.lexical_head = None
        self.logical_form = None
        self.mood = None

    def set_syntactic_category(self, category: str):
        self.syntactic_category = category

    def get_syntactic_category(self):
        return self.syntactic_category

    def set_tense(self, tense: str):
        self.tense = tense

    def get_tense(self):
        return self.tense

    def set_aspect(self, aspect: str):
        self.aspect = aspect

    def get_aspect(self):
        return self.aspect
    
    def set_mood(self, mood: str):
        self.mood = mood

    def get_mood(self):
        return self.mood

    def set_semantic_role(self, role: str):
        self.semantic_role = role

    def get_semantic_role(self):
        return self.semantic_role

    def set_lexical_head(self, head: str):
        self.lexical_head = head

    def get_lexical_head
        return self.lexical_head
    
    def set_logical_form(self, form: str):
        self.logical_form = form

    def get_logical_form
        return self.logical_form


class LFGParseTree:
    def __init__(self, root: LFGParseTreeNode):
        self.root = root
        self.sentence = ""

    def set_sentence(self, sentence: str):
        self.sentence = sentence

    def is_leaf(self):
        return not self.children

    def to_string(self) -> str:
        if self.is_leaf():
            return self.token

        child_strings = [child.to_string() for child in self.children]
        return f"({self.label} {' '.join(child_strings)})"
    
    def f_structure_matrix(self):
        """
        Returns the f-structure represented as an attribute-value matrix.
        """
        # Initialize the matrix
        matrix = []
        
        # Recursive function to traverse the parse tree
        def traverse(node):
            # Get the functional labels of the current node
            labels = node.get_all_functional_labels()
            
            # If the node has children, recursively traverse them
            if node.children:
                for child in node.children:
                    traverse(child)
                    
            # If the node is a leaf, add its functional labels to the matrix
            else:
                row = []
                for key, value in labels.items():
                    row.append((key, value))
                matrix.append(row)

        # Start traversing the tree
        traverse(self.root)
        
        # Return the matrix
        return matrix
    
    def to_latex(self, filepath: str):
        f_structure_latex = self._to_latex_helper(self.root)
        c_structure_latex = self._to_c_structure_latex_helper(self.root)
        caption = "C-structure tree and F-structure representation of the parse tree"
        label = "parse_tree"

        latex_code = f"""
        \\documentclass{{article}}
        \\usepackage{{tikz-qtree}}
        \\usepackage{{tabularx}}
        \\usepackage[active,tightpage]{{preview}}
        \\usepackage{{graphicx}}
        \\PreviewEnvironment{{center}}
        \\begin{{document}}
        \\begin{{figure}}[h]
        \\centering
        \\begin{{tabularx}}{{1.5\\textwidth}}{{X l}}
        {c_structure_latex} & {f_structure_latex}\\\\
        \\end{{tabularx}}
        \\caption{{{caption}}}
        \\label{{{label}}}
        \\end{{figure}}
        \\end{{document}}
        """
        with open(filepath, "w") as f:
            f.write(latex_code)

    def _to_c_structure_latex_helper(self, node):
        # children = " ".join([self._to_c_structure_latex
        
    def to_networkx(self):
        graph = nx.DiGraph()
        stack = [(self.root, None)]
        while stack:
            node, parent = stack.pop()
            graph.add_edge(parent, node.label)
            for child in node.children:
                stack.append((child, node.label))
        return graph

    def draw(self, layout: str = 'spring', color_map: Dict[str, str] = None):
        """
        tree = LFGParseTree(root_node)
        color_map = {'NP': 'red', 'VP': 'green', 'PP': 'blue'}
        tree.draw(layout='spring', color_map=color_map)
        """
        G = nx.Graph()
        queue = [(self.root, None)]
        while queue:
            node, parent = queue.pop(0)
            G.add_node(node.label)
            if parent:
                G.add_edge(parent.label, node.label)
            for child in node.children:
                queue.append((child, node))
        if color_map:
            color_values = [color_map.get(node.label, 'white') for node in G.nodes()]
            nx.draw(G, pos=nx.drawing.nx_agraph.graphviz_layout(G, prog=layout), node_color=color_values)
        else:
            nx.draw(G, pos=nx.drawing.nx_agraph.graphviz_layout(G, prog=layout))
        plt.show()

    def get_annotations(self):
        annotations = {}
        stack = [(self.root, None)]
        while stack:
            node, parent = stack.pop()
            for label, value in node.get_all_functional_labels().items():
                annotations[(parent, node.label)] = f"{label}={value}"
            for child in node.children:
                stack.append((child, node.label))
        return annotations

    
class FStructure:
    def __init__(self):
        """
        Construct a new FStructure object.
        """
        self.attributes = {}
        self.constraints = []
        self.f_structures = []

    def add(self, attribute: str, value: str):
        """
        Add a new attribute-value pair to the f-structure
        :param attribute: (str) the attribute name
        :param value: (str) the value of the attribute
        """
        if attribute not in self.attributes:
            self.attributes[attribute] = set()
        self.attributes[attribute].add(value)
    
    def set(self, attribute: str, value: str):
        """
        Set the value of the specified attribute
        :param attribute: (str) the attribute name
        :param value: (str) the value of the attribute
        """
        self.attributes[attribute] = {value}
    
    def get(self, attribute: str):
        """
        Get the value of the specified attribute
        :param attribute: (str) the attribute name
        :return: (str) the value of the attribute
        """
        if attribute in self.attributes:
            return self.attributes[attribute]
        else:
            return None
    
    def remove(self, attribute: str):
        """
        Remove the specified attribute from the f-structure
        :param attribute: (str) the attribute name
        """
        if attribute in self.attributes:
            self.attributes.pop(attribute)
    
    def get_all_attributes(self):
        """
        get all attributes and their values
        :return: dict of attributes and their values
        """
        return self.attributes

    def has_attribute(self, attribute: str):
        """
        check if the f-structure has the specified attribute
        :param attribute: (str) attribute name
        :return: (bool) True if has the attribute, False otherwise
        """
        return attribute in self.attributes

    def add_functional_label(self, label: str, value: str):
        """
        Add a new functional label
        :param label: (str) functional label
        :param value: (str) corresponding label value
        """
        self.attributes[label] = value

    def get_functional_label(self, label: str):
        """
        get the value of the functional label specified
        :param label: (str) functional label
        :return: (str) corresponding label value
        """
        return self.attributes.get(label)

    def remove_functional_label(self, label: str):
        """
        remove the specified functional label from the f-structure
        :param label: (str) functional label
        """
        self.attributes.pop(label, None)

    def get_all_functional_labels(self):
        """
        get all functional labels
        :return: dict of functional labels in the XLFG standard format
        """
        return self.attributes
    
    def add_constraint(self, constraint: str):
        """
        Add a new constraint to the f-structure
        :param constraint: (str) the constraint to be added
        """
        self.constraints.append(constraint)
    
    def remove_constraint(self, constraint: str):
        """
        Remove the specified constraint from the f-structure
        :param constraint: (str) the constraint to be removed
        """
        self.constraints.remove(constraint)
    
    def check_constraints(self):
        """
        Check if all the constraints are satisfied
        :return: (bool) True if all constraints are satisfied, False otherwise
        """
        for constraint in self.constraints:
            if not constraint(self.attributes):
                return False
        return True
        
    def add_f_structure(self, f_structure: dict):
        """
        Add a new f-structure to the current f-structure
        :param f_structure: (dict) the f-structure to be added
        """
        self.f_structures.append(f_structure)
        
    def get_f_structures(self):
        """
        Get all f-structures
        :return: (list) all f-structures
        """
        return self.f_structures
    
    def generate_sentence(self) -> str:
        """
        Generate a sentence from the f-structure
        :return: (str) the sentence
        """
        sentence = ""
        for attribute, value in self.attributes.items():
            if attribute == "pred":
                sentence += value + " "
            elif attribute.startswith("arg"):
                sentence += value + " "
        return sentence.strip()
        
    def transfer_language(self, transfer_rules: dict):
        """
        Transfer the f-structure to a different language using the provided transfer rules.
        :param transfer_rules: (Dict[str, str]) A dictionary where keys are the attributes in the original language,
            and values are the corresponding attributes in the target language.
            :return: (dict) the transfered attributes
        """
        new_attributes = {}
        for attribute, value in self.attributes.items():
            if attribute in transfer_rules:
                new_attribute = transfer_rules[attribute]
                new_attributes[new_attribute] = value
        return new_attributes

