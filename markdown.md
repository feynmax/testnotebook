# Markdown Files

Whether you write your book's content in Jupyter Notebooks (`.ipynb`) or
in regular markdown files (`.md`), you'll write in the same flavor of markdown
called **MyST Markdown**.
This is a simple file to help you get started and show off some syntax.

## What is MyST?

MyST stands for "Markedly Structured Text". It
is a slight variation on a flavor of markdown called "CommonMark" markdown,
with small syntax extensions to allow you to write **roles** and **directives**
in the Sphinx ecosystem.

For more about MyST, see [the MyST Markdown Overview](https://jupyterbook.org/content/myst.html).

## Sample Roles and Directives

Roles and directives are two of the most powerful tools in Jupyter Book. They
are kind of like functions, but written in a markup language. They both
serve a similar purpose, but **roles are written in one line**, whereas
**directives span many lines**. They both accept different kinds of inputs,
and what they do with those inputs depends on the specific role or directive
that is being called.

Here is a "note" directive:

```{note}
:class: dropdown

Here is a note
```

$x^2-4$
It will be rendered in a special box when you build your book.

````{admonition} Die pq-Formel
:class: important, dropdown

|  | abc-Formel | pq-Formel |
|:--- | :---: | :---: |
| **Formel:** | $x_{1, 2} = \dfrac{-b \pm \sqrt{b^2-4ac\,}}{2a}$ | $x_{1, 2} = -\dfrac{p}2 \pm \sqrt{\left(\dfrac{p}2\right)^2 -q\,}$ |
| **Diskriminante:** | $D = b^2-4ac$ | $D = \left(\dfrac{p}2\right)^2 -q$ |
````

Here is an inline directive to refer to a document: {doc}`markdown-notebooks`.

````{admonition} Anzahl der Lösungen und Vorzeichen der Diskriminante
:class: warning, dropdown

```{math}
\textsf{Es gibt } \begin{cases}
\textsf{keine Lösung,} & \textsf{wenn } D<0 \\
\textsf{1 Lösung,} & \textsf{wenn } D=0 \\
\textsf{2 Lösungen,} & \textsf{wenn } D>0 \end{cases}
```
````


## Citations

You can also cite references that are stored in a `bibtex` file. For example,
the following syntax: `` {cite}`holdgraf_evidence_2014` `` will render like
this: {cite}`holdgraf_evidence_2014`.

Moreover, you can insert a bibliography into your page with this syntax:
The `{bibliography}` directive must be used for all the `{cite}` roles to
render properly.
For example, if the references for your book are stored in `references.bib`,
then the bibliography is inserted with:

```{bibliography}
```

## Learn more

This is just a simple starter to get you started.
You can learn a lot more at [jupyterbook.org](https://jupyterbook.org).
