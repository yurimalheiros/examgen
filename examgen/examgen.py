import os
import shutil
import string
import random
import importlib.util
from string import Template
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


class Question(object):
    """
    An exam question.

    @question: question text/markdown.
    @choices: list of question choices.
    @correct_index: the correct choice index.
    """
    def __init__(self, question, choices, correct_index):
        self.question = question
        self.choices = choices
        self.correct_index = correct_index


class Exam(object):
    """
    An exam.
    """
    def __init__(self, exam_path, random_questions=False, random_answers=False):
        """
        Constructor.

        @exam_path: the exam filename.
        @random_questions: True to shuffle the questions, False to keep the order.
        @random_answers: True to shuffle the choices, False to keep the order.
        """

        self.exam_path = exam_path
        self.random_questions = random_questions
        self.random_answers = random_answers

        self.exam_directory = os.path.dirname(self.exam_path)
        self.exam_file = os.path.basename(self.exam_path)
        self.exam_name = self.exam_file.split(".")[0]

        # An exam is a python module.
        # See README for instructions on how to create an exam.
        spec = importlib.util.spec_from_file_location("exam", exam_path)
        self.exam = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.exam)
        
        self.questions = []

        # All questions are written in markdown following some rules.
        # See README for instructions on how to create a question.
        for question_file in self.exam.questions:
            # you can pass a tuple of questions, then one of them will be picked randomly
            if type(question_file) == tuple:
                question_file = random.choice(question_file)

            question_filepath = os.path.join(self.exam_directory, f"{question_file}.md")
            self.questions.append(self.read_question(question_filepath))

        if self.random_questions:
            random.shuffle(self.questions)
        
    def read_question(self, filename):
        """
        Parse a question file.
        It returns a Question object.

        @filename: the question filename.
        """
        question = ""
        choices = []
        correct_index = None

        with open(filename) as f:
            text = f.read()

            # The question text, the choices, and comments
            # are separated by a "---" line
            text_split = text.split("---\n")
            question = text_split[0]
            choices_text = text_split[1] 

            question = question.strip() + "\n"
            choices_list = choices_text.strip().split("\n")

            if self.random_answers:
                random.shuffle(choices_list)

            # The correct choice has a "x" before its text
            for index, value in enumerate(choices_list):
                if value[0] == "x":
                    correct_index = index

                choices.append(value[2:])       

            return Question(question, choices, correct_index)

    def _format_choices(self, choices):
        choices_text = ""

        for index, value in enumerate(choices):
            choices_text += f"{string.ascii_lowercase[index]}) {value}\n"

        return choices_text

    def build_markdown(self, examcode=None):
        """
        Generate a markdown file of the exam.
        """
        
        script_directory = os.path.abspath(os.path.dirname(__file__))
        questions = ""
        result = ""

        # Processing questions
        for index, question in enumerate(self.questions):
            with open(os.path.join(script_directory, "template", "question-template.md")) as f:
                question_text = question.question

                choices = question.choices
                choices_text = self._format_choices(choices)

                t = Template(f.read())
                questions += t.substitute({"number": index+1,
                                        #    "marks": "1,0",
                                           "content": question_text,
                                           "answers": choices_text})

        # Combine everything in the exam template
        with open(os.path.join(script_directory, "template", "exam-template.md")) as f:
            t = Template(f.read())
            result = t.substitute({"institution": self.exam.institution,
                                   "course": self.exam.course,
                                   "professor": self.exam.professor,
                                   "exam": self.exam.exam,
                                   "questions": questions,
                                   "examcode": f"#{examcode}" if examcode is not None else ""})

        generated_md_filepath = os.path.join(self.exam_directory, f"{self.exam_name}-generated.md")
        with open(generated_md_filepath, "w") as f:
            f.write(result)

    def generate_pdf(self, output_name=None, folder=False):
        """
        It uses pandoc to convert the markdown file in a pdf.

        @output_name: the name of the pdf file. It uses the exam file name by default.
        @folder: add the pdf file in the folder with this name. It uses the current directory by default.
        """
        
        script_directory = os.path.abspath(os.path.dirname(__file__))
        generated_md_filepath = os.path.join(self.exam_directory, f"{self.exam_name}-generated.md")
        media_filepath = os.path.join(self.exam_directory, "media")

        if output_name is None:
            output_name = self.exam_name

        if folder:
            output_name = os.path.join(folder, output_name)

        output_filepath = os.path.join(self.exam_directory, f"{output_name}.pdf")

        os.system(f"pandoc --webtex='https://latex.codecogs.com/svg.latex?' --metadata pagetitle='examgen' -t html5 '{generated_md_filepath}' -o '{output_filepath}' --css '{script_directory}/template/style.css' --extract-media '{media_filepath}' --resource-path '{self.exam_directory}'")
        
        # remove temp files
        os.remove(generated_md_filepath)
        
        if os.path.exists(media_filepath):
            shutil.rmtree(media_filepath)

    def generate_answers(self, output_name=None, folder=False):
        """
        Generate the answers of an exam.

        @output_name: the name of the answers file is this parameter + "-answers.txt".
                      It uses the exam file name + "-answers.txt" by default.
        @folder: add the answers file in the folder with this name. It uses the current directory by default.
        """
        if output_name is None:
            output_name = self.exam_name

        if folder:
            output_name = os.path.join(folder, output_name)

        output_filepath = os.path.join(self.exam_directory, f"{output_name}-answers.txt")

        with open(output_filepath, "w") as f:
            for index, value in enumerate(self.questions):
                f.write(f"{index+1} - {string.ascii_lowercase[value.correct_index]}\n")

    def generate(self):
        """
        Shortcut method to build markdown, generate pdf and answer key.
        """
        self.build_markdown()
        self.generate_pdf()
        self.generate_answers()


