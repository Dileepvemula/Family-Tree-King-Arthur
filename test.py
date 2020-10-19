import sys
import pytest

import meet_the_family as ft


def create_tree():
    """
    Initial tree created is: Family of 'A':
                      A----Z*
                       /|\
                     /  | \
                    /   |  \
               X*--B    C*  D*--Y
                  /        / \
                 /        /   \
                E        F*    G        where * represents female

    :return: returns the whole tree created
    """
    ftree = ft.GraphADT()
    ftree.add_vertex(data={"name": "A", "spouse_name": "Z", "gender": "Male"})
    ftree.add_vertex(data={"name": "B", "spouse_name": "X", "gender": "Male"})
    ftree.add_vertex(data={"name": "C", "spouse_name": None, "gender": "Female"})
    ftree.add_vertex(data={"name": "D", "spouse_name": "Y", "gender": "Female"})
    ftree.add_vertex(data={"name": "E", "spouse_name": None, "gender": "Male"})
    ftree.add_vertex(data={"name": "F", "spouse_name": None, "gender": "Female"})
    ftree.add_vertex(data={"name": "G", "spouse_name": None, "gender": "Male"})

    ftree.add_edge(ftree.vertices["A"], ftree.vertices["B"])
    ftree.add_edge(ftree.vertices["A"], ftree.vertices["C"])
    ftree.add_edge(ftree.vertices["A"], ftree.vertices["D"])
    ftree.add_edge(ftree.vertices["B"], ftree.vertices["E"])
    ftree.add_edge(ftree.vertices["D"], ftree.vertices["F"])
    ftree.add_edge(ftree.vertices["D"], ftree.vertices["G"])
    return ftree


def test_tree_creation():
    """
    Asserts if the tree created vertices and  edges as required along with class attribute
    values and updated values such as incident edges and children when creating edges.
    """
    ftree_obj = create_tree()
    result = []
    message_children = "Test creation unsuccessful. Children of {} should be {} but returned {}"
    message_gender = "Gender set wrong. Gender of {} should be {} but returned {}"
    message_spouse = "Spouse set wrong. Spouse of {} is {} but returned {}"
    message_parents = "Parents set wrong. Parents of {} are {} but returned {}"
    message_exists = "{} does not exist but exist_status returned {}"
    result.append(len(ftree_obj.vertices["C"].children))
    result.append(len(ftree_obj.vertices["A"].children))
    result.append(len(ftree_obj.vertices["B"].children))
    result.append(ftree_obj.vertices["A"].gender)
    result.append(ftree_obj.vertices["A"].get_spouse_gender())
    result.append("H" in ftree_obj.vertices)
    result.append(ftree_obj.vertices["D"].spouse_name)
    result.append((ftree_obj.vertices["E"].incident_edges[0].name,
                   ftree_obj.vertices["E"].incident_edges[0].spouse_name))
    assert result[0] == 0, message_children.format("C", 0, result[0])
    assert result[1] == 3, message_children.format("A", 3, result[1])
    assert result[3] == 'Male', message_gender.format("A", "Male", result[3])
    assert result[5] == False, message_exists.format("H", result[5])
    assert result[6] == "Y", message_spouse.format("D", "Y", result[6])
    assert result[7] == ("B", "X"), message_parents.format("E", "B and X", result[7])
    assert not result[2] == 3, message_children.format("B", 3, result[2])
    assert not result[4] == 'Male', message_gender.format("Z", "Female", result[4])


