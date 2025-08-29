###############################################################################
#   TYPE INFO 
#   The format is jayko's indicator, and then all the stuff we need to
#   translate it to C.
###############################################################################
TYPE_INFO = {
        "i32": {
            "c_type": "int",
            "printf": "%d",
            "size": 4,
            "category": "int",
            }, 
        "u8": {
            "c_type": "uint8_t",
            "printf": "%hhu",
            "size": 1,
            "category": "int",
            },
        "str": {
            "c_type": "char*",
            "printf": "%s",
            "size": None, # dynamic
            "category": "pointer",
            },
        "char": {
            "c_type": "char",
            "printf": "%c",
            "size": None, # dynamic
            "category": "pointer",
            }
}

###############################################################################
#  AST NODES DEFINITONS
###############################################################################
class LET_AST_NODE:
    def __init__(self):
        self.type = "LET_AST_NODE"
        self.lvalue = None                  # the variable name
        self.rvalue = None                  # the root of the subtree forming the expression to be stored in lvalue
        self.declared_type = None
    def code_gen(self, symbol_table):
        identifier = self.lvalue.code_gen(symbol_table)

        # base_type_table = {"u8": "uint8_t", "i32": "int"}
        base_type = self.declared_type["base"]
        print(f"[let_ast_node] base_type = {base_type}")
        print(f"[let_ast_node] self.rvalue = {self.rvalue}")

        c_type = TYPE_INFO[base_type]["c_type"]

        # if its a dynamic array like let arr: u8[] = [];
        if self.declared_type and self.declared_type["is_array"]:
            array_typename = f"Array_{base_type}"

            
            # typedef for this base (deals with the fact that we only want one u8 type array per
            # program, even though we may declare multiple u8 type arrays in our code
            # self.code_gen_context.require_array_typedef(base_type)

            # for empty arrays, initialize with {0}
            return f"\t{array_typename} {identifier} = {{0}};\n"
        # normal variable
        rhs = self.rvalue.code_gen(symbol_table)
        return f"\t{c_type} {identifier} = {rhs};\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type} value = {self.lvalue} "

# we absolutely need to incorporate the difference between a decaration and an assignemnt
class ASSIGNMENT_AST_NODE:
    def __init__(self):
        self.type = "ASSIGNMENT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        rhs = self.rvalue.code_gen(symbol_table)
        identifier = self.lvalue.code_gen(symbol_table)
        return f"\t {identifier } = {rhs};\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type} value = {self.lvalue} "

