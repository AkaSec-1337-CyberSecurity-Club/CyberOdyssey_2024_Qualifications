# [**Secure Library**](#)

## Description:
* I created the most secure library in the universe, try to get the secret flag from the library.

## Difficulty:
* Easy

## Objective:
The object of this challenge is to get the flag by reading the `flag.txt` file.

## Deployment:
```sh
docker build -t secure-library .
docker run -p 4041:4041 secure-library
```

## Solution:
The challenge introduces a vulnerability caused by the fact that file descriptors are not properly closed after being opened, leading to an FD leak. In Linux, open file descriptors can be accessed via the `/proc` filesystem, specifically through `/proc/self/fd/`, which holds symbolic links to all open file descriptors of the running process. When the program opens `flag.txt`, it leaves the file descriptor (which is FD 6 in this case) open, making it possible to bypass the program’s restrictions on reading the flag. By navigating to `/proc/self/fd/6`, you can directly access the content of `flag.txt` without triggering any of the content obfuscation logic in the program, allowing you to retrieve the flag.