def test_vertex_creation():
    """
    Asserts if the vertex created is in right format with all class attributes initialized as required
    """
    result = []
    message_VC = "Vertex {} not created."
    message_name = "Vertex {} name not correct. Should be {} but returned {}"
    message_gender = "Vertex {} gender not correct. Should be {} but returned {}"
    message_spouse = "Vertex {} gender should be {} but returned {}"
    message_parents = "Vertex {} parents should be empty but returned {}"
    message_children = "Vertex {} children count should be 0 but returned {}"
    v = ft.Vertex(data={"name": "test_name", "gender": "Male", "spouse_name": None})
    result.append(v)
    result.append(v.name)
    result.append(v.gender)
    result.append(v.spouse_name)
    result.append(bool(v.incident_edges))
    result.append(len(v.children))

    assert result, message_VC.format("v")
    assert result[1] == "test_name", message_name.format("v", "test_name", result[1])
    assert result[2] == "Male", message_gender.format("v", "Male", result[2])
    assert result[3] is None, message_spouse.format("v", None, result[3])
    assert result[5] == 0, message_children.format("v", result[5])
    assert not result[0] is None, message_VC.format("v")
    assert not result[2] == "Female", message_gender.format("v", "Male", result[2])
    assert not result[3] == "", message_spouse.format("v", None, result[3])
    assert not result[4], message_parents.format("v", result[4])


def test_spouse_gender_vertex():
    """
    Tests get_spouse_gender() method of Vertex class. Asserts if the spouse gender returned
    is opposite of vertex gender
    """
    v = ft.Vertex(data={"name": "test_name", "gender": "Male", "spouse_name": "W"})
    message = "Spouse gender of {} should be {} but returned {}"
    result = v.get_spouse_gender()
    assert result == "Female", message.format("v", "Female", result)
    assert result is not None, message.format("v", "Female", result)


def test_edge_creation():
    """
    Tests if the edge created is as expected with start and end vertices correct and 
    incident edges of end vertex are updated.
    """
    v = ft.Vertex(data={"name": "test_name", "gender": "Male", "spouse_name": "W"})
    u = ft.Vertex(data={"name": "test_name2", "gender": "Female", "spouse_name": None})
    edge = ft.Edge(v, u)
    result = bool(edge.end.incident_edges)
    message_start = "{} should be the start vertex but returned {} with name {}"
    message_end = "{} should be the end vertex but returned {} with name {}"
    message = "Edge not created between {} and {} as exist status of incident edges of {} is {} "
    assert edge.start == v, message_start.format("v", edge.start, edge.start.name)
    assert edge.end == u, message_end.format("u", edge.end, edge.end.name)
    assert result, message.format("v", "u", "u", result)
    assert not edge.start == u, message_start.format("v", edge.start, edge.start.name)
    assert not edge.end == v, message_end.format("u", edge.end, edge.end.name)
    assert not bool(edge.start.incident_edges), message.format("u", "v", "v", bool(edge.start.incident_edges))


def test_add_child():
    """
    Tests if the child is added or not. Asserts add_child() method that child is added only through
    mother and only if both parents exist and one of them is a female and other is male.
    """
    ftree_obj = create_tree()
    message = "Child addition status of {} to {} should be {}, but returned {}"
    result = [ftree_obj.add_child("C", "I", "Male"), ftree_obj.add_child("E", "J", "Female"),
              ftree_obj.add_child("X", "K", "Male"), ftree_obj.add_child("A", "L", "Female"),
              ftree_obj.add_child("Z", "M", "Male"), ftree_obj.add_child("H", "N", "Female"),
              ftree_obj.add_child("Y", "V", "Male")]
    #  1 : Success
    # -1 : Failure
    #  0 : Parent not found
    assert result[0] == -1, message.format("I", "C", -1, result[0])
    assert result[1] == -1, message.format("J", "E", -1, result[1])
    assert result[2] == 1, message.format("K", "X", 1, result[2])
    assert result[3] == -1, message.format("L", "A", -1, result[3])
    assert result[4] == 1, message.format("M", "Z", 1, result[4])
    assert result[5] == 0, message.format("N", "H", 0, result[5])
    assert not result[0] == 1, message.format("I", "C", -1, result[0])
    assert not result[1] == 1, message.format("J", "E", -1, result[1])
    assert not result[3] == 1, message.format("L", "A", -1, result[3])
    assert not result[6] == 1, message.format("V", "Y", -1, result[6])


