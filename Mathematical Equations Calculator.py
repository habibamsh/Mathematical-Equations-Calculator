# Mathematical-Equations-Calculator
#Date: 10/24/2020

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
        self.count=0
    
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
        #Returns false if there is a top value in the stack and returns true otherwise
        return self.top == None

    def __len__(self): 
        #Returns the number of nodes in the stack
        return self.count

    def push(self,e):
        #creates a new node with value e
        new_node = Node(e)

        #If the stack is not empty, 'new_node.next' is made to be the top node and then 'new_node' is made the new top node
        if self.top != None:
            new_node.next = self.top
            self.top = new_node
        #if the stack is empty, 'new_node' is made to be the new top node
        else:
            self.top = new_node

        #the node count is increase by 1
        self.count += 1
        return None

     
    def pop(self):
        #If there is a top node, its connection is severed from the node after the next node is assigned as the new top
        #The removed node's stored value is returned and the node count is reduced by 1
        if self.top != None:
            removed_node = self.top
            self.top = self.top.next
            removed_node.next = None
            self.count -= 1
            return removed_node.value

        #If the stack is empty return None
        else:
            return None

    def peek(self):
        #if the stack is not empty, returns the top node's value
        if self.top != None:
            return self.top.value
        #Otherwise return None
        else:
            return None


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

    def isNumber(self, txt):
        #This is used for scanning given expressions whether the input is a number or string.
        #Returns true if it's a number, and false otherwise
        try:
            float(txt)
            return True
        except(ValueError):
            return False





    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('2 ^ 4')
            '2.0 4.0 ^'
            >>> x._getPostfix('2')
            '2.0'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2 * 5.34 + 3 ^ 2 + 1 + 4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( 2.5 )')
            '2.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * ( ( 5 + -3 ) ^ 2 + ( 1 + 4 ) )')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( 2 * ( ( 5 + 3 ) ^ 2 + ( 1 + 4 ) ) )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( ( 2 * ( ( 5 + 3 ) ^ 2 + ( 1 + 4 ) ) ) )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2 * ( -5 + 3 ) ^ 2 + ( 1 + 4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('2 * 5 + 3 ^ - 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ) 1 + 4 (')
            >>> x._getPostfix('2 * 5% + 3 ^ + -2 + 1 + 4')
        '''

        postOp = Stack()
        #'infix' stores the input of the function
        infix = txt
        #'infix_list' stores each variable of 'infix' seperately
        infix_list = infix.split()
        #this list will be used to store the postfix form of the expression
        postfix_list = []
        #List of operators, the lower the index the higher the priority
        operator_list = [')','(','^','*','/','+','-']
        #This list stores every occurrence of parentheses
        pars_list1 = []
        #This list stores every number
        pars_list2 = []
        #This list stores every operator
        pars_list3 = []
        #This is used to join 'postfix_list' into a string
        join_list = ' '

        #This loop goes through postfix_list for later use in error checks
        for pars in infix_list:
            #This stores parentheses into pars_list1
            if pars == '(' or pars == ')':
                pars_list1.append(pars)
                #If at any point, the number of right parentheses is more than left parentheses return None
                if pars_list1.count('(') < pars_list1.count(')'):
                    return None
            #If 'pars' is a number, append it into 'pars_list2'
            elif self.isNumber(pars):
                pars_list2.append(pars)
            #if 'pars' is an operator, append it into 'pars_list3'
            elif pars in operator_list:
                pars_list3.append(pars)

        #This if statement does error checks, if the number of operators is larger than or equal to the number of digits, return None
        #or the difference between the number of operators and the number of digits is not 1, return None
        if len(pars_list2) <= len(pars_list3) or len(pars_list2) - len(pars_list3) != 1:
            return None
        #If the number of left and right parentheses do not match, return None
        elif infix_list.count('(') != infix_list.count(')'):
            return None

        else:
            try:
                #This loop goes through 'infix_list'
                for string in infix_list:
                    #if the string is a digit, append it into 'postfix_list'
                    if self.isNumber(string):
                        postfix_list.append(str(float(string)))

                    #else it is an operator
                    else:
                        #If the 'postOp' stack is empty or the string is a left parentheses or the top of the stack is a left parentheses and the string is not a right parentheses
                        #push the operator into the stack
                        if (postOp.isEmpty() or (string == '(' or postOp.peek() == '(')) and string != ')':
                            postOp.push(string)

                        else:
                            #This loops if the stack is not empty
                            while not postOp.isEmpty():
                                #if the operator is a positive or has lower priorety than the stack's top value, or the string is a right parentheses or the string a multiplication with the top of the stack being a division
                                if string == '+' or operator_list.index(string) >= operator_list.index(postOp.top.value) or string == ')' or (string == '*' and postOp.peek() == '/'):
                                    #if the top of the stack is not a left parentheses, append the top value of the stack into 'postfix_list'
                                    if postOp.peek() != '(':
                                        postfix_list.append(postOp.pop())

                                    #if the top of the stack eventually gets to a parentheses, remove it from the stack and break the while loop
                                    else:
                                        postOp.pop()
                                        break
                                #if the string has a high priorety and the top of the stack is not of equal priorety or a parentheses, break the while loop
                                else:
                                    break
                            #if the string is not a right parentheses, push it into the stack
                            if string != ')':
                                postOp.push(string)
            #If there is an invalid string in infix_list, return None
            except(ValueError):
                return None
        #After the 'for' loop is over, append the remaining operators from the stack into 'postfix_list'
        while not postOp.isEmpty() and postOp.peek() != '(':
            postfix_list.append(postOp.pop())
        #Join 'postfix_list' into a string and return it
        return join_list.join(postfix_list)


                    


        


    @property
    def calculate(self):
        '''
            Required: calculate must call postfix
                      calculate must create and use a Stack to compute the final result as shown in the video lecture
            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr(' 2 - 3 * 4')
            >>> x.calculate
            -10.0
            >>> x.setExpr(' 3 * ( ( ( 10 - 2 * 3 ) ) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('8 / 4 * ( 3 - 2.45 * ( 4 - 2 ^ 3 ) ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 + 2 * ( 5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * ( 2 + ( 3.0 ) * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 / 3 ) ) - 2 / 3 ^ 2')
            >>> x.calculate
            1442.7777777777778
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 + + 3 + 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 + 2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * ( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( * 10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calculateStack=Stack()
        
        #Input set expression into the '_getPostfix' function, and try splitting the returned string into a seperated list 'postfix_list'
        try:
            postfix_list = self._getPostfix(self.getExpr).split()
        #Return None if an error was encounted when calling '_getPostfix'
        except(AttributeError):
            return(None)

        from operator import mul, truediv, add, sub
        #A dictionary of operators as values and their string counterpart as keys
        operator_dictionary = {'^':pow , '*':mul , '/':truediv , '+':add , '-':sub}

        #This 'for' loop goes through 'postfix_list'
        for string in postfix_list:
            #If the string is a digit, push it into the 'calculateStack' stack
            if self.isNumber(string):
                calculateStack.push(string)

            #If the string is an operator, pop two numbers from the stack, perform the operation, and push the result into the stack
            else:
                num2 = calculateStack.pop()
                num1 = calculateStack.pop()
                result = float(operator_dictionary.get(string)(float(num1),float(num2)))
                calculateStack.push(result)

        #Return the final result
        return(calculateStack.pop())

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
    >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2')
    >>> C.states == {}
    True
    >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 28.0}
    True
    >>> print(C.calculateExpressions())
    {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 28.0}
    >>> C.states == {'x1': 23.0, 'x2': 28.0}
    True
    >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1')
    >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 24.5}
    True
    >>> C.states == {'x1': 24.5, 'x2': 427.0}
    True
    >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D')
    >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 41.0}
    True
    >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
    True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C.isVariable('volume')
            True
            >>> C.isVariable('4volume')
            False
            >>> C.isVariable('volume2')
            True
            >>> C.isVariable('vol%2')
            False
        '''
        #Return True if the variable name is alpha numeric and its first index is a letter
        return (word.isalnum() and word[0].isalpha())
       

    def replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C.replaceVariables('1')
            '1'
            >>> C.replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C.replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''

        #this stores the keys of the 'self.states' dictionary into a list
        variable_list = list(self.states.keys())
        #this stores the values of the 'self.states' dictionary into a list
        value_list = list(self.states.values())
        #This splits each variable of the entered expression 'expr' into 'expression_list'
        expression_list = expr.split()
        #This creates a list which will be joined to return the final string
        final_list = []
        #This will be used for the 'join' method
        expression_string = ' '

        #This 'for' loop goes through 'expression_list'
        for string in expression_list:
            try:
                #If 'string' is in 'variable_list', using its index find the counterpart in 'value_list' and append it into 'final_list'
                find_variable = variable_list.index(string)
                find_value = str(value_list[find_variable])
                final_list.append(find_value)
            except(ValueError):
                #If 'string' is not found in 'variable_list', append it into 'final_list' and continue the loop
                final_list.append(string)
                continue
        #Join 'final_list' into a string and return it
        return expression_string.join(final_list)
    
    def calculateExpressions(self):
        self.states = {}
        calc = Calculator()
        #This splits 'self.expressions' seperated by semicolons and stores it into a list
        expression_split = self.expressions.split(';')
        #This dictionary will be the return value
        final_dictionary = {}

        #This 'for' loop goes through the expressions in 'expression_split'
        for expression in expression_split:
            #if'expression' is the final expression in 'expression_split', store the requested value with '_return_' as its key into 'final_dictionary'  
            if expression == expression_split[-1]:
                final_dictionary['_return_'] = float(self.replaceVariables(expression.split()[-1]))

            else:
                #'variable_split' further splits the expression seperated by '='   ['a = 2'] will become ['a ', ' 2']
                variable_split = expression.split('=')
                #This list further splits the expression in 'variable_split' and removes all ' ' spaces   ['a ',' 2'] will become ['a', '2']
                variable_replace = []
                variable_replace.append(variable_split[0].replace(' ', '', 1))
                variable_replace.append(variable_split[1].replace(' ', '', 1))

                #if the second index is a digit, assign the first index as its key and store them into 'self.states', and copy 'self.states' into 'final_dicitonary' with 'expression' as its key
                if variable_replace[1].isdigit():
                    self.states[variable_replace[0]] = float(variable_replace[1])
                    final_dictionary[expression] = self.states.copy()

                #If the second index of 'variable_replace' is an expression
                #call the function 'replaceVariables' with the second index of 'variable_replace' as the input and store it in 'infix_expression'
                else:
                    infix_expression = self.replaceVariables(variable_replace[1])
                    #call 'setExpr' with 'infix_expression' as its input
                    calc.setExpr(infix_expression)
                    #Set a variable as a key with the return of the calculated expression as its value in 'self.states'   self.states[a] = 5.0
                    self.states[variable_replace[0]] = calc.calculate
                    #The expression 'expression' is set as a key with a copy of the 'self.states' dictionary as its value
                    final_dictionary[expression] = self.states.copy()

        #Returns 'final_dictionary'
        return final_dictionary
