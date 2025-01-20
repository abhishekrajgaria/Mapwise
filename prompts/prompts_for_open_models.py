def get_shuff_eer_wo_dict(question):
    return f"""Assume, given image does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use internal knowledge. 

Answer the question with the help of the following steps:
Step 1: Identify the abbreviations of the regions relevant to the question.
Step 2: Identify the other abbreviation associated with the important regions only using the map.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

Now answer the Question using the given map with a legend.
Question - {question}
Output - Let's think step by step, explain the steps, then provide the final  answer as {{"answer": }}"""


def get_shuff_eer_with_dict(question, dictionary):
    return f"""Assume, given image does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use internal knowledge. 

Use the following dictionary for identifying the new position of states.

{dictionary}

Answer the question with the help of the following steps:
Step 1: Identify the abbreviations of the regions relevant to the question.
Step 2: Identify the other abbreviation associated with the important regions only using the map.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

Now answer the Question using the given map with a legend.
Question - {question}
Output - Let's think step by step, explain the steps, then provide the final  answer as {{"answer": }}"""


def get_shuff_cot_zero_with_dict(question, dictionary):
    return f"""
Assume, given image does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use internal knowledge. 

Use the following dictionary for identifying the new position of states.

{dictionary}

Now answer the Question using the given map with a legend.
Question - {question}
Output - Let's think step by step, explain the steps and then provide the final answer as {{"answer":}}
 """


def get_shuff_cot_zero_wo_dict(question):
    return f"""
Assume, given map does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use any internal knowledge, other than what is provided in the map. 

Now answer the Question using the given map with a legend.
Question - {question}
Output - Let's think step by step, explain the steps and then provide the final answer as {{"answer":}}
 """


def get_img_cot_zero_shot_with_dict(question, dictionary):
    return f"""Your task is to answer the question based on the provided image using a well-reasoned response.
Note - The map in the image represents fictional names for each states as specified in the following dictionary, use this dictionary while analyzing the map.

{dictionary}

Question - {question}
Output: Let's think step by step, explain the steps and then provide full final answer."""


def get_img_eer_with_dict(question, dictionary):
    return f"""
You will be provided with a map of a country and a question you need to answer based on the map.
Note - The map in the image represents fictional names for each states as specified in the following dictionary, use the following dictionary while analyzing the map.

{dictionary}

Answer the question with the help of the following steps:
Step 1: Identify the names of the regions relevant to the question.
Step 2: Identify the states associated with the important regions.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

Question: {question}
Output: Let's follow the given steps, state the output of each step and then provide full final answer.
"""


def get_eer_prompt(question):
    return f"""You will be provided with a map of a country and a question you need to answer based on the map.

Answer the question with the help of the following steps:
Step 1: Identify the names of the regions relevant to the question.
Step 2: Identify the states associated with the important regions.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

Question: {question}
Output: Let's follow the given steps, state the output of each step and then provide full final answer"""


def get_cot_prompt_zero_shot(question):
    return f"""Your task is to answer the question based on the provided image with a well-reasoned response.

Question: {question}
Output: Let's think step by step, explain the steps and then provide full final answer
"""


def get_direct_prompt(question):
    return f"""Your task is to answer the question based on the provided Image.

Question: {question}
Output your answer.
"""
