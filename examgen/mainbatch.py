from examgen import Batch

batch = Batch("exam1", 3, random_answers=True, merge=True, front_and_back=True)
batch.generate()
