import os
import string
import random
from string import Template
from importlib import import_module
from PyPDF2 import PdfFileMerger


class Question(object):
    """
    An exam question.

    @question: question text/markdown
    @alternatives: list of question alternatives
    @correct_index: the correct alternative index
    """
    def __init__(self, question, alternatives, correct_index):
        self.question = question
        self.alternatives = alternatives
        self.correct_index = correct_index


class Exam(object):
    """
    An exam.

    @exam_name: the exam filename.
    @random_questions: True to shuffle the questions, False to keep the order.
    @random_answers: True to shuffle the alternatives, False to keep the order.
    """
    def __init__(self, exam_name, random_questions=False, random_answers=False):
        self.exam_name = exam_name
        self.random_questions = random_questions
        self.random_answers = random_answers

        # An exam is a python module.
        # See README for instructions on how to create a exam.
        self.exam = import_module(self.exam_name)
        self.questions = []

        # All questions are written in markdown following some patterns.
        # See README for instructions on how to create a question.
        for question_file in self.exam.questions:
            self.questions.append(self.read_question(f"{question_file}.md"))

        if self.random_questions:
            random.shuffle(self.questions)
        
    def read_question(self, filename):
        """
        Parse a question file.
        It returns a Question object.
        """
        question = ""
        alternatives = []
        correct_index = None

        with open(filename) as f:
            text = f.read()

            # The question text and the alternatives are separated by a "---" line
            question, alternatives_text = text.split("---")

            question = question.strip()
            alternatives_list = alternatives_text.strip().split("\n")

            if self.random_answers:
                random.shuffle(alternatives_list)

            # The correct alternative has a "x" before its text
            for index, value in enumerate(alternatives_list):
                if value[0] == "x":
                    correct_index = index

                alternatives.append(value[2:])       

            return Question(question, alternatives, correct_index)

    def _format_alternatives(self, alternatives):
        alternatives_html = ""

        for index, value in enumerate(alternatives):
            alternatives_html += f"{string.ascii_lowercase[index]}) {value}\n"

        return alternatives_html

    def build_markdown(self, examcode=None):
        """
        Generate a markdown file of the exam.
        """
        
        questions = ""
        result = ""

        # Processing questions
        for index, question in enumerate(self.questions):
            with open(os.path.join("template", "question-template.md")) as f:
                question_text = question.question
                alternatives = question.alternatives

                alternatives_html = self._format_alternatives(alternatives)

                t = Template(f.read())
                questions += t.substitute({"number": index+1,
                                        #    "marks": "1,0",
                                           "content": question_text,
                                           "answers": alternatives_html})

        # Combine everything in the exam template
        with open(os.path.join("template", "exam-template.md")) as f:
            t = Template(f.read())
            result = t.substitute({"institution": self.exam.institution,
                                   "course": self.exam.course,
                                   "professor": self.exam.professor,
                                   "exam": self.exam.exam,
                                   "questions": questions,
                                   "examcode": f"#{examcode}" if examcode is not None else ""})

        with open(f"{self.exam_name}-generated.md", "w") as f:
            f.write(result)

    def generate_pdf(self, output_name=None, folder=False):
        """
        Uses pandoc to convert the markdown file in a pdf.

        @output_name: the name of the pdf file. It uses the exam file name by default.
        @folder: add the pdf file in the folder with this name. It uses the current directory by default.
        """
        if output_name is None:
            output_name = self.exam_name

        if folder:
            output_name = os.path.join(folder, output_name)

        os.system(f"pandoc --metadata pagetitle='examgen' -t html5 {self.exam_name}-generated.md -o {output_name}.pdf --css template/style.css")

    def generate_answers(self, output_name=None, folder=False):
        """
        Generate the answers of an exam.

        @output_name: the name of is this parameter + "-answers.txt".
                      It uses the exam file name + "-answers.txt" by default.
        @folder: add the answers file in the folder with this name. It uses the current directory by default.
        """
        if output_name is None:
            output_name = self.exam_name

        if folder:
            output_name = os.path.join(folder, output_name)

        with open(f"{output_name}-answers.txt", "w") as f:  
            for index, value in enumerate(self.questions):
                f.write(f"{index+1} - {string.ascii_lowercase[value.correct_index]}\n")

    def generate(self):
        """
        Shortcut method to build markdown, generate pdf and answer key.
        """
        self.build_markdown()
        self.generate_pdf()
        self.generate_answers()


class BatchGenerator(object):
    """
    A helper class to generate multiple tests.
    It is useful to generate random exams.
    """
    def __init__(self):
        self.exams = []

    def generate(self, exam_name, quantity, random_questions=False, random_answers=False, merge=False):
        """
        Generate multiple exams.

        @exam_name: the exam filename.
        @quantity: the number of exams to generate.
        @random_questions: True to shuffle the questions, False to keep the order.
        @random_answers: True to shuffle the alternatives, False to keep the order.
        @merge: True to merge all exams in one pdf, False to not merge.
        """
        os.makedirs("batch", exist_ok=True)

        for i in range(quantity):
            exam = Exam(exam_name, random_questions=random_questions,
                        random_answers=random_answers)

            exam.build_markdown(examcode=i)
            exam.generate_pdf(f"{exam_name}-{i}", folder="batch")
            exam.generate_answers(f"{exam_name}-{i}", folder="batch")

            self.exams.append(exam)

        if merge:
            merger = PdfFileMerger()
            
            for i in range(quantity):
                pdf_file_path = os.path.join("batch", f"{exam_name}-{i}.pdf")
                merger.append(pdf_file_path, import_bookmarks=False)

            pdf_merge_file_path = os.path.join("batch", f"{exam_name}-merge.pdf")
            with open(pdf_merge_file_path, 'wb') as f:
                merger.write(f)


