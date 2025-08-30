# jayko-core
Custom built general purpose programming language with a hand written and parser.  The compilation process carries on in the following way: When you write a `jayko` program, the text file with the source code you wrote is treated as input to `jayko.py`.  `jayko.py` contains the tokenizer and parser.  Tokenization is then called on the source code.  This is the act of taking the raw source code and determining how the characters form meaningful units.  It is what lets us know that `let` is not a 

The strategy I implemented for parsing comes from Vaughn Pratt's [Top Down Operator Precedence](https://dl.acm.org/doi/10.1145/512927.512931).

# WARNING:
Anything could change in this repository at any time.  

## Goals of the Project: 
Over time, I want `jayko` to become useful to me as a tool for serious software development. To achieve this there are many things that still need to be done.  
- Implement dynamic array for generic data types

- Runtime cheks for dynamic array

- Functions

- Read from `stdin`

- HashMap implementation for generic data types.

- Contextualize code generation so that mulitple definitions of custom data types aren't added to the output C file.

In addition there are several types of programs I want to write to show the langauge can solve real problems. 
-  BrainFuck interpreter
-  Rule 110
-  JSON Parser


### Declaring variables 
To declare variables in jayko we use a rust-like syntax with the `let` keyword. `jayko` presently supports `

`let my_variable: u8 = 69;`

`let my_integer: i32 = 3141592;`

`let ch: char = 'c';`

`let alot_of_chars: str = "Hello from Jayko!";`

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


