# Exam Generator

This project uses Markdown and Python to generate exams.

## Features

- Write questions in Markdown
- Generate PDF exams
- Generate answer keys
- Randomize questions and answers
- Generate multiple randomized exams

## Creating an exam

First you need to create an exam file. It is a python module. Then, just create an exam.py file for example.

You need set up five variables in the module: instutition name, course name, professor name, exam title, questions.
Below there is an example of an exam file:


```python
institution = "Federal University of Paraiba"
course = "Artificial Intelligence"
professor = "Yuri Malheiros"
exam = "2nd Exam"

questions = ["question1", "question2", "question3", "question4", "question5"]
```

The first four items are very direct, you only need to put the text you want.
For the questions, you must provide a list with the names of the question files.
In the case above, the exam has five questions.
The first question was created in the file called question1.md, the second in the file question2.md and so on.

Let's check how to create a question file.

## Creating a question

A question file follow a markdown-ish syntax.
Bellow there is an example of a question file:

```markdown
Which algorithm is used for unsupervised machine learning:

---

- KNN
- Linear regression
x K-means
- Decision tree
- Logistic regression
```

The file has two parts divided by the "---" line. The first part (above the ---) is the question text. You can write any markdown in that part. In the second part (below the ---) you put the answers. They must be created as a list, and the correct one has a "x" instead of "-".

## Generating an exam

To generate an exam you only need to run the program:

```python
from examgen import Exam

exam = Exam("exam1", random_questions=True, random_answers=True)
exam.generate()
```

Change the "exam1" string to the name of your exam file. 
The parameters random_questions and random_answers control if you want to randomize questions and answers.
This code can be found in the main.py file.

NOTE: ExamGen uses pandoc to generate PDF files from Markdown.

## Generating multiple exams

To generate multiple exams you only need to run the program below. It is useful to
generate multiple random exams.

```python
from examgen import BatchGenerator

batch = BatchGenerator()
batch.generate("exam1", 5, random_questions=True, random_answers=True)
```

Change the "exam1" string to the name of your exam file, and the value "5" to the number of exams
you want to generate.
The parameters random_questions and random_answers control if you want to randomize questions and answers.
This code can be found in the mainbatch.py file.

If you want to merge all generated exams in one pdf, you can use the parameter `merge`:

```python
batch.generate("exam1", 5, random_questions=True, random_answers=True, merge=True)
```

It is simpler to print one file than multiple pdfs.
