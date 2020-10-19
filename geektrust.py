import sys


class Vertex:
    """
    Class to represent a vertex

    Attributes:
        data : dict
            key, value pairs of info relating to a vertex

    Methods:
        get_spouse_gender():
            Returns the spouse gender of Vertex
    """

    def __init__(self, data):
        """
        Constructs all necessary attributes of Vertex object from data

        :param data : dict
            key, value pairs of info relating to a vertex
        """
        self.name = data["name"]
        self.gender = data["gender"]
        self.spouse_name = data["spouse_name"]
        self.children = []
        self.incident_edges = {}

    def get_spouse_gender(self):
        """
         checks the gender of the vertex and returns the opposite gender as spouse gender if spouse exists
        :return:
        """
        if self.gender == "Male" and self.spouse_name != "":
            return "Female"
        elif self.gender == "Female" and self.spouse_name != "":
            return "Male"
        return ""


class Edge:
    """
    Class to represent an Edge

    Attributes:
        start_vertex : vertex (dict)
            starting point of the edge to be created
        end_vertex : vertex (dict)
            end point of the edge to be created
    """

    def __init__(self, start_vertex, end_vertex):
        """
        Constructs an edge between 2 vertices given and updates incident edges of end vertex with start vertex
        :param start_vertex : vertex (dict)
            starting point of the edge to be created
        :param end_vertex : vertex (dict)
            end point of the edge to be created
        """
        self.start = start_vertex
        self.end = end_vertex
        self.end.incident_edges[0] = self.start


