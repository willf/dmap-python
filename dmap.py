# perhaps this will get bigger...
class Frame(object):
    pass


# is it a class?
def is_class(x):
    return isinstance(x, type)


# is it an instance? cf. insstance(x,y)
def is_instance(x):
    if isinstance(x, type):
        return 0
    else:
        return 1

# what is this class it a subclass of?
# x.__bases__

# what is this an instance of?
# type(x)

# what are the attributes ... ???
# instance -- x.__dict__ has instance attributes + values
# class    -- x.__dict__ has class attributes + values??


def attribute_value(obj, attribute):
    for abst in all_abstractions(obj):
        val = None
        try:
            val = abst.__dict__.get(attribute, None)
        except AttributeError:
            pass
        if val is not None:
            return val
    return None

# what are the methods?
# dir(x)


# not quite right ...
def methods_of(parent):
    return filter(None, dict(parent.__dict__).itervalues())

# is this an instance of that?
# isinstance(x,y)

# is this a subclass of that?
# issubclass(child,parent)

# what is the name of this class?
# x.__name__


def name(x):
    name = x
    try:
        name = x.__name__
    finally:
        return name

# what is the class that has this name?
# either a variable or eval('name')
# eval looks name up in globals ...


def set_name(x, name):
    if is_instance(x):
        x.__name__ = name


# is this one of those?
def isa(child, parent):
    # print "isa:",child," one of these ",parent
    if (child == parent):
        return 1
    elif is_class(parent) and isinstance(child, parent):
        return 1
    elif is_class(child) and is_class(parent) and issubclass(child, parent):
        return 1
    else:
        return 0


# what are the (all of) the parents of this object?
def parents(x):
    if is_class(x):
        return list(x.__bases__)
    else:
        return [x.__class__]


def allparents(x):
    if is_class(x):
        return list(x.__mro__)
    else:
        return list(type(x).__mro__)


def all_abstractions(x):
    if isinstance(x, Description):
        return all_abstractions(x.base)
    elif is_class(x):
        return list(x.__mro__)
    else:
        return [x] + list(type(x).__mro__)

# what are the subclasses of this class?
# ??? -- everything is in globals()


def subclasses_of(parent):
    return filter(
        lambda x: is_class(x) and x != parent and issubclass(x, parent),
        globals().itervalues())

# what are the instances of this class?
# ??? -- everything is in globals()


def instances_of(parent):
    return filter(lambda x: isinstance(x, parent), globals().itervalues())

# constraints ...
# what are the constraints on this attribute?
# ???

# default values, instance variables, etc.

# facets ??


def is_attribute_specifier(x):
    return type(x) == tuple


def attribute_specifier(x):
    return x[0]


def make_attribute_specifier(x):
    return (x, )


class Feature(object):
    """
    Feature:

    Attributes:
    attribute:     --
    value:     --
    """

    def __init__(self, attribute=None, value=None):
        self.__attribute = attribute
        self.__value = value
        # don't worry about descriptions that are featureless
        if isinstance(value, Description) and value.features == []:
            self.__value = value.base

    # accessors for Feature
    def get_attribute(self):
        return self.__attribute

    def set_attribute(self, attribute):
        self.__attribute = attribute

    attribute = property(get_attribute, set_attribute)

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    value = property(get_value, set_value)

    def __repr__(self):
        return '<Feature: ' + repr(self.attribute) + ':' + repr(
            self.value) + '>'


class Description(object):
    """
    Description:

    Attributes:
    base:     --
    features:     --
    """

    def __init__(self, base=None, features=list()):
        self.__base = base
        self.__features = list(features)  # hmm...

    # accessors for Description
    def get_base(self):
        return self.__base

    def set_base(self, base):
        self.__base = base

    base = property(get_base, set_base)

    def get_features(self):
        return self.__features

    def set_features(self, features):
        self.__features = features

    features = property(get_features, set_features)

    def all_abstractions(self):
        return all_abstractions(self.base)

    def __repr__(self):
        return '<Description: ' + repr(self.base) + ' ' + repr(
            self.features) + '>'


class Prediction(object):
    """
    Prediction:

    Attributes:
    base:     --
    pattern:     --
    start:     --
    next:     --
    description:     --
    """

    def __init__(self,
                 base=None,
                 pattern=None,
                 start=None,
                 next=None,
                 features=list()):
        self.__base = base
        self.__pattern = pattern
        self.__start = start
        self.__next = next
        self.__features = list(features)  # hmm...

    # accessors for Prediction
    def get_base(self):
        return self.__base

    def set_base(self, base):
        self.__base = base

    base = property(get_base, set_base)

    def get_pattern(self):
        return self.__pattern

    def set_pattern(self, pattern):
        self.__pattern = pattern

    pattern = property(get_pattern, set_pattern)

    def get_start(self):
        return self.__start

    def set_start(self, start):
        self.__start = start

    start = property(get_start, set_start)

    def get_next(self):
        return self.__next

    def set_next(self, next):
        self.__next = next

    next = property(get_next, set_next)

    def get_features(self):
        return self.__features

    def set_features(self, features):
        self.__features = features

    features = property(get_features, set_features)

    def target(self):
        spec = self.pattern[0]
        if is_attribute_specifier(spec):
            base = self.base
            attribute = attribute_specifier(spec)
            value = attribute_value(base, attribute)
            if (attribute is None):
                error("Not an attribute")
            else:
                return value
        else:
            return spec


