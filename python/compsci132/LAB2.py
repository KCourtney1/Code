# LAB2
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

import math

# -------- SECTION 1
class Instructor:
    '''
        >>> t1= Instructor('John Doe')
        >>> t1.get_name()
        'John Doe'
        >>> t1.get_courses()
        []
        >>> t1.add_course('MATH140')
        >>> t1.get_courses()
        ['MATH140']
        >>> t1.add_course('STAT100')
        >>> t1.get_courses()
        ['MATH140', 'STAT100']
        >>> t1.add_course('STAT100')
        >>> t1.get_courses()
        ['MATH140', 'STAT100']
        >>> t1.remove_course('MATH141')
        >>> t1.get_courses()
        ['MATH140', 'STAT100']
        >>> t1.remove_course('MATH140')
        >>> t1.get_courses()
        ['STAT100']
    '''

    def __init__(self, name):
        #--- YOUR CODE STARTS HERE
        self.name = name
        self.courses = []

    def get_name(self):
        #--- YOUR CODE STARTS HERE
        return self.name

    def set_name(self, new_name):
        #--- YOUR CODE STARTS HERE
        self.name = new_name

    def get_courses(self):
        #--- YOUR CODE STARTS HERE
        return self.courses

    def remove_course(self, course):
        #--- YOUR CODE STARTS HERE
        if course in self.courses:
            self.courses.remove(course)

    def add_course(self,course):
        #--- YOUR CODE STARTS HERE
        if not course in self.courses:
            self.courses.append(course)


# -------- SECTION 2      
class Pantry:
    """"
        >>> sara_pantry = Pantry()                
        >>> sara_pantry.stock_pantry('Bread', 2)
        'Pantry Stock for Bread: 2.0'
        >>> sara_pantry.stock_pantry('Cookies', 6) 
        'Pantry Stock for Cookies: 6.0'
        >>> sara_pantry.stock_pantry('Chocolate', 4) 
        'Pantry Stock for Chocolate: 4.0'
        >>> sara_pantry.stock_pantry('Pasta', 3)     
        'Pantry Stock for Pasta: 3.0'
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 6.0, 'Chocolate': 4.0, 'Pasta': 3.0}
        >>> sara_pantry.get_item('Pasta', 2)     
        'You have 1.0 of Pasta left'
        >>> sara_pantry.get_item('Pasta', 6) 
        'Add Pasta to your shopping list!'
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 6.0, 'Chocolate': 4.0, 'Pasta': 0.0}
        >>> ben_pantry = Pantry()                    
        >>> ben_pantry.stock_pantry('Cereal', 2)
        'Pantry Stock for Cereal: 2.0'
        >>> ben_pantry.stock_pantry('Noodles', 5) 
        'Pantry Stock for Noodles: 5.0'
        >>> ben_pantry.stock_pantry('Cookies', 9) 
        'Pantry Stock for Cookies: 9.0'
        >>> ben_pantry.stock_pantry('Cookies', 8) 
        'Pantry Stock for Cookies: 17.0'
        >>> ben_pantry.get_item('Pasta', 2)       
        "You don't have Pasta"
        >>> ben_pantry.get_item('Cookies', 2.5) 
        'You have 14.5 of Cookies left'
        >>> sara_pantry.transfer(ben_pantry, 'Cookies')
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 20.5, 'Chocolate': 4.0, 'Pasta': 0.0}
        >>> ben_pantry.transfer(sara_pantry, 'Rice')
        >>> ben_pantry.transfer(sara_pantry, 'Pasta')
        >>> ben_pantry
        I am a Pantry object, my current stock is {'Cereal': 2.0, 'Noodles': 5.0, 'Cookies': 0.0}
        >>> ben_pantry.transfer(sara_pantry, 'Pasta')
        >>> ben_pantry
        I am a Pantry object, my current stock is {'Cereal': 2.0, 'Noodles': 5.0, 'Cookies': 0.0}
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 20.5, 'Chocolate': 4.0, 'Pasta': 0.0}
    """

    def __init__(self):
        self.items = {}
    
    def __repr__(self):
        #--- YOUR CODE STARTS HERE
        return f"I am a Pantry object, my current stock is {self.items}"

    def stock_pantry(self, item, qty):
        #--- YOUR CODE STARTS HERE
        if item in self.items:
            self.items[item] += float(qty)
            return f"Pantry Stock for {item}: {self.items[item]}"
        else:
            self.items[item] = float(qty)
            return f"Pantry Stock for {item}: {self.items[item]}"


    def get_item(self, item, qty):
        #--- YOUR CODE STARTS HERE
        if item in self.items:
            if qty < self.items[item]:
                self.items[item] -= qty
                return f"You have {self.items[item]} of {item} left"
            else:
                self.items[item] -= self.items[item] 
                return f"Add {item} to your shopping list!"
        return f"You don't have {item}" 
            
    def transfer(self, other_pantry, item):
        #--- YOUR CODE STARTS HERE
        if item in other_pantry.items and other_pantry.items[item]>0:
            if item in self.items :
                self.items[item] += other_pantry.items[item]
                other_pantry.items[item] -= other_pantry.items[item]
            else:
                self.items[item] = other_pantry.items[item]
                other_pantry.items[item] -= other_pantry.items[item]


