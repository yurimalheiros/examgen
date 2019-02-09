# Exam Generator

Generate exams using Markdown and Python.


## Features

- Write questions in Markdown
- Generate PDF exams
- Generate answer keys
- Randomize questions and answers
- Generate multiple randomized exams

## Install

Using pip:

```
$ pip install examgen
```

Using the repository code:

```
$ python setup.py install
```

## Creating an exam

First you need to create an exam file. It is a python module. Then, just create an exam.py file for example.

You need set up five variables in the module: institution name, course name, professor name, exam title, questions.
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
Below there is an example of a question file:

```markdown
Which algorithm is used for unsupervised machine learning:

---

- KNN
- Linear regression
x K-means
- Decision tree
- Logistic regression
```

The file has two parts divided by the "---" line. The first part (above the ---) is the question text. You can write any markdown in that part. In the second part (below the ---) you put the answers. They must be created as a list, and the correct one has an "x" instead of "-".


### Comments

Questions may have a comment section. For this, you need to insert a extra "---" line after the answers. Below the "---" you can write any comment you want. Check the example below:

```markdown
Which algorithm is used for unsupervised machine learning:

---

- KNN
- Linear regression
x K-means
- Decision tree
- Logistic regression

---

This is a comment.
```


## Generating an exam

To generate an exam, use the Command Line Interface (CLI).

```bash
examgen -e EXAM_FILE
```

EXAM_FILE is the python file with the information of the exam.

The CLI supports other options:

- **-rq, --random-questions**: randomize the questions positions in the exam.
- **-ra, --random-answers**: randomize the answers positions in each question.
- **-b, --batch**: generate multiple exams.
- **-q, --quantity INTEGER**: set the number of exams in batch generation.
- **-m, --merge**: merge all exams in one file in batch generation.
- **-fb, --front-and-back**: use this option if you want to print the merged exams using the front and back of the sheets.

Note: ExamGen uses pandoc to generate PDF files from Markdown.


## Question bank

Randomize question order sometimes is not the behavior we want. So, we provide an alternative way to 
mix questions in exams. 

Using question bank, you can create many questions and set which questions can appear as the first question, or in the second question, or third, etc.

To do this you only need to set the questions in the exam file as follows:

```python
institution = "Federal University of Paraiba"
course = "Artificial Intelligence"
professor = "Yuri Malheiros"
exam = "2nd Exam"

questions = [("q1v1", "q1v2"), ("q2v1", "q2v2, q2v3"), "q3", ("q4v1", "q4v2"), "q5"]
```

In the example above, the first question will be picked randomly between the questions in the files q1v1.md and q1v2.md. The second question will be q2v1.md, q2v2.md or q2v3.md. Notice that not all questions need to have multiple possibilities, it this example, the third question will always be the question in the file q3.md. The fourth question also have two possibilities, and the last question will always be q5.md.
In summary, use a tuple to define the possible questions, and the exam generator will pick one randomly.

This feature is very useful for generating multiple random exams.