def test_get_relationship():
    """
    Tests get_relationship() method of GraphADT class. Asserts the list returned from the method with expected list
    """
    ftree_obj = create_tree()
    message = "Relationship wrong. {} of {} should be {} but returned {}"
    result = [ftree_obj.get_relationship("E", "Paternal-Uncle")]
    assert result[0] == [], message.format("Paternal-Uncle", "E", [], result[0])
    ftree_obj.add_child("Z", "H", "Male")
    result.append(ftree_obj.get_relationship("E", "Paternal-Uncle"))
    result.append(ftree_obj.get_relationship("X", "Paternal-Uncle"))
    result.append(ftree_obj.get_relationship("A", "Paternal-Uncle"))
    result.append(ftree_obj.get_relationship("F", "Paternal-Uncle"))
    result.append(ftree_obj.get_relationship("I", "Paternal-Uncle"))
    assert result[1] == ["H"], message.format("Paternal-Uncle", "E", ["H"], result[1])
    assert result[2] == [], message.format("Paternal-Uncle", "X", [], result[2])
    assert result[3] == [], message.format("Paternal-Uncle", "A", [], result[3])
    assert result[4] == [], message.format("Paternal-Uncle", "F", [], result[4])
    assert result[5] is None, message.format("Paternal-Uncle", "I", None, result[5])

    result.append(ftree_obj.get_relationship("E", "Maternal-Uncle"))
    result.append(ftree_obj.get_relationship("X", "Maternal-Uncle"))
    result.append(ftree_obj.get_relationship("A", "Maternal-Uncle"))
    result.append(ftree_obj.get_relationship("F", "Maternal-Uncle"))
    result.append(ftree_obj.get_relationship("I", "Maternal-Uncle"))
    assert result[6] == [], message.format("Maternal-Uncle", "E", [], result[6])
    assert result[7] == [], message.format("Maternal-Uncle", "X", [], result[7])
    assert result[8] == [], message.format("Maternal-Uncle", "A", [], result[8])
    assert result[9] == ["B", "H"], message.format("Maternal-Uncle", "F", ["B", "H"], result[9])
    assert result[10] is None, message.format("Maternal-Uncle", "I", None, result[10])

    result.append(ftree_obj.get_relationship("E", "Paternal-Aunt"))
    result.append(ftree_obj.get_relationship("X", "Paternal-Aunt"))
    result.append(ftree_obj.get_relationship("A", "Paternal-Aunt"))
    result.append(ftree_obj.get_relationship("F", "Paternal-Aunt"))
    result.append(ftree_obj.get_relationship("I", "Paternal-Aunt"))
    assert result[11] == ["C", "D"], message.format("Paternal-Aunt", "E", ["C", "D"], result[11])
    assert result[12] == [], message.format("Paternal-Aunt", "X", [], result[12])
    assert result[13] == [], message.format("Paternal-Aunt", "A", [], result[13])
    assert result[14] == [], message.format("Paternal-Aunt", "F", [], result[14])
    assert result[15] is None, message.format("Paternal-Aunt", "I", None, result[15])

    result.append(ftree_obj.get_relationship("E", "Maternal-Aunt"))
    result.append(ftree_obj.get_relationship("X", "Maternal-Aunt"))
    result.append(ftree_obj.get_relationship("A", "Maternal-Aunt"))
    result.append(ftree_obj.get_relationship("F", "Maternal-Aunt"))
    result.append(ftree_obj.get_relationship("I", "Maternal-Aunt"))
    assert result[16] == [], message.format("Maternal-Aunt", "E", [], result[16])
    assert result[17] == [], message.format("Maternal-Aunt", "X", [], result[17])
    assert result[18] == [], message.format("Maternal-Aunt", "A", [], result[18])
    assert result[19] == ["C"], message.format("Maternal-Aunt", "F", ["C"], result[19])
    assert result[20] is None, message.format("Maternal-Aunt", "I", None, result[20])

    message_same = "{} of {} and {} should be same as they are a couple but returned otherwise"
    result.append(ftree_obj.get_relationship("X", "Son"))
    result.append(ftree_obj.get_relationship("D", "Son"))
    result.append(ftree_obj.get_relationship("C", "Son"))
    result.append(ftree_obj.get_relationship("I", "Son"))
    result.append(ftree_obj.get_relationship("B", "Son"))
    assert result[21] == ["E"], message.format("Son", "X", ["E"], result[21])
    assert result[22] == ["G"], message.format("Son", "D", ["G"], result[22])
    assert result[23] == [], message.format("Son", "C", [], result[23])
    assert result[24] is None, message.format("Son", "I", None, result[24])
    assert result[25] == ["E"], message.format("Son", "B", ["E"], result[25])
    assert result[21] == result[25], message_same.format("Son", "X", "B")

    result.append(ftree_obj.get_relationship("X", "Daughter"))
    result.append(ftree_obj.get_relationship("D", "Daughter"))
    result.append(ftree_obj.get_relationship("C", "Daughter"))
    result.append(ftree_obj.get_relationship("I", "Daughter"))
    result.append(ftree_obj.get_relationship("Y", "Daughter"))
    assert result[26] == [], message.format("Daughter", "X", [], result[26])
    assert result[27] == ["F"], message.format("Daughter", "D", ["F"], result[27])
    assert result[28] == [], message.format("Daughter", "C", [], result[28])
    assert result[29] is None, message.format("Daughter", "I", None, result[29])
    assert result[30] == ["F"], message.format("Daughter", "Y", ["F"], result[30])
    assert result[27] == result[30], message_same.format("Daughter", "D", "Y")

    result.append(ftree_obj.get_relationship("I", "Siblings"))
    result.append(ftree_obj.get_relationship("X", "Siblings"))
    result.append(ftree_obj.get_relationship("A", "Siblings"))
    result.append(ftree_obj.get_relationship("C", "Siblings"))
    result.append(ftree_obj.get_relationship("E", "Siblings"))
    result.append(ftree_obj.get_relationship("F", "Siblings"))
    result.append(ftree_obj.get_relationship("G", "Siblings"))
    assert result[31] is None, message.format("Siblings", "I", None, result[31])
    assert result[32] == [], message.format("Siblings", "X", [], result[32])
    assert result[33] == [], message.format("Siblings", "A", [], result[32])
    assert result[34] == ["B", "D", "H"], message.format("Siblings", "C", ["B", "D", "H"], result[32])
    assert result[35] == [], message.format("Siblings", "E", [], result[32])
    assert result[36] == ["G"], message.format("Siblings", "F", ["G"], result[32])
    assert result[37] == ["F"], message.format("Siblings", "G", ["F"], result[32])

    result.append(ftree_obj.get_relationship("I", "Brother"))
    result.append(ftree_obj.get_relationship("X", "Brother"))
    result.append(ftree_obj.get_relationship("A", "Brother"))
    result.append(ftree_obj.get_relationship("B", "Brother"))
    result.append(ftree_obj.get_relationship("C", "Brother"))
    result.append(ftree_obj.get_relationship("E", "Brother"))
    assert result[38] is None, message.format("Brother", "I", None, result[38])
    assert result[39] == [], message.format("Brother", "X", [], result[39])
    assert result[40] == [], message.format("Brother", "A", [], result[40])
    assert result[41] == ["H"], message.format("Brother", "B", ["H"], result[41])
    assert result[42] == ["B", "H"], message.format("Brother", "C", ["B", "H"], result[42])
    assert result[43] == [], message.format("Brother", "E", [], result[43])

    result.append(ftree_obj.get_relationship("I", "Sister"))
    result.append(ftree_obj.get_relationship("X", "Sister"))
    result.append(ftree_obj.get_relationship("A", "Sister"))
    result.append(ftree_obj.get_relationship("H", "Sister"))
    result.append(ftree_obj.get_relationship("C", "Sister"))
    result.append(ftree_obj.get_relationship("E", "Sister"))
    assert result[44] is None, message.format("Sister", "I", None, result[44])
    assert result[45] == [], message.format("Sister", "X", [], result[45])
    assert result[46] == [], message.format("Sister", "A", [], result[46])
    assert result[47] == ["C", "D"], message.format("Sister", "H", ["C", "D"], result[47])
    assert result[48] == ["D"], message.format("Sister", "C", ["D"], result[48])
    assert result[49] == [], message.format("Sister", "E", [], result[49])

    result.append(ftree_obj.get_relationship("I", "Sister-In-Law"))
    result.append(ftree_obj.get_relationship("X", "Sister-In-Law"))
    result.append(ftree_obj.get_relationship("Y", "Sister-In-Law"))
    result.append(ftree_obj.get_relationship("H", "Sister-In-Law"))
    result.append(ftree_obj.get_relationship("E", "Sister-In-Law"))
    result.append(ftree_obj.get_relationship("A", "Sister-In-Law"))
    assert result[50] is None, message.format("Sister-In-Law", "I", None, result[50])
    assert result[51] == ["C", "D"], message.format("Sister-In-Law", "X", ["C", "D"], result[51])
    assert result[52] == ["C"], message.format("Sister-In-Law", "Y", ["C"], result[52])
    assert result[53] == ["X"], message.format("Sister-In-Law", "H", ["X"], result[53])
    assert result[54] == [], message.format("Sister-In-Law", "E", [], result[54])
    assert result[55] == [], message.format("Sister-In-Law", "A", [], result[55])

    result.append(ftree_obj.get_relationship("I", "Brother-In-Law"))
    result.append(ftree_obj.get_relationship("X", "Brother-In-Law"))
    result.append(ftree_obj.get_relationship("Y", "Brother-In-Law"))
    result.append(ftree_obj.get_relationship("H", "Brother-In-Law"))
    result.append(ftree_obj.get_relationship("E", "Brother-In-Law"))
    result.append(ftree_obj.get_relationship("A", "Brother-In-Law"))
    assert result[56] is None, message.format("Brother-In-Law", "I", None, result[56])
    assert result[57] == ["H"], message.format("Brother-In-Law", "X", ["H"], result[57])
    assert result[58] == ["B", "H"], message.format("Brother-In-Law", "Y", ["B", "H"], result[58])
    assert result[59] == ["Y"], message.format("Brother-In-Law", "H", ["Y"], result[59])
    assert result[60] == [], message.format("Brother-In-Law", "E", [], result[60])
    assert result[61] == [], message.format("Brother-In-Law", "A", [], result[61])