# -------- SECTION 3
class Player:
    """
        >>> p1 = Player('Susy')
        >>> print(p1)
        No game records for Susy
        >>> p1.update_loss()
        >>> p1
        *Game records for Susy*
        Total games: 1
        Games won: 0
        Games lost: 1
        Best game: None
        >>> p1.update_win(5)
        >>> p1.update_win(2)
        >>> p1
        *Game records for Susy*
        Total games: 3
        Games won: 2
        Games lost: 1
        Best game: 2 attempts
    """
    def __init__(self, name):
        #--- YOUR CODE STARTS HERE
        self.player_name = name
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.best_game = 6
         

    def update_win(self, att):
        #--- YOUR CODE STARTS HERE
        if att<self.best_game:
            self.best_game = att
        self.games_played += 1
        self.games_won += 1
    
    def update_loss(self):
        #--- YOUR CODE STARTS HERE
        self.games_played += 1
        self.games_lost += 1
    

    def __str__(self):
        #--- YOUR CODE STARTS HERE

        if self.games_played == 0:
            return f"No game records for {self.player_name}"
        elif self.games_won == 0:
            return f"""*Game records for {self.player_name}*
Total games: {self.games_played}
Games won: {self.games_won}
Games lost: {self.games_lost}
Best game: {None}"""
        return f"""*Game records for {self.player_name}*
Total games: {self.games_played}
Games won: {self.games_won}
Games lost: {self.games_lost}
Best game: {self.best_game} attempts"""
        
    __repr__=__str__

class Wordle:
    """
        >>> p1 = Player('Susy')
        >>> p2 = Player('Taylor')
        >>> w1 = Wordle(p1, 'water')
        >>> w2 = Wordle(p2, 'cloud')
        >>> w3 = Wordle(p1, 'jewel')
        >>> w1.play('camel')
        '_A_E_'
        >>> w1.play('ranes')
        'rA_E_'
        >>> w1.play('baner')
        '_A_ER'
        >>> w1.play('pacer')
        '_A_ER'
        >>> w1.play('water')
        'You won the game'
        >>> w1.play('rocks')
        'Game over'
        >>> w1.play('other')
        'Game over'
        >>> w3.play('beast')
        '_E___'
        >>> w3.play('peace')
        '_E__e'
        >>> w3.play('keeks')
        '_Ee__'
        >>> w3.play('jewel')
        'You won the game'
        >>> w2.play('classes')
        'Guess must be 5 letters long'
        >>> w2.play('cs132')
        'Guess must be all letters'
        >>> w2.play('audio')
        '_ud_o'
        >>> w2.play('kudos')
        '_udo_'
        >>> w2.play('would')
        '_oulD'
        >>> w2.play('bound')
        'The word was cloud'
        >>> w2.play('cloud')
        'Game over'
        >>> p1
        *Game records for Susy*
        Total games: 2
        Games won: 2
        Games lost: 0
        Best game: 4 attempts
        >>> p2
        *Game records for Taylor*
        Total games: 1
        Games won: 0
        Games lost: 1
        Best game: None
    """

    def __init__(self, player, word):
        #--- YOUR CODE STARTS HERE
        self.player = player
        self.word = word
        self.attempts = 1
        self.game_over = False
    

    def process_guess(self, guess):
        #--- YOUR CODE STARTS HERE
        processed_guess = ""
        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                processed_guess += guess[i].upper()
            elif guess[i] in self.word:
                processed_guess += guess[i].lower()
            else:
                processed_guess += "_"
        return processed_guess
            

    def play(self, guess):
        #--- YOUR CODE STARTS HERE
        if self.game_over:
            return "Game over"
        elif guess == self.word:
            self.game_over = True
            self.player.update_win(self.attempts)
            return "You won the game"
        elif self.attempts == 6:
            self.game_over = True
            self.player.update_loss()
            return  f"The word was {self.word}"
        else:
            if len(guess) != 5:
                self.attempts += 1
                return "Guess must be 5 letters long"
            if not guess.isalpha():
                self.attempts += 1
                return "Guess must be all letters"
        self.attempts += 1
        return self.process_guess(guess)
            
       



