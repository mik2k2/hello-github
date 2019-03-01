

Pseudocode Specification
========================


Code notations
---------------

- text referencing code will be formatted like ``this``
- if there is a variable content in a code notation, it will be enclosed by `` `single` `` backticks
- if content is optional, if will be enclosed in ``|pipes|``
- if there is a choice of content, the possibilities will be enclosed in ``|pipes|`` (_not_ indicating optionality) separated by the ``tilde~sign``
- ... is used to display repetitive options
- the arrow used, ⬅, is U+11013
- numbers in repetitive options will be dispayed with a question mark

Basic Construction
------------------

The language atomically consists of literal values, identifiers, operators and directives.  
An __expression__ is a combination of literal values, identifiers and expressions with operators having any number of spaces between them.  
A __statement__ is defined as expressions combined with directives in a legal way. Statements may be combined into a single statement, all statements are placed on separate lines having the same indentation as the first one. This grouping may contain empty lines at any location and still be considered valid.  
An __identifier__ refers to a variable's name and specific value. Values may be _bound_ to identifiers. An identifier may hold values of different types only by means of scoping. An  identifier must consist of alphanumberic characters (including the underscore ``_`` character, may not begin with a number and is case-sensitive.

Literal Values
--------------

- a _string_
    - text enclosed between "double quotes"
    - it may contain any character. Following "escapes" are possible:
        - ``\"``: a double quote as content of the string.
        - ``\n``: the newline character
        - ``\t``: the tab character
        - ``\\``: the backslash character
        - ``\v{`expresssion`}``: the string representation of `` `expression` ``
    - its type is ``str``
- an *integer*
    - any number consisting of only digits and spaces (allowed to enhance readability)
    - its type is ``int``
- a _real number_
    - a number containing a decimal point in form of a period. It may include spaces before and after, but not directly next to the point to enhance readability
    - a special builltin constant ``inf`` is provided for infinite values
    - its type if ``real`` or ``float``
- a _boolean_
    - one the the builitn constants ``true`` of ``flase``
    - its type is ``bool``
- a _void value_
    - it has no type and is accessible through the builtin constant ``void``
- a _map_
    - it maps a key to a value
    - its type is `` map[`no`: `key type` ⬅ `value type`] ``, where `` `no` `` is the number of keys and values (a literal or constant ``int``), `` `key type` `` is the type of the keys and `` `value type` `` is the values' type. The base class is ``map``
    - its literal representation is ``[`key 1`⬅`value 1`, ...]``
- an _array_
    - it is a sized and ordered collection of elements of the same type
    - its type is ``array[`no1`, ..., `noN`, `type`]``, where `` `no?` `` are the numbers (literal or constant ``int``) of items in each nesting level and `` `type` `` is the type the items in the last nesting level have have. The base class is ``array``
    - Note the same array type may be written in different ways, e.g. ``array[2, array[2, int]]`` is the same as ``array[2, 2, int]``, although the latter is preferred for ease of reading and typing
    - its literal presentation is ``[`value 1`, ...]``
    - the literal representation may contain less values than the array declaration. The unfilled values are set to ``void``.
    
Directives
----------

Directives provide structure and meanings to the language. Statements must, if not indicated otherwise and they include multiple sub-statements, begin on a following line and be indented.

- declaration directive
    - `` `identifier1`, ..., `identfierN`: `type` ``
    - (re)create new identifiers `` `identifier1` `` to `` `identifierN` `` that may contain values of type `` `type` ``
    - if `` `type` `` has an argument-less constructor, assign its evaluation to the newly created identifiers. Otherwse, their values will be ``void`` until assigned.
    - this directive may only be used inside a scope directive (see below)
- assignment directive
    - `` `identifier`⬅`value` ``
    - assign the value of the evaluated `` `expression` `` to `` `identifier` ``
- constant directive
    - `` `identifier` := `type`: `constan value` ``
    - create a new identifier for the given type and assign `` `constant value` `` to it.
    - block all declaration attempts (through constant directive or declaration directive) of the identifier in lower scopes
    - this directive may only be used inside a scope directive (see below)
