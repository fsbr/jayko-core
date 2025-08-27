####################################################################
# TOKEN DEFNITIONS ARE FINALLY IN THEIR OWN FILES
####################################################################
from ast_node_defs import *
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
        self.lbp = 5
    def led(self, left, jayko_instance):
        node = ASSIGNMENT_AST_NODE()
        node.lvalue = left
        node.rvalue = jayko_instance.expr(4)
        return node
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

class U8_TOKEN:
    def __init__(self):
        self.type = "U8_TOKEN"
        self.value = "u8"
    def __repr__(self):
        return f"TokenType = {self.type}"

class I32_TOKEN:
    def __init__(self):
        self.type = "I32_TOKEN"
        self.value = "i32"
    def __repr__(self):
        return f"TokenType = {self.type}"

class STR_TOKEN:
    def __init__(self):
        self.type = "STR_TOKEN"
        self.value = "str" 
    def __repr__(self):
        return f"TokenType = {self.type}"

class CHAR_TOKEN:
    def __init__(self):
        self.type = "CHAR_TOKEN"
        self.value = "char" 
    def __repr__(self):
        return f"TokenType = {self.type}"

class DOT_TOKEN:
    def __init__(self):
        self.type = "DOT_TOKEN"
        self.lbp = 100 
    def led(self, left, jayko_instance):
        method_token = jayko_instance.expect("IDENTIFIER_TOKEN")
        print("[dot_token.led() method_token = {method_token}")
        method_token = method_token.value

        jayko_instance.expect("LPAREN_TOKEN")
        arg_expr = jayko_instance.expr()
        print(f"[dot_token.led() arg_expr = {arg_expr}")
        jayko_instance.expect("RPAREN_TOKEN")

        node = DA_APPEND_AST_NODE()
        node.target = left              # kind of awkward becuase we eventually need to add error checking for like (1+2).append()
        node.value = arg_expr
        node.target_type = jayko_instance.symbol_table[node.target.value]   # i can't really tell if this only works for one case or what the edge cases even are for it.
        print(f"[dot token led] node.target = {node.target}")
        print(f"[dot token led] node.value = {node.value}")
        print(f"[dot token led] node.target_type = {node.target_type}")
        return node
    def __repr__(self):
        return f"TokenType = {self.type}"

class STRING_LITERAL_TOKEN:
    def __init__(self):
        self.type = "STRING_LITERAL_TOKEN"
        self.lbp = 0 # no idea what it should actually be, so just picking the same as the other literals
        self.value = None
    def nud(self):
        node = STRING_LITERAL_AST_NODE()
        node.value = self.value
        node.value_type = "str"
        return node
    def __repr__(self):
        return f"TokenType = {self.type} value = {self.value}"

class CHAR_LITERAL_TOKEN:
    def __init__(self):
        self.type = "CHAR_LITERAL_TOKEN"
        self.lbp = 0 # no idea what it should actually be, so just picking the same as the other literals
        self.value = None
    def nud(self):
        node = STRING_LITERAL_AST_NODE()
        node.value = self.value
        node.value_type = "char"
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

class LPAREN_TOKEN:
    def __init__(self,):
        self.type = "LPAREN_TOKEN"
        #parse inside parenthesis
    def nud(self, jayko_instance):
        expr_node = jayko_instance.expr(0)
        jayko_instance.expect("RPAREN_TOKEN")
        return expr_node

    def __repr__(self):
        return f"TokenType = {self.type}"

class RPAREN_TOKEN:
    def __init__(self):
        self.type = "RPAREN_TOKEN"
        self.lbp = 0
    def __repr__(self):
        return f"TokenType = {self.type}"

class COLON_TOKEN:
    def __init__(self):
        self.type = "COLON_TOKEN"
    def __repr__(self):
        return f"TokenType = {self.type}"

class LSQUARE_TOKEN:
    def __init__(self):
        self.type = "LSQUARE_TOKEN"
        self.lbp = 100
    def nud(self, jayko_instance):
        nx = jayko_instance.peek_tokens()
        if nx.type == "RSQUARE_TOKEN":
            jayko_instance.advance_tokens() # consume ]
            return EMPTY_ARRAY_LITERAL_AST_NODE()
        raise SyntaxError("non-empty array literals not yet supported")

    def led(self, left, jayko_instance):
        node = DA_INDEX_AST_NODE()
        node.target = left
        print(f"[lsquare_token] node.target={node.target}")
        node.index = jayko_instance.expr()
        jayko_instance.expect("RSQUARE_TOKEN")
        return node
    def __repr__(self):
        return f"TokenType = {self.type}"

class RSQUARE_TOKEN:
    def __init__(self):
        self.type = "RSQUARE_TOKEN"
        self.lbp = 0
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

class NEQ_TOKEN:
    def __init__(self):
        self.type = "NEQ_TOKEN"
        self.lbp = 5
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)

        equality_node = NEQ_AST_NODE()
        equality_node.lvalue = left
        equality_node.rvalue = right
        return equality_node
        
    def __repr__(self):
        return f"TokenType != {self.type}"

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
    

class GEQ_TOKEN:
    def __init__(self):
        self.type = "GEQ_TOKEN"
        self.lbp = 6
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)

        geq_node = GEQ_AST_NODE()
        geq_node.lvalue = left
        geq_node.rvalue = right
        return geq_node
        
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
        self.unary_lbp = 50
    def nud(self, jayko_instance):
        right = jayko_instance.expr(self.unary_lbp)
        node = SUB_UNARY_AST_NODE()
        node.value = right
        return node
    def led(self, left, jayko_instance):
        right = jayko_instance.expr(self.lbp)
        node = SUB_AST_NODE() 
        node.lvalue = left
        node.rvalue = right
        return node
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
