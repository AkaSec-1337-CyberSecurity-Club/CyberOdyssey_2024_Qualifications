# CTFtime

The challenge was fairly simple and cool at the same time, it was about the nitty-gritty detail that `URL()` method in javascript that ultimately gets used in the `fetch()` function (correct me if am wrong) removes the `\n` charachter, so you would bypass the checks using a payload like this: `/team..%0a/env/FLAG`.
