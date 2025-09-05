# jayko-core
Custom built general purpose programming language with a hand written tokenizer and parser.  The compilation process carries on in the following way: When you write a `jayko` program, the text file with the source code you wrote is treated as input to `jayko.py`.  `jayko.py` contains the tokenizer and parser.  Tokenization is then called on the source code.  This is the act of taking the raw source code and determining how the characters form meaningful units.  It is what lets us know that `let` is not an identifier, but a keyword for declaring variables.  Tokens make up the meaningful units of what the source code are, contains useful error information (such as what line number the token exists on in the source file, and append those tokens to a list.  Tokens can take up more than one character, so for certain tokens, a simple lookahead function is implemented, in order to tell the difference between, for example, `==` and `=`.

Parsing operates on the token stream that the tokenizer output.  The strategy I implemented for parsing comes from Vaughn Pratt's [Top Down Operator Precedence](https://dl.acm.org/doi/10.1145/512927.512931). I don't recommend reading the paper for a practical understanding of this topic, I used [this tutorial by Fredirk Lundh](https://web.archive.org/web/20150228044653/http://effbot.org/zone/simple-top-down-parsing.htm) from 2008.  Parsing takes place in the following way.  For statements, we hard code what the syntax should be, and use the Pratt method for parsing expressions. For example a `let` statement is `let <identifier>: <type_signature> = <expr>`.  Then you call the Pratt `expr()` function on the `<expr>` part. This employs a `nud()` and a `led()` function depending on if the operator is a prefix or an infix operator respectively.  I am not sure if making the distinction between statements and expressions is important to Pratt, or if it's possible to just have `nud` and `led` on every token.  Tha'ts how it works right now but it could change in the future. 

Parsing produces data structure called an Abstract Syntax Tree. Performing post order traversal (evaluating the deepest nodes first) on this tree ensures that expressions are evaluated in the order we set them to be. The concept is illustrated well in [Bob Nystrom's Crafting Interpreters](https://craftinginterpreters.com/representing-code.html).  

Finally, using the syntax tree, we emit (hopefully!) valid programs in C!

### Dependencies
`jayko` depends on `gcc`, `python3` (I use 3.8 but I'm sure other versions would work), and `clang-format`. 

# WARNING:
Anything could change in this repository at any time.

## Goals of the Project: 
Over time, I want `jayko` to become useful to me as a tool for serious software development. To achieve this there are many things that still need to be done.  
- Implement dynamic array for generic data types **(25-AUG-2025)**
- Runtime checks for dynamic array 
- Variable Scope
- Type Checking
- Functions  **(31-AUG-2025)**
- Read files from `stdin` **(1-SEP-2025)**.
- HashMap implementation for generic data types.
- Contextualize code generation so that mulitple definitions of custom data types aren't added to the output C file.
- Our own Virtual Machine to run the code from (although compiling to C is a time honoured tradition).  

In addition there are several types of programs I want to write to show the langauge can solve real problems. 
-  BrainFuck interpreter -- Completed on 28-Aug-2025
-  Rule 110 -- Completed on 28-Aug-2025
-  JSON Parser


### Declaring variables 
To declare variables in jayko we use a rust-like syntax with the `let` keyword. `jayko` presently supports `

`let my_variable: u8 = 69;`

`let my_integer: i32 = 3141592;`

`let ch: char = 'c'; // single quotes indicates a character`

`let alot_of_chars: str = "Hello from Jayko!"; // double quotes indicates a string`

### Binary operators supported
`+, -, *, ==, <, <=, >, >=, %`  Boolean operator `and` is supported.  `

### Printing
The print command is currently called `say`.  You can `say <string literal> | <identifier> | <expr>`.  I haven't yet implemented format specifiers like `%d` yet. Until that happens, you can get meaningful output by putting many `say` statements on the same line, like `say "hello "; say "world! "; say "i = "; say i;`.  

### Dynamic Array
There is also a dynamic array implementation for generic types.

`let xarr: i32[] = [];`

From here we support appending onto the array using `xarr.append(420);` .
You can also change the elements inside the array using the conventional methods. 
`xarr[0] =31;` should set the first element of xarr to 31.  

### Control Flow
`jayko` supports two types of control flow at present.  `loop <expr> { [statements] }` will loop as long as `<expr>` evaluates to true. `if <expr> {statements} else if { [statements] } else { [statements]}` provides branching. 
```
loop i < 3 {
    say i; 
    i = i + 1;
}
```
`jayko` supports if then else as follows

```
if x>5 and x< 10 {
    say "hello\n";
} else if x>=10 {
    say "bigger than 10\n";
} else {
    say "less than five\n";
}
```



### Declaring Functions
`jayko` functions are declared as follows
```
fn my_function(x: i32, y:i32) {
    return x+y;
}
```
Right now functions are only passed by value, which has a lot of limitations.  Support for pointer/array types is incoming.

### Reading files:
The built in `read_file(<path/to/filename>)` reads text into a string.  Example usage:
```
let source_code: str = read_file("source_code.c");
```


## Further  Reading
[Crafting Interpreters](https://craftinginterpreters.com/contents.html)
Definitely a good book from an implementation standpoint.


