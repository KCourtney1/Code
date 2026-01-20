# HW3
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        # YOUR CODE STARTS HERE
        # True if this stack is empty, False otherwise
        if not self.top:
            return True
        return False

    def __len__(self): 
        # YOUR CODE STARTS HERE
        current = self.top
        count = 0
        while current:
            current = current.next
            count += 1
        return count
    
    def push(self,value):
        # YOUR CODE STARTS HERE
        temp = self.top
        self.top = Node(value)
        self.top.next = temp

     
    def pop(self):
        # YOUR CODE STARTS HERE
        if self.top:
            temp = self.top
            self.top = temp.next
            return temp.value

    def peek(self):
        # YOUR CODE STARTS HERE
        return self.top.value


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
            >>> x._isNumber('1213213')
            True
            >>> x._isNumber('p2.56')
            False
            >>> x._isNumber('3122.56.1231')
            False
            >>> x._isNumber('3 123 12 3123 13 123 12')
            False
            >>> x._isNumber('1.$ 1@2.3 12')
            False
        '''
        if "." in txt:
            txt = txt.split(".")
            if len(txt)>2:
                return False
            else:
                if "-"in txt[0]:
                    txt = [txt[0][1:]] + [txt[1]]
                if txt[0]=="":
                    txt[0] = "0"
                if txt[0].strip().isnumeric() and txt[1].strip().isnumeric():
                    return True
                return False
        if "-"in txt:
            txt = txt[1:]
        return txt.isnumeric()
    
    def priority(char):
            if char == "+" or char == "-":
                return 1
            if char == "*" or char == "/":
                return 2
            if char == "^":
                return 3
            return 0
    
    def postfix_split(EQ):
        """ 
            >>> Calculator.postfix_split('2-3*4')
            >>> Calculator.postfix_split('-1.0--.10')
            ["-1.0","-","-1.0"]
            >>> Calculator.postfix_split('-1.0+-.10')
            >>> Calculator.postfix_split('2*5.34+3^2+1+4')
        """
        #I wouldn't even be able to tell you what's happing down there
        cleanded_EQ = []
        while EQ:
            if EQ[0] != " ":
                group = ""
                neg_count = 0
                while EQ and not EQ[0] in "+*/^() ":
                    if EQ[0]=='-':
                        if neg_count>0:
                            EQ = "  " + EQ
                        neg_count += 1
                        if group != "":
                            EQ = "  " + EQ
                    if EQ[0] != " ":
                        group += EQ[0]
                    EQ = EQ[1:]
                if group:
                    cleanded_EQ += [group]
                if EQ and EQ[0] in "+-*/^()":
                    cleanded_EQ += [EQ[0]]
            EQ = EQ[1:]
        return cleanded_EQ
    
    def invalid_expression(self,EQ):
            """
            >>> x=Calculator()
            >>> x.invalid_expression(Calculator.postfix_split('2*5.34+3^2+1+4'))
            False
            >>> x.invalid_expression(Calculator.postfix_split('2    5'))
            True
            >>> x.invalid_expression(Calculator.postfix_split('-1.0--.10'))
            False
            >>> x.invalid_expression(Calculator.postfix_split('-1.0+-.10'))
            False
            >>> x.invalid_expression(Calculator.postfix_split('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))'))
            False
            >>> x.invalid_expression(Calculator.postfix_split('2 *      5% + 3       ^ + -2 +1 +4'))
            True
            >>> x.invalid_expression(Calculator.postfix_split('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))'))
            False
            >>> x.invalid_expression(Calculator.postfix_split('( .5 )'))
            False
        """ 
            balanced_parentheses = 0
            numbers = 0
            operators = 0
            while EQ:
                if EQ[0] == "(":
                    if balanced_parentheses < 0:
                        return True
                    balanced_parentheses+=1
                    EQ = EQ[1:]
                elif EQ[0] == ")":
                    balanced_parentheses-=1
                    EQ = EQ[1:]
                elif EQ and EQ[0] in "-+*/^":
                    operators +=1
                    EQ = EQ[1:]
                elif EQ and Calculator._isNumber(self,EQ[0]):
                    numbers += 1
                    EQ = EQ[1:]
                else:
                    return True

            if balanced_parentheses != 0:
                return True
            if not numbers == operators+1:
                return True
            return False

    def _getPostfix(self, EQ):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('7^2^3')
            "7 2 ^ 3^"
            >>> x._getPostfix('2    5')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x._getPostfix('     2 ^       4')
            '2.0 4.0 ^'
            >>> x._getPostfix('          2 ')
            '2.0'
            >>> x._getPostfix('2.1        * 5        + 3       ^ 2 +         1 +             4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2*5.34+3^2+1+4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( .5 )')
            '0.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('((2 *((5 + 3) ^ 2 + (1 +4 ))))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2* (       -5 + 3 ) ^2+ ( 1 +4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x._getPostfix('     2 * 5 + 3  ^ * 2 + 1 + 4')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x._getPostfix('25 +')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x._getPostfix(' 2 * ( 5      + 3 ) ^ 2 + ( 1 +4 ')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^  2 + ) 1 + 4 (')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x._getPostfix('2 *      5% + 3       ^ + -2 +1 +4')
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
        '''
        # YOUR CODE STARTS HERE
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        EQ = Calculator.postfix_split(EQ)
        if Calculator.invalid_expression(self,EQ):
            return "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
        
        postfix = []
        for char in EQ:
            if char == "(":
                postfixStack.push(char)
            elif char == ")":
                while postfixStack.isEmpty() == False and postfixStack.top.value != "(":
                    postfix += [postfixStack.top.value]
                    postfixStack.pop()
                if postfixStack.isEmpty() == False:
                    postfixStack.pop()
            elif char in "+-*/^":
                while postfixStack.isEmpty() == False and Calculator.priority(postfixStack.top.value) >= Calculator.priority(char):
                    postfix += [postfixStack.pop()]
                postfixStack.push(char)
            else:
                postfix.append(str(float(char)))
        while not postfixStack.isEmpty():
            postfix += [postfixStack.pop()]
        return " ".join(postfix)


        

    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            
            >>> x=Calculator()
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr('2-3*4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('4        + 3 -       2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 +          3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('      4 +           3.65  - 2        / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25      * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ((( 10 - 2*3 )) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('      8 / 4 * (3 - 2.45 * ( 4   - 2 ^ 3 )       ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 +        2 * (         5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            >>> x.calculate
            1442.7777777777778
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 ++ 3+ 2")
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr("4  3 +2")
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr('( 2 ) * 10 - 3 *( 2 - 3 * 2 ) )')
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr(' ) 2 ( *10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr('(    3.5 ) ( 15 )')
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr('3 ( 5) - 15 + 85 ( 12)') 
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
            >>> x.setExpr("( -2/6) + ( 5 ( ( 9.4 )))")
            >>> x.calculate
            "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        def operation(string_operator, num1, num2):
            if string_operator == "*":
                return num1 * num2
            if string_operator == "-":
                return num1 - num2
            if string_operator == "+":
                return num1 + num2
            if string_operator == "/":
                return num1 / num2
            if string_operator == "^":
                return num1 ** num2
        calcStack = Stack()   # method must use calcStack to compute the  expression

        # YOUR CODE STARTS HERE
        if self._getPostfix(self.getExpr)=="ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom":
            return "ERROR: You couldn't pour water out of a bucket if the instructions were written on the bottom"
        Postfix_Expr = self._getPostfix(self.getExpr).split()
        for item in Postfix_Expr:
            if item in "+-*/^":
                num2 = calcStack.pop()
                num1 = calcStack.pop()
                total = operation(item, num1, num2)
                calcStack.push(total)
            else:
                calcStack.push(float(item))
        return calcStack.top.value
            
            

#=============================================== Part III ==============================================

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
            >>> C._isVariable('%voleqwe2')
            False
        '''
        # YOUR CODE STARTS HERE
        if word[0].isalpha():
            word = word[1:]
            for char in word:
                if not char.isalnum():
                    return False
            return True
        return False
       

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('105 + %x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        # YOUR CODE STARTS HERE
        expr = expr.split(sep=None)
        for i in range(len(expr)):
            if expr[i][0].isalpha():
                if expr[i] in self.states:
                    expr[i] = f"{self.states[expr[i]]}"
                else:
                    return None
            if not Calculator._isNumber(self, expr[i]) and not expr[i] in "*-+/^()":
                return None
        return " ".join(expr)

    def get_varible_name(self, expr):
        varible = ""
        while expr[0] != " ":
            varible += expr[0]
            expr = expr[1:]
        return varible
    def get_varible_value(self, expr):
        while expr:
            if Calculator._isNumber(self,expr[0]):
                value = float(expr[0])
            expr = expr[1:]
        return value
    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        # YOUR CODE STARTS HERE
        self.expressions = self.expressions.split(";")
        self.states[self.get_varible_name(self.expressions[0])]= self.get_varible_value(self.expressions[0])
        self.expressions.pop(0)
        for expression in self.expressions:
            expression = self._replaceVariables(expression)



def run_tests():
    import doctest

    # Run tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run tests per function - Uncomment the next line to run doctest by function. Replace Stack with the name of the function you want to test
    doctest.run_docstring_examples(Calculator.postfix_split, globals(), name='HW3',verbose=True)   

if __name__ == "__main__":
    run_tests()