import os

def increment_by_5(lst):
    """
        precondition: lst is a list of numbers
        postcondition: returns a new list where every element of lst is increased by 5. non-destructive
        >>> increment_by_5([-5, 10 ,26, 8])
        [0, 15, 31, 13]
        >>> my_lst = [9, 8, 7, 24, 26, 23]
        >>> increment_by_5(my_lst)
        [14, 13, 12, 29, 31, 28]
        >>> my_lst
        [9, 8, 7, 24, 26, 23]
    """
    if len(lst) == 1:
        return [lst[0]+5]
    else:
        return [lst[0]+5]+increment_by_5(lst[1:])

def to_evens(lst):
    """
        precondition: lst is a list of numbers
        postcondition: returns a new list where every odd element of lst is increased by 1. non-destructive
        >>> to_evens([-5, 10, 19, 26, 8, 7]) 
        [-4, 10, 20, 26, 8, 8]
        >>> my_lst = [9, 8, 7, 24, 26, 23]   
        >>> to_evens(my_lst)
        [10, 8, 8, 24, 26, 24]
        >>> my_lst
        [9, 8, 7, 24, 26, 23]
    """
    if len(lst) == 1:
        if lst[0]%2 != 0:
            return [lst[0]+1]
        else:
            return [lst[0]]
    else:
        if lst[0]%2 != 0:
            return [lst[0]+1]+to_evens(lst[1:])
        else:
            return [lst[0]]+to_evens(lst[1:])

def next_double(lst):
    """
        precondition: lst is a list of numbers
        postcondition: returns an integer that represents the number of elements that are followed by their double in lst. non-destructive
        >>> next_double([1,2,4,8,16,32,64,128,256])
        8
        >>> next_double([1,3,4,2,32,8,128,-5,6]) 
        0
        >>> next_double([1,0,0,-5,-10,32,64,128,2,9,18])
        5
        >>> next_double([1,2])
        1
        >>> next_double([1])   
        0
    """
    if len(lst) == 1:
        return 0
    elif len(lst)==2:
        if lst[0]*2 == lst[1]:
            return 1
        else:
            return 0
    else:
        if lst[0]*2 == lst[1]:
            return 1+next_double(lst[1:])
        else:
            return 0+next_double(lst[1:])

def create_square_matrix(file):
    """
        precondition: file represents the name of a .txt file. file contains comma-separated integer values representing the elements of the matrix.
        postcondition: returns a 2D list (square matrix) based on the contents of the file
        creates a 2d list given a 2dmatrix on a .txt file 1, 2, 3 to [[1, 2, 3],[1, 2, 3],[1, 2, 3]]
                                                          1, 2, 3
                                                          1, 2, 3

        >>> create_square_matrix('num_1.txt')
        [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
        >>> create_square_matrix('num_2.txt') 
        [[16, 14, 7, 30, 23], [24, 17, 10, 8, 31], [32, 25, 18, 11, 4], [5, 28, 26, 19, 12], [13, 6, 29, 22, 20]]
    """
    
    target_path = os.path.join(os.path.dirname(__file__), file)
    square_lst = []
    with open(target_path,"r") as the_file:
        contents = the_file.readlines()
        for row in contents:
            row = row.split(",")
            num_lst = []
            for num in row:
                num = num.strip(", ")
                num_lst.append(int(num))
            square_lst.append(num_lst)
    return square_lst

def is_magic_square(file):
    """
        precondition: file represents the name of a .txt file that contains comma-separated integer values representing the elements of the matrix
        postcondition: returns True if the 2D list is a magic square, False otherwise.
        >>> is_magic_square('num_1.txt') 
        True
        >>> is_magic_square('num_2.txt') 
        True
        >>> is_magic_square('num_3.txt') 
        True
        >>> is_magic_square('num_4.txt') 
        False
        >>> is_magic_square('num_5.txt') 
        False
    """
    # get total of first row then save that then compare next rows ,colums, and horizantal to that, if diffrent return false otherwise true
    square_matrix = create_square_matrix(file)

    first_total = 0
    diagonal_total1 = 0
    diagonal_total2 = 0
    for i in range(len(square_matrix)):
        total = 0
        for j in range(len(square_matrix[i])):
            total += square_matrix[i][j]
            if i == j:
                diagonal_total1 += square_matrix[i][j]
                diagonal_total2 += square_matrix[i][-(j+1)]
        if i == 0:
            first_total = total
        elif first_total != total:
            return False
        
    if diagonal_total1 == first_total == diagonal_total2:
        return True
    return False
            
def decrypt(input_file, key, output_file):
        return encrypt_message(input_file, -1*key, output_file)

def encrypt_message(file,key,output_file):
    """
        precondition: function takes three arguments, a string, file, that represents the name of a .txt file, an integer, key, and a string, output_file, that represents the name of a .txt file.
        postcondition: reads the contents from file and encrypts its contents using the Caesar cipher method with the provided key. The encrypted message is then saved into output_file using the same format as the original file (words per line).
        uppercase and lowercase letters (case sensitivity remains in decrypted message), numbers, spaces and punctuation remain the same.
        >>> encrypt_message('text_1.txt', 7, 'enc_t1.txt')   
        >>> decrypt('enc_t1.txt', 7, 'plain_t1.txt')
    """
    # dictionary of what values change to if they are the key(char in word) then will replace with that value otherwise keeps value(punctioation/spaces) and adds to new string
    target_path = os.path.join(os.path.dirname(__file__), file)
    out_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(target_path, "r") as the_file, open(out_path, 'w') as out_file:
        content = the_file.readlines()
        for row in content:
            line = ""
            for char in row:
                newUnicodeValue = ord(char)+key
                if 65 <= ord(char) <= 90:
                    if newUnicodeValue > 90:
                        newUnicodeValue -= 26
                    line+= chr(newUnicodeValue)
                elif 97 <= ord(char) <=122:
                    if newUnicodeValue > 122:
                        newUnicodeValue -= 26
                    line+= chr(newUnicodeValue)
                else:
                    line += char
            out_file.write(f"{line}")

def run_tests_b():
  import doctest
  doctest.run_docstring_examples(encrypt_message, globals(), name="HW2", verbose=True)
  
if __name__== "__main__":
  run_tests_b()