def test_spouse_search():
    """
    Tests the spouse_search() method of GraphADT class. This method is expected to return
    True if the given name is spouse of the vertices of graph object.
    False otherwise
    test method asserts the returned values of spouse_search method with expected values.
    """
    ftree_obj = create_tree()
    message = "Spouse search of {} should return {}, but returned {}"
    result = [ftree_obj.spouse_search("Z"), ftree_obj.spouse_search("Y"), ftree_obj.spouse_search("C"),
              ftree_obj.spouse_search("A"), ftree_obj.spouse_search("H")]
    assert result[0] == True, message.format("Z", True, result[0])
    assert result[1] == True, message.format("Y", True, result[1])
    assert result[2] == False, message.format("C", False, result[2])
    assert not result[3] == True, message.format("A", False, result[3])
    assert not result[4] == True, message.format("H", False, result[4])


def test_get_spouse_name():
    """
    Tests get_spouse_name() method of GraphADT class. This method returns the vertex.name
    of the name used as argument to this method. Asserts the returned value with the expected values.
    """
    ftree_obj = create_tree()
    message = "Get spouse name of {} should return {} if spouse exists, but returned {}"
    result = [ftree_obj.get_spouse_name("C"), ftree_obj.get_spouse_name("H"), ftree_obj.get_spouse_name("Y"),
              ftree_obj.get_spouse_name("A")]
    assert result[0] == "", message.format("C", "", result[0])
    assert result[1] == "", message.format("H", "", result[1])
    assert result[2] == "D", message.format("Y", "D", result[2])
    assert result[3] == "", message.format("A", "", result[3])
    assert not result[3] == "Z", message.format("A", "", result[3])