class GraphADT:
    """
    Class to represent GraphADT with addition of vertices and edges.

    Methods :
    add_vertex(data)
        Creates vertex(data) and adds it to vertices dict of Graph obj.

    add_edge(source, endpoint)
        Creates an edge between source and endpoint vertices and adds this edge to edges dict of Graph obj

    spouse_search(name)
        Checks if the name is spouse_name of any the vertices and return True if found. Else False

    get_spouse_name(name)
        Searches and returns the vertex name if the name is spouse_name of any vertex of Graph obj.

    add_child(mother_name, name, gender)
        creates a vertex(name) and edge between mother_name and name with given gender only if mother_name
        is a valid female vertex with spouse or if mother_name is spouse of a valid male vertex.

    get_relationship(name, relation)
        For the given relation, appends a result array with names of vertices that match the relation
        between all vertices and name vertex.
    """

    def __init__(self):
        """
        Constructs GraphADT with initial dict of empty vertices and edges
        """
        self.vertices = {}
        self.edges = {}

    def add_vertex(self, data):
        """
        Creates vertex(data) and adds it to vertices dict of Graph obj.
        :param data: dict
            key, value pairs of info relating to a vertex
        :return: Updated Graph obj
        """
        self.vertices[data["name"]] = Vertex(data)
        return self

    def add_edge(self, source, endpoint):
        """
        Creates an edge between source and endpoint vertices and adds this edge to edges dict of Graph obj
        Updates children of source as endpoint vertex.
        :param source : Vertex (dict)
            starting point of the edge to be created
        :param endpoint : Vertex (dict)
            end point of the edge to be created
        :return : Updated Graph obj
        """
        self.edges[source] = Edge(source, endpoint)
        source.children.append(endpoint)
        return self

    def spouse_search(self, name):
        """
        Checks if the name is spouse_name of any the vertices and return True if found. Else False
        :param name: str
            name of spouse of vertex to be searched
        :return: bool
            True if name is spouse name of any vertex else False
        """
        for key in self.vertices:
            if self.vertices[key].spouse_name == name:
                return True
        return False

    def get_spouse_name(self, name):
        """
        Searches and returns the vertex.name if the name is spouse_name of any vertex of Graph obj.

        :param name: str
            spouse name of vertex to be searched
        :return: str
            vertex.name whose spouse_name == name
            Else: Empty str
        """
        for key in self.vertices:
            if self.vertices[key].spouse_name == name:
                return self.vertices[key].name
        return ''

    def add_child(self, mother_name, name, gender):
        """
        creates a vertex(name) and edge between mother_name and name with given gender only if mother_name
        is a valid female vertex with spouse or if mother_name is spouse of a valid male vertex.

        :param mother_name: str
            parent name to add the child to
        :param name: str
            name of child vertex to be added
        :param gender: str
            gender of child to be added
        :return: int
            status of child addition to mother_name(1/-1/0)
        """
        # checks if mother_name is in vertices dict and gender of mother_name is Male or not
        if mother_name in self.vertices and self.vertices[mother_name].gender == 'Male':
            return -1
        elif mother_name in self.vertices:
            # checks if spouse of mother exists or not and adds child
            if self.vertices[mother_name].spouse_name is not None:
                self.add_vertex(data={"name": name, "spouse_name": None, "gender": gender})
                self.add_edge(self.vertices[mother_name], self.vertices[name])
                return 1
            else:
                return -1
        # checks if mother_name is spouse of any vertex
        elif self.spouse_search(mother_name):
            if self.vertices[self.get_spouse_name(mother_name)].gender == "Female":
                return -1
            else:
                self.add_vertex(data={"name": name, "spouse_name": None, "gender": gender})
                self.add_edge(self.vertices[self.get_spouse_name(mother_name)], self.vertices[name])
                return 1
        return 0

    def get_relationship(self, name, relation):
        """
        For the given relation, appends a result array with names of vertices that match the relation
        between all vertices and name vertex.
        :param name: str
            name of vertex whose relation to be returned
        :param relation: str
            relation name
        :return: None or list
            None or list containing relation names of name
        """
        result = []
        # returns None if name is not a vertex or is not a spouse name of any vertex
        if name not in self.vertices and not self.spouse_search(name):
            return
        else:
            if relation == 'Paternal-Uncle':
                # Spouses of vertex does not have Paternal-Uncle
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    # vertex of name's parent
                    direct_parent = name_vertex.incident_edges[0]
                    # Father's brother is Paternal Uncle and not Mother's
                    if direct_parent.gender == 'Female':
                        return result
                    else:
                        for item in direct_parent.incident_edges[0].children:
                            if item.gender == 'Male' and item.name != direct_parent.name:
                                result.append(item.name)
                        return result
            elif relation == 'Maternal-Uncle':
                # Spouses of vertex does not have Maternal-Uncle
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    # Mother's brother is Maternal Uncle and not Father's
                    if direct_parent.gender == 'Male':
                        return result
                    else:
                        for item in direct_parent.incident_edges[0].children:
                            if item.gender == 'Male' and item.name != direct_parent.name:
                                result.append(item.name)
                        return result
            elif relation == 'Paternal-Aunt':
                # Spouses of vertex does not have Paternal-Aunt
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    # Father's sister is Paternal Aunt and not Mother's
                    if direct_parent.gender == 'Female':
                        return result
                    else:
                        for item in direct_parent.incident_edges[0].children:
                            if item.gender == 'Female' and item.name != direct_parent.name:
                                result.append(item.name)
                        return result
            elif relation == 'Maternal-Aunt':
                # Spouses of vertex does not have Maternal-Aunt
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    # Mother's sister is Maternal Aunt and not Father's
                    if direct_parent.gender == 'Male':
                        return result
                    else:
                        for item in direct_parent.incident_edges[0].children:
                            if item.gender == 'Female' and item.name != direct_parent.name:
                                result.append(item.name)
                        return result
            elif relation == 'Son':
                # if name is vertex.spouse_name
                if self.spouse_search(name):
                    name_vertex = self.vertices[self.get_spouse_name(name)]
                else:
                    # if name is vertex name
                    name_vertex = self.vertices[name]
                for item in name_vertex.children:
                    if item.gender == 'Male':
                        result.append(item.name)
                return result
            elif relation == 'Daughter':
                # if name is vertex.spouse_name
                if self.spouse_search(name):
                    name_vertex = self.vertices[self.get_spouse_name(name)]
                else:
                    # if name is vertex name
                    name_vertex = self.vertices[name]
                for item in name_vertex.children:
                    if item.gender == 'Female':
                        result.append(item.name)
                return result
            elif relation == 'Siblings':
                # Spouses of vertex does not have Siblings
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    for item in direct_parent.children:
                        result.append(item.name)
                    result.remove(name_vertex.name)
                    return result
            elif relation == 'Sister':
                # Spouses of vertex does not have Siblings
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    for item in direct_parent.children:
                        if item.gender == 'Female' and item.name != name:
                            result.append(item.name)
                    return result
            elif relation == 'Brother':
                # Spouses of vertex does not have Siblings
                if self.spouse_search(name):
                    return result
                else:
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    for item in direct_parent.children:
                        if item.gender == 'Male' and item.name != name:
                            result.append(item.name)
                    return result
            elif relation == 'Sister-In-Law':
                # For Spouse's Sister
                if self.spouse_search(name):
                    result = self.get_relationship(self.get_spouse_name(name), "Sister")
                else:
                    # For Brother's Spouse
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    for item in direct_parent.children:
                        if item.name != name_vertex.name and item.gender == 'Male' and item.spouse_name is not None:
                            result.append(item.spouse_name)
                return result
            elif relation == 'Brother-In-Law':
                # For Spouse's Brother
                if self.spouse_search(name):
                    result = self.get_relationship(self.get_spouse_name(name), "Brother")
                else:
                    # For Sister's Spouse
                    name_vertex = self.vertices[name]
                    # Checking if parent of name is null or not
                    if not bool(name_vertex.incident_edges):
                        return result
                    direct_parent = name_vertex.incident_edges[0]
                    for item in direct_parent.children:
                        if item.name != name_vertex.name and item.gender == 'Female' and item.spouse_name is not None:
                            result.append(item.spouse_name)
                return result
        return result


def print_child_addition(child_addition):
    """
    Prints respective strings for respective child_addition values of 1, 0, -1
    :param child_addition: int
        ADD_CHILD status (1 or 0 or -1)
    """
    if child_addition == 1:
        print("CHILD_ADDITION_SUCCEEDED")
    elif child_addition == -1:
        print("CHILD_ADDITION_FAILED")
    elif child_addition == 0:
        print("PERSON_NOT_FOUND")


