# Using Parsers

## Pattern Matching with Queries

Many code analysis tasks involve searching for patterns in syntax trees. Tree-sitter provides a small declarative language for expressing these patterns and searching for matches. The language is similar to the format of Tree-sitter's [unit test system](./creating-parsers#command-test).

### Query Syntax

A _query_ consists of one or more _patterns_, where each pattern is an [S-expression](https://en.wikipedia.org/wiki/S-expression) that matches a certain set of nodes in a syntax tree. The expression to match a given node consists of a pair of parentheses containing two things: the node's type, and optionally, a series of other S-expressions that match the node's children. For example, this pattern would match any `binary_expression` node whose children are both `number_literal` nodes:

```scheme
(binary_expression (number_literal) (number_literal))
```

Children can also be omitted. For example, this would match any `binary_expression` where at least _one_ of child is a `string_literal` node:

```scheme
(binary_expression (string_literal))
```

#### Fields

In general, it's a good idea to make patterns more specific by specifying [field names](#node-field-names) associated with child nodes. You do this by prefixing a child pattern with a field name followed by a colon. For example, this pattern would match an `assignment_expression` node where the `left` child is a `member_expression` whose `object` is a `call_expression`.

```scheme
(assignment_expression
  left: (member_expression
    object: (call_expression)))
```

#### Negated Fields

You can also constrain a pattern so that it only matches nodes that _lack_ a certain field. To do this, add a field name prefixed by a `!` within the parent pattern. For example, this pattern would match a class declaration with no type parameters:

```scheme
(class_declaration
  name: (identifier) @class_name
  !type_parameters)
```

#### Anonymous Nodes

The parenthesized syntax for writing nodes only applies to [named nodes](#named-vs-anonymous-nodes). To match specific anonymous nodes, you write their name between double quotes. For example, this pattern would match any `binary_expression` where the operator is `!=` and the right side is `null`:

```scheme
(binary_expression
  operator: "!="
  right: (null))
```

#### Capturing Nodes

When matching patterns, you may want to process specific nodes within the pattern. Captures allow you to associate names with specific nodes in a pattern, so that you can later refer to those nodes by those names. Capture names are written _after_ the nodes that they refer to, and start with an `@` character.

For example, this pattern would match any assignment of a `function` to an `identifier`, and it would associate the name `the-function-name` with the identifier:

```scheme
(assignment_expression
  left: (identifier) @the-function-name
  right: (function))
```

And this pattern would match all method definitions, associating the name `the-method-name` with the method name, `the-class-name` with the containing class name:

```scheme
(class_declaration
  name: (identifier) @the-class-name
  body: (class_body
    (method_definition
      name: (property_identifier) @the-method-name)))
```

#### Quantification Operators

You can match a repeating sequence of sibling nodes using the postfix `+` and `*` _repetition_ operators, which work analogously to the `+` and `*` operators [in regular expressions](https://en.wikipedia.org/wiki/Regular_expression#Basic_concepts). The `+` operator matches _one or more_ repetitions of a pattern, and the `*` operator matches _zero or more_.

For example, this pattern would match a sequence of one or more comments:

```scheme
(comment)+
```

This pattern would match a class declaration, capturing all of the decorators if any were present:

```scheme
(class_declaration
  (decorator)* @the-decorator
  name: (identifier) @the-name)
```

You can also mark a node as optional using the `?` operator. For example, this pattern would match all function calls, capturing a string argument if one was present:

```scheme
(call_expression
  function: (identifier) @the-function
  arguments: (arguments (string)? @the-string-arg))
```

#### Grouping Sibling Nodes

You can also use parentheses for grouping a sequence of _sibling_ nodes. For example, this pattern would match a comment followed by a function declaration:

```scheme
(
  (comment)
  (function_declaration)
)
```

Any of the quantification operators mentioned above (`+`, `*`, and `?`) can also be applied to groups. For example, this pattern would match a comma-separated series of numbers:

```scheme
(
  (number)
  ("," (number))*
)
```

#### Alternations

An alternation is written as a pair of square brackets (`[]`) containing a list of alternative patterns.
This is similar to _character classes_ from regular expressions (`[abc]` matches either a, b, or c).

For example, this pattern would match a call to either a variable or an object property.
In the case of a variable, capture it as `@function`, and in the case of a property, capture it as `@method`:

```scheme
(call_expression
  function: [
    (identifier) @function
    (member_expression
      property: (property_identifier) @method)
  ])
```

This pattern would match a set of possible keyword tokens, capturing them as `@keyword`:

```scheme
[
  "break"
  "delete"
  "else"
  "for"
  "function"
  "if"
  "return"
  "try"
  "while"
] @keyword
```

#### Wildcard Node

A wildcard node is represented with an underscore (`_`), it matches any node.
This is similar to `.` in regular expressions.
There are two types, `(_)` will match any named node,
and `_` will match any named or anonymous node.

For example, this pattern would match any node inside a call:

```scheme
(call (_) @call.inner)
```

#### Anchors

The anchor operator, `.`, is used to constrain the ways in which child patterns are matched. It has different behaviors depending on where it's placed inside a query.

When `.` is placed before the _first_ child within a parent pattern, the child will only match when it is the first named node in the parent. For example, the below pattern matches a given `array` node at most once, assigning the `@the-element` capture to the first `identifier` node in the parent `array`:

```scheme
(array . (identifier) @the-element)
```

Without this anchor, the pattern would match once for every identifier in the array, with `@the-element` bound to each matched identifier.

Similarly, an anchor placed after a pattern's _last_ child will cause that child pattern to only match nodes that are the last named child of their parent. The below pattern matches only nodes that are the last named child within a `block`.

```scheme
(block (_) @last-expression .)
```

Finally, an anchor _between_ two child patterns will cause the patterns to only match nodes that are immediate siblings. The pattern below, given a long dotted name like `a.b.c.d`, will only match pairs of consecutive identifiers: `a, b`, `b, c`, and `c, d`.

```scheme
(dotted_name
  (identifier) @prev-id
  .
  (identifier) @next-id)
```

Without the anchor, non-consecutive pairs like `a, c` and `b, d` would also be matched.

The restrictions placed on a pattern by an anchor operator ignore anonymous nodes.

#### Predicates

You can also specify arbitrary metadata and conditions associated with a pattern
by adding _predicate_ S-expressions anywhere within your pattern. Predicate S-expressions
start with a _predicate name_ beginning with a `#` character. After that, they can
contain an arbitrary number of `@`-prefixed capture names or strings.

Tree-Sitter's CLI supports the following predicates by default:

##### eq?, not-eq?, any-eq?, any-not-eq?

This family of predicates allows you to match against a single capture or string
value.

The first argument must be a capture, but the second can be either a capture to
compare the two captures' text, or a string to compare first capture's text
against.

The base predicate is "#eq?", but its complement "#not-eq?" can be used to _not_
match a value.

Consider the following example targeting C:

```scheme
((identifier) @variable.builtin
  (#eq? @variable.builtin "self"))
```

This pattern would match any identifier that is `self` or `this`.

And this pattern would match key-value pairs where the `value` is an identifier
with the same name as the key:

```scheme
(
  (pair
    key: (property_identifier) @key-name
    value: (identifier) @value-name)
  (#eq? @key-name @value-name)
)
```

The prefix "any-" is meant for use with quantified captures. Here's
an example finding a segment of empty comments

```scheme
((comment)+ @comment.empty
  (#any-eq? @comment.empty "//"))
```

Note that "#any-eq?" will match a quantified capture if
_any_ of the nodes match the predicate, while by default a quantified capture
will only match if _all_ the nodes match the predicate.

##### match?, not-match?, any-match?, any-not-match?

These predicates are similar to the eq? predicates, but they use regular expressions
to match against the capture's text.

The first argument must be a capture, and the second must be a string containing
a regular expression.

For example, this pattern would match identifier whose name is written in `SCREAMING_SNAKE_CASE`:

```scheme
((identifier) @constant
  (#match? @constant "^[A-Z][A-Z_]+"))
```

Here's an example finding potential documentation comments in C

```scheme
((comment)+ @comment.documentation
  (#match? @comment.documentation "^///\s+.*"))
```

Here's another example finding Cgo comments to potentially inject with C

```scheme
((comment)+ @injection.content
  .
  (import_declaration
    (import_spec path: (interpreted_string_literal) @_import_c))
  (#eq? @_import_c "\"C\"")
  (#match? @injection.content "^//"))
```

##### any-of?, not-any-of?

The "any-of?" predicate allows you to match a capture against multiple strings,
and will match if the capture's text is equal to any of the strings.

Consider this example that targets JavaScript:

```scheme
((identifier) @variable.builtin
  (#any-of? @variable.builtin
        "arguments"
        "module"
        "console"
        "window"
        "document"))
```

This will match any of the builtin variables in JavaScript.

_Note_ — Predicates are not handled directly by the Tree-sitter C library.
They are just exposed in a structured form so that higher-level code can perform
the filtering. However, higher-level bindings to Tree-sitter like
[the Rust Crate](https://github.com/tree-sitter/tree-sitter/tree/master/lib/binding_rust)
or the [WebAssembly binding](https://github.com/tree-sitter/tree-sitter/tree/master/lib/binding_web)
do implement a few common predicates like the `#eq?`, `#match?`, and `#any-of?`
predicates explained above.

To recap about the predicates Tree-Sitter's bindings support:

- `#eq?` checks for a direct match against a capture or string
- `#match?` checks for a match against a regular expression
- `#any-of?` checks for a match against a list of strings
- Adding `not-` to the beginning of any of these predicates will negate the match
- By default, a quantified capture will only match if _all_ of the nodes match the predicate
- Adding `any-` before the `eq` or `match` predicates will instead match if any of the nodes match the predicate
