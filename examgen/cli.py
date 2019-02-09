import os
import click

try:
    # when run cli.py through the installed script
    from examgen.examgen import Exam, Batch
except ModuleNotFoundError:
    # when run cli.py directly
    from examgen import Exam, Batch


@click.command()
@click.option("-e", "--exam", "exam", required=True, type=click.File())
@click.option("-rq", "--random-questions", "random_questions", is_flag=True)
@click.option("-ra", "--random-answers", "random_answers", is_flag=True)
@click.option("-b", "--batch", "batch", is_flag=True)
@click.option("-q", "--quantity", "quantity", type=int)
@click.option("-m", "--merge", "merge", is_flag=True)
@click.option("-fb", "--front-and-back", "front_and_back", is_flag=True)
def generate(exam, random_questions, random_answers, batch,
             quantity, merge, front_and_back):
    
    exam_path = os.path.abspath(exam.name)

    if batch:
        if quantity is None:
            raise click.UsageError("You must define the quantity in the batch generation.")

        batch = Batch(exam_path, quantity, random_answers=random_answers,
                      random_questions=random_questions, merge=merge,
                      front_and_back=front_and_back)
        batch.generate()
    else:
        exam = Exam(exam_path, random_answers=random_answers,
                    random_questions=random_questions)
        exam.generate()
  

if __name__ == "__main__":
    generate()