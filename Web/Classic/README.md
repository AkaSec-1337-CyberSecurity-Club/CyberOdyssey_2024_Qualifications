# Classic

This challenge had two steps to it:

## Getting The First RCE

The first step is to get an RCE in the php server (`notes`), this could be done by abusing the `file_put_contents()` function, specifically its `ftp://` url handling (read the function docs), here is a [writeup](https://github.com/dfyz/ctf-writeups/tree/master/hxp-2020/resonator) that explains the exploit more thoroughly.

## Getting The Second RCE

The Second step was about getting an RCE in the python server, and would be done through connecting to the **unsafely** opened uwsgi socket port, which as clearly documented would allow an attacker to get an RCE in your server, after that it's just about sending the appropriate packet to smuggle you're flag to your nearest webhook, you can use [this tool](https://github.com/vulhub/vulhub/blob/master/uwsgi/unacc/poc.py) to do so.
