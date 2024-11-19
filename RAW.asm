// Computes the sum 1 + 2 + ... + 10 and puts the result in R0.

// Initialize variables
@i
M=0
@sum
M=0

// Loop to calculate the sum
(LOOP)
    @i
    D=M
    @10
    D=D-A
    @end
    D;JGT   // If i > 10, jump to the end of the program
    
    @i
    D=M
    @sum
    M=D+M   // sum = sum + i
    
    @i
    M=M+1   // Increment i
    @loop
    0;JMP   // Jump back to the beginning of the loop

// End of program
(END)
    @sum
    D=M     // Move the value of sum to D register
    @0
    M=D     // Store the sum in R0
    
    @end
    0;JMP   // Infinite loop to halt the program