class DMAP(object):
    """
    DMAP:

    Attributes:
    anytime_predictions:     --
    dynamic_predictions:     --
    position:     --
    call_backs:     --
    seen:     --
    complete:     --
    """

    def __init__(self):
        self.__anytime_predictions = {}
        self.__dynamic_predictions = {}
        self.__position = 0
        self.__call_backs = {}
        self.__seen = list()
        self.__complete = list()

    # accessors for DMAP
    def get_anytime_predictions(self):
        return self.__anytime_predictions

    def set_anytime_predictions(self, anytime_predictions):
        self.__anytime_predictions = anytime_predictions

    anytime_predictions = property(get_anytime_predictions,
                                   set_anytime_predictions)

    def get_dynamic_predictions(self):
        return self.__dynamic_predictions

    def set_dynamic_predictions(self, dynamic_predictions):
        self.__dynamic_predictions = dynamic_predictions

    dynamic_predictions = property(get_dynamic_predictions,
                                   set_dynamic_predictions)

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    position = property(get_position, set_position)

    def get_call_backs(self):
        return self.__call_backs

    def set_call_backs(self, call_backs):
        self.__call_backs = call_backs

    call_backs = property(get_call_backs, set_call_backs)

    def add_call_back(self, klass, procedure):
        cbs = self.call_backs.get(klass, [])
        if procedure in cbs:
            cbs.remove(procedure)
        self.call_backs[klass] = cbs + [procedure]

    def get_seen(self):
        return self.__seen

    def set_seen(self, seen):
        self.__seen = seen

    seen = property(get_seen, set_seen)

    def get_complete(self):
        return self.__complete

    def set_complete(self, complete):
        self.__complete = complete

    complete = property(get_complete, set_complete)

    def clear(self, anytime=0, call_backs=0):
        self.position = 0
        self.seen = list()
        self.complete = list()
        self.dynamic_predictions = {}
        if (anytime == 1):
            self.anytime_predictions = {}
        if (call_backs == 1):
            self.call_backs = {}

    def parse(self, sentence):
        for word in sentence:
            self.position = self.position + 1
            self.reference(word, self.position, self.position)

    def reference(self, item, start, end):
        for abstraction in all_abstractions(item):
            for prediction in self.anytime_predictions.get(abstraction,
                                                           list()):
                self.advance(prediction, item, start, end)
            for prediction in self.dynamic_predictions.get(abstraction,
                                                           list()):
                self.advance(prediction, item, start, end)
            for callback in self.call_backs.get(abstraction, list()):
                callback(item, start, end)

    def advance(self, prediction, item, start, end):
        if (prediction.next is None) or (prediction.next == start):
            # intialize prediction values
            base = prediction.base
            pattern = prediction.pattern[1:]
            start = start
            if (prediction.start is not None):
                start = prediction.start
            features = self.extend(prediction, item)
            # reference or create new
            if (pattern == []):
                self.reference(self.find(base, features), start, end)
            else:
                self.index_dynamic(Prediction(base, pattern, start, (
                    self.position + 1), features))

    def find(self, base, features):
        return Description(base, features)

    def extend(self, prediction, item):
        specialization = prediction.pattern[0]
        if is_attribute_specifier(specialization):
            itemis = item
            if isinstance(itemis, Description):
                itemis = itemis.base
            if isa(prediction.target(), itemis):
                return features
            else:
                fea = Feature(attribute_specifier(specialization), item)
                prediction.features.append(fea)
                return prediction.features
        else:
            return prediction.features

    def associate(self, base, pattern):
        if base == pattern[0]:
            pass
        else:
            prediction = Prediction(base=base, pattern=pattern)
            self.index_anytime(prediction)

    def index_anytime(self, prediction):
        target = prediction.target()
        predictions = self.anytime_predictions.get(target, list())
        predictions.append(prediction)
        self.anytime_predictions[target] = predictions

    def index_dynamic(self, prediction):
        target = prediction.target()
        predictions = self.dynamic_predictions.get(target, list())
        predictions.append(prediction)
        self.dynamic_predictions[target] = predictions


if __name__ == '__main__':

    class Human(Frame):
        pass

    class FHuman(Human):
        pass

    class MHuman(Human):
        pass

    class Action(Frame):
        pass

    class Loves(Action):
        actor = Human
        object = Human

    class Believes(Action):
        actor = Human
        object = Action

    class John(MHuman):
        pass

    class Mary(FHuman):
        pass

    p = DMAP()

    def reference_printer(f, s, e):
        print("Referencing", name(f.base), "from", s, "to", e)

    p.add_call_back(Frame, reference_printer)

    p.associate(John, ["John"])
    p.associate(Mary, ["Mary"])
    p.associate(Loves, [("actor", ), "loves", ("object", )])
    p.associate(Believes, [("actor", ), 'believes', 'that', ("object", )])

    p.parse('Mary believes that John believes that John loves Mary'.split(' '))
