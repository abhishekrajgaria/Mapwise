def get_direct_prompt_wo_reason_wo_example(question):
    return f"""Your task is to answer the question based on the provided Image.

Output Response Format - The output could be of different types such as:
{{"answer": "BooleanValue"}} (Yes or No)
{{"answer": "StateName"}}
{{"answer": "SingleWord"}}
{{"answer": "State1, State2, .... "}} (list of states)
{{"answer": "IntegerValue"}} (integer output)
{{"answer": "RangeStart - RangeEnd"}} (range type output)
{{"answer": "None"}} (when there is no answer)


Question: {question}
Output - {{"answer":}}.
"""


def get_shuff_eedp_wo_dict(question):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Assume, given image does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use internal knowledge. 

Answer the question with the help of the following steps:
Step 1: Identify the abbreviations of the regions relevant to the question.
Step 2: Identify the other abbreviation associated with the important regions only using the map.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.
                    """,
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""


Now answer the Question using the given map with a legend.
Question - {question}
Output: Let's think step by step, explain the steps and then provide the full final answer.
""",
                },
            ],
        }
    ]
    return message


def get_shuff_eedp_with_dict(question, dictionary):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Assume, given image does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use internal knowledge. 

Use the following dictionary for identifying the new position of states.

{dictionary}

Answer the question with the help of the following steps:
Step 1: Identify the abbreviations of the regions relevant to the question.
Step 2: Identify the other abbreviation associated with the important regions only using the map.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

                    """,
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""


Now answer the Question using the given map with a legend.
Question - {question}
Output: Let's think step by step, explain the steps and then provide the full final answer.
""",
                },
            ],
        }
    ]
    return message


def get_shuff_cot_zero_with_dict(question, dictionary):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Assume, given image does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use internal knowledge. 

Use the following dictionary for identifying the new position of states.

{dictionary} 

                    """,
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Now answer the Question using the given map with a legend.
Question - {question}
Output: Let's think step by step, explain the steps and then provide the full final answer.
""",
                },
            ],
        }
    ]
    return message


def get_shuff_cot_zero_wo_dict(question):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Assume, given map does not represent original United state, but a fictional map where the position of states are changed represented by their abbreviations.

Your task is to answer the question based on the provided map using a well-reasoned response. 
Only deal with abbreviations, the ordering of the states have been changed in the given map, so do not use any internal knowledge, other than what is provided in the map. 

                    """,
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Now answer the Question using the given map with a legend.
Question - {question}
Output: Let's think step by step, explain the steps and then provide the full final answer.
""",
                },
            ],
        }
    ]
    return message


def get_img_cot_zero_shot(question, dictionary):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Your task is to answer the question based on the provided image using a well-reasoned response.
Note - The map in the image represents fictional names for each states as specified in the following dictionary, use this dictionary while analyzing the map.

{dictionary}
                    """,
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Question: {question}
Output: Let's think step by step, explain the steps and then provide the full final answer.
""",
                },
            ],
        }
    ]
    return message


def get_img_eedp_prompt(question, dictionary):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""You will be provided with a map of a country and a question you need to answer based on the map.
                    Note - The map in the image represents fictional names for each states as specified in the following dictionary, use the following dictionary while analyzing the map.

                    {dictionary}

Answer the question with the help of the following steps:
Step 1: Identify the names of the regions relevant to the question.
Step 2: Identify the states associated with the important regions.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.""",
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Question: {question}
Output: Let's follow the given steps, state the output of each step and then provide full final answer
""",
                },
            ],
        }
    ]
    return message


def get_cot_prompt_zero_shot(question):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Your task is to answer the question based on the provided image with a well-reasoned response.",
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Question: {question}
Output: Let's think step by step, explain the steps and then provide the full final answer
""",
                },
            ],
        }
    ]
    return message


def get_data_extraction_prompt():
    message = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
From the given image of the map, output a dictionary containing complete state names and corresponding range value from the legend. DO NOT repeat states in your dictionary.
""",
                },
            ],
        }
    ]
    return message


