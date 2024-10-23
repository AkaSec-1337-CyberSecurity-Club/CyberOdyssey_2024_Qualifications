# Pengolius

###### a semi-polymorphic virus


This challenge was basically a virus, that infect **ELF x86_64** binaries.

It starts by checking if strace is being run on the virus, or if there is a debugger attached to it (Running ptrace on it self).

If the conditions are met, The virus decrypt Its body, and maps it to an executable region, It also initilize some variable that will be used in the infection routine , then jumps to the mapped region.

the infection routine is as follow :

1. Initialize stack to hold variables.
2. Open the /tmp/chall folder, check each entry if Its a file.
3. mmap the file, check if Its an executable and a valid x86_64 (by checking the signature in the header).
4. search for the PT_LOAD that contain the text code (PT_LOAD with read eand exec permissions).
5. check if there is enough 0 paddings in the end of the segments to hold the virus.
as for this part i didnt use any famous infection methods, this one wont work on all binaries.
6. generate a new key to encrypt the body with, also chose a random decryptor (i only had 3 decryptors hh).
7. read the signature from **/var/.x1ee9w** . if the file doesnt exist it creates it .
8. for the flag, based on the signature, if there has been 42 infection, It stars decrypting the flag,based on 0x1337 + 42, as the key.
   each infection decrypt one character of the flag and place It after the number next to the version **Pengolius version 1.0**.
   ```c
    Pengolius version 1.0 made with <3 by pengu - 1360
    Pengolius version 1.1 made with <3 by pengu - 1361
    Pengolius version 1.7 made with <3 by pengu - 1362
    Pengolius version 1.5 made with <3 by pengu - 1363
    Pengolius version 1._ made with <3 by pengu - 1364
    ```
9. patch the binary with the decryptor, the new key, and write it to the empty padding at the end of the text segment.
10. basically if you know how the routine works you could have run this bash script and get the flag : 
    ```c
    rm /var/.x1ee9w
    mkdir /tmp/chall
    for i in {1..100};do cp /bin/ls /tmp/chall/ls$i; done
    ./pengolius
    for i in {1..100}; do strings /tmp/chall/./ls$i | grep "Pengo"; done | sort -t '-' -k2
    ```
