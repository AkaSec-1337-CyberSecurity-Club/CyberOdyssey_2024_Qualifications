# easy license

###### crack a license for jvne

well this was an easy challenge, I dont know  why ppl did not solve it.

Since its .net,open the executable file in DnSpy, a decompiler for .net in windows.

the license check :
1. the license should be 17 character long. 8 character and '-' and 8 characters
2. the checker split the input by '-', then check each part with a different function.
3. Use Z3 to crack each part.
solve.py has the z3 code that gives the license.