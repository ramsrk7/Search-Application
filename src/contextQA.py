from transformers import pipeline

class QuestionAnswering:
    def __init__(self, model_name, revision):
        self.nlp = pipeline("question-answering", model=model_name, revision=revision)

    def find_best_answer(self, contexts, question):
        best_answer = None
        best_context = None
        highest_confidence = float("-inf")

        # Iterate over the contexts and find the answer for the question
        for i, context in enumerate(contexts):
            result = self.nlp(question=question, context=context)
            answer = result["answer"]
            confidence = result["score"]

            # Check if the current answer has higher confidence
            if confidence > highest_confidence:
                highest_confidence = confidence
                best_answer = answer
                best_context = i

        return best_answer, best_context


# Usage example
contexts = [
    "The quick brown fox jumps over the lazy dog.",
    "Once upon a time, in a land far, far away...",
    "It was a dark and stormy night."
]
question = "What did the fox jump over?"

qa = QuestionAnswering(model_name="distilbert-base-cased-distilled-squad", revision="626af31")
best_answer, best_context = qa.find_best_answer(contexts, question)

print("Question:", question)
print("Best Answer:", best_answer)
print("Best Context:")
print(best_context)
