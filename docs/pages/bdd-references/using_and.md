---
layout: default
title: Using AND
nav_order: 4
has_children: false
parent: BDD Reference
---

# Using AND

`AND` can be used in `WHEN` and `THEN` steps where one step is not sufficient to define the success or failure condition.

Few examples can be ;

```gherkin
Then it must contain tags
And its value must not be null
```

```gherkin
When it contains policy
And it contains Statement
And its Effect is Allow 
And it contains Principal
```

```gherkin
When its name is not public
And it contains tags
Then it must contain <tag_keys>
And its value must match the "<pattern>" regex
```