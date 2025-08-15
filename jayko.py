# we are calling the language jayko right now. but we can change that later.
from enum import Enum, auto
import subprocess

class TokenType(Enum):
    LET = auto()
    SAY = auto()
    IDENTIFIER = auto()
    ASSIGN = auto()
    NUMBER = auto()
    DOUBLE_QUOTE = auto()
    ADD = auto()
    MUL = auto()
    SEMICOLON = auto()

class LBP(Enum):
    # LBP = left binding power.  it determines the binding sensitivity of each token
    # for Pratt's Parsing method
    LET = 0
    SAY = 0
    IDENTIFIER = 0
    ASSIGN = 0
    NUMBER = 0
    DOUBLE_QUOTE = 0 
    ADD = 2 
    MUL = 3 
    
# i think we dont use these types of nodes, because different nodes interact with rbp differently.
class NodeType(Enum):
    VARIABLE_DECLARATION = auto()
    IDENTIFIER = auto()
    NUMBER_LITERAL = auto()
    STRING_LITERAL = auto()
    SAY = auto()
    BINOP = auto()

class ASTNode():
    def __init__(self):
        self.node_type = None
        self.node_data = None
        self.lbp = 0            # the code runs with this but doenst do anything useful yet.
        self.children = []

    def nud(self):
        pass
    def led(self):
        pass

