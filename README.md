# ġħeruq
_Ġħeruq_ /ɛːrʊʔ/ is a simple tool for autmated root detection for Maltese, with checks against the Hans Wehr's _A Dictionary of Modern Written Arabic_ for potential cognate root matches if the sqlite3 database file is found locally.

The only intent is to work out roots with some level of reliability. Comparisons to Arabic serve as an additional check of accuracy, as a Maltese root of Semitic origin which does _not_ have a corresponding Arabic root may be either mistakenly identified as semitic, mistakenly parsed for binyan patterns or mimmation, or otherwise erroneous.

This repository does not include a copy of the Hans Wehr database file. You will need to find this elsewhere on GitHub.

I put this program together after searching for something which served this purpose without success. There are still some issues to be solved and improvements to be made, but for most cases it is working as expected now.

## features

The current version handles most Maltese words of Semitic origin. This includes handling of prefixes (e.g. m-, t-, n-), infixes (-t-) and some cases of -in plurals. Nisba suffixes are not fully handles, especially in cases such as _waħdanija_/_وحدانية_, but are on the to-do list.

Non-Semitic words will also often work, providing the root as given in Ġabra, were it to occur, but will Obviously not return Arabic results.

## example

To use, import the functions contained in the `gheruq` package and create a new instance of `Gheruq()` with the target word. In this case, _qattieġħ_, "somebody who cuts".

```python
>>> from gheruq import *
>>> x = Gheruq("qattieġħ")
```

Using `segments` will return the orthographic form of the word as a list divided by underlying phonemic segments.

```python
>>> print(x.segments)
['q', 'a', 't', 't', 'ie', 'ġħ']
```

The Maltese root according to the conventions of Aquilina/Ġabra can be returned with `root`.

```python
>>> print(x.root)
q-t-ġħ
```

Cognate Arabic roots which occur in the Hans Wehr dictionary can be returned with `arabic`. Note that additional packages to ensure the correct shape and directionality are not included here, so the order of letters in your output may differ depending on your system.

```python
>>> print(x.arabic)
قطع
قتع
```

As another example, results with _twieġħed_, "to be promised":

```python
>>> y = Gheruq("twieġħed")
>>> print(y.segments)
['t', 'w', 'ie', 'ġħ', 'e', 'd']
>>> print(y.root)
w-ġħ-d
>>> print(y.arabic)
وعد
وغد
```

And _kittieb_, "writer":

```python
>>> z = Gheruq("kittieb")
>>> print(z.root)
k-t-b
>>> print(z.arabic)
كتب
```