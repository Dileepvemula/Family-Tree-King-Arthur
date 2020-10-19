Please make sure you have Python3 and pip installed before you begin.

To run this application, using command prompt, move to the directory where these files are stored.
Run the following commands:

        pip install -r requirements.txt

To run the main python file, run the following command:
        python -m  meet_the_family <absolute path to input file>

2 sample input files are provided in IO folder with names "input1.txt" and "input2.txt"
whose expected outputs are in "output1.txt" and "output2.txt" respectively.
Each input file contains lines of the format:

        ADD_CHILD mother_name child_name gender
        GET_RELATIONSHIP name relation_name

To run the test file, run the following command:
        python -m  test



Note:
Assumptions:
1. Same Sex Marriage is not allowed.
2. Divorce and marriage again is not allowed.
3. Child addition is possible only if both parents exist (Single parent not allowed)

GET_RELATIONSHIP supports the following relations:
1. Paternal-Uncle
2. Maternal-Uncle
3. Paternal-Aunt
4. Maternal-Aunt
5. Son
6. Daughter
7. Siblings
8. Brother
9. Sister
10. Sister-In-Law
11. Brother-In-Law
