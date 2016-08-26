# dmap-python
The DMAP conceptual parser in Python

Will Fitzgerald

Note: This write-up is based directly on Chris Riesbeck’s write-up of DMAP-Lite, a version of DMAP written in Common Lisp.

## The Basic Idea

There is one central idea in DMAP. Start with a memory, i.e., an organized body of general and specific conceptual knowledge. For DMAPython, we assume this is represented as Python classes and instances, augmented with certain introspection capabilities.

Next, associate various linguistic patterns with the concepts in memory to which they refer. For example, the English phrase “interest rates” can refer to the concept (class) InterestRates, while a phrase of the form “someone says something” can refer to the concept (class) CommunicationEvent. A phrase may be associated with more than one concept and vice versa.

Finally, analyze text with matching the linguistic patterns to the text to find what concepts in memory are being referred to. There’s a standard DMAP algorithm that does this in a fairly efficient, incremental, parallel manner. Other algorithms no doubt exist. The critical point is: Language understanding should be viewed primarily as a semantic recognition process rather than a syntactic construction process.  That is, we’re focused on looking for concepts in memory, not building syntax trees.

## Direct Memory Access Parsing

DMAP assumes a memory of concepts, events, dialog structures, etc. already exists. When DMAP interprets a language stream, it looks for and reports references to memory structures. For example, reading “interest rates” references InterestRates, and “interest rates are rising” might reference an instance of InterestRatesRising.

If InterestRates is a Python class, DMAPython, connecting it to “interest rates” is easy:

p.associate(InterestRates,[“interest”,”rates”])

where “p” is an instance of a DMAP parser. This attaches the concept sequence [“interest”,”rates”] to the base concept InterestRates.

Getting DMAPython to understand “interest rates are rising” is only slightly more complicated. Appropriately enough, most of the work comes in defining the memory structures. Let’s assume the following Python declararations:

```Python
class Variable(Framee):
  pass

class Change(Frame):
  pass

class Increase(Change):
  pass

class Event(Frame):
  pass

class InterestRates(Variable):
  pass

class ChangeEvent(Event):
  variable = Variable
  change = Change
```
When DMAPython reads “interest rates are rising,” we’d like to say that it saw a ChangeEvent with the value of the variable attribute set to InterestRates and the value of the change attribute set to Increase. This can be accomplished with:

```Python
p.associate(Increase,['rising'])
p.associate(ChangeEvent, [('variable'),'are',('change')])
```

Note that the concept sequence for ChangeEvent has tuples in addition to strings. These are called attribute specifiers or role specifiers. A role specifier is satisfied if its filler is an instance or subclass of that role in the base concept is referenced. For example, InterestRates satisfied the role specifier (“variable”) in the above concept sequence because the filler of the role in a ChangeEvent is Variable and InterestRates is a subclass of Variable.

## “Earth to DMAP”: Connecting DMAP to another program

A program can tell DMAP Python to parse a sentence simply by calling `p.parse(sentence)`, where sentence is a sequence of words. For example, `p.parse('milton friedman says interest rates will rise'.split())`. The parse method will return a list of all concepts which are reference by the entire sentence.

Call-backs can also be defined with:

```Python
p.defineCallback(class, function)
```
so that whenever something which is an instance, subclass, or the class itself is reference, the function is called. The parameters are the concept, and a start and end integer (indices of the position in the text where the sequence began and ended). For example, to print out whenever an object is reference, the following procedure can be defined:

```Python
def printReferenced(object, start, end):
  print “Saw” , object, “from”, start, “to”,end
```

It can be added to the parser with `p.defineCallback(object,printReferenced)`

## Keeping an open mind: DMAP and ambiguity

DMAP will reference contradictory concepts when ambiguities are involved. DMAP does not resolve contradictions directly. It lets things play themselves out. For example, “check” has many senses, but only the ItemizeBill sense completes the sequence begun by “John paid the …” and thereby leads to an event reference. DMAP references all the senses of “check” but only the ItemizedBill sense leads to anything.

So, just because DMAP references something doesn’t meant that it is really used. It is best to put callbacks on the “big” structures, such as events and causal forms (except for debugging, of course).

## Thanks for the memory: Connecting DMAP to the Python Class system

The introspection features of the Python class system need to be extended with four relatively simple methods—well, really three simple methods, and one relatively difficult one. These are:

| Method | Arguments | Return value |
| ------ | --------- | ------------ |
|`attribute_value` | _concept_,_attribute_ | The value of attribute for concept (where “concept” is an instance or class). This is essentially concept.attribute |
|`all_abstractions` | _concept_ | All of the abstractions of concept, including itself. This is essentially the concept plus its “mro”.|
| `isa` | _child_, _parent_ | Is the parent equal to some abstraction of child (including, perhaps, equal to the parent? |
| `find` | _concept_, _attribute/values_ | A specialization of the concept that has these attributes and values.  This is a bit tricky to do in Python. | 


## Implementation Concepts

Prediction structures are the basic data structure in DMAP. They link a concept sequence with a base concept. In addition, predictions represent partially recognized sequences, and have:

-	a base sequence,
-	a sequence of items yet to be seen,
-	a position in the text where the sequence began,
-	a position in the text where the next item is expected,
-	a list of attributes/value tuples that have been seen so far (see below).

## Target practice

The target of a prediction is the concept pointed to by the first item in the sequence. The target might be a word, e.g., “interest” in the sequence `['interest','rates']`, or a class, for example, Variable if the sequence is `[('variable') will ('change')]`. When DMAP sees an instance or subclass of a target of a prediction, it advances  the prediction. Advancing means looking for the next item in the sequence, as well as maintaining other bookkeeping information.

DMAP does not actually change a prediction when it advances it. Instead it clones the prediction, updating the sequence and next position appropriately. This is necessary because the original prediction may be advanced more than once by different senses of the text.

## Features of greatness

If the input item is the same as the target of the prediction, then advancing the prediction is just as described. However, the input might be more specific than the target. For example, the target may be Variable, but the input is InterestRates. Therefore, if the target specifier is a attribute specifier (e.g., `('variable')`, then DMAP adds the feature—a pairing of attribute, input—to a list of features stored in the prediction.

## All good things come to an end

When the last item of a sequence has been seen, DMAP is ready to reference an instance of the base concept. DMAP calls `find(base,attribute/values)` to  determine what this should be, where _base_ is the base concept of the prediction, and _attribute/values_ are the attribute/value pairs collected during prediction advancement.
