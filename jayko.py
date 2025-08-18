# FRESH START FOR JAYKO
import sys, subprocess

####################################################################
# EVENTUALLY I WANT THESE CUMBERSOME TOKEN CLASSES IN THEIR OWN FILE
####################################################################
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
        self.lbp = 1
        self.value = None
    def nud(self):
        node = INT_LITERAL_AST_NODE()
        node.value = self.value
        return node
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
        self.lbp = 10
    def led(self, left, jayko_instance):
        print("ADD_TOKEN.led")
        right = jayko_instance.expr(self.lbp)

        add_node = ADD_AST_NODE() 
        add_node.lvalue = left
        add_node.rvalue = right

        return add_node
    def __repr__(self):
        return f"TokenType = {self.type}"

class MUL_TOKEN:
    def __init__(self):
        self.type = "MUL_TOKEN"
        self.lbp = 20
    def led(self, left, jayko_instance):
        print("MUL_TOKEN.led")
        right = jayko_instance.expr(self.lbp)

        mul_node = MUL_AST_NODE() 
        mul_node.lvalue = left
        mul_node.rvalue = right
        return mul_node
    def __repr__(self):
        return f"TokenType = {self.type}"

class EOF_TOKEN:
    def __init__(self):
        self.type = "EOF_TOKEN"
        self.lbp = 0
    def __repr__(self):
        return f"TokenType = {self.type}"

###############################################################################
#  AST NODES SHOULD ALSO GO IN THEIR OWN FILE SOME DAY                        #
###############################################################################
class ASSIGNMENT_AST_NODE:
    def __init__(self):
        self.type = "ASSIGNMENT_AST_NODE"
        self.lvalue = None                  # the variable name
        self.rvalue = None                  # the root of the subtree forming the expression to be stored in lvalue
    def code_gen(self):
        if self.rvalue.type == "INT_LITERAL_AST_NODE": 
            ctype = "int"
        return f"\t{ctype} {self.lvalue.value} = {self.rvalue.value};\n"


    def __repr__(self):
        return f"AST_NODE type = {self.type} value = {self.lvalue} "

class IDENTIFIER_AST_NODE:
    def __init__(self):
        self.type = "IDENTIFIER_AST_NODE"
        self.value = None                                               # WE ONLY SUPPORT INTEGERS RN
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class INT_LITERAL_AST_NODE:
    def __init__(self):
        self.type = "INT_LITERAL_AST_NODE"
        self.value = None
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class ADD_AST_NODE:
    def __init__(self):
        self.type = "ADD_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class MUL_AST_NODE:
    def __init__(self):
        self.type = "MUL_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class SAY_AST_NODE:
    def __init__(self):
        self.type = "SAY_AST_NODE"
        self.value = None
    def code_gen(self):
        return f"\tprintf( \"%d\\n\", {self.value} );\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"



