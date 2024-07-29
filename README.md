# ġħeruq
_Ġħeruq_ /ɛːrʊʔ/ is a simple tool for autmated root detection for Maltese, with checks against the Hans Wehr's _A Dictionary of Modern Written Arabic_ for potential cognate root matches if the sqlite3 database file is found locally.

The only intent is to work out roots with some level of reliability. Comparisons to Arabic serve as an additional check of accuracy, as a Maltese root of Semitic origin which does _not_ have a corresponding Arabic root may be either mistakenly identified as semitic, mistakenly parsed for binyan patterns or mimmation, or otherwise erroneous.

This repository does **not** include a copy of the Hans Wehr database file. You will need to find this elsewhere, such as on GitHub.

See the [issues page](https://github.com/patkaiist/gheruq/issues) for a list of known problems.

## quick start

```bash
git clone https://github.com/patkaiist/gheruq.git
cd gheruq && python cli.py
```

Then hit ENTER to use a random pre-coded example word.

## features

The current version handles most Maltese words of Semitic origin. This includes handling of prefixes (e.g. _m-_, _t-_, _n-_), infixes (_-t-_) and some cases of _-in_ plurals. Nisba suffixes are not fully handled, especially in cases such as _waħdanija_/ وحدانية, but are on the to-do list.

Non-Semitic words will also often work, providing the root as given in Ġabra, were it to occur, but will Obviously not return Arabic results.

## examples

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

## command line app

If you don't feel like importing into python, you can directly run the `cli.py` app. It takes as an input the Maltese word, and then displays everything else that you might need to know about the root, like so:

```python
Type 'help' for additional information. Leave blank for a random example.

segments
f e t t ie ħ i

likely Maltese root
f-t-ħ

alignment
f   e   t   t   ie  ħ   i
1   0   1   2   0   1   0

possible Arabic roots

فطح
 1 faṭaḥa a (faṭḥ) and <b>II</b> to spread out, make broad and flat, flatten ( s.th.)
 2 afṭaḥ2 and  mufaṭṭaḥ broad-headed, broad-nosed

فتح
 1 fataḥa a (fatḥ) to open ( s.th.); to turn on ( a faucet); to switch on, turn on ( an appar
 2 opening; introduction, commencement, beginning │   opening of a credit, presentation
 3 the vowel point a (gram.)
 4 futḥa pl.  futaḥ, -āt opening, aperture, breach, gap, hole; sluice
 5 mufattaḥ appetizing; (pl. -āt) aperitif

فتخ
 1 iftikār pride, vainglory, boasting, bragging
 2 muftakir proud, vainglorious, boastful, bragging; outstanding, excellent, first-rate, perfect,

>
```

For additional information on the numerical values under alignment, you can type `help` as the word, and see something like this:

```python
> help

alignment key
1 - primary root radical
2 - repeated radical
3 - non-root affix
4 - weak root radical
0 - non-root vowel


>
```

To quit, you can type `q`, `quit`, `quit()`, `exit`, or just CTRL-C force quit the script. It will otherwise always give you the `>` prompt to check more words.

If you type `clear` as the word it will clear the screen, and hitting ENTER without any word will randomly choose from around a dozen pre-chosen words.
