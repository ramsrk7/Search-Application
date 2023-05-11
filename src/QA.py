from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")

context = context = r"""Chelsea's mini-revival continued with a third victory in a row as they consigned struggling Leicester City to a fifth consecutive defeat.
Buoyed by their Champions League win over Borussia Dortmund, Chelsea started brightly and Ben Chilwell volleyed in from a tight angle against his old club.
Chelsea's Joao Felix and Leicester's Kiernan Dewsbury-Hall hit the woodwork in the space of two minutes, then Felix had a goal ruled out by the video assistant referee for offside.
Patson Daka rifled home an excellent equaliser after Ricardo Pereira won the ball off the dawdling Felix outside the box.
But Kai Havertz pounced six minutes into first-half injury time with an excellent dinked finish from Enzo Fernandez's clever aerial ball.
Mykhailo Mudryk thought he had his first goal for the Blues after the break but his effort was disallowed for offside.
Mateo Kovacic sealed the win as he volleyed in from Mudryk's header.
The sliding Foxes, who ended with 10 men following Wout Faes' late dismissal for a second booking, now just sit one point outside the relegation zone.
""".replace('\n', ' ')

inputs = tokenizer(context, return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
question, answer = question_answer.split(tokenizer.sep_token)

print("question:", question)
print("answer:", answer)