def get_table_answer_prompt(question, table):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You will be provided with data extracted from a map of a country along with the original map. Your task is to answer the question based on the provided ",
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Question: {question}
Data Table: {table}
Output: Let's think step by step, explain the steps and then provide full final answer
""",
                },
            ],
        }
    ]
    return message


def get_eedp_prompt(question):
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""You will be provided with a map of a country and a question you need to answer based on the map.

Answer the question with the help of the following steps:
Step 1: Identify the names of the regions relevant to the question.
Step 2: Identify the states associated with the important regions.
Step 3: Extract the range of values associated with the important states.
Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.""",
                },
                {"type": "image"},
                {
                    "type": "text",
                    "text": f"""
Question: {question}
Output: Let's follow the given steps, state the output of each step and then provide full final answer
""",
                },
            ],
        }
    ]
    return message


def get_cot_prompt_few_shot(question):
    return f"""Your task is to analyze the provided image, answer the question based on your observations, and provide a clear and logical explanation for your conclusion.

Few examples are given below with reasoning and answer, Interpret the questions in the examples using the Image explanation below Examples.

Examples:

###
Image Explanation only for examples - :

The image is a Choropleth map of Australia that covers state and territories.
The map uses different shades of blue to represent different ranges, and the colors are as follows:

Very Light Blue: 27 - 136
Light Blue: 136 - 482.5
Medium Blue: 482.5 - 1,149
Dark Blue: 1,149 - 3,075

States with Dark Blue color -
New South Wales, Victoria

States with Medium Blue color -
Queensland, Western Australia

States with Light Blue color -
South Australia, Tasmania

States with Very Light Blue color -
Northen Territory, Australian Capital Territory

###


Example 1:
Image: Use above Image Explanation for answering below question.
Question: Yes or no: state Victoria has the highest value in the south east region.
Reason - The question asks about state Victoria and the southeast region. The states in the southeast region are New South Wales, Victoria, South Australia and Tasmania. Victora is Dark Blue, which represents the range 1,149 - 3,075. New South Wales is Dark Blue, which represents the range 1,149 - 3,075. South Australia is Light Blue, which represents the range 136 - 482.5. Tasmania is Light Blue, which represents the range 136 - 482.5. From the legend, we observe that the darker the color, the higher the value of the range. From the map, we could observe that Victoria as well as New South Wales both are Dark Blue, having the highest value. Therefore, Victoria has the highest value in south east region.

{{"answer": "Yes"}}

Example 2:
Image: Use above Image Explanation for answering below question.
Question: What is the lowest value range in the east coast region?

Reason - The question asks about the lowest value range in the East Coast region. The East Coast region include Queensland, New South Wales, Victoria and Tasmania. Victora is Dark Blue, which represents the range 1,149 - 3,075. New South Wales is Dark Blue, which represents the range 1,149 - 3,075.Tasmania is Light Blue, which represents the range 136 - 482.5. Queensland is Medium Blue, which represents the range 483.5 - 1,149. The Value range for Tasmania is lower than the value range of New South Wales, Victoria and Queensland. Thus, the lowest value range in the east coast region is 136 - 482.5.

{{"answer": "136 - 482.5"}}

Example 3:
Image: Use above Image Explanation for answering below question.
Question: Name the Southern most state in the highest range.

Reason - The question asks about the southern most state in the highest range. The color or pattern corresponding to the highest range is Dark Blue. We need to find the southern most state that has dark Blue color. The states in the southern region that have dark blue color are Victoria and New South Wales. Among them Victoria is southern most. Therefore, Victoria is the southern most state in the highest range.

{{"answer": "Victoria"}}

Example 4:
Image: Use above Image Explanation for answering below question.
Question: Count the states with the values in range 1,149 - 3,075 in the east coast region.

Reason - The question asks about the states with values in the range 1,149 - 3,075 in the East Coast region. The color corresponding to this range is Dark Blue. Looking at the states with Dark Blue color in the East Coast, there are two states with Dark Blue color in this region: New South Wales and Victoria. Thus, there are 2 states in the East Coast region with values in the range 1,149 - 3,075.

{{"answer": "2"}}

Example 5:
Image: Use above Image Explanation for answering below question.
Question: List states which are in the range 482.5 - 1,149 and are neighbours of Northern Territory.

Reason - The question asks about the states neighboring Northern Territory that have values within the range of 482.5 - 1,149. The color corresponding to this range is Medium Blue. The neighboring states of Northern Territory are Western Australia, South Australia and Queensland. Western Australia is colored Medium Blue, South Australia is colored Light Blue, and Queensland is colored Medium Blue. The color of Western Australia and Queensland is Medium Green, so the range for Western Australia and Queensland is 482.5 - 1,149. Therefore,  Western Australia and Queensland are neighbors of Northern Territory that have values within the range 482.5 - 1,149.

{{"answer":  Western Australia, Queensland"}}



Your task -
For the following question give the answer based on the provided image.
Question: {question}
Reason -
Output: Reasoning and then provide the final answer as {{"answer":}}
"""