# -------- SECTION 4
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line: 
    ''' 
        >>> p1 = Point2D(-7, -9)
        >>> p2 = Point2D(1, 5.6)
        >>> line1 = Line(p1, p2)
        >>> line1.getDistance
        16.648
        >>> line1.getSlope
        1.825
        >>> line1
        y = 1.825x + 3.775
        >>> line2 = line1*4
        >>> line2.getDistance
        66.592
        >>> line2.getSlope
        1.825
        >>> line2
        y = 1.825x + 15.1
        >>> line1
        y = 1.825x + 3.775
        >>> line3 = line1*4
        >>> line3
        y = 1.825x + 15.1
        >>> line5=Line(Point2D(6,48),Point2D(9,21))
        >>> line5
        y = -9.0x + 102.0
        >>> Point2D(45,3) in line5
        False
        >>> Point2D(34,-204) in line5
        True
        >>> line6=Line(Point2D(2,6), Point2D(2,3))
        >>> line6.getDistance
        3.0
        >>> line6.getSlope
        inf
        >>> isinstance(line6.getSlope, float)
        True
        >>> line6
        Undefined
        >>> line7=Line(Point2D(6,5), Point2D(9,5))
        >>> line7.getSlope
        0.0
        >>> line7
        y = 5.0
        >>> Point2D(9,5) in line7
        True
        >>> Point2D(89,5) in line7
        True
        >>> Point2D(12,8) in line7
        False
        >>> (9,5) in line7
        False
    '''
    def __init__(self, point1, point2):
        #--- YOUR CODE STARTS HERE
        self.point1 = point1
        self.point2 = point2

    #--- YOUR CODE STARTS HERE
    @property
    def getDistance(self):
        return round(math.sqrt(((self.point2.x-self.point1.x)**2)+((self.point2.y-self.point1.y)**2)),3)
       
    @property
    #--- YOUR CODE STARTS HERE
    def getSlope(self):
        if self.point1.x-self.point2.x == 0:
            return float("inf")
        elif self.point1.y-self.point2.y == 0:
            return 0.0
        return round((self.point2.y-self.point1.y)/(self.point2.x-self.point1.x),3)
    
    @property
    #--- YOUR CODE STARTS HERE
    def getintercept(self):
        if not type(self.getSlope) == str:
            return round(self.point1.y - (self.getSlope*self.point1.x),3)


    #--- YOUR CODE CONTINUES HERE
    def __repr__(self):
        if self.getSlope != float("inf"):
            if self.getSlope != 0.0:
                return f"y = {self.getSlope}x + {self.getintercept}"
            return f"y = {self.getintercept}"
        else:
            return "Undefined"
    
    def __mul__(self, other):
        return Line(Point2D(self.point1.x * other, self.point1.y * other),Point2D(self.point2.x * other, self.point2.y * other))
    
    def __contains__(self,point):
        if isinstance(point,Point2D):
            if self.getSlope != 0.0:
                if math.isclose(point.y, (point.x*self.getSlope + self.getintercept)):
                    return True
                return False
            if point.y == self.getintercept:
                return True
            return False
        return False



def run_tests():
    import doctest

    # Run tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run tests per function - Uncomment the next line to run doctest by function. Replace Pantry with the name of the class you want to test
    doctest.run_docstring_examples(Wordle, globals(), name='LAB2',verbose=True)

if __name__ == "__main__":
    run_tests()