class Batch(object):
    """
    A helper class to generate multiple tests.
    It is useful to generate random exams.
    """
    def __init__(self, exam_path, quantity, random_questions=False,
                 random_answers=False, merge=False, front_and_back=False):
        """
        Constructor.

        @exam_path: the exam filename.
        @quantity: the number of exams to generate.
        @random_questions: True to shuffle the questions, False to keep the order.
        @random_answers: True to shuffle the choices, False to keep the order.
        @merge: True to merge all exams in one pdf, False to not merge.
        @front_and_back: True to generate a pdf to be printed front and back, False to print only in the front.
                         This is only used if the merge parameter is True.
        """

        self.exam_path = exam_path
        self.quantity = quantity
        self.random_questions = random_questions
        self.random_answers = random_answers
        self.merge = merge
        self.front_and_back = front_and_back

        self.exam_directory = os.path.dirname(self.exam_path)
        self.exam_file = os.path.basename(self.exam_path)
        self.exam_name = self.exam_file.split(".")[0]

    def generate(self):
        """
        Generate multiple exams.
        """
        
        batch_directory = os.path.join(self.exam_directory, "batch")
        os.makedirs(batch_directory, exist_ok=True)  
      
        for i in range(self.quantity):
            exam = Exam(self.exam_path, random_questions=self.random_questions,
                        random_answers=self.random_answers)

            exam.build_markdown(examcode=i)
            exam.generate_pdf(f"{self.exam_name}-{i}", folder=batch_directory)
            exam.generate_answers(f"{self.exam_name}-{i}", folder=batch_directory)

        if self.merge:
            merger = PdfFileMerger()
            
            for i in range(self.quantity):
                pdf_file_path = os.path.join(batch_directory, f"{self.exam_name}-{i}.pdf")

                if self.front_and_back:
                    self._add_blank_page_if_odd(pdf_file_path)

                merger.append(pdf_file_path, import_bookmarks=False)

            pdf_merge_file_path = os.path.join(batch_directory, f"{self.exam_name}-merge.pdf")
            with open(pdf_merge_file_path, 'wb') as f:
                merger.write(f)

    def _add_blank_page_if_odd(self, filepath):
        with open(filepath, "rb") as pdf_file:
            pdf = PdfFileReader(pdf_file)
            n_pages = pdf.getNumPages()
            
            if n_pages > 1 and (n_pages % 2 == 1):
                out_pdf = PdfFileWriter()
                out_pdf.appendPagesFromReader(pdf)
                out_pdf.addBlankPage()
                out_stream = open('/tmp/examgentemp.pdf', 'wb')
                out_pdf.write(out_stream)
                out_stream.close()
        
                shutil.move('/tmp/examgentemp.pdf', filepath)
        