# FRESH START FOR JAYKO
import sys

class LET_TOKEN:
    def __init__(self):
        self.type = "LET_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class IDENTIFIER_TOKEN:
    def __init__(self):
        self.type = "IDENTIFIER_TOKEN"
        self.value = None
    def __repr__(self):
        return f"TokenType = {self.type}, value = {self.value}"

class ASSIGNMENT_TOKEN:
    def __init__(self):
        self.type = "ASSIGNMENT_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class INT_LITERAL_TOKEN:
    def __init__(self):
        self.type = "INT_LITERAL_TOKEN"
        self.value = None
    def nud(self):
        return self.value
    def __repr__(self):
        return f"TokenType = {self.type} value = {self.value}"

class SAY_TOKEN:
    def __init__(self):
        self.type = "SAY_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"
        
class SEMICOLON_TOKEN:
    def __init__(self):
        self.lbp = 0
        self.type = "SEMICOLON_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class ADD_TOKEN:
    def __init__(self):
        self.type = "ADD_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class MUL_TOKEN:
    def __init__(self):
        self.type = "MUL_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class Jayko:
    def __init__(self):
        self.raw_characters = ""            # holds the text of the source code
        self.raw_char_cursor = 0            # the index of the cursor for the raw characters

        self.candidate_tokens = []          # breaks up the text into the individual parts of speech
        self.token_cursor = 0

    def read_source(self,input_file):
        # read_source(): takes the source code and puts every character into
        # self.raw_characters 

        source = open(input_file)
        for line in source.readlines():
            self.raw_characters+=line.strip("\n")
        print("raw, characters")
        print(self.raw_characters)

    def tokenize(self):
        # the tokenize() function takes the list of raw characters and processes them into 
        # a list of token objects
        print("BEGIN TOKENIZING")
        candidate_token_str = ""

        while self.raw_char_cursor < (len(self.raw_characters)-1):
            current_char = self.raw_characters[ self.raw_char_cursor ] 
            next_char = self.peek_chars()

            if current_char.isalnum():              # in this case, it could be an identifier, or a keyword
                candidate_token_str += current_char
                while next_char.isalnum():
                    self.advance_chars()
                    current_char = self.raw_characters[ self.raw_char_cursor ] 
                    next_char = self.peek_chars()
                    candidate_token_str += current_char
                    #print(f"current_char, next_char, self.raw_char_cursor, self.raw_characters")
                    #print(f"{current_char}, {next_char}, {self.raw_char_cursor}, {self.raw_characters}")
                    #print(f"cts: {candidate_token_str}")

                # after this loop is done, the token is finished, so we need to reset the candidate token buffer
                # TODO: determine if the token is a number, string or identifier
                # self.candidate_tokens.append(candidate_token_str)

                token_to_add = self.token_dispatch(candidate_token_str)
                self.candidate_tokens.append(token_to_add)

                candidate_token_str = ""
            elif ( current_char in ("*", "+") ): 
                candidate_token_str +=current_char
                token_to_add = self.token_dispatch(candidate_token_str)
                self.candidate_tokens.append(token_to_add)
                self.advance_chars()

                candidate_token_str = ""

                if ( next_char in ("*", "+") ): 
                    raise SyntaxError("We do not support double operators yet")

            elif current_char == ":":               # needs to handle :=
                candidate_token_str +=current_char
                if next_char == "=":
                    self.advance_chars()
                    current_char = self.raw_characters[ self.raw_char_cursor ] 
                    next_char = self.peek_chars()
                    candidate_token_str += current_char
                    #print(f"in the : part {candidate_token_str}")
                    
                else:
                    raise SyntaxError("We only support := right now")

                token_to_add = self.token_dispatch(candidate_token_str)
                self.candidate_tokens.append(token_to_add)

                candidate_token_str = ""

            if next_char == ";":
                # we have to add the semi colon token, to make it easier to parse statements
                candidate_token_str = next_char
                token_to_add = self.token_dispatch(candidate_token_str)
                self.candidate_tokens.append(token_to_add)
                candidate_token_str = ""

            self.advance_chars()
        print("END TOKENIZING!\n\n")

    def token_dispatch(self, candidate_token_str):
        # this function should look at the candidate_token_str and form the token object
        if candidate_token_str == "let":
            token_to_add = LET_TOKEN()
        elif candidate_token_str == ";":
            token_to_add = SEMICOLON_TOKEN()
        elif candidate_token_str == "*":
            token_to_add = MUL_TOKEN()
        elif candidate_token_str == "+":
            token_to_add = ADD_TOKEN()
        elif candidate_token_str == ":=":
            token_to_add = ASSIGNMENT_TOKEN()
        elif candidate_token_str == "say":
            token_to_add = SAY_TOKEN()
        elif candidate_token_str.isnumeric():
            token_to_add = INT_LITERAL_TOKEN()
            token_to_add.value = int(candidate_token_str)
        elif candidate_token_str.isalnum():
            token_to_add = IDENTIFIER_TOKEN()
            token_to_add.value = str(candidate_token_str)
        else:
            print(f"candidate token str {candidate_token_str} not found")
            print("Exiting...")
            quit()


        return token_to_add

    def parse(self):
        # Parsing should take the list of self.candidate_tokens
        # and output the AST
        current_token = self.candidate_tokens[ self.token_cursor ]
        if current_token.type == "LET_TOKEN":
            self.parse_let()


    def parse_let(self):
        # a LET statement is 
        # "let" identifier ":=" <expr> ";"
        print(self.candidate_tokens[ self.token_cursor ] ) 
        self.expect("LET_TOKEN") 
        self.expect("IDENTIFIER_TOKEN")
        self.expect("ASSIGNMENT_TOKEN")

        print("before entering self.expr")
        print(f"*****token is {self.candidate_tokens[ self.token_cursor ]}")
        value = self.expr()
        print("DEEP FUCKIGNM VALUE ", value)
        self.expect("SEMICOLON_TOKEN")
          

    def expr(self, rbp = 0):
        # function for pratt parsing
        current_token = self.candidate_tokens[ self.token_cursor ] 
        next_token = self.next_token()
        left = current_token.nud()
        while rbp < next_token.lbp:
            current_token = next_token
            token = self.next_token()
            left = current_token.led(left)
        return left






    #####################################################
    # HELPER METHODS FOR LEXING AND PARSING
    #####################################################
    def peek_chars(self):
        return self.raw_characters[self.raw_char_cursor+1]

    def advance_chars(self):
        value = self.raw_characters[ self.raw_char_cursor ]
        self.raw_char_cursor +=1
        return value

    def peek_tokens(self):
        return self.candidate_tokens[self.token_cursor+1]

    def advance_tokens(self):
        value = self.candidate_tokens[ self.token_cursor]
        self.token_cursor +=1
        return value

    def next_token(self):
        self.token_cursor +=1
        value = self.candidate_tokens[ self.token_cursor ]
        return value

    def expect(self, token_type):
        t = self.advance_tokens()
        if t.type != token_type:
            raise SyntaxError(f"Expected {token_type} got {t.type}")
        

if __name__ == "__main__":
    
    # the way to load the file in is PRESCRIBED for now so as long as we do it this way we will be fine

    source_file = sys.argv[1] 
    print("source_file", sys.argv[1])

    j = Jayko()
    j.read_source(source_file)
    j.tokenize()
    print(f" candidate_tokens = {j.candidate_tokens}")
    j.parse()
    #j.generate_code()
