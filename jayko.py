#!/usr/bin/python3 -i
#  FRESH START FOR JAYKO
import sys, subprocess
from token_defs import *
from ast_node_defs import *

###############################################################################
#  LEXING AND PARSING FOR JAYKO
###############################################################################
class Jayko:
    def __init__(self):
        self.raw_characters = ""            # holds the text of the source code
        self.raw_char_cursor = 0            # the index of the cursor for the raw characters

        self.candidate_tokens = []          # breaks up the text into the individual parts of speech
        self.token_cursor = 0
        self.current_line = 1               # track line number so we have a non zero error output
        
        self.root = []                      # root is where the ast is formed, in order

        # debugging stuff
        self.expr_call_count = 0

        self.big_string = ""                # big_string is where the c code ends up

        # symbol table (it is finally time to learn how it works)
        # runtime stuff
        self.symbol_table = {}              # empty dict rn

    def read_source(self,input_file):
        # read_source(): takes the source code and puts every character into
        # self.raw_characters 
        # we will also check for semi colons at the end of each line during this phase
        # because it is pretty easy to do so.

        source = open(input_file)
        for line in source.readlines():
            #self.raw_characters+=line.strip("\n")
            self.raw_characters+=line

        print("raw, characters")
        print(repr(self.raw_characters))

    def tokenize(self):

        while self.raw_char_cursor < len(self.raw_characters):
            ch = self.raw_characters[ self.raw_char_cursor ]

            # 1) Skip whitespace
            if ch.isspace():
                if ch == "\n":
                    self.current_line +=1 
                    print(f"{self.current_line}")
                self.advance_chars()
                continue

            # 2) Identifiers or Keywords
            if ch.isalpha() or ch == "_":
                buf = [ch]
                self.advance_chars()
                while self.raw_char_cursor < len(self.raw_characters):
                    c = self.raw_characters[self.raw_char_cursor]
                    if c.isalnum() or c == "_":
                        buf.append(c)
                        self.advance_chars()
                    else:
                        break

                str = "".join(buf)
                self.candidate_tokens.append(self.token_dispatch("".join(buf)))
                continue

            # 3) Numbers (ints for now)
            if ch.isdigit():
                buf = [ch]
                self.advance_chars()
                while self.raw_char_cursor < len(self.raw_characters) and \
                      self.raw_characters[self.raw_char_cursor].isdigit():
                    buf.append(self.raw_characters[self.raw_char_cursor])
                    self.advance_chars()

                self.candidate_tokens.append(self.token_dispatch("".join(buf)))
                continue

            # 3) Two character operator :=
            if ch == "=":
                # now we lookahead but we dont move yet
                nx = self.peek_chars()
                if nx == "=":
                    self.advance_chars()                # consume ":" 
                    self.advance_chars()                # consume "="
                    self.candidate_tokens.append(self.token_dispatch("=="))
                    continue
                #else:
                #    raise SyntaxError("We only support := right now")

            if ch == "<":
                nx = self.peek_chars()
                if nx == "=":
                    self.advance_chars()                # consume "<"
                    self.advance_chars()                # consume "="
                    self.candidate_tokens.append(self.token_dispatch("<="))
                    continue
                    
            if ch == ">":
                nx = self.peek_chars()
                if nx == "=":
                    self.advance_chars()                # consume "<"
                    self.advance_chars()                # consume "="
                    self.candidate_tokens.append(self.token_dispatch(">="))
                    continue

            if ch == "!":
                nx = self.peek_chars()
                if nx == "=":
                    self.advance_chars()                # consume "!"
                    self.advance_chars()                # consume "="
                    self.candidate_tokens.append(self.token_dispatch("!="))
                    continue

            if ch == "/":
                nx = self.peek_chars()
                if nx == "/":
                    self.advance_chars()
                    self.advance_chars()                # consume both "/"'s
                    while ch != "\n":
                        ch = self.raw_characters[ self.raw_char_cursor ]
                        self.advance_chars()
                    self.current_line+=1
                    continue


            # 4) Single-char punctuators/operators
            if ch in ("*", "+", "-", ":", ";", "%", "{", "}", "=", "<", ">", "(",")", "[", "]", "."):
                self.candidate_tokens.append(self.token_dispatch(ch))
                self.advance_chars()
                continue

            # 5) Strings
            if ch == '"':
                buf = ['"']
                self.advance_chars()
                while self.raw_char_cursor < len(self.raw_characters):
                    c = self.raw_characters[self.raw_char_cursor]
                    buf.append(c)
                    self.advance_chars()
                    if c == '"':
                        break
                self.candidate_tokens.append(self.token_dispatch("".join(buf)))
                continue

            # Chars 
            if ch == "'":
                buf = ["'"]
                self.advance_chars()
                while self.raw_char_cursor < len(self.raw_characters):
                    c = self.raw_characters[self.raw_char_cursor]
                    buf.append(c)
                    self.advance_chars()
                    if c == "'":
                        break
                self.candidate_tokens.append(self.token_dispatch("".join(buf)))
                continue

            # 6) Unknown Char
            raise SyntaxError(f"l{self.current_line}: Unexpected character: {ch}")

        # add the EOF_TOKEN() instead of doing it with guards in advance, the guards should still be safe
        eof_token = EOF_TOKEN()
        eof_token.line_no = self.current_line
        self.candidate_tokens.append(eof_token)

    def token_dispatch(self, candidate_token_str):
        # this function should look at the candidate_token_str and form the token object
        # should probably re implement this dispatch using a dict that just matches the token
        # to the translation within the dictionary
        if candidate_token_str == "let":
            token_to_add = LET_TOKEN()
        elif candidate_token_str == "loop":
            token_to_add = LOOP_TOKEN()
        elif candidate_token_str == "u8":
            token_to_add = U8_TOKEN()
        elif candidate_token_str == "i32":
            token_to_add = I32_TOKEN()
        elif candidate_token_str == "str":
            token_to_add = STR_TOKEN()
        elif candidate_token_str == "char":
            token_to_add = CHAR_TOKEN()
        elif candidate_token_str == ";":
            token_to_add = SEMICOLON_TOKEN()
        elif candidate_token_str == ":":
            token_to_add = COLON_TOKEN()
        elif candidate_token_str == "{":
            token_to_add = LBRACE_TOKEN()
        elif candidate_token_str == "}":
            token_to_add = RBRACE_TOKEN()
        elif candidate_token_str == "(":
            token_to_add = LPAREN_TOKEN()
        elif candidate_token_str == ")":
            token_to_add = RPAREN_TOKEN()
        elif candidate_token_str == "[":
            token_to_add = LSQUARE_TOKEN()
        elif candidate_token_str == "]":
            token_to_add = RSQUARE_TOKEN()
        elif candidate_token_str == "if":
            token_to_add = IF_TOKEN()
        elif candidate_token_str == "else":
            token_to_add = ELSE_TOKEN()
        elif candidate_token_str == "*":
            token_to_add = MUL_TOKEN()
        elif candidate_token_str == "+":
            token_to_add = ADD_TOKEN()
        elif candidate_token_str == "-":
            token_to_add = SUB_TOKEN()
        elif candidate_token_str == "==":
            token_to_add = EQUALITY_TOKEN()
        elif candidate_token_str == "and":
            token_to_add = AND_TOKEN()
        elif candidate_token_str == "<":
            token_to_add = LT_TOKEN()
        elif candidate_token_str == "<=":
            token_to_add = LEQ_TOKEN()
        elif candidate_token_str == ">=":
            token_to_add = GEQ_TOKEN()
        elif candidate_token_str == "!=":
            token_to_add = NEQ_TOKEN()
        elif candidate_token_str == ">":
            token_to_add = GT_TOKEN()
        elif candidate_token_str == "%":
            token_to_add = MOD_TOKEN()
        elif candidate_token_str == ".":
            token_to_add = DOT_TOKEN()
        elif candidate_token_str == "=":
            token_to_add = ASSIGNMENT_TOKEN()
        elif candidate_token_str == "say":
            token_to_add = SAY_TOKEN()
        elif candidate_token_str.isnumeric():
            token_to_add = INT_LITERAL_TOKEN()
            token_to_add.value = int(candidate_token_str)
        elif candidate_token_str.replace("_","").isalnum():
            token_to_add = IDENTIFIER_TOKEN()
            token_to_add.value = str(candidate_token_str)
        elif candidate_token_str[0] == "\"" and candidate_token_str[-1] == "\"":
            token_to_add = STRING_LITERAL_TOKEN()
            token_to_add.value = candidate_token_str
        elif candidate_token_str[0] == "'" and candidate_token_str[-1] == "'":
            token_to_add = CHAR_LITERAL_TOKEN()
            token_to_add.value = candidate_token_str
        else:
            print(f"candidate token str {candidate_token_str} not found")
            print("Exiting...")
            quit()
        print(f"[token dispatch] about to return {token_to_add}")

        # add the line number so we dont have completely zero error output
        if token_to_add:
            token_to_add.line_no = self.current_line

        return token_to_add

    def parse(self):
        while self.token_cursor < len(self.candidate_tokens):
            if self.peek_tokens().type == "EOF_TOKEN":
                break
            statement = self.parse_statement()
            self.root.append(statement)

    def parse_statement(self):
        # Parsing should take the list of self.candidate_tokens
        # and output the AST
        while self.token_cursor < len(self.candidate_tokens):
            current_token = self.candidate_tokens[ self.token_cursor ]
            if current_token.type == "LET_TOKEN":
                let_subtree = self.parse_let()
                return let_subtree

            elif current_token.type == "IDENTIFIER_TOKEN":
                subtree = self.expr()
                self.expect("SEMICOLON_TOKEN")
                print(f"[parse_statement, id_tok] subtree = {subtree}")
                return subtree

            elif current_token.type == "SAY_TOKEN":
                say_subtree = self.parse_say()
                return say_subtree
            elif current_token.type == "IF_TOKEN":
                if_subtree = self.parse_if()
                return if_subtree
            elif current_token.type == "LOOP_TOKEN":
                loop_subtree = self.parse_loop()
                return loop_subtree
            elif current_token.type == "LBRACE_TOKEN":
                block_subtree = self.parse_block()
                return block_subtree
                printf(f"[parse], block_subtree = {block_subtree}")
            elif current_token.type == "EOF_TOKEN":
                break
            else:
                print(f"We do not know how to process the token {current_token}")
                quit()

    #def parse_index(self):
    #    node = DA_INDEX_AST_NODE()
    #    identifier = self.candidate_tokens[ self.token_cursor ]
    #    node.target = identifier.value
    #    node.target_type = self.symbol_table[node.target]

    #    self.expect("LSQUARE_TOKEN")
    #    node.index = self.expr()
    #    self.expect("RSQUARE_TOKEN")
    #    return node

    def parse_block(self):
        print("[parse_block], entered")
        self.expect("LBRACE_TOKEN")
        statements = []
        while not self.match("RBRACE_TOKEN"):
            print(f"[parse_block] self.candidate_tokens[ self.token_cursor ]")
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        node = BLOCK_AST_NODE()
        node.statements = statements
        return node

    def parse_say(self):
        # a SAY statement is
        # "say" <identifier> ";"
        # and eventually we want it to be
        # "say" <identifier> | <expr> ";"
        self.expect("SAY_TOKEN")
        subtree = self.expr()
        say_node = SAY_AST_NODE()
        say_node.value = subtree


        self.expect("SEMICOLON_TOKEN")
        return say_node

    def parse_let(self):
        # a LET statement is 
        # "let" identifier ":=" <expr> ";"
        # "let" 
     
        self.expect("LET_TOKEN") 

        self.expect("IDENTIFIER_TOKEN")
        identifier = self.expected_token().value 
        id_node_to_add = IDENTIFIER_AST_NODE()
        id_node_to_add.value = identifier

        declared_type = None
        # if self.match("COLON_TOKEN"):
        self.expect("COLON_TOKEN")
        declared_type = self.parse_type()

        id_node_to_add.value_type = declared_type

        self.expect("ASSIGNMENT_TOKEN")
        value = self.expr()
        self.expect("SEMICOLON_TOKEN")

        # assume for now that assignment node is the head of the subtree
        let_node_to_add = LET_AST_NODE()
        let_node_to_add.lvalue = id_node_to_add
        let_node_to_add.rvalue = value
        let_node_to_add.declared_type = declared_type

        # also append the info to our brand new symbol table!
        self.symbol_table[identifier] = declared_type

        return let_node_to_add

    def parse_type(self):
            self.expect_multiple( ("I32_TOKEN", "U8_TOKEN", "STR_TOKEN", "CHAR_TOKEN") )

            base_type = self.expected_token().value
            print(f"[parse_type] base type = {base_type}")

            is_array = False
            if self.match("LSQUARE_TOKEN"):
                self.expect("RSQUARE_TOKEN")
                is_array = True

            return {
                "base": base_type,
                "is_array": is_array
            }
    
    def parse_assignment(self):
        # an ASSIGNMENT statement is 
        # <identifier> "=" <expr> ";"
        self.expect("IDENTIFIER_TOKEN")
        identifier = self.expected_token().value 
        id_node_to_add = IDENTIFIER_AST_NODE()
        id_node_to_add.value = identifier

        self.expect("ASSIGNMENT_TOKEN")

        value = self.expr()

        self.expect("SEMICOLON_TOKEN")

        # assume for now that assignment node is the head of the subtree
        assignment_node_to_add = ASSIGNMENT_AST_NODE()
        assignment_node_to_add.lvalue = id_node_to_add
        assignment_node_to_add.rvalue = value
        print("\n\n\n")

        return assignment_node_to_add

    def parse_if(self):
        # an IF statement is 
        # if <expr> <block> else? if? <block>
       
        self.expect("IF_TOKEN")
        if_condition = self.expr()
        then_block = self.parse_block()

        else_block = None
        if self.peek_tokens().type == "ELSE_TOKEN":
            self.advance_tokens()   # consume "else"
            if self.peek_tokens().type == "IF_TOKEN":
                else_block = self.parse_if()
            else:
                else_block = self.parse_block()
         
        if_node_to_add = IF_AST_NODE()
        if_node_to_add.if_condition = if_condition
        if_node_to_add.then_block = then_block
        if_node_to_add.else_block = else_block
        return if_node_to_add

    def parse_loop(self):
        # a LOOP statement is 
        # LOOP expr block
        self.expect("LOOP_TOKEN")
        loop_condition = self.expr()
        loop_block = self.parse_block()

        loop_node_to_add = LOOP_AST_NODE()
        loop_node_to_add.loop_condition = loop_condition
        loop_node_to_add.loop_block = loop_block
        return loop_node_to_add

    def expr(self, rbp = 0):
        print(f"[expr] rbp={rbp}  peek={self.peek_tokens().type}  peek.lbp={getattr(self.peek_tokens(), 'lbp', None)}  cursor={self.token_cursor}")
        t = self.advance_tokens()

        if t.type in ("LPAREN_TOKEN", "LSQUARE_TOKEN", "SUB_TOKEN"):
            left = t.nud(self)
        else:
            left = t.nud()

        self.expr_call_count+=1

        # while rbp < self.peek_tokens().lbp: # ok
        while True:
            tok = self.peek_tokens()
            if tok.type in ("LET_TOKEN", "SAY_TOKEN", "EOF_TOKEN", "SEMICOLON_TOKEN"):
                break
            if rbp >= tok.lbp:
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
        f.write("#include <stdint.h>\n")
        f.write("#include \"c_src/jayko_array.h\"\n")
        f.write("DA_TYPEDEF(uint8_t, Array_u8);\n")             # eventually we want our program to know about the types that have a dynamic array and 
        f.write("DA_TYPEDEF(int, Array_i32);\n")                # only deefine them once at the top of the program.
        f.write("\n")
        f.write("int main() {\n")   
        f.write(self.big_string)
        f.write("\treturn 0;\n")
        f.write("}\n")
        f.close()

    def traversal(self, node):
        # implements post order traversal for the AST
        print(f"PROCESSING NODE OF TYPE {node.__dict__}")
        return node.code_gen(self.symbol_table) 


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
    def peek_tokens(self,offset=0):
        # why it's not self.token_cursor + 1, is because self.advance_tokens advances the cursor
        # when used in conjunction with peek_tokens, so the "peek" token is actually where the 
        # cursor is at a given time.
        idx = self.token_cursor + offset
        if idx >= len(self.candidate_tokens):
           return EOF_TOKEN() 
        return self.candidate_tokens[ self.token_cursor ] # self.token_cursor + 1 "works"

    def advance_tokens(self):
        if self.token_cursor >= len(self.candidate_tokens):
            return EOF_TOKEN()
        value = self.candidate_tokens[ self.token_cursor ]
        self.token_cursor +=1
        return value

    def expected_token(self):
        return self.candidate_tokens[ self.token_cursor-1 ]

    def expect(self, token_type):
        t = self.advance_tokens()
        if t.type != token_type:
            prev_token_index = self.token_cursor - 2 
            print(f"[expect] prev_token_index = {prev_token_index}")
            if prev_token_index >= 0:
                prev_token = self.candidate_tokens[ self.token_cursor - 2]  # since theres a call to advnace_tokens(), the "previous token" in terms of parsing errors, was 2 tokens ago
                print(f"prev_token = {prev_token}")
                raise SyntaxError(f"Expected {token_type} got {t.type} on L:{prev_token.line_no} - {t.line_no}")
            else:
                raise SyntaxError(f"Expected {token_type} got {t.type} around L:{t.line_no}")
        return t

    def expect_multiple(self, token_tuple):
        t = self.advance_tokens()
        print(f"[expect_multiple] token_tuple = {token_tuple}")
        for ctok in token_tuple:
            print(f"[expect_multiple] ctok = {ctok}")
            print(f"[expect_multiple] t.type = {t.type}")
            if t.type == ctok:
                return t
        raise ValueError("The token type wasn't found in the token tuple")
         

    def match(self, token_type):
        # checks the next token
        if (self.peek_tokens().type == token_type):
            self.advance_tokens()
            return True
        return False
     
    ########################################################################
    # DEBUGGING
    ########################################################################
    def print_ast(self, node, indent = 0):
        print("     "*indent + str(node))
        if hasattr(node, "value"):
            self.print_ast(node.value, indent+1)
        if hasattr(node, "lvalue"):
            self.print_ast(node.lvalue, indent+1)
        if hasattr(node, "rvalue"):
            self.print_ast(node.rvalue, indent+1)

if __name__ == "__main__":
    
    # the way to load the file in is PRESCRIBED for now so as long as we do it this way we will be fine

    # Delete the old output file
    subprocess.run(["rm", "output.c"])
    subprocess.run(["rm", "output"])

    source_file = sys.argv[1] 
    print("source_file", sys.argv[1])

    j = Jayko()
    j.read_source(source_file)
    j.tokenize()
    #print(f" candidate_tokens = {j.candidate_tokens}")
    #print("\n== TOKEN DUMP")
    #for tok in j.candidate_tokens:
    #    print(f"tok -> {tok}")
    j.parse()

    print("PRINTING THE TREES")
    for top_level_node in j.root:
        j.print_ast(top_level_node)
    j.generate_code()


    ## Run GCC on the newly created output
    print("Compiling...")
    subprocess.run(["gcc", "-o", "output", "output.c"])

    print("\n\nPROGRAM OUTPUT: ")
    subprocess.run(["./output"])
