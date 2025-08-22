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
        self.lbp = 0
    def nud(self):
        node = IDENTIFIER_AST_NODE()
        node.value = self.value
        return node
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
        self.lbp = 0 # 1 works
        self.value = None
    def nud(self):
        node = INT_LITERAL_AST_NODE()
        node.value = self.value
        return node
    def __repr__(self):
        return f"TokenType = {self.type} value = {self.value}"

class STRING_LITERAL_TOKEN:
    def __init__(self):
        self.type = "STRING_LITERAL_TOKEN"
        self.lbp = 0 # no idea what it should actually be, so just picking the same as the other literals
        self.value = None
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

class LBRACE_TOKEN:
    def __init__(self):
        self.lbp = 0
        self.type = "LBRACE_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class RBRACE_TOKEN:
    def __init__(self):
        self.lbp = 0
        self.type = "RBRACE_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class IF_TOKEN:
    def __init__(self):
        self.type = "IF_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class LOOP_TOKEN:
    def __init__(self):
        self.type = "LOOP_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"
    
class ELSE_TOKEN:
    def __init__(self):
        self.type = "ELSE_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class TRUE_TOKEN:
    def __init__(self):
        self.type = "TRUE_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class FALSE_TOKEN:
    def __init__(self):
        self.type = "TRUE_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class EQUALITY_TOKEN:
    def __init__(self):
        self.type = "EQUALITY_TOKEN"
        self.lbp = 5
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)

        equality_node = EQUALITY_AST_NODE()
        equality_node.lvalue = left
        equality_node.rvalue = right
        return equality_node
        
    def __repr__(self):
        return f"TokenType = {self.type}"

class LT_TOKEN:
    def __init__(self):
        self.type = "LT_TOKEN"
        self.lbp = 6
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)

        lt_node = LT_AST_NODE()
        lt_node.lvalue = left
        lt_node.rvalue = right
        return lt_node
        
    def __repr__(self):
        return f"TokenType = {self.type}"

class GT_TOKEN:
    def __init__(self):
        self.type = "GT_TOKEN"
        self.lbp = 6
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)

        lt_node = GT_AST_NODE()
        lt_node.lvalue = left
        lt_node.rvalue = right
        return lt_node
        
    def __repr__(self):
        return f"TokenType = {self.type}"

class LEQ_TOKEN:
    def __init__(self):
        self.type = "LEQ_TOKEN"
        self.lbp = 6
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)

        leq_node = LEQ_AST_NODE()
        leq_node.lvalue = left
        leq_node.rvalue = right
        return leq_node
        
    def __repr__(self):
        return f"TokenType = {self.type}"
    

class ADD_TOKEN:
    def __init__(self):
        self.type = "ADD_TOKEN"
        self.lbp = 10
    def led(self, left, jayko_instance):
        print("ADD_TOKEN.led")
        print(f"[led {self.type}] lbp={self.lbp}  cursor={jayko_instance.token_cursor}")
        right = jayko_instance.expr(self.lbp)

        add_node = ADD_AST_NODE() 
        add_node.lvalue = left
        add_node.rvalue = right
        return add_node
    def __repr__(self):
        return f"TokenType = {self.type}"

class SUB_TOKEN:
    def __init__(self):
        self.type = "SUB_TOKEN"
        self.lbp = 10
    def led(self, left, jayko_instance):
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
        print(f"[led {self.type}] lbp={self.lbp}  cursor={jayko_instance.token_cursor}")
        right = jayko_instance.expr(self.lbp)

        mul_node = MUL_AST_NODE() 
        mul_node.lvalue = left
        mul_node.rvalue = right
        return mul_node
    def __repr__(self):
        return f"TokenType = {self.type}"

class MOD_TOKEN:
    def __init__(self):
        self.type = "MOD_TOKEN"
        self.lbp = 20
    def led(self, left, jayko_instance):
        #print("MUL_TOKEN.led")
        #print(f"[led {self.type}] lbp={self.lbp}  cursor={jayko_instance.token_cursor}")
        right = jayko_instance.expr(self.lbp)

        mod_node = MOD_AST_NODE() 
        mod_node.lvalue = left
        mod_node.rvalue = right
        return mod_node
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
class LET_AST_NODE:
    def __init__(self):
        self.type = "LET_AST_NODE"
        self.lvalue = None                  # the variable name
        self.rvalue = None                  # the root of the subtree forming the expression to be stored in lvalue
    def code_gen(self):
        rhs = self.rvalue.code_gen()
        identifier = self.lvalue.code_gen()
        return f"\tint {identifier} = {rhs};\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type} value = {self.lvalue} "

# we absolutely need to incorporate the difference between a decaration and an assignemnt
class ASSIGNMENT_AST_NODE:
    def __init__(self):
        self.type = "ASSIGNMENT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        rhs = self.rvalue.code_gen()
        identifier = self.lvalue.code_gen()
        return f"\t {identifier } = {rhs};\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type} value = {self.lvalue} "



