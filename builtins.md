Pseudocode builtins
===================

The language provides following features for direct use:

Types
-----

- ``object``
    - the universal base type
    - all new types implicitly inherit from it
    - it provides the following special methods:
        - ``@str``
            - return a ``str`` of the form ``"$object of `type`@`id`$"``, `` `type` `` being the object's type and `` `id` `` being a unique identifier for the object
        - ``@bool: return true``
- ``str``
    - the type of strings
    - it provides following special methods
        - ``@construct``
            - returns an empty string
            - note constructions from other types are handled by that type via ``@str``
        - ``@str: return self``
        - ``@int``:
            - if ``self`` is a valid literal``int``, return it. Otherise, raise an Error
            - For this purpose, the ``-`` operator may also be present and will be applied
        - ``@real``:
            - if ``self`` is a valid constant ``real``, return it, otherwise return ``real(int(self))``
            - The ``-`` operator may be present and will be applied; ``inf`` is considered a valid literal float
        - ``@bool: return bool(self.length)``
        - ``@itemget int -> str:``
            - return the character at index (starting from 0) ``item``. Raise an error if ``item >= self.length or item < 0``
        - ``@itemset int ⬅ str``
            - assign the given character ``value`` to the given index ``item``. If ``item = self.length``, ``value`` is added to the end of the string. If ``item > self.length or item < 0``, raise an error.
        - ``@+other@deffor str``
            - return a concatation of ``self`` and ``other``
        - ``bool@=other@deffor str``
            - return ``true`` if``self`` is equal to ``other``
    - it provides the following normal methods:
        - ``upper() -> str``
            - return ``self`` replacing lower-case characters with their upper-case counterparts
        - ``lower() -> str``
            - return ``self`` replacing upper-case characters with their lower-case counterparts
        - ``find(char: str) -> int: return self.find(char, 0)``
        - ``find(char: str, start: int)  -> int``
            - return the index of the first occurence of ``char`` after ``start``
            - return ``-1`` if it can't be found
    - it provides the following attribute:
        - ``length: int``
            - the length of the string
- ``basenumber``:
    - the base type for ``int`` and ``real``
    - it provides the following special methods:
        - ``@str``
            - return the literal representation of ``self``
            - it does not contain any whitespace, regardless ofhow the number was deined
        - ``@real``
            - return the floating point equivalten of ``self``
        - ``@int``
            - return the integer equivalent of ``self``.
            - Floor toward negative infinity
        - ``@bool: return not self = 0``
        - ``@other+@deffor basenumber``
            - return the sum of ``self`` and ``other``
        - ``@other-@deffor basenumber``
            - subtract ``self`` from ``other`` and return the result
        - ``@other-@deffor void``
            - return ``self`` with opposite sign
        - ``@other+@deffor void: return self``
        - ``@other*@deffor basenumber``
            - multiply ``self`` and ``other`` and return the result
        - ``@/other@deffor basenumber``
            - divide ``self`` by ``other`` and return the result
            - if ``self`` or ``other`` are ``int``, floor the result toward negative infinity before returning it
        - ``@^other@deffor basenumber``
            - return ``self`` to the power of ``other``
        - ``bool@=other@deffor basenumber``
            - return ``true`` if ``self`` and ``other`` are equal in value, fasle otherwise
            - e.g. ``(42=42.0)=true``; ``(42=42)=true``; ``(42=42.1)=false``;
            ``42="42"`` not defined
        - ``bool@other>@deffor basenumber``
            - return ``true`` if ``other`` is greater in value than ``self``, ``flase`` otherwise
        - ``bool@other<@deffor basenumber``
            - return ``true`` if ``self`` is greater in value than ``other``, ``false`` otherwise
        - ``bool@other>=@deffor basenumber: return other>self or other=self``
        - ``bool@other<=@deffor basenumber: return other<self or other=self``
- ``int``
    - subclass of ``basenumber`` for integer avlues
    - its ``@construct`` returns ``0``