def test_print_child_addition(capsys):
    """
    Tests if the output printed to the command prompt is as expected to the respective inputs.
    """
    message = "Print statement should be {} but printed {}"
    ft.print_child_addition(1)
    captured = capsys.readouterr()
    assert captured.out == "CHILD_ADDED\n", message.format("CHILD_ADDED", captured.out)
    assert not captured.out == "PERSON_NOT_FOUND\n", message.format("CHILD_ADDED", captured.out)
    assert not captured.out == "CHILD_ADDITION_FAILED\n", message.format("CHILD_ADDED", captured.out)

    ft.print_child_addition(0)
    captured = capsys.readouterr()
    assert captured.out == "PERSON_NOT_FOUND\n", message.format("PERSON_NOT_FOUND", captured.out)
    assert not captured.out == "CHILD_ADDITION_FAILED\n", message.format("PERSON_NOT_FOUND", captured.out)
    assert not captured.out == "CHILD_ADDED\n", message.format("PERSON_NOT_FOUND", captured.out)

    ft.print_child_addition(-1)
    captured = capsys.readouterr()
    assert captured.out == "CHILD_ADDITION_FAILED\n", message.format("CHILD_ADDITION_FAILED", captured.out)
    assert not captured.out == "PERSON_NOT_FOUND\n", message.format("CHILD_ADDITION_FAILED", captured.out)
    assert not captured.out == "CHILD_ADDED\n", message.format("CHILD_ADDITION_FAILED", captured.out)