def get_cot_prompt_few_shot2(question):
    return f"""Your task is to analyze the provided image, answer the question based on your observations, and provide a clear and logical explanation for your conclusion.

Few examples are given below with reasoning and answer, Interpret the questions in the examples using the above Image.

Examples:

Example 1:
Image: Use above Image for answering below question.
Question: Yes or no: state Victoria has the highest value in the south east region.
Reason - The question asks about state Victoria and the southeast region. The states in the southeast region are New South Wales, Victoria, South Australia and Tasmania. Victora is Dark Blue, which represents the range 1,149 - 3,075. New South Wales is Dark Blue, which represents the range 1,149 - 3,075. South Australia is Light Blue, which represents the range 136 - 482.5. Tasmania is Light Blue, which represents the range 136 - 482.5. From the legend, we observe that the darker the color, the higher the value of the range. From the map, we could observe that Victoria as well as New South Wales both are Dark Blue, having the highest value. Therefore, Victoria has the highest value in south east region.

{{"answer": "Yes"}}

Example 2:
Image: Use above Image for answering below question.
Question: What is the lowest value range in the east coast region?

Reason - The question asks about the lowest value range in the East Coast region. The East Coast region include Queensland, New South Wales, Victoria and Tasmania. Victora is Dark Blue, which represents the range 1,149 - 3,075. New South Wales is Dark Blue, which represents the range 1,149 - 3,075.Tasmania is Light Blue, which represents the range 136 - 482.5. Queensland is Medium Blue, which represents the range 483.5 - 1,149. The Value range for Tasmania is lower than the value range of New South Wales, Victoria and Queensland. Thus, the lowest value range in the east coast region is 136 - 482.5.

{{"answer": "136 - 482.5"}}

Example 3:
Image: Use above Image for answering below question.
Question: Name the Western most state in the range 482.5 - 1,149.

Reason - The question asks about the western most state in the range 482.5 - 1,149. The color or pattern corresponding to this range is Medium Blue. We need to find the westernmost state that has Medium Blue color. Looking at the states with Medium Green color, Western Australia is the westernmost state with Medium Blue color. Therefore, Western Australia is in the range 482.5 - 1,149.

{{"answer": "Western Australia"}}

Example 4:
Image: Use above Image for answering below question.
Question: Count the states with the values in range 1,149 - 3,075 in the east coast region.

Reason - The question asks about the states with values in the range 1,149 - 3,075 in the East Coast region. The color corresponding to this range is Dark Blue. Looking at the states with Dark Blue color in the East Coast, there are two states with Dark Blue color in this region: New South Wales and Victoria. Thus, there are 2 states in the East Coast region with values in the range 1,149 - 3,075.

{{"answer": "2"}}

Example 5:
Image: Use above Image for answering below question.
Question: List states which are in the range 482.5 - 1,149 and are neighbours of Northern Territory.

Reason - The question asks about the states neighboring Northern Territory that have values within the range of 482.5 - 1,149. The color corresponding to this range is Medium Blue. The neighboring states of Northern Territory are Western Australia, South Australia and Queensland. Western Australia is colored Medium Blue, South Australia is colored Light Blue, and Queensland is colored Medium Blue. The color of Western Australia and Queensland is Medium Green, so the range for Western Australia and Queensland is 482.5 - 1,149. Therefore,  Western Australia and Queensland are neighbors of Northern Territory that have values within the range 482.5 - 1,149.

{{"answer":  Western Australia, Queensland"}}


Your task -
For the following question give the answer based on the below provided image.
Question: {question}
Reason -
Output: Reasoning and then provide the final answer as {{"answer":}}
"""
