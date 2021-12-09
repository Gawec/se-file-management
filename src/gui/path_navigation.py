class Navigator:

    def __init__(self):
        self.stack = []
        self.length = 0
        self.current = -1

    # helper functions
    def is_at_top(self):
        return self.current == self.length - 1

    def is_at_true_top(self):
        return self.current == len(self.stack) - 1 ###############
    
    def is_at_bottom(self):
        return self.current == 0

    def is_empty(self):
        return self.current == -1
    
    # getter functions
    def get_length(self):
        return self.length

    def get_current(self):
        return self.current

    def get_current_path(self):
        if self.is_empty():
            print('Error: Stack is empty.')
            return False

        return self.stack[self.current]



    # MAIN FUNCTION
    def  new_direction(self, path):
        '''MAIN FUNCTION OF CLASS   ||   adds <path> after <current> index and forgets everything after it'''
        if self.is_at_true_top() or self.is_empty():
            self.stack.append(path)
        else:
            self.stack[self.current + 1] = path

        self.current += 1
        self.length = self.current + 1

    # positioning functions
    def set_current(self, index):
        '''Change position of <current>'''

        if index < 0 or index >= self.length:
            print('Error: index out of bounds')
            return False
        
        self.current = index
        return self.stack[self.current]

    def backward(self):
        '''  moves <current> back by 1 and then returns current element'''

        if self.is_at_bottom():
            print('Error: current index is at bottom of stack')
            return self.stack[0]
        
        self.current -= 1
        return self.stack[self.current]

    def forward(self):
        '''moves <current> forward by 1 and then returns current element '''
        
        if self.is_at_top():
            print('Error: current index is at top of stack')
            return self.stack[self.length - 1]

        self.current += 1
    
        return self.stack[self.current]

    # other insertion functions
    def append_path(self, path):
        '''adds <path> to top of navigation stack   ||   changes position of <current> to top of stack    ||   added function just in case'''

        self.stack.append(path)
        self.length += 1
        self.current = self.length - 1

    def insert_path(self, path, index):
        '''adds <path> to nav stack at index without changing <current> or rest of stack    |   added function just in case'''

        if index < 0 or index > self.length:
            print('Error: index out of bounds')
            return False
        
        if index == self.length:
            self.stack.append(path)
            self.length += 1
            return True

        self.stack[index] = path
        return True

    # print function
    def print(self):
        '''prints out height of stack, the current index and the stack itself'''

        print('\n-------------------\n')
        print(f'Height of stack: {self.length}')
        print(f'Index of current element: {self.current}')
        print(f'Stack: \n')
        print(self.stack[:self.length])
        print('\n-------------------\n')