- if-directive
    -  ``if `condition`: `statement 1` |else: `statement 2`|``
    - if `` `condition` `` evaluates to ``true``, execute ``statement 1`` otherwise execute ``statement 2``, if given
- while-directive
    - ``while `condition`: `statement` ``
    - execute `` `statement` `` as long as `` `condition` `` evaluates to ``true``
    - `` `condition` `` is checked _before_ each execution
- for-directive
    - ``for `identifier` |from `initial`| to `condition` |step `step`|: `statement` ``
    - set `` `identifier` `` to `` `initial` `` if given, else to ``0`` (Note: if the identifier is not declared as ``int``, ommiting `` `initial` `` is illegal)
    - execute `` `statement` `` as long as `` `identifier` <     `condition` `` if `` `condition` `` is instance of ``basenumber``, otherwise as long as `` `condition` `` evaluates to ``true``. This check is performed _before_ every execution
    - perform the following action on `` `identifier` `` _after_ each execution of `` `statement` ``:
        - increment by ``1`` if `` `step` `` is not set
        - perform `` `identifier` ⬅ `identifier` + `step` `` if `` `step` `` is an expression
        - execute `` `step` `` if it is a statement. It may not contain other statements.
- definition directive
    - ``def `identifier`(`arg1`: `arg type 1`|@|ref~val||, ..., `argN`: `arg type N`|@|ref~val||)| -> `return type`|: `statement` ``
    - define a function (if `` `return type` `` is set) or a procedure (otherwise) with the given identifier and prevent future definitions with equal name, argument numbers, types and order and return type
    - passage of arguments is as follows
        - if ``@ref`` is added to a `` `arg type ?` ``, the passage is "by reference", i.e. all modifications (including reassignment) to the formal parameter are reflected in the acutal parameter. This is useful for "returnig" multiple values
        - if ``@val`` is added to a `` `arg type ?` ``, the passage is "by value", i.e the value is entirely copied and no changes will be reflected. 
        - if no suffix is added, the passage is by value of a reference. This means that changes to the object (e.g. attribute modifications) are reflected, reassignment is not.
- return directive
    - ``return `expression` ``
    - evaluate `` `expression` `` and return the value as result of the containing function. It immediately exits the function.
- type directive
    - ``type `identifier` |⬅`base`|: `satement` ``
    - `` `statement` `` must be at least one definition directive and may contain a scope directive as first content
    - create a new type with the given name and optionally base class  and block all future uses of `` `identifier` `` as identifier
    - Seen "User-defined types (classes)" for more information
- Scope directive
    - ``VARS: `statement` ``
    - `` `statement` `` may consist only of definition, alias and constant directives
    - this defines a new scope for the file, function, method or procedure, or, for types, their instances.
    - identifier lookups are performed from inner- to outermost scope
    - a scope directive may "shadow" outer identifiers, if these are neither constents nor types or outer-level functions or procedures
- Import directive
    - ``@import `library`| to `identifier`|``
    - This directive must be included in a file before any other code if used
    - If `` `library` `` is a valid identifier, bind the library `` `library` `` from the standard libraries to `` `identifier` `` if specified, else to ``library``
    - If `` `library` `` is a string constant, import the .pseudo file following the path in `` `library` `` (if relative, to the directory containing the current file) as a library and bind it to `` `identifier ` `` which must be given in this case
    - Disallow all future declarations of the identifier to which the library is bound
    - Library elements are looked up as attributes (see operators)
- alias directive:
    - ``@alias `name` = `value` ``
    - create a new valid identifier `` `name` `` that holds the type `` `value` ``
    - it may only be used in a file-level scope directive
    - this is especially useful when dealing regularly with a complex type

Operators
---------

- ``+`` "add"; precedence 4
- ``-`` "subtract"; precedence 4
- ``*`` "multiply"; precedence 3
- ``/`` "divide"; precedence 3
- ``=`` "equals"; precedence 5
- ``≠`` "unequals"; entirely equivalent to ``not`` the result of ``=`` with the same arguments
- ``and`` "and"; precedence 5
- ``or`` "or"; precedence 5
- ``not`` "not"; precedence 5
- ``^`` "to the power of"; precedence 2
- ``mod`` "modulus"; precedence 3

