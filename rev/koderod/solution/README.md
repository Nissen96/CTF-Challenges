# Writeup

This challenge is meant to be solved through call graph analysis.

As mentioned in the challenge description, the binary doesn't run at all. Opening it with a disassembler/decompiler, we find lots of seemingly randomly named functions, calling each other at random. Notice, there is a `start` and `end` function, and also one matching the flag format, `DDC`.

This might hint at the function names being what's important - you need to find the right path through the binary that gets to the `end` function, and the names of the functions called along the way will spell out the flag. Most functions branch out through multiple paths, so it is simplest to start from the `end`. Checking function references, this is only called by one function, which itself is just called by one, etc.

There are a few ways of getting the call stack leading to the end.

**Method 1: Automated**

We create a small script that runs through the output of `objdump -d koderod` and finds all (CALLER, CALLED) function pairs. Starting from the one with `CALLED=end`, we note down the `CALLER`, then find the `CALLER` of that etc. until we reach the start. An example script can be found in [solve.py](solve.py).

**Method 2: Visual Call Graph**

Continuing instead with the decompiler, you can visualize the call graph for a function.
Starting at the `end` function, this call graph will show the entire path of calls made, that ends up in this.

In Ghidra for instance, this is done by choosing "Display Function Call Trees" in the top graph.
This gives you a view of the incoming and outgoing calls to this function
In the incoming calls, you see which function called this one and can right-click and choose "Expand Nodes to Depth Limit" until reaching the first, `DDC{`.
Then write the function names down from bottom to top and you have the flag.


## Flag

`DDC{th3_c4ll_gr4ph_w1ll_b3_y0ur_gu1d3}`
