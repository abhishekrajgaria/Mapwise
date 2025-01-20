format_prompt = """

You will be provided with the question, the expected answer format and the model's response. You will have to extract the answer from the model\'s response and represent it in the expected answer format.

Answer format: {answer_format}

Answer Response Format - The answer could be of different types such as:
If the answer format is "Single" the answer can be the name of a State or a Single word.
If the answer format is "Binary" the answer can be either "Yes" or "No"
If the answer format is "Range" the answer will be of the format RangeStart - RangeEnd.
If the answer format is "Count" the answer must be a integer.
If the answer format is "List" the answer will be in the form of "Element1, Element2, Element3..."
Finally the answer can also be "None" if there is no answer.

Must extract answer in the format {{"answer": <answer>}}.

Question: {question}

Model response: {response}

"""