class IDENTIFIER_AST_NODE:
    def __init__(self):
        self.type = "IDENTIFIER_AST_NODE"
        self.value = None                                               # WE ONLY SUPPORT INTEGERS RN
        self.value_type = None
    def code_gen(self, symbol_table):
        return str(self.value)
     
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class INT_LITERAL_AST_NODE:
    def __init__(self):
        self.type = "INT_LITERAL_AST_NODE"
        self.value = None
        self.value_type = "i32"
        
    def code_gen(self, symbol_table):
        return str(self.value)
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class STRING_LITERAL_AST_NODE:
    def __init__(self):
        self.type = "STRING_LITERAL_AST_NODE"           
        self.value = None                               
    def code_gen(self, symbol_table):
        return str(self.value)
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class EQUALITY_AST_NODE:
    def __init__(self):
        self.type = "EQUALITY_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        print("Generating code for EQUALITY")
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} == {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class NEQ_AST_NODE:
    def __init__(self):
        self.type = "NEQ_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} != {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class LT_AST_NODE:
    def __init__(self):
        self.type = "LT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} < {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class GT_AST_NODE:
    def __init__(self):
        self.type = "GT_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} > {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class LEQ_AST_NODE:
    def __init__(self):
        self.type = "LEQ_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} <= {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class GEQ_AST_NODE:
    def __init__(self):
        self.type = "GEQ_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} >= {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class ADD_AST_NODE:
    def __init__(self):
        self.type = "ADD_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        print("Generating code for ADD")
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} + {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class SUB_AST_NODE:
    def __init__(self):
        self.type = "SUB_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} - {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class SUB_UNARY_AST_NODE:
    def __init__(self):
        self.type = "SUB_UNARY_NODE"
        self.value = None
    def code_gen(self, symbol_table):
        code = self.value.code_gen(symbol_table)
        return f"-{code}"

class MUL_AST_NODE:
    def __init__(self):
        self.type = "MUL_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        print("Generating code for MUL")
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} * {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class AND_AST_NODE:
    def __init__(self):
        self.type = "AND_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} && {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class MOD_AST_NODE:
    def __init__(self):
        self.type = "MOD_AST_NODE"
        self.lvalue = None
        self.rvalue = None
    def code_gen(self, symbol_table):
        print("Generating code for MOD")
        left_code = self.lvalue.code_gen(symbol_table)
        right_code = self.rvalue.code_gen(symbol_table)
        return f"({left_code} % {right_code})"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, lvalue = {self.lvalue}, rvalue = {self.rvalue}"

class SAY_AST_NODE:
    def __init__(self):
        self.type = "SAY_AST_NODE"
        self.value = None
        self.route = None                               # route is to dispatch to the correct code generation
    def code_gen(self, symbol_table):
        what_to_print = self.value.value                # this sucks but idk how to wire say to expr()

        if what_to_print in symbol_table:
            type_info = symbol_table[what_to_print]["base"]
        else:
            type_info = self.value.value_type
        format_specifier = TYPE_INFO[type_info]["printf"]
        return f"\tprintf(\"{format_specifier}\",{self.value.value});\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type}, value = {self.value}"

class BLOCK_AST_NODE:
    def __init__(self):
        self.type = "BLOCK_AST_NODE"
        self.statements = []
    def code_gen(self, symbol_table):
        buf = []
        for ast_node in self.statements:
            buf.append(f"{ast_node.code_gen(symbol_table)}")
        return "".join(buf)

    def __repr__(self):
        return f"AST_NODE type = {self.type}, with {len(self.statements)} statements in it"

class IF_AST_NODE:
    def __init__(self):
        self.type = "IF_AST_NODE"
        self.if_condition = None
        self.then_block = None
        self.else_block = None
    def code_gen(self, symbol_table):
        cond = self.if_condition.code_gen(symbol_table)
        then_block = self.then_block.code_gen(symbol_table)
        if self.else_block != None:
            else_block = self.else_block.code_gen(symbol_table)
            return f"\tif ( {cond} )\n \t{{ {then_block} \n \t}} else {{ \n \t {else_block} \t}}\n"

        return f"\tif ({cond}) \n \t{{ {then_block} }} "
    def __repr__(self):
        return f"AST_NODE type = {self.type}, with if_condition = {self.if_condition}, then_block = {self.then_block}, else_block = {self.else_block}"

class LOOP_AST_NODE:
    def __init__(self):
        self.type = "LOOP_AST_NODE"
        self.loop_condition = None 
        self.loop_block = None
    def code_gen(self, symbol_table):
        cond = self.loop_condition.code_gen(symbol_table)
        loop_block = self.loop_block.code_gen(symbol_table)
        return f"\twhile ( {cond})\n\t {{ {loop_block} }}\n "
    def __repr__(self):
        return f"AST_NODE type = {self.type}, with loop_condition = {self.loop_condition}, and loop_block = {self.loop_block}" 

class EMPTY_ARRAY_LITERAL_AST_NODE:
    def __init__(self):
        self.type = "EMPTY_ARRAY_LITERAL_AST_NODE"
    def code_gen(self, symbol_table):
        pass                # cant remember why it's this
    def __repr__(self):
        return f"AST_NODE type = {self.type}"

class DA_APPEND_AST_NODE:
    def __init__(self):
        self.type = "DA_APPEND_AST_NODE"
        self.target = None      # array
        self.value = None       # the value we want to append
        self.target_type = None
    def code_gen(self, symbol_table):
        arr = self.target.code_gen(symbol_table)
        val = self.value.code_gen(symbol_table)
        array_type = self.target_type["base"]
        return f"\tArray_{array_type}_append(&{arr}, {val});\n"
    def __repr__(self):
        return f"AST_NODE type = {self.type}"

class DA_INDEX_AST_NODE:
    def __init__(self):
        self.type = "DA_INDEX_AST_NODE"
        self.target = None                          # array
        self.target_type = None                     # type of the target
        self.index = None                           # index we want to index into
    def code_gen(self, symbol_table):
        # Point p4 = PointArray_get(&xs, 0);
        print(f"[da_index_ast_node], self.target_type = {self.target_type}")
        print(f"[da_index_ast_node], self.target = {self.target}")

        target_value = self.target.value
        arr = self.target.code_gen(symbol_table)
        idx = self.index.code_gen(symbol_table)
        if self.target.value in symbol_table:
            print("YES\n\n\n")
            print(f"symbol_table[target_value] = {symbol_table[target_value]}")
            if symbol_table[target_value]["base"] == "str":
                print("GENERATE NEW CODE HERE")

                return f"{arr}[{idx}]"

        return f"{arr}.items[{idx}]"
    def __repr__(self):
        return f"AST_NODE type = {self.type}"


class DA_INDEX_ASSIGN_AST_NODE:
    def __init__(self):
        self.type = "DA_INDEX_ASSIGN_AST_NODE"
        self.target = None          # array
        self.index = None           # the index
        self.target_type = None     # the type of the array
        self.value = None           # 
    
    def code_gen(self, symbol_table):
        arr = self.target.code_gen(symbol_table)
        idx = self.index.code_gen(symbol_table)
        val = self.value.code_gen(symbol_table)
        array_type = self.target_type["base"]
        return f"{arr}.items[idx] = {val};" 


#class METHOD_CALL_AST_NODE:
#    def __init__(self):
#        self.type = "METHOD_CALL_AST_NODE"
#        self.target = None
#        self.method = None
#        self.args = []
#    def code_gen(self, symbol_table):
#        target = self.target.code_gen(symbol_table)
#        arg_code = ", ".join(arg.code_gen(symbol_table) for arg in self.args)
#        return f"\tArray_u8_{self.method}(&{target}, {arg_code});\n"