- ``real``, aliased by ``float``
    - subclass of ``basenumber`` for floating point values
    - its ``@construct`` return ``0.0``
    
- ``bool``
    - type for boolean values
    - its instances are the builtin constants ``true`` and ``false``
    - it provides following methods:
        - ``@other and@deffor bool``
            - return ``true`` if both ``self`` and ``other`` are ``true``, ``false`` otherwise
        - ``@other or@deffor bool``
            - return ``false`` if both ``self`` and ``other`` are ``false``, ``true`` otherwise
        - ``@other not@deffor void``
            - return ``true`` if ``self`` is ``false`` and ``false`` if ``self`` is ``true``
- ``map``
    - base class for maps
    - it provides the following method
        - ``@str``
            - return a string of the form ``"{`k1`: `v1`, ..., `kN`: `vN`}"`` with `` `k?` `` being the string representations of the keys and `` `v?` `` being the string representations of the corresponding values
    - it provides following attribute
        - ``length: int``: the number of key/value pairs
    - its subclasses provide the following methods, `` `typeK` `` being the type of the keys and `` `typeV` `` being the values'type
        - ``@itemset `typeK` ⬅ `typeV` ``
            - set the value of the given key to the passed item
            - if the key currently has no value and the number of assigned key/value pairs is less than the declared number, create a new one, otherwise raise an error
        - ``@itemget `typeK` -> `typeV` ``
            - return the value referenced by the given key
            - if the key does not exist, raise an error
        - ``haskey(k: `typeK`) -> bool``
            - return ``true`` if the passed key is present, ``false`` otherwise
- ``array``
    - base class for arrays
    - it provides the following method:
        - ``@str``
            - return a string of the form ``"[`e1`, ..., `eN`]"`` with `` `e?` `` being the string representations of the respective elements
    - it provides the following attribute:
        - ``length: int``: by default the declared length of the array. It is customary to set it to the number of assigned items
    - its subclasses (specific types of array) provide the following methods, `` `typeE` `` being the type of the elements:
        -``@itemset int ⬅ `typeE` ``
            - set the element at the given index to `` `value` ``
            - `` `item` `` must be between 0 (referencing the first element) and the actual length (not ``self.length``) -1 (last element)
        - ``@itemget int -> `typeE` ``
            - get the element at the given index
            - `` `item` `` must be between 0 (referencing the first element) and the actual length (not ``self.length``) -1 (last element)


Functions and Procedures
------------------------

- ``write(obj: object)``
    - write the string representation of the passed object to standard output
- ``read() -> str``
    - read the next line from standard input and return it, strippin the newline character

Values
------

Note: ``$magic$`` is used in places where appropriate representation in Pseudocode is not possible. 

- ``true := bool: $magic$``: the boolean value for trueness
- ``flase := bool: $magic$``: the boolean value of falseness
- ``void := $magic$: $magic$``: a typeless value
- ``args: array[$magic$, str]``: the command-line argumnts, as a string array if appropriate length

Libraries
---------

These libraries may all be imported with their respective identifier as per the import directive

- ``math``
    - This library provides the following mathematical functions:
        - ``sin_deg(x: basenumber) -> real`` return the sine of ``x`` degrees
        - ``sin_rad(x: basenumber) -> real`` return the sine of ``x`` radiants
        - ``cos_deg(x: basenumber) -> real`` return the cosine of ``x`` degrees
        - ``cos_rad(x: basenumber) -> real`` return the cosine of ``x`` radiants
        - ``tan_deg(x: basenumber) -> real`` return the tangent of ``x`` degrees
        - ``tan_rad(x: basenumber) -> real`` return the tangent of ``x`` radiants
        - ``sqrt(x: basenumber) -> real`` return the square root of ``x``
        - ``root(n: basenumber) -> real`` return the ``n``th root of ``x``
        - ``randint(a: int, b: int) -> int`` return a random ``int`` between ``a`` and ``b``, including both endpoints
        - ``random() -> real`` return a random number between ``0.0`` and ``1.0``, including both endpoints
