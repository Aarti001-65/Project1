import sqlite3

DB = "myproject.db"

# 10 exams × 10 questions = 100 MCQs
# Each tuple: (exam_id, question, option_a, option_b, option_c, option_d, correct_answer)

questions = [
    # 1 - HTML Fundamentals
    (1, "What does HTML stand for?", "Hyper Text Markup Language", "High Text Machine Language", "Hyperlink Text Management Language", "Home Tool Markup Language", "Hyper Text Markup Language"),
    (1, "Which tag is used for the largest heading?", "<h6>", "<h1>", "<head>", "<heading>", "<h1>"),
    (1, "Which tag creates a paragraph?", "<p>", "<para>", "<text>", "<pg>", "<p>"),
    (1, "Which tag is used to create a hyperlink?", "<link>", "<a>", "<href>", "<url>", "<a>"),
    (1, "Which attribute specifies an image source?", "href", "src", "link", "path", "src"),
    (1, "Which tag is used to insert an image?", "<image>", "<img>", "<picture>", "<src>", "<img>"),
    (1, "Which HTML element creates an unordered list?", "<ol>", "<ul>", "<li>", "<list>", "<ul>"),
    (1, "Which tag is used to create a table row?", "<td>", "<th>", "<tr>", "<row>", "<tr>"),
    (1, "Which tag defines a table cell?", "<cell>", "<td>", "<tr>", "<tablecell>", "<td>"),
    (1, "Which declaration defines an HTML5 document?", "<!DOCTYPE html>", "<HTML5>", "<DOCTYPE HTML5>", "<html version='5'>", "<!DOCTYPE html>"),

    # 2 - Java OOP & Advanced
    (2, "Which concept allows one class to acquire properties of another class?", "Encapsulation", "Inheritance", "Abstraction", "Compilation", "Inheritance"),
    (2, "Which keyword is used to inherit a class in Java?", "inherits", "extends", "implements", "super", "extends"),
    (2, "Which keyword refers to the current object?", "self", "this", "current", "object", "this"),
    (2, "Which keyword is used to call a parent class constructor or member?", "parent", "base", "super", "this", "super"),
    (2, "What is method overloading?", "Same method name with different parameters", "Same method with different classes only", "Changing a variable", "Deleting a method", "Same method name with different parameters"),
    (2, "What is method overriding?", "Defining a subclass method with the same signature", "Creating many constructors", "Changing variable type", "Calling a static method", "Defining a subclass method with the same signature"),
    (2, "Which keyword is used to create an abstract class?", "interface", "abstract", "virtual", "extends", "abstract"),
    (2, "Which keyword prevents a class from being inherited?", "static", "const", "final", "private", "final"),
    (2, "Which collection does not allow duplicate elements?", "List", "Set", "Array", "String", "Set"),
    (2, "Which exception occurs when an integer is divided by zero?", "NullPointerException", "IOException", "ArithmeticException", "ClassNotFoundException", "ArithmeticException"),

    # 3 - Java Programming Basics
    (3, "Which method is the entry point of a Java program?", "start()", "main()", "run()", "execute()", "main()"),
    (3, "Which keyword is used to declare a class?", "class", "Class", "define", "object", "class"),
    (3, "Which data type stores true or false?", "int", "boolean", "char", "float", "boolean"),
    (3, "Which symbol ends a Java statement?", ".", ":", ";", ",", ";"),
    (3, "Which keyword creates an object?", "create", "new", "object", "make", "new"),
    (3, "Which data type stores a single character?", "String", "char", "character", "byte", "char"),
    (3, "Which operator is used for logical AND?", "&", "&&", "||", "!", "&&"),
    (3, "Which loop executes while a condition is true?", "if", "while", "switch", "case", "while"),
    (3, "Which keyword is used to return a value from a method?", "send", "return", "back", "output", "return"),
    (3, "Which package is automatically imported in every Java program?", "java.util", "java.io", "java.lang", "java.net", "java.lang"),

    # 4 - Python Advanced Concepts
    (4, "What is a Python decorator used for?", "Modifying or extending function behavior", "Creating hardware drivers", "Deleting functions", "Only declaring variables", "Modifying or extending function behavior"),
    (4, "Which keyword creates a generator function?", "generate", "yield", "generator", "return", "yield"),
    (4, "What does *args allow in a function?", "Variable number of positional arguments", "Only keyword arguments", "Only one argument", "No arguments", "Variable number of positional arguments"),
    (4, "What does **kwargs allow in a function?", "Variable number of keyword arguments", "Only positional arguments", "Only integers", "A single dictionary key", "Variable number of keyword arguments"),
    (4, "Which structure handles exceptions?", "if-else", "try-except", "for-while", "switch-case", "try-except"),
    (4, "Which Python feature creates an anonymous function?", "lambda", "def", "anon", "func", "lambda"),
    (4, "Which data type stores key-value pairs?", "list", "tuple", "dictionary", "set", "dictionary"),
    (4, "What is list comprehension?", "A compact way to create lists", "A way to delete lists", "A database command", "A class constructor", "A compact way to create lists"),
    (4, "Which module is commonly used for regular expressions?", "regex", "re", "regexp", "pattern", "re"),
    (4, "What is inheritance in Python?", "A class acquiring behavior from another class", "Copying a file", "Installing a package", "Creating a variable", "A class acquiring behavior from another class"),

    # 5 - Python Programming Basics
    (5, "Which function displays output in Python?", "display()", "echo()", "print()", "show()", "print()"),
    (5, "Which symbol is used for a single-line comment?", "//", "#", "/*", "--", "#"),
    (5, "Which data type stores whole numbers?", "float", "str", "int", "bool", "int"),
    (5, "Which function is used to get input from the user?", "scan()", "input()", "read()", "get()", "input()"),
    (5, "Which collection is ordered and mutable?", "tuple", "list", "set", "frozenset", "list"),
    (5, "Which collection is immutable?", "list", "dictionary", "tuple", "set", "tuple"),
    (5, "Which keyword is used for a condition?", "if", "when", "condition", "check", "if"),
    (5, "Which loop is commonly used to iterate over a sequence?", "for", "repeat", "loop", "iterate", "for"),
    (5, "What is the correct file extension for Python files?", ".java", ".py", ".python", ".pt", ".py"),
    (5, "Which operator is used for exponentiation?", "^", "**", "//", "%%", "**"),

    # 6 - HTML Forms & Web Structure
    (6, "Which tag creates an HTML form?", "<form>", "<input>", "<fieldset>", "<data>", "<form>"),
    (6, "Which input type is used for a password?", "text", "secret", "password", "hidden", "password"),
    (6, "Which attribute gives a form control its submitted name?", "id", "name", "label", "key", "name"),
    (6, "Which form method sends data in the request body?", "GET", "POST", "SEND", "PUTONLY", "POST"),
    (6, "Which tag creates a drop-down list?", "<select>", "<dropdown>", "<list>", "<optionlist>", "<select>"),
    (6, "Which tag defines an item inside a select list?", "<item>", "<option>", "<choice>", "<selectitem>", "<option>"),
    (6, "Which tag groups related form controls?", "<group>", "<fieldset>", "<section>", "<formgroup>", "<fieldset>"),
    (6, "Which element is used to provide a caption for a form control?", "<caption>", "<label>", "<title>", "<name>", "<label>"),
    (6, "Which semantic element usually represents the main navigation?", "<navigate>", "<nav>", "<menuitem>", "<links>", "<nav>"),
    (6, "Which semantic element represents the main content of a page?", "<content>", "<main>", "<bodycontent>", "<primary>", "<main>"),

    # 7 - CSS Fundamentals
    (7, "What does CSS stand for?", "Cascading Style Sheets", "Computer Style Syntax", "Creative Style System", "Colorful Style Sheets", "Cascading Style Sheets"),
    (7, "Which property changes text color?", "font-color", "text-color", "color", "foreground", "color"),
    (7, "Which property changes the background color?", "bgcolor", "background-color", "background-style", "color-bg", "background-color"),
    (7, "Which symbol selects an element by id?", ".", "#", "*", "@", "#"),
    (7, "Which symbol selects a class?", "#", ".", "*", "$", "."),
    (7, "Which property controls font size?", "font-size", "text-size", "size", "font", "font-size"),
    (7, "Which property makes text bold?", "font-style", "font-weight", "text-bold", "weight-font", "font-weight"),
    (7, "Which property adds space inside an element's border?", "margin", "padding", "spacing", "inside-space", "padding"),
    (7, "Which property adds space outside an element's border?", "padding", "margin", "border-space", "outside", "margin"),
    (7, "Which CSS property changes the width of an element?", "size", "width", "element-width", "length", "width"),

    # 8 - CSS Advanced Styling
    (8, "Which layout system is designed for one-dimensional layouts?", "Grid", "Flexbox", "Float", "Table", "Flexbox"),
    (8, "Which layout system is designed for two-dimensional layouts?", "Flexbox", "Grid", "Inline", "Float", "Grid"),
    (8, "Which property controls the stacking order of positioned elements?", "stack", "z-index", "layer", "order-index", "z-index"),
    (8, "Which pseudo-class applies when the mouse pointer is over an element?", ":click", ":hover", ":mouse", ":over", ":hover"),
    (8, "Which property is used to make an element transparent?", "opacity", "transparent", "visibility-color", "alpha", "opacity"),
    (8, "Which media feature is commonly used for responsive design?", "screen-width", "max-width", "device-size", "responsive", "max-width"),
    (8, "Which property controls how an image fits inside a box?", "image-fit", "object-fit", "fit-image", "background-fit", "object-fit"),
    (8, "Which CSS function can calculate a value using expressions?", "calc()", "compute()", "math()", "value()", "calc()"),
    (8, "Which property creates rounded corners?", "corner-radius", "border-radius", "radius", "round-border", "border-radius"),
    (8, "Which property controls an element's position relative to its normal location?", "position", "location", "place", "move", "position"),

    # 9 - SQL & Database Basics
    (9, "What does SQL stand for?", "Structured Query Language", "Simple Query Language", "System Query Logic", "Structured Question Language", "Structured Query Language"),
    (9, "Which command retrieves data from a table?", "GET", "SELECT", "FETCHALL", "READ", "SELECT"),
    (9, "Which command adds a new row?", "ADD", "INSERT", "CREATE", "APPENDROW", "INSERT"),
    (9, "Which command modifies existing data?", "CHANGE", "UPDATE", "MODIFYROW", "ALTERDATA", "UPDATE"),
    (9, "Which command removes rows from a table?", "REMOVE", "DELETE", "DROP", "CLEAR", "DELETE"),
    (9, "Which command creates a table?", "MAKE TABLE", "CREATE TABLE", "NEW TABLE", "BUILD TABLE", "CREATE TABLE"),
    (9, "Which key uniquely identifies a row?", "Foreign key", "Primary key", "Candidate value", "Index value", "Primary key"),
    (9, "Which clause filters rows?", "FILTER", "WHERE", "HAVINGONLY", "CHECK", "WHERE"),
    (9, "Which clause sorts query results?", "SORT BY", "ORDER BY", "GROUP BY", "ARRANGE", "ORDER BY"),
    (9, "Which aggregate function counts rows?", "SUM()", "COUNT()", "NUMBER()", "TOTAL()", "COUNT()"),

    # 10 - SQL Queries & Advanced Database
    (10, "Which clause groups rows with the same values?", "ORDER BY", "GROUP BY", "WHERE", "SORT", "GROUP BY"),
    (10, "Which clause filters grouped results?", "WHERE", "HAVING", "GROUPFILTER", "AFTER GROUP", "HAVING"),
    (10, "Which SQL operation combines rows from related tables?", "JOIN", "MERGE ONLY", "CONNECT", "RELATE", "JOIN"),
    (10, "Which JOIN returns matching rows from both tables?", "FULL JOIN", "INNER JOIN", "LEFT JOIN", "CROSS JOIN", "INNER JOIN"),
    (10, "Which JOIN keeps all rows from the left table?", "RIGHT JOIN", "LEFT JOIN", "INNER JOIN", "CROSS JOIN", "LEFT JOIN"),
    (10, "Which constraint prevents duplicate values in a column?", "UNIQUE", "DISTINCT", "NO DUPLICATE", "SINGLE", "UNIQUE"),
    (10, "Which constraint ensures a column cannot contain NULL?", "REQUIRED", "NOT NULL", "NO EMPTY", "CHECK NULL", "NOT NULL"),
    (10, "Which command removes a table and its structure?", "DELETE TABLE", "DROP TABLE", "REMOVE TABLE", "CLEAR TABLE", "DROP TABLE"),
    (10, "Which operator combines results of two SELECT queries?", "COMBINE", "UNION", "JOIN", "MERGE", "UNION"),
    (10, "Which function returns the largest value?", "TOP()", "MAX()", "HIGH()", "LARGEST()", "MAX()"),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Avoid adding the same question twice.
inserted = 0
skipped = 0

for row in questions:
    exists = cur.execute(
        "SELECT 1 FROM questions WHERE exam_id = ? AND question = ?",
        (row[0], row[1])
    ).fetchone()

    if exists:
        skipped += 1
        continue

    cur.execute("""
        INSERT INTO questions
        (exam_id, question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, row)
    inserted += 1

conn.commit()

print(f"Questions inserted: {inserted}")
print(f"Questions already present/skipped: {skipped}")

print("\nQuestion count for each exam:")
for exam_id in range(1, 11):
    name = cur.execute(
        "SELECT name FROM exams WHERE id = ?", (exam_id,)
    ).fetchone()
    count = cur.execute(
        "SELECT COUNT(*) FROM questions WHERE exam_id = ?", (exam_id,)
    ).fetchone()[0]
    print(f"{exam_id}: {name[0] if name else 'Unknown'} -> {count} questions")

conn.close()