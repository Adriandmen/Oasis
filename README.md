# Oasis

Oasis is a **stack-based** language specialized in sequences. Not only as in the commands, but also as in how it calculates the sequences. With smart memory usage and memoization, it can calculate several sequences within seconds of time, without getting a recursion error or memory overflow.

### How does a program look like?

Due to it's nature, you can only make a _niladic_ program (which takes no argument), or a _monadic_ program (which takes 1 argument). This might be changed in the future, because it's quite restricted at the moment. Let's see how the actual code looks like:

    [code][predefined base cases]

First, the predefined base cases are taken off the actual code. These are used for the starting values for a sequence. For example, the code:

    bc+10

stands for:

    a(n) = bc+
    a(0) = 0
    a(1) = 1

The explanation for the code `bc+`:

    b    # Calculates a(n - 1)
     c   # Calculates a(n - 2)
      +  # Adds them up

You probably already have guessed it :P. This calculates the Fibonacci sequence. [It calculates `n = 1000` in a split second](http://oasis.tryitonline.net/#code=YmMrMTA&input=&args=MTAwMA+LXQ).

### Where is the implicit input?

Instead of the implicit input, this calculates the previous term of the sequence for the first time it's requested and `n - 2` for the second time it's requested, et cetera. This depends on the arity of a command. For example, if `+` was called on an empty stack, it would first use `a(n - 1)` and since the second time it's called on an empty stack, it uses `a(n - 2)`.

### Exercise

All commands will be stored in the file [`info.txt`](https://github.com/Adriandmen/Oasis/blob/master/info.txt). Using this and the documentation above, it's possible to golf the above Fibonacci calculator to _2 bytes_. 

### Note

Some thing are important when using Oasis:

 - This language is fairly new, so commands can be changed without prior notice.
 - Rather than input on STDIN, Oasis uses the command line arguments for input.
