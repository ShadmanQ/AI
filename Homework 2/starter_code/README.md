**

# HW2 CSCI 35000/761000

**

### What was completed:
Player_3.py can successfully use expectiminimax with alpha-beta pruning to reach 2048. The program uses a static evaluation function, taking into account the maximum value present in the board state along with the following heuristics:

 - Monotonicity
 - Smoothness
 - Number of free cells in the board state.


Each heuristic was also assigned a weight, these were given through mixture of trial and error and borrowing weights from [Mark Overlan's AI solver for 2048](https://github.com/ovolve/2048-AI). 

### Difficulties:
The biggest issues came down to:

 - The chance elements
 -  The static evaluation function 

I had figured out eventually through other literature that the chance element generation should go in the logic for the min half of minimax. From there it was figuring out the most reliable heuristic measures to use for the static evaluation. The most difficult aspect of it was deciding which ones would be the most useful + the easiest to implement, the three I went with give me reliable performance.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjE1MzQ1ODc3XX0=
-->