###############################################################################
#  LEXING AND PARSING FOR JAYKO
###############################################################################
class Jayko:
    def __init__(self):
        self.raw_characters = ""            # holds the text of the source code
        self.raw_char_cursor = 0            # the index of the cursor for the raw characters

        self.candidate_tokens = []          # breaks up the text into the individual parts of speech
        self.token_cursor = 0

        
        self.root = []                      # root is where the ast is formed, in order

        # debugging stuff
        self.expr_call_count = 0

        self.big_string = ""                # big_string is where the c code ends up

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
        # the hack thing to do rn is to just make sure operators are separated by spaces.
        print("BEGIN TOKENIZING")
        candidate_token_str = ""

        while self.raw_char_cursor < (len(self.raw_characters)):        # working
        #while self.raw_char_cursor < (len(self.raw_characters)):        # working
            current_char = self.raw_characters[ self.raw_char_cursor ] 
            next_char = self.peek_chars()

            # this actually fails for the situation of 4*5, because it goes in here.... im not sure
            # what the right way to look at it is. 
            # for now though, it requires all the impelmented binop tokens to be separated by space
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
            elif ( current_char in ("*", "+",";") ): 
                candidate_token_str +=current_char
                token_to_add = self.token_dispatch(candidate_token_str)
                self.candidate_tokens.append(token_to_add)
                self.advance_chars()

                candidate_token_str = ""

                if ( next_char in ("*", "+",";") ): 
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
                print("DO WE EVER DO THE NEXT CHAR VERSION")
                self.advance_chars()
                candidate_token_str = next_char
                token_to_add = self.token_dispatch(candidate_token_str)
                self.candidate_tokens.append(token_to_add)
                candidate_token_str = ""

            self.advance_chars()
        self.candidate_tokens.append(EOF_TOKEN())
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
        while self.token_cursor < len(self.candidate_tokens):
            current_token = self.candidate_tokens[ self.token_cursor ]
            if current_token.type == "LET_TOKEN":
                let_subtree = self.parse_let()
                self.root.append(let_subtree)
            elif current_token.type == "SAY_TOKEN":
                say_subtree = self.parse_say()
                self.root.append(say_subtree)
            elif current_token.type == "EOF_TOKEN":
                break


            # put this after the different grammar structures and
            # pray it isnt an off by 1... this isn't getting us to the next line of code
            current_token = self.candidate_tokens[ self.token_cursor ] 
            print(f"in parse, self.token_cursor = {self.token_cursor}")
            print(f"in parse, len(self.candidate_tokens)= {len(self.candidate_tokens)}")
            print(f"in parse, current token is = {current_token}")


    def parse_say(self):
        # a SAY statement is
        # "say" <identifier> ";"
        # and eventually we want it to be
        # "say" <identifier> | <expr> ";"
        self.expect("SAY_TOKEN")
        self.expect("IDENTIFIER_TOKEN")
        identifier = self.expected_token().value 
        self.expect("SEMICOLON_TOKEN")

        say_node = SAY_AST_NODE()
        say_node.value = identifier 

        return say_node
            

    def parse_let(self):
        # a LET statement is 
        # "let" identifier ":=" <expr> ";"
       
     
        self.expect("LET_TOKEN") 

        self.expect("IDENTIFIER_TOKEN")
        identifier = self.expected_token().value 
        id_node_to_add = IDENTIFIER_AST_NODE()
        id_node_to_add.value = identifier

        self.expect("ASSIGNMENT_TOKEN")

        print("\nbefore self.expr() is first called")
        print(f"current token = {self.candidate_tokens[ self.token_cursor ]}\n")
        value = self.expr()
        print(f"DEEP FUCKING VALUE {value}")

        self.expect("SEMICOLON_TOKEN")

        # assume for now that assignment node is the head of the subtree
        assignment_node_to_add = ASSIGNMENT_AST_NODE()
        assignment_node_to_add.lvalue = id_node_to_add
        assignment_node_to_add.rvalue = value
        print("\n\n\n")

        return assignment_node_to_add

    def expr(self, rbp = 0):
        t = self.advance_tokens()

        p_token = self.candidate_tokens[ self.token_cursor ] 
        left = t.nud()
        
        self.expr_call_count+=1
        print(f"CALLING EXPR {self.expr_call_count}")
        print(f"\nt = {t}")
        print(f"p_token() = {p_token}")
        print(f"p_token.lbp {p_token.lbp}")
        print(f" top of loop rbp {rbp}")
        print(f"go into loop?,  {rbp < p_token.lbp}\n")

        # while rbp < self.peek_tokens().lbp: # ok
        while True:
            if self.peek_tokens().type in ("LET_TOKEN", "SEMICOLON_TOKEN", "SAY_TOKEN", "EOF_TOKEN"):
                break
            if rbp >= self.peek_tokens().lbp:
                break

            t = self.advance_tokens()
            left = t.led(left, self)
        return left

    def generate_code(self):
        # the idea of this is that it will take self.root, and traverse each subtree to generate code
        # that evaluates what we wrote in Jayko
        print("BEGIN GENERATING CODE")
        print(f"self.root  = {self.root}")

        # i wonder if this should be called "statement node"?
        for top_level_node in self.root:
            print(f"top_level_node = {top_level_node}")
            text_to_add = self.traversal(top_level_node)
            self.big_string += text_to_add

        self.form_output_file()
    
    def form_output_file(self):
        # this function should take the big string and stick it into one (potentially huge) main file
        # until we learn of smarter ways to generate cod
        f = open("output.c", "w")
        f.write("#include <stdio.h>\n")
        f.write("\n")
        f.write("int main() {\n")   
        f.write(self.big_string)
        f.write("\treturn 0;\n")
        f.write("}\n")
        f.close()

    def traversal(self, node):
        # implements post order traversal for the AST
        print(f"PROCESSING NODE OF TYPE {node.__dict__}")
        return node.code_gen()
        
        


    #####################################################
    # HELPER METHODS FOR LEXING AND PARSING
    #####################################################

    # for raw text
    def peek_chars(self, offset = 1):
        peek_index = self.raw_char_cursor + offset 
        print(f"peek_indx = {peek_index}")
        print(f"len(self.raw_characters) = {len(self.raw_characters)}")
        if peek_index < len(self.raw_characters):
            return self.raw_characters[peek_index]
        else:
            return None

    def advance_chars(self):
        self.raw_char_cursor +=1
        if self.raw_char_cursor < len(self.raw_characters):
            value = self.raw_characters[ self.raw_char_cursor ]
            return value
        else:
            return None

    # for tokens
    def peek_tokens(self):
        return self.candidate_tokens[ self.token_cursor+1 ]

    def advance_tokens(self):
        value = self.candidate_tokens[ self.token_cursor ]
        self.token_cursor +=1
        return value

    def next_token(self):
        #self.token_cursor +=1
        print(f"self.token_cursor = {self.token_cursor}")
        print(f"length of token list = {len(self.candidate_tokens)}")
        value = self.candidate_tokens[ self.token_cursor+1 ]
        return value

    def expected_token(self):
        return self.candidate_tokens[ self.token_cursor-1 ]

    def expect(self, token_type):
        t = self.advance_tokens()
        if t.type != token_type:
            raise SyntaxError(f"Expected {token_type} got {t.type}")
        

if __name__ == "__main__":
    
    # the way to load the file in is PRESCRIBED for now so as long as we do it this way we will be fine

    # Delete the old output file
    subprocess.run(["rm", "output.c"])

    source_file = sys.argv[1] 
    print("source_file", sys.argv[1])

    j = Jayko()
    j.read_source(source_file)
    j.tokenize()
    print(f" candidate_tokens = {j.candidate_tokens}")
    j.parse()
    j.generate_code()

    # Run GCC on the newly created output
    print("Compiling...")
    subprocess.run(["gcc", "-o", "output", "output.c"])

    print("PROGRAM OUTPUT: ")
    subprocess.run(["./output"])