def test_print_relationship(capsys):
    """
    Tests if the output printed to the command prompt is as expected to the respective inputs.
    """
    message = "Print statement should be {} but printed {}"
    ft.print_relationship(None)
    captured = capsys.readouterr()
    assert captured.out == "PERSON_NOT_FOUND\n", message.format("PERSON_NOT_FOUND", captured.out)
    assert not captured.out == "NONE\n", message.format("NONE", captured.out)
    assert not captured.out == " \n", message.format("PERSON_NOT_FOUND", captured.out)

    ft.print_relationship([])
    captured = capsys.readouterr()
    assert captured.out == "NONE\n", message.format("NONE", captured.out)
    assert not captured.out == "PERSON_NOT_FOUND\n", message.format("NONE", captured.out)
    assert not captured.out == " \n", message.format("NONE", captured.out)

    ft.print_relationship([3, 2, 1, 4])
    captured = capsys.readouterr()
    assert captured.out == "3 2 1 4 \n", message.format("3 2 1 4", captured.out)
    assert not captured.out == "1 2 3 4 \n", message.format("3 2 1 4", captured.out)
    assert not captured.out == "4 3 2 1 \n", message.format("3 2 1 4", captured.out)
    assert not captured.out == "3 \n2 \n1 \n4 \n", message.format("3 2 1 4", captured.out)

    ft.print_relationship([1])
    captured = capsys.readouterr()
    assert captured.out == "1 \n", message.format("1 ", captured.out)

    ft.print_relationship((1, 2, 3))
    captured = capsys.readouterr()
    assert captured.out == "1 2 3 \n", message.format("1 2 3", captured.out)
    assert not captured.out == "3 2 1 \n", message.format("1 2 3", captured.out)
    assert not captured.out == "3 \n2 \n1 \n", message.format("1 2 3", captured.out)

    ft.print_relationship(())
    captured = capsys.readouterr()
    assert captured.out == "NONE\n", message.format("NONE ", captured.out)
    assert not captured.out == "PERSON_NOT_FOUND\n", message.format("NONE", captured.out)
    assert not captured.out == " \n", message.format("NONE", captured.out)


if __name__ == '__main__':
    pytest.main(sys.argv)