Element lookups and assigments are possible with `` `container`[`item`] |⬅`new`|`` (Precedence 1). Attribute lookups and assignments are possible with `` `object`.`identifier |⬅`new`|`` (not operators).

Operators with lower precedence are evaluated first. Operators with equal precedenct are evaluated from left to right. Paranthesis ``()`` may be used to change the evaluation order: expressions in parenthesis are evaluated first. If an operation is not possible with the given values, the precedence order is skipped, e.g. ``2^-1`` will first attempt to evaluate ``2^`` and, as that is not possible, evaluate ``2^(-1)``.

User-defined types (classes)
----------------------------

The user may define their own types that can subsequently be used. This is done by the type directive. The scope optionally introduced in the directive is separate for every instance of the class. All definitions inside the type directive are methods. 

They are defined as normal functions or procedures, but they are passed an implicit parameter ``self`` that represents the instance the method is called on. It may also include the following special methods (exactly as written here, without ``def``, parameters or parenthesis but `` `statement` `` possibly starting on the following line):

- ``@str: `statement` ``
    - used when a conversion to ``str`` is requested. _Must_ return a ``str``.
- ``@int: `statement` ``
    - used when a conversion to ``int`` is requested. _Must_ return an ``int``.
- ``@float: `statement` `` or `` `@real` ``
    - used when a conversion to ``float`` is requested. _Must_ return a ``float``.
    - only one of the two possibilities may be defined.
- ``@bool: `statement` ``
    - used when a conversion to ``bool`` is requested. _Must_ return a ``bool``.
- ``@construct|`params`|: `statement` ``
    - where `` `params` `` is a parameter list as in the definition directive
    - This is called when creating a new instance. It is also passed the implicit ``self`` and __must not__ return anything.
- ``@itemget |`type`| -> `return type`: `statement` ``
    this is used when the element lookup is used on the instance. `` `type` `` is the type of `` `item` `` and `` `return type` `` the type of the returned element. If `` `type` `` is not provided, the method is used as fallback if one with a matching type is found. It is passed an additional implicit parameter ``item`` representing the value of `` `item` ``.
- ``@itemset `typeI` ⬅ `typeV`: `statement` ``
    this is used when an element is set on the instance. It is passed an additional implicit parameter ``item`` representing the value of `` `item` `` and ``value`` representing `` `new` ``. `` `typeI` `` is the type of `` `item` ``. `` `typeV` `` represents the type of the parameter ``value``.

Additionally to these methods, operators may be overloaded with methods as ``|`rval`|@`operator`other|@deffor `type`|`` (for operators on the left side of the instance) and ``|`rval`|@other`operator`|@deffor`type`|`` (for operators on the right side of the instance), where `` `operator` `` is an operator. 

When an operator is used on an instance, the corresponding function is called. There is no guarantee regarding which function is called, i.e. `` `a` `operator` `b` `` may call `` @`operator`other `` of `` `a` `` or `` @other`operator` `` of `` `b` `` if both are appropriately defined. However, only one must be defined for the operation to be legal and will be called if the only one It is passed the other value as other and the instance as self. If the operator is used without other value, other is void. 

`` `type` `` may be a type, __also one that is not yet defined__. It defines the type the operation with the class is defined for and may be ``void`` to indicate the method should be called without other value, i.e. the method will be called with other being instance of `` `type` ``. Multiple operator overrides may be defined with different `` `type` ``.  If no ``type`` is given, the method is used as a catch-all if no method with a matching type is otherwise found, but only when an other value is actually present (not ``void``).

If a special (overloading) method requests one of the types ``str``, ``int``, ``real`` or ``bool`` as argument and the operation is used with 

If `` `rval` `` is given, it is the value returned. If not provided, it is implicitly the containing type; the return self is also executed implicitly. Operations must return a value. Note: comparisons (``= > < >= <=``) will often return ``bool``. This has the be set as `` `rval` ``.