class Jayko:
    def __init__(self):
        self.reserved_keywords = {"let", "say"}

        self.token_list = []                        # 
        self.statements = []
        self.root = []                              # root of the AST
        self.big_string = ""                        # where all the code for gcc is going to end up


        self.cursor = 0                             # for moving around token list

    def peek(self, offset=0):
        return self.token_list[self.cursor + offset]

    def advance(self):
        value = self.token_list[self.cursor]
        self.cursor += 1
        return value

    def expect(self, tokentype):
        t = self.advance()
        if t[0] != tokentype:
            raise SyntaxError(f"expected {tokentype}, got {t[0]}")
        
    def read_source_code(self):
        self.f = open("hello.jko", "r")
        for line in self.f.readlines():
            # print(line.strip("\n"))
            self.tokenize2(line.strip("\n"))

    def tokenize2(self,line):
        # right now the tokenizer doesnt support multiple character lookahead,
        # so operators and identifiers need to be separated by a space.
        print("BEGIN TOKENIZING")
        print(line)
        self.candidate_tokens = []
        candidate_token = ""
        for i,char in enumerate(line):
            # dealing with spaces
            if char == " ":
                continue
            # peek
            try: next_char = line[i+1]
            except IndexError: next_char = None
            
            candidate_token += char
            if next_char == " ":
                # this is the end of a token manually inputted by me
                print("check what token it is SPACE CASE") 
                print(candidate_token)
                self.candidate_tokens.append(candidate_token)
                candidate_token = ""
                continue
            elif next_char == ";":
                # the stuff we have now must be the end of a token, because ; is the end of a line
                print("check what token it is SEMICOLON CASE")
                self.candidate_tokens.append(candidate_token)
                candidate_token = ""
                continue
            elif next_char == None:
                print("should just be appending a semicolon here")
                self.candidate_tokens.append(candidate_token)
                
        print("TOKEN LIST")
        print(self.candidate_tokens)
        for t in self.candidate_tokens:
            self.token_dispatch(t)

        print("FINAL TOKEN STREAM")
        print(self.token_list)

    def token_dispatch(self, token):
        if token == "let":
            self.token_list.append( (TokenType.LET,) )
        elif token == ":=":
            self.token_list.append( (TokenType.ASSIGN,) )
        elif token == "say":
            self.token_list.append( (TokenType.SAY,) )
        elif token == ";":
            self.token_list.append( (TokenType.SEMICOLON,) )
        elif token == "+":
            self.token_list.append( (TokenType.ADD,) )
        elif token == "*":
            self.token_list.append( (TokenType.MUL,) )
        elif token.isdigit():
            self.token_list.append( (TokenType.NUMBER, int(token) ) ) 
        else:
            # for now we just assume anything not this is an identifier
            if token not in self.reserved_keywords:
                self.token_list.append( (TokenType.IDENTIFIER, token) )
           

    def expr(rbp= 0):
        t = self.advance()
        left = t.nud(self)

    def pratt(self):
        # lets just see if we can produce a list of objects that each token should be
        # Inputs: self.token_list
        # Outputs: self.ast_nodes
        # lets get a list of statements for now

         
        # look at the first token
        current_token = self.token_list[self.cursor]
        print(current_token)
        if current_token[0] == TokenType.LET:
            self.root.append( self.parse_let() )

    def parse_let(self):
        # the way these expect/advance and peek helpers work is becuase
        # self.cursor is "global" wrt to the Jayko class
        self.expect(TokenType.LET)
        ident = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = 42 #expr()      # here is where pratt logic would take place

        self.advance()
        self.expect(TokenType.SEMICOLON)

        identifier_node = ASTNode()
        identifier_node.type = NodeType.IDENTIFIER
        identifier_node.data = ident

        variable_declaration_node = ASTNode() 
        variable_declaration_node.node_type = NodeType.VARIABLE_DECLARATION
        variable_declaration_node.children.append(identifier_node)
        return variable_declaration_node

    #def build_ast(self):
    #    # this problem just feels more complicated
    #    # need to differentiate between statements, expressions, and terms (precedence levels)
    #    # lets get the absolute simplest top down working 
    #    print("BEGIN PARSING\n")
    #    cursor = 0
    #    while cursor < len(self.token_list):
    #        if self.token_list[cursor][0] == TokenType.LET:
    #            node_to_add = ASTNode()
    #            node_to_add.node_type = NodeType.VARIABLE_DECLARATION
    #            # then we know we need to see an identifier token next 
    #            cursor += 1

    #            if self.token_list[cursor][0] == TokenType.IDENTIFIER: 
    #                id_node_to_add = ASTNode()
    #                id_node_to_add.node_type = NodeType.IDENTIFIER
    #                id_node_to_add.node_data = self.token_list[cursor][1]
    #                node_to_add.children.append( id_node_to_add )
    #                cursor+=1
    #            else:
    #                print("SyntaxError: Expected an IDENTIFIER token")
    #                quit()

    #            if self.token_list[cursor][0] == TokenType.ASSIGN:
    #                cursor+=1
    #            else:
    #                print("SyntaxError: Expected an ASSIGN token")
    #            # after this we need to add the 
    #            if self.token_list[cursor][0] == TokenType.NUMBER:
    #                num_node_to_add = ASTNode()
    #                num_node_to_add.node_type = NodeType.NUMBER_LITERAL
    #                num_node_to_add.node_data = self.token_list[cursor][1]
    #                node_to_add.children.append( num_node_to_add )
    #                cursor+=1
    #            else:
    #                print("SyntaxError: Expected a NUMBER token")
    #                quit()

    #        if cursor>=len(self.token_list): break  # HACK FIX LATER IM JUST REALLY EXCITED

    #        print(self.token_list)
    #        print("cursor ", cursor)
    #        if self.token_list[cursor][0] == TokenType.SAY:
    #            node_to_add = ASTNode()
    #            node_to_add.node_type = NodeType.SAY
    #            # then we know we need to see an identifier token next
    #            cursor+=1
    #            if self.token_list[cursor][0] == TokenType.IDENTIFIER:
    #                id_node_to_add = ASTNode()
    #                id_node_to_add.node_type = NodeType.IDENTIFIER
    #                id_node_to_add.node_data = self.token_list[cursor][1]
    #                node_to_add.children.append( id_node_to_add )
    #                cursor+=1
    #            else:
    #                print("SyntaxError: Expected an IDENTIFIER token")
    #                quit()

    #        cursor += 1 
    #    print(node_to_add.node_type, node_to_add.children)      
    #    # FIX LATER, like make it more "modular or wahtever"
    #    self.root.append(node_to_add)
    #    print("DONE PARSING") 
    #    #for item in self.root:
    #    #    print("WENT BACK HERE")
    #    #    self.big_string += self.generate_big_string(item)

    def generate_output(self):
        for item in self.root:
            self.big_string+= self.generate_big_string(item)
        self.generate_output_file()

    def generate_big_string(self, node):
        # we only want it to work for a VARIABLE_DECLARATION node right now
        # this is called post-order traversal of the tree

        small_string = "\t" + self.traversal(node) + "\n" 
        print("small string -> ", small_string)
        return small_string

    def traversal(self,node):
        print("PROCESSING NODE OF TYPE " , node.node_type)
        if node.node_type == None:
            print("Encountered NoneType Node, exiting") 
            quit()

        if node.node_type == NodeType.VARIABLE_DECLARATION:
            var_name = self.traversal(node.children[0])   # Identifier
            value = self.traversal(node.children[1])      # Expression
            return f"int {var_name} = {value};"

        if node.node_type == NodeType.IDENTIFIER:
            return str(node.node_data)

        if node.node_type == NodeType.NUMBER_LITERAL:
            return str(node.node_data)
        
        if node.node_type == NodeType.SAY:
            var_name = self.traversal(node.children[0])    # Identifier
            return f"printf(\"%d\\n\", {var_name} );"
    
        for child in node.children:
            self.traversal(child) 

        print(node.node_data)

    def generate_output_file(self):
        self.output = open("output.c","w")

        self.output.write("#include<stdio.h>\n")
        self.output.write("int main(){\n")
        self.output.write(self.big_string+"\n")
        self.output.write("\t" + "return 0;\n")
        self.output.write("}\n")


        self.output.close()

if __name__ == "__main__":
    subprocess.run(["rm", "output.c"])

    j = Jayko() 
    j.read_source_code()
    j.pratt()
    # j.generate_output()

    #subprocess.run(["gcc", "-o", "output", "output.c"])
    #subprocess.run(["./output"])