def print_relationship(res):
    """
    Prints elements of list res with a whitespace. if res is empty, prints NONE and if none, prints PERSON_NOT_FOUND
    :param res: <list> containing string elements or None.
    """
    if res is None:
        print("PERSON_NOT_FOUND")
    elif len(res) == 0:
        print("NONE")
    else:
        for item in res:
            print(item, end=" ")
        print("")


if __name__ == '__main__':
    input_file = sys.argv[1]

    ftree = GraphADT()
    # King Arthur Vertex
    ftree.add_vertex(data={"name": "King Arthur", "spouse_name": "Queen Margaret", "gender": "Male"})

    # Level 1 vertices
    ftree.add_vertex(data={"name": "Bill", "spouse_name": "Flora", "gender": "Male"})
    ftree.add_vertex(data={"name": "Charlie", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "Percy", "spouse_name": "Audrey", "gender": "Male"})
    ftree.add_vertex(data={"name": "Ronald", "spouse_name": "Helen", "gender": "Male"})
    ftree.add_vertex(data={"name": "Ginerva", "spouse_name": "Harry", "gender": "Female"})

    # Level 2 vertices
    ftree.add_vertex(data={"name": "Victoire", "spouse_name": "Ted", "gender": "Female"})
    ftree.add_vertex(data={"name": "Dominique", "spouse_name": None, "gender": "Female"})
    ftree.add_vertex(data={"name": "Louis", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "Molly", "spouse_name": None, "gender": "Female"})
    ftree.add_vertex(data={"name": "Lucy", "spouse_name": None, "gender": "Female"})
    ftree.add_vertex(data={"name": "Rose", "spouse_name": "Malfoy", "gender": "Female"})
    ftree.add_vertex(data={"name": "Hugo", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "James", "spouse_name": "Darcy", "gender": "Male"})
    ftree.add_vertex(data={"name": "Albus", "spouse_name": "Alice", "gender": "Male"})
    ftree.add_vertex(data={"name": "Lily", "spouse_name": None, "gender": "Female"})

    # Level 3 Vertices
    ftree.add_vertex(data={"name": "Remus", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "Draco", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "Aster", "spouse_name": None, "gender": "Female"})
    ftree.add_vertex(data={"name": "William", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "Ron", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "Ginny", "spouse_name": None, "gender": "Female"})

    # Adding edges to vertices
    ftree.add_edge(ftree.vertices["King Arthur"], ftree.vertices["Bill"])
    ftree.add_edge(ftree.vertices["King Arthur"], ftree.vertices["Charlie"])
    ftree.add_edge(ftree.vertices["King Arthur"], ftree.vertices["Percy"])
    ftree.add_edge(ftree.vertices["King Arthur"], ftree.vertices["Ronald"])
    ftree.add_edge(ftree.vertices["King Arthur"], ftree.vertices["Ginerva"])

    ftree.add_edge(ftree.vertices["Bill"], ftree.vertices["Victoire"])
    ftree.add_edge(ftree.vertices["Bill"], ftree.vertices["Dominique"])
    ftree.add_edge(ftree.vertices["Bill"], ftree.vertices["Louis"])
    ftree.add_edge(ftree.vertices["Percy"], ftree.vertices["Molly"])
    ftree.add_edge(ftree.vertices["Percy"], ftree.vertices["Lucy"])
    ftree.add_edge(ftree.vertices["Ronald"], ftree.vertices["Rose"])
    ftree.add_edge(ftree.vertices["Ronald"], ftree.vertices["Hugo"])
    ftree.add_edge(ftree.vertices["Ginerva"], ftree.vertices["James"])
    ftree.add_edge(ftree.vertices["Ginerva"], ftree.vertices["Albus"])
    ftree.add_edge(ftree.vertices["Ginerva"], ftree.vertices["Lily"])

    ftree.add_edge(ftree.vertices["Victoire"], ftree.vertices["Remus"])
    ftree.add_edge(ftree.vertices["Rose"], ftree.vertices["Draco"])
    ftree.add_edge(ftree.vertices["Rose"], ftree.vertices["Aster"])
    ftree.add_edge(ftree.vertices["James"], ftree.vertices["William"])
    ftree.add_edge(ftree.vertices["Albus"], ftree.vertices["Ron"])
    ftree.add_edge(ftree.vertices["Albus"], ftree.vertices["Ginny"])
    # reading data from input file
    with open(input_file, 'r') as f:
        for line in f:
            line = line.split()
            # calling ADD_CHILD() method
            if line[0] == 'ADD_CHILD':
                if line[1] == 'King' or line[1] == 'Queen':
                    print_child_addition(ftree.add_child(line[1] + " " + line[2], line[3], line[4]))
                else:
                    print_child_addition(ftree.add_child(line[1], line[2], line[3]))
            # calling GET_RELATIONSHIP() method
            elif line[0] == 'GET_RELATIONSHIP':
                if line[1] == 'King' or line[1] == 'Queen':
                    print_relationship(ftree.get_relationship(line[1] + " " + line[2], line[3]))
                else:
                    print_relationship(ftree.get_relationship(line[1], line[2]))
