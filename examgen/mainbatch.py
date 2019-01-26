from examgen import BatchGenerator

batch = BatchGenerator()
batch.generate("exam1", 5, random_questions=True, random_answers=True, merge=True)
