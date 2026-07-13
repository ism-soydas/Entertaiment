# Hangman game final version
# The goal in this game is to find the correct answer by guessing letters or the word directly before the hangman is fully drawn
# Under development
# Note: In this project, the variable "hak" was intentionally kept in Turkish as a developer signature.
# It corresponds to "attempts" or "lives" in English.

# Libraries
import random as rd
import time as t
import pandas as pd
import sys

# Class Architecture
class Hanging_Man(object):
    def __init__(self):
        """   
              This area contains the variable for the appropriate data table for the user.
              It will have the original word for the user to make guesses on, and
              a dictionary structure of letters for the user to test whether their inputs are letters or not.
                                                                                                        """
        self.df = None
        # Here, a data table related to different topics for the user to guess words will be loaded
        self.orj_word = None
        # Here, a random word will be generated in later stages according to the category desired by the user
        self.miss_word = None
        # This will be the game area where the user plays
        self.letters = {'A','B','C','Ç','D','E','F','G','Ğ','H','I','İ','J','K',
                        'L','M','N','O','Ö','P','R','S','Ş','T','U','Ü','V','Y','Z'}
        # self.letters will be used in the letter validation process as mentioned in self.words
        self.deletiDictC = set()
        # self.deletiDictC is a section where the correct letters used by the user are temporarily stored
        # It will be used later in PrbingLet and CreateRandSent functions
        self.all_deli_Dict = set()
        # Shows all the letters the user has used in the game
        # It will be used later in the PrbingLet function
        
    def drawing_man(self, hak):
        """   Here, the hangman drawing process will be executed based on the user's mistakes   """

        if hak == 1:
            return """
                  |
                  |
                  |
                  |"""
        elif hak == 2:
            return """
                   ___
                  |
                  |
                  |
                  |"""
        elif hak == 3:
            return """
                   ___
                  |  o
                  |
                  |
                  |"""
        elif hak == 4:
            return """
                   ___
                  |  o
                  | /\\
                  |
                  |"""
        elif hak == 5:
            return """
                   ___
                  |  o
                  | /\\
                  | /\\ 
                  |"""
    def copy_of_letters_table(self):
        """
              Creating an alternative letter table 
                                                                               """
        return self.letters.copy()
        # Here we create a letter table for the user to use
        # The main goal is to perform operations without losing our reference self.letters dictionary structure
        
    def begin_of_game(self):
        
        """      
               Here, the process of resetting the old area for game repetition 
               or initializing the start if the user is just starting the game 
               will be done. self.miss_word will serve this function.
                                                                               """
        self.miss_word = ""
        # It will create our temporary table
        
    def message_end_of_game(self, _mess):
        return "Congratulations, you won the game :)" if _mess < 5 else "You lost the game :("
        # Here, an end-of-game message will be given to the user based on their remaining attempts
        
    def create_space_of_game_for_random_word(self, l, ct):
        
        """   
              Here, there will be a specific word area for the user to understand their progress
              based on each letter or word guess. 
              Depending on the progress, the selected letters will be displayed in a section 
              (briefly in a different function) to show the user which letters have been used or not. 
                                                                               """
        result_mes, cont = None, None
        # result_mes shows the result based on the move in the game
        # cont gives the error message for the main function which is user_space 
        # As a result of this, if this letter is in the word or used before, the value of the attempt variable increases
        # If the new letter entered by the user is used for the first time and is in the word, the result will return True
        
        prev_size_dDC= len(list(self.deletiDictC))
        # It will be used later to compare the new dictionary structure with the old structure dimensionally    
        for lets in self.orj_word:
            cont_spc = True
            # cont_spc will check if there is a space between the words here
            
            if lets == " ":
                self.miss_word += '|'
                cont_spc = False
            # We detect the space in the word with lets == " " and throw it into the condition
            # And we add the | sign to self.miss_word to express that space
            # cont_spc will be the condition preventing the _ sign from being placed because a space is found here
            
            if lets in self.deletiDictC:
                self.miss_word += lets
            # Here it is checked if the letter exists in the word if the letter has been used before
            # After the checking stage, it is printed if it existed before
            
            elif l == lets and l not in self.deletiDictC:
                self.miss_word += self.is_new_correct_letter(lets)
                result_mes, cont = self.messages_which_is_per_step_of_game('Correct'), True
            # Here, it is first checked whether the letter in the word and the letter entered by the user are the same
            # If the letters are the same and this letter has not been used before, it is directed to the self.is_new_correct_letter() function
            # To briefly summarize this function, it marks the used letter as used and prints that letter to the game screen
            # self.messages_which_is_per_step_of_game() function sends a message according to the in-game developments and cont = True because it is the correct letter            
            
            elif l != lets and cont_spc:
                self.miss_word += '_'
            # If the letter has not been used before and does not match the word, it will print _
            # If there is a space in the random word, cont_spc will write this | sign to indicate it 
            
            self.miss_word += ' '
            # Aims to make the _ sign more prominent to provide a better user experience
            
        # Here we use self.orj_word and the initially generated random word (in the for loop)
        # We take each letter in the for loop and add it to self.miss_word depending on the if-else command
        # This adding process will refresh the game area depending on whether the user guesses the letter correctly or not
        
        if ct and prev_size_dDC == len(list(self.deletiDictC)):
            result_mes, cont = (self.messages_which_is_per_step_of_game('Wrong'), False if l not in self.deletiDictC 
                  else self.messages_which_is_per_step_of_game('There is in before'), False)
            # Here, it performs a size comparison as we mentioned at the beginning of the for loop
            # Additionally, we used a control variable named ct so that it doesn't confuse the beginning and middle of the game
            # self.messages_which_is_per_step_of_game() function sends a message according to in-game developments under if-else control

        print(self.miss_word.rstrip())
        # Here we will print the resulting table
        # The reason we use .rstrip() is to clear the space that will occur on the far right of the table
        
        return result_mes, cont if ct else None, None
        # Here we will send the variables back to check them in user_space
        # The reason for the else is, as we mentioned, depending on the possibility of ct being False
        
    def messages_which_is_per_step_of_game(self, gim):
        if gim == 'Wrong':
            return "The letter you entered is not in the mentioned word."
        elif gim == 'Correct':
            return "The letter you entered is correct, congratulations."
        elif gim == 'There is in before':
            return "The letter you entered has already been used."
        
        # Here are messages indicating that the words are correct, incorrect, and whether they have been used before. 
        
    def is_new_correct_letter(self, lets):
        """   
              Here we show the last correct letter said by the user.
                                                                               """
        self.deletiDictC.add(lets)
        # Here, if the letter is correct, we throw the letter into the set of correctly found letters.
        return f"{lets}"
        # Here, in the create_space_of_game_for_random_word function, since the new letter entered by the user is correct, it will return the letter to be printed.  
        
    def using_section(self):
        """
              In this area, a standard menu operation will be performed for the user to 
              guess a letter or guess a word.
                                                                               """
        cont, opt = True, None
        # Here, the cont variable will provide an exit process if the user performs the correct operation inside the while loop.
        # The opt variable will check if the value entered by the user is equal to option 1 or 2.
        while cont:
            
            try:
                opt = str(input("""Press 1 if you want to guess a word
                                Press 2 if you want to guess a letter: """))
                opt = opt.lstrip(' ')
                # Here we ask the user for the appropriate option.
                # With .lstrip(), we delete the spaces left by the user from the left so they don't cause problems.
                                
                if not (opt == '1' or opt == '2'):
                    raise ValueError("Your input does not match the options.")
                # If the options do not match, we will give an error message and exit the try-except structure and repeat the process.
                cont = False
                # Exit command from the while loop.
                
            except ValueError as e:
                print(f"Error Message: {e}")
            # We check for the possibility of the user making a wrong move with the try-except structure. 
            
        return opt
        # If the value entered by the user is equal, it will return to user_space (main function).
        
    def guessing_word(self):
        """
              This area will be used for the user to make a word guess.
                                                                               """
        def is_there_letters(w):
         
            for i in w:
                if i not in self.letters:
                    return False
                # If element i is not a letter, it will return False.
            return True
            # If all i elements are letters, accept it as a word and give approval to the user.
            
        # The is_there_letters function will check whether the input entered by the user has the characteristics of a word.
        
        cont, word = True, None
        # Here cont will control the exit from the while loop.
        # word will hold the word entered by the user (the guessed value).
        
        while cont:
            word = str(input("Please enter your guessed word: ")).upper().strip()
            # It will take the guessed word from the user.
            # For accurate and noise-free data, both the spaces on the sides will be cleared and since all letters of the data are uppercase, it will be converted.
            try:
                if (is_there_letters(word) if len(word) != 0 else True):
                    raise ValueError("Your guess is not a valid word.")
                # There will be a 2-layer verification here.
                # First layer: something entered must definitely be written, otherwise it will return to the error message.
                # In the second layer, it will be checked whether every term in the word is a letter.
                # Even if one of these layers returns True, it will be removed from the try-except structure and a new word will be requested from the user.
                cont = False
                # When cont becomes False, the while loop will be exited.
            except ValueError as e:
                print(f"Error Message: {e}")
            # We check for the possibility of the user making a wrong move with the try-except structure.      
        
        if word == self.orj_word:
            self.create_if_guessing_word_is_right()
            # This function will perform a drawing process to show that the word is correct.
        
            return "The word you entered is correct.", True
        else:
            return "The word you entered is incorrect.", False
        # Here, if the word matches the original word, it will say that the word is correct, otherwise it will show the opposite.
        # It will additionally return a True value to satisfy the condition of ending the game in the user_space area.
        # It will additionally return a False value to satisfy the condition of continuing the game in the user_space area.
        
    def create_if_guessing_word_is_right(self):
        """   
              Here, depending on the condition that the user finds the correct word, 
              the process of printing the word will be executed.
                                                                               """
        for let in self.orj_word:
            
            self.miss_word += (let, ' ')
            # Here we add all the letters we got onto self.miss_word according to self.orj_word.
            # The reason we add a space is that the letters need to be in distinct positions.
            
        # Here we use a for loop to get all the letters of the original word to print.
        
        print(self.miss_word.rstrip())
        # Here we print self.miss_word in a way that deletes the extra space we added from the right.
        
        self.begin_of_game()
        # We reset the self.miss_word so that there is no unnecessary data in the memory. 
        
    def guessing_letter(self):
        """
              This is the area where the user guesses a letter to find the word.
                                                                               """
        def is_there_letter(l):
            if l not in self.table:
                return True
            # Here it mentions that if the letter satisfies the condition of not being in self.table, it will return True.
            # This True triggers the error function in try-except in the guessing_letter function.
            
            self.all_deli_Dict.add(l)
            # Here we want the letter entered by the user to be added to the self.all_deli_Dict function whether it is correct or incorrect.
            
            self.table.remove(l)
            # We remove the element from the main table so that if the user enters the same letter again, the function won't get stuck in the same operations.
            
            print("New table: ", self.table)
            return False
            # Here we present the new table to the user and return False to exit the error function in try-except.
            
        # In this function, it will be checked whether the new letter entered by the user has been used before.
        # Accordingly, if the letter is new, the deletion process from the main table will be performed.
        
        cont = True
        # The cont variable will control the while loop here.
        while cont:
            letter = str(input("Please enter your guessed letter: ")).upper().strip()
            # Here we ask the user for the letter they want to guess.
            # To prevent noise, we convert the letters to uppercase due to the data and change the letters on the sides.
            
            try:
                if (is_there_letter(letter) if len(letter) != 0 else True):
                    raise ValueError("Your input is not a letter.")
                # There will be a 2-layer verification here.
                # First layer: something entered must definitely be written, otherwise it will return to the error message.
                # In the second layer, it will be checked whether every term in the word is a letter.
                # Even if one of these layers returns True, it will be removed from the try-except structure and a new word will be requested from the user.
                cont = False
                # Here we change the value of the cont variable to False to exit the while loop. 
                
            except ValueError as e:
                print("Error message: {}".format(e))
            # We check for the possibility of the user making a wrong move with the try-except structure.      
        
        return self.create_space_of_game_for_random_word(letter, True)
        # Here we send the user to the self.create_space_of_game_for_random_word function so they can see the current state of the game area.
        # The reason we send True is so that the game area doesn't fall into the illusion that the game has been restarted.
        # And we return the 2 variables we got from self.create_space_of_game_for_random_word back to the user_space function.

    def create_random_word(self, idx):
        """
              Here it generates a random element based on the category chosen by the user.
                                                                               """
        category = self.df.columns[idx]
        # Here we enter the column value corresponding to the numerical variable into category.
        
        random_index = rd.randint(0, len(self.df[category]) - 1)
        # Here, since a random element will be selected, a random_index belonging to that element is chosen.
        
        self.orj_word = str(self.df.at[random_index, category]).upper()
        # Here we will create an element from the table based on the index number and column over self.df.
        # We will make the letters uppercase to get away from noise and for a fluent display.
        
    def objects(self):     
        """ 
              In this area, we show the user the topics they can choose from.
                                                                               """                    
        return """ Please enter the number of the topic you want from the options given below 
        1 -> Cities
        2 -> Movies
        3 -> Animals
        4 -> Professions
        5 -> Plants   """
    # Here we return a specific feedback message to the user.

    def choose_type_of_word(self):
        """
              In this area, the user is asked which category they want to select.
                                                                               """
        def read_the_file():
            try:    
                self.df = pd.read_excel(r"Hanging_man_DataBase.xlsx")
                # Here we read the file.
                
            except FileNotFoundError:
                print("Error message: File not found !!! ")
                sys.exit()
                # Here, if the file is not found, we throw an error and exit.
                
            except Exception:
                print("Error message: An error occurred while reading the file !!!")
                sys.exit()
                # Here, if an error occurred while reading the file, we give an error and exit.
                
        # In the read_the_file function, we will check if the file is intact or usable.
        
        print(self.objects())
        # Here we show the options the user can choose.
        
        read_the_file()
        # Here we check if the file is working, if it is, we assign the dataset in the file into self.df.
        
        cont, sort = True, None
        # cont will control the exit from the while loop.
        # sort takes the value entered by the user.
        
        while cont:
            sort = str(input("Please enter one of the mentioned options: ")).strip()
            # Here the user is asked to enter one of the mentioned options.
            # Spaces from the right and left are cleared with .strip().
            
            try:
                if sort not in {'1','2','3','4','5'}:
                    raise ValueError("There is no such option type.")
                # Here it is checked whether the value entered by the user is truly an option.
                # If not, it prints an error message.
                cont = False
                # cont = False allows us to exit the while loop.
                
            except ValueError as e:
                print(f"Error Message: {e}")
            # We check for the possibility of the user making a wrong move with the try-except structure.
        
        return int(sort) - 1
        # From here, we return the index of the category to the function that chooses a random word.
        
    def user_space(self):
        """
              This area will be our Main function. Here we create the Game table, 
              we generate the self.miss_word value for drawing before using the game area, 
              and we build the control system that will depend on certain iterations. 
              We direct the user to an area to choose the type of the random word, 
              and finally, if the user wants to quit the game, we terminate the system 
              with the Exit function.        
                                                                               """
        def _exit():
            sys.exit()
            # Since this exit will be directly from the system, we will use the sys library.
            
        # We will use this function to exit the system.
        
        print("""Welcome to the game
        Please wait ... """)
        t.sleep(3)
        # Here we welcome the user and make them wait for 3 seconds.
        
        hak, pck = 0, None
        # Here will be the number of attempts based on the wrong move made by the user.
        # And there will be a pck variable to be used in the area where the user requests a letter guess or word guess.
        
        idx = self.choose_type_of_word()
        # From here we ask the user which category they want to choose.
        
        self.create_random_word(idx)
        # As a result, we choose a random word depending on the category.
        
        self.begin_of_game()
        # Here we create or reset the self.miss_word variable for the game area.
        
        text, tri = self.create_space_of_game_for_random_word(None, False)
        # Here we direct the user to the area where the generated word will be shown before starting the game.
        # The reason we assign to text, tri is that we perform a return operation in the self.create_space_of_game_for_random_word function.
        
        self.table = self.copy_of_letters_table()
        # Here we will create a copy table that we can use to avoid resetting the main table.
        
        while hak != 5:
            pck = self.using_section()
            # Here we will direct the user to a menu area for Word guessing or Letter guessing and get the user's choice.
            
            control = lambda pck: self.guessing_word() if pck == '1' else self.guessing_letter()
            text, tri = control(pck)
            # Here, with lambda, we will assign to functions based on the user's choice. 
            # And we will create a function called control to get the outputs.
            # From these outputs, text will send a return message depending on the user's move.
            # tri will serve 2 operations:
            # Operation 1 of tri: if the word guess is correct (for pck == '1'), it will mention that the game is over and exit the loop.
            # Operation 2 of tri: depending on the result the user gets from both self.guessing_word() and self.guessing_letter() functions 
            # Operation 2 of tri (continued): it will increase the attempt value and draw the hangman.
            # The break command executed in tris will provide the exit operation depending on the condition.
                
            print(text)
            # Here it will print the returned message depending on the user's move.
            
            if pck == '1' and tri:
                print(self.message_end_of_game(hak))
                break
            # The part for tri operation - 1. 
            
            if not tri:
                hak += 1
                print(self.drawing_man(hak))
            # The part for tri operation - 2.
            
            if '_' not in self.miss_word:
                print(self.message_end_of_game(hak))
                break
            # Here, after creating self.miss_word, we will check if there is an _ inside the section we will use in the game area.
            
            self.begin_of_game()
            # From here we will reset the table. 
            
            print(f'''Remaining letters: {",".join(self.table)}
                  Used Letters: {",".join(self.all_deli_Dict)}
                  Remaining Attempts: {5 - hak}''')
            # What we do here is show the user the remaining letters, used letters, and remaining attempts.       
            
        if hak == 5:
            print(self.message_end_of_game(hak))
        # Here if attempt == 5, it will be directed to the self.message_end_of_game() option and the "you lost the game" message will be given.
        
        self.user_space() if self.process_end_of_game() else _exit()
        # Here, with the self.process_end_of_game function, the game will restart or exit depending on the user's choice.

    def process_end_of_game(self):
        """
              In this area, we tell the user that the game is over 
              and offer them options to restart or exit the game.
                                                                               """
        l_ct = True
        # The l_ct variable will control our while loop. 
        
        while l_ct:
             
            select_ls = str(input("""Game over! 
                                  Press 1 if you want to play again
                                  Press 2 if you do not want to and want to quit: """)).strip()
            # Here we offer the user options to restart or exit the game.
            # Additionally, with the .strip() command, we prevent noise that might occur due to spaces.
            
            try:
                if select_ls not in ['1', '2']:
                    raise ValueError("The option you entered is not valid in the game, please try again.")
                # Here we check if there is an option called select_ls.
                l_ct = False
                # We exit the while loop by setting l_ct = False.
                
            except ValueError as e:
                print(f"Error message: {e}")
            # We check for the possibility of the user making a wrong move with the try-except structure.      
        return True if select_ls == '1' else False
        # Here we return the value that triggers Exit and play again depending on the option entered by the user.
    pass
 
if __name__ == "__main__":
    hgm = Hanging_Man()
    hgm.user_space()
# Here we create a main option to start the game. 
# We start the game by calling the user_space() function with the object we created.