class IDENTIFIER_AST_NODE:
    def __init__(self):
        self.type = "IDENTIFIER_AST_NODE"
        self.value = None                                               # WE ONLY SUPPORT INTEGERS RN
    def code_gen(self):
        return str(self.value)
     
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class INT_LITERAL_AST_NODE:
    def __init__(self):
        self.type = "INT_LITERAL_AST_NODE"
        self.value = None
    def code_gen(self):
        return str(self.value)
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class STRING_LITERAL_AST_NODE:
    def __init__(self):
        self.type = "STRING_LITERAL_AST_NODE"           
        self.value = None                               
    def code_gen(self):
        return str(self.value)
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class EQUALITY_AST_NODE:
    def __init__(self):
        self.type = "EQUALITY_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        print("Generating code for EQUALITY")
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} == {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class LT_AST_NODE:
    def __init__(self):
        self.type = "LT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} < {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class GT_AST_NODE:
    def __init__(self):
        self.type = "GT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} > {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class LEQ_AST_NODE:
    def __init__(self):
        self.type = "LT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} <= {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"
    

class ADD_AST_NODE:
    def __init__(self):
        self.type = "ADD_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        print("Generating code for ADD")
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} + {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class SUB_AST_NODE:
    def __init__(self):
        self.type = "SUB_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} - {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class MUL_AST_NODE:
    def __init__(self):
        self.type = "MUL_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        print("Generating code for MUL")
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} * {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class MOD_AST_NODE:
    def __init__(self):
        self.type = "MOD_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self):
        print("Generating code for MOD")
        left_code = self.lvalue.code_gen()
        right_code = self.rvalue.code_gen()
        return f"({left_code} % {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class SAY_AST_NODE:
    def __init__(self):
        self.type = "SAY_AST_NODE"
        self.value = None
        self.route = None                               # route is to dispatch to the correct code generation
    def code_gen(self):
        if self.route == "IDENTIFIER_TOKEN" or self.route == "INT_LITERAL_TOKEN":                         # this feels like a hack, because we are 
            return f"\tprintf( \"%d\\n\", {self.value} );\n"    # assuming depth 1 expressions.
        if self.route == "STRING_LITERAL_TOKEN":
            l1 = f"\tchar str[] = {self.value};\n"
            l2 = f"\tprintf( \"%s\\n\", str );\n"
            return l1 + l2 
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class BLOCK_AST_NODE:
    def __init__(self):
        self.type = "BLOCK_AST_NODE"
        self.statements = []
    def code_gen(self):
        buf = []
        for ast_node in self.statements:
            buf.append(f"{ast_node.code_gen()}")
        return "".join(buf)

    def __repr__(self):
        return f"AST_NODE type = {self.type}, with {len(self.statements)} statements in it"

class IF_AST_NODE:
    def __init__(self):
        self.type = "IF_AST_NODE"
        self.if_condition = None
        self.then_block = None
        self.else_block = None
    def code_gen(self):
        cond = self.if_condition.code_gen()
        then_block = self.then_block.code_gen()
        if self.else_block != None:
            else_block = self.else_block.code_gen()
            return f"if ( {cond} ){{ {then_block} }} else {{ {else_block} }}"

        return f" if ({cond}) {{ {then_block} }} "
    def __repr__(self):
        return f"AST_NODE type = {self.type}, with if_condition = {self.if_condition}, then_block = {self.then_block}, else_block = {self.else_block}"

class LOOP_AST_NODE:
    def __init__(self):
        self.type = "LOOP_AST_NODE"
        self.loop_condition = None 
        self.loop_block = None
    def code_gen(self):
        cond = self.loop_condition.code_gen()
        loop_block = self.loop_block.code_gen()
        return f"while ( {cond}) {{ {loop_block} }} "
    def __repr__(self):
        return f"AST_NODE type = {self.type}, with loop_condition = {self.loop_condition}, and loop_block = {self.loop_block}" 



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
        # we will also check for semi colons at the end of each line during this phase
        # because it is pretty easy to do so.

        source = open(input_file)
        for line in source.readlines():
            self.raw_characters+=line.strip("\n")

        print("raw, characters")
        print(self.raw_characters)

    def tokenize(self):

        while self.raw_char_cursor < len(self.raw_characters):
            ch = self.raw_characters[ self.raw_char_cursor ]

            # 1) Skip whitespace
            if ch.isspace():
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
            if ch == ":":
                # now we lookahead but we dont move yet
                nx = self.peek_chars()
                if nx == "=":
                    self.advance_chars()                # consume ":" 
                    self.advance_chars()                # consume "="
                    self.candidate_tokens.append(self.token_dispatch(":="))
                    continue
                else:
                    raise SyntaxError("We only support := right now")

            if ch == "<":
                nx = self.peek_chars()
                if nx == "=":
                    self.advance_chars()                # consume "<"
                    self.advance_chars()                # consume "="
                    self.candidate_tokens.append(self.token_dispatch("<="))
                    continue
                    



            # 4) Single-char punctuators/operators
            if ch in ("*", "+", "-", ";", "%", "{", "}", "=", "<", ">"):
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

            # 6) Unknown Char
            raise SyntaxError(f"Unexpected character: {ch}")

    def token_dispatch(self, candidate_token_str):
        # this function should look at the candidate_token_str and form the token object
        # should probably re implement this dispatch using a dict that just matches the token
        # to the translation within the dictionary
        if candidate_token_str == "let":
            token_to_add = LET_TOKEN()
        elif candidate_token_str == "loop":
            token_to_add = LOOP_TOKEN()
        elif candidate_token_str == ";":
            token_to_add = SEMICOLON_TOKEN()
        elif candidate_token_str == "{":
            token_to_add = LBRACE_TOKEN()
        elif candidate_token_str == "}":
            token_to_add = RBRACE_TOKEN()
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
        elif candidate_token_str == "=":
            token_to_add = EQUALITY_TOKEN()
        elif candidate_token_str == "<":
            token_to_add = LT_TOKEN()
        elif candidate_token_str == "<=":
            token_to_add = LEQ_TOKEN()
        elif candidate_token_str == ">":
            token_to_add = GT_TOKEN()
        elif candidate_token_str == "%":
            token_to_add = MOD_TOKEN()
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
        elif candidate_token_str[0] == "\"" and candidate_token_str[-1] == "\"":
            token_to_add = STRING_LITERAL_TOKEN()
            token_to_add.value = candidate_token_str
        else:
            print(f"candidate token str {candidate_token_str} not found")
            print("Exiting...")
            quit()


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
            #elif current_token.type == "IDENTIFIER_TOKEN":
            #    # if we see an identifier token at the start of a statment theres a couple things
            #    # that could be happening
            #    nx = self.candidate_tokens[ self.token_cursor + 1]
            #    print(f"[parse_statemetn] nx = {nx}")
            #    if nx.type == "ASSIGNMENT_TOKEN":
            #        print(f"[parse_statement] nx.type == ASSIGNMENT_TOKEN")
            #        assignment_subtree = self.parse_assignment()
            #    else: #nx.type == "EQUALITY_TOKEN":
            #        print(f"[parse_statement] else")
            #        assignment_subtree = self.expr()
            #    return assignment_subtree

            elif current_token.type == "IDENTIFIER_TOKEN":
                assignment_subtree = self.parse_assignment()
                return assignment_subtree
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


        # self.expect("IDENTIFIER_TOKEN")
        # I think a better thing to do is change the expect() function so that it can accept
        # multiple different token types, but I'm not really sure how to do that/don't really
        # feel like figuring it out right now, but I should do it because it makes the parsing
        # logic look a LOT better 
        t = self.advance_tokens() # we would have normally called this in expect
        if (t.type == "STRING_LITERAL_TOKEN" or t.type == "IDENTIFIER_TOKEN" or t.type == "INT_LITERAL_TOKEN"):
            identifier = self.expected_token().value 

            say_node = SAY_AST_NODE()
            say_node.value = identifier 
            say_node.route = t.type

        else:
            raise SyntaxError(f"[parse_say] Encountered an Incorrect Node Type {t.type}")
            

        self.expect("SEMICOLON_TOKEN")
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

        self.expect("SEMICOLON_TOKEN")

        # assume for now that assignment node is the head of the subtree
        let_node_to_add = LET_AST_NODE()
        let_node_to_add.lvalue = id_node_to_add
        let_node_to_add.rvalue = value
        print("\n\n\n")

        return let_node_to_add
    
    def parse_assignment(self):
        # an ASSIGNMENT statement is 
        # <identifier> ":=" <expr> ";"
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

        left = t.nud()
        
        self.expr_call_count+=1

        # while rbp < self.peek_tokens().lbp: # ok
        while True:
            tok = self.peek_tokens()
            if tok.type in ("LET_TOKEN", "SEMICOLON_TOKEN", "SAY_TOKEN", "EOF_TOKEN"):
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
        # why it's not self.token_cursor + 1, is because self.advance_tokens advances the cursor
        # when used in conjunction with peek_tokens, so the "peek" token is actually where the 
        # cursor is at a given time.
        return self.candidate_tokens[ self.token_cursor ] # self.token_cursor + 1 "works"

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

    def match(self, token_type):
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
    print(f" candidate_tokens = {j.candidate_tokens}")
    j.parse()

    #print("PRINTING THE TREES")
    #for top_level_node in j.root:
    #    j.print_ast(top_level_node)
    j.generate_code()


    ## Run GCC on the newly created output
    print("Compiling...")
    subprocess.run(["gcc", "-o", "output", "output.c"])

    print("\n\nPROGRAM OUTPUT: ")
    subprocess.run(["./output"])
