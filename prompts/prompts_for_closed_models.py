def get_shuff_eer_with_dict(question, dictionary):
    return f"""
    Assume, given map does not represent original United state, but a fictional map where the position of states are shuffled, new position are represented by their abbreviations.

    Your task is to answer the question based on the provided map using a well-reasoned response.
    Only deal with abbreviations, the ordering of the states have been changed in the given map.

    Use the following dictionary for identifying the new position of states. The structure of the dictionary is as follows:
    The position of state in the key is changed to the posiiton of the state in the value.

    Shuffled dictionary:
    {dictionary}

    Answer the question with the help of the following steps:
    Steps:
    Step 1: Identify the abbreviations of the regions relevant to the question.
    Step 2: Identify the other abbreviation associated with the important regions only using the map.
    Step 3: Extract the range of values associated with the important states.
    Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

    Then provide the Final Answer as {{"answer":}}

    Output Response Format:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)


    You Task
    Follow the above steps to answer the following question based on the given image and provide a final answer as {{"answer":}}.

    Question - {question}

    Steps:
    """


def get_shuff_eer_wo_dict(question):
    return f"""
    Assume, given map does not represent original United state, but a fictional map where the position of states are shuffled, new position are represented by their abbreviations.

    Your task is to answer the question based on the provided map using a well-reasoned response.
    Only deal with abbreviations, the ordering of the states have been changed in the given map.

    Answer the question with the help of the following steps:
    Steps:
    Step 1: Identify the abbreviations of the regions relevant to the question.
    Step 2: Identify the other abbreviation associated with the important regions only using the map.
    Step 3: Extract the range of values associated with the important states.
    Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

    Then provide the Final Answer as {{"answer":}}

    Output Response Format:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)


    You Task
    Follow the above steps to answer the following question based on the given image and provide a final answer as {{"answer":}}.

    Question - {question}

    Steps:
    """


def get_shuff_cot_zero_with_dict(question, dictionary):
    return f"""
    Assume, given map does not represent original United state, but a fictional map where the position of states are shuffled, new position are represented by their abbreviations.

    Your task is to answer the question based on the provided map using a well-reasoned response.
    Only deal with abbreviations, the ordering of the states have been changed in the given map.

    Use the following dictionary for identifying the new position of states. The structure of the dictionary is as follows:
    The position of state in the key is changed to the posiiton of the state in the value.

    Shuffled dictionary:
    {dictionary}

    Output Response Format:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)


    Question - {question}
    Output - Let's think step by step, explain the steps and then provide the final answer as {{"answer":}}
    """


def get_shuff_cot_zero_wo_dict(question):
    return f"""
    Assume, given map does not represent original United state, but a fictional map where the position of states are shuffled, new position are represented by their abbreviations.

    Your task is to answer the question based on the provided map using a well-reasoned response.
    Only deal with abbreviations, the ordering of the states have been changed in the given map.

    Output Response Format:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)


    Question - {question}

    Output - Let's think step by step, explain the steps and then provide the final answer as {{"answer":}}
    """


def get_img_cot_zero_shot_with_dict(question, dictionary):
    return f"""Your task is to answer the question based on the provided image using a well-reasoned response.
    Note - The map in the image represents fictional names for each states as specified in the following dictionary, use this dictionary while analyzing the map.

    Imaginary Dictionary:
    {dictionary}

    Output Response Format:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)

    Question - {question}
    Output: Let's think step by step, explain the steps and then provide final answer as {{"answer":}}."""


def get_img_eer_with_dict(question, dictionary):
    return f"""
    Answer the question based on the provided image using a well-reasoned response.
    Note - The map in the image represents fictional names for each states as specified in the following dictionary, use this dictionary while analyzing the map.

    Imaginary Dictionary:
    {dictionary}

    Answer the question with the help of the following steps:
    Steps:
    Step 1: Identify the abbreviations of the regions relevant to the question.
    Step 2: Identify the other abbreviation associated with the important regions only using the map.
    Step 3: Extract the range of values associated with the important states.
    Step 4: Answer the question based on the extracted information by thinking step by step and providing a well-reasoned response.

    Then provide the Final Answer as {{"answer":}}

    Output Response Format:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)

    You Task
    Follow the above steps to answer the following question based on the given image and provide a final answer as {{"answer":}}.

    Question - {question}

    Steps:

    """


def get_eer_prompt(question):
    return f"""
        You should answer the question step by step, explicitly stating the answer for each step. Your final answer should be in the format of answer: <answer>
        You are an expert at answering questions based on maps. You will be given a map and a question and you will have to answer the question through the following four steps. 
        
        Make sure to answer the question step by step strictly following the 4 steps mentioned and answering only on the basis of the map provided.",
        Steps:
        Step 1: Extract the names of the regions which are relevant for answering the given question.
        
        For the given question, you will have to extract the names of all the relevant regions which are required for answering the question. If the question mentions a state directly, also consider that in the list of relevant regions.
        
        Here are a few examples:
        Question: Is the average population greater for places in the East Coast compared to that of New York?
        Regions: ["States in the East Coast", "New York"]
        
        Question: Yes or No: The average GDP of states bordering Beijing is less than the GDP of states bordering South China Sea.
        Regions: ["States bordering Beijing", "States bordering South China Sea"]
        
        Question: Name the state with the least crop sales among the states in the NorthEast region.
        Regions: ["States in the NorthEast region"]
        
        Your answer should be in the format of a list with the names of all the relevant regions.
        Step 2: Extract the names of the states in the relevant regions
        
        For each relevant region, extract the names of the states which fall in the region and would be required for answering the questions.
        
        Here are a few examples:
        Map of country: USA
        Regions: ["States in the East Coast", "States in the West Coast"]
        States: {{"States in the East Coast" : ["Washington", "Oregon", "California", "Alaska", "Hawaii"], "New York": ["New York"]}}
        
        Map of country: China
        Regions: ["States bordering Beijing", "States bordering South China Sea"]
        States: {{"States bordering Beijing" : ["Hebei", "Tianjin", "New Mexico", "Texas"], "States bordering South China Sea" : ["Guangdong", "Fujian", "Zhejiang", "Hainan", "Guangxi"]}}
        
        Map of country: India
        Regions: ["States in the NorthEast Region"]
        States: {{"States in the NorthEast Region" : ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura", "Sikkim"]}}
        
        Your answer should be in the format of a dictionary as shown in the examples.
        Step 3: Extract the values corresponding to the states from the given map.
        
        For all the relevant states extracted in step 2, you will have to refer to the map and extract the corresponding values for those states from the map by using the legend given in the map.
        
        Do this for each state individually. You can treat this as a task for simply extracting values from a map according to the legend. 
        
        For each relevant state "X" in the list, answer the question "What is the value for state X in the given map?"
        
        Report all answers at the end in the form of a table.
        Step 4: Answering the question based on the extracted data.
        
        To answer the question you have to use the table of states and their corresponding values as extracted in step 3. For answering the question, you should use reasoning and think step by step to arrive at the final answer. State all your reasoning steps.

        Then provide the Final Answer as {{"answer":}}

        Output Response Format:
        {{"answer": "BooleanValue"}} (Yes or No)
        {{"answer": "StateName"}}
        {{"answer": "SingleWord"}}
        {{"answer": "State1, State2, .... "}} (list of states)
        {{"answer": "IntegerValue"}} (integer output)
        {{"answer": "RangeStart - RangeEnd"}} (range type output)
        {{"answer": "None"}} (when there is no answer)

        Your Task
        Follow the above steps to answer the following question based on the given map and provide a final answer as {{"answer":}}.

        Question: {question}

        Steps:
        """


def get_non_dec_order(context):
    return f"""Your task is to order the states in non-decreasing order from the below provided context, make use of the following symbols for representing the order "<, =". Only give output.

    Context: {context}
    Output - {{"answer":}}
    """


def get_direct_prompt(question):
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


def get_cot_prompt_zero_shot(question):
    return f"""Your task is to answer the question based on the provided image with a well-reasoned response.

    Output Response Format - The output could be of different types such as:
    {{"answer": "BooleanValue"}} (Yes or No)
    {{"answer": "StateName"}}
    {{"answer": "SingleWord"}}
    {{"answer": "State1, State2, .... "}} (list of states)
    {{"answer": "IntegerValue"}} (integer output)
    {{"answer": "RangeStart - RangeEnd"}} (range type output)
    {{"answer": "None"}} (when there is no answer)

    Question: {question}
    Output: Let's think step by step, explain the steps and then provide final answer as {{"answer":}}
"""


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

Few examples are given below with reasoning and answer, Interpret the questions in the examples using the first Image.

Examples:

Example 1:
Image: Use first Image for answering below question.
Question: Yes or no: state Victoria has the highest value in the south east region.
Reason - The question asks about state Victoria and the southeast region. The states in the southeast region are New South Wales, Victoria, South Australia and Tasmania. Victora is Dark Blue, which represents the range 1,149 - 3,075. New South Wales is Dark Blue, which represents the range 1,149 - 3,075. South Australia is Light Blue, which represents the range 136 - 482.5. Tasmania is Light Blue, which represents the range 136 - 482.5. From the legend, we observe that the darker the color, the higher the value of the range. From the map, we could observe that Victoria as well as New South Wales both are Dark Blue, having the highest value. Therefore, Victoria has the highest value in south east region.

{{"answer": "Yes"}}

Example 2:
Image: Use first Image for answering below question.
Question: What is the lowest value range in the east coast region?

Reason - The question asks about the lowest value range in the East Coast region. The East Coast region include Queensland, New South Wales, Victoria and Tasmania. Victora is Dark Blue, which represents the range 1,149 - 3,075. New South Wales is Dark Blue, which represents the range 1,149 - 3,075.Tasmania is Light Blue, which represents the range 136 - 482.5. Queensland is Medium Blue, which represents the range 483.5 - 1,149. The Value range for Tasmania is lower than the value range of New South Wales, Victoria and Queensland. Thus, the lowest value range in the east coast region is 136 - 482.5.

{{"answer": "136 - 482.5"}}

Example 3:
Image: Use first Image for answering below question.
Question: Name the Western most state in the range 482.5 - 1,149.

Reason - The question asks about the western most state in the range 482.5 - 1,149. The color or pattern corresponding to this range is Medium Blue. We need to find the westernmost state that has Medium Blue color. Looking at the states with Medium Green color, Western Australia is the westernmost state with Medium Blue color. Therefore, Western Australia is in the range 482.5 - 1,149.

{{"answer": "Western Australia"}}

Example 4:
Image: Use first Image for answering below question.
Question: Count the states with the values in range 1,149 - 3,075 in the east coast region.

Reason - The question asks about the states with values in the range 1,149 - 3,075 in the East Coast region. The color corresponding to this range is Dark Blue. Looking at the states with Dark Blue color in the East Coast, there are two states with Dark Blue color in this region: New South Wales and Victoria. Thus, there are 2 states in the East Coast region with values in the range 1,149 - 3,075.

{{"answer": "2"}}

Example 5:
Image: Use first Image for answering below question.
Question: List states which are in the range 482.5 - 1,149 and are neighbours of Northern Territory.

Reason - The question asks about the states neighboring Northern Territory that have values within the range of 482.5 - 1,149. The color corresponding to this range is Medium Blue. The neighboring states of Northern Territory are Western Australia, South Australia and Queensland. Western Australia is colored Medium Blue, South Australia is colored Light Blue, and Queensland is colored Medium Blue. The color of Western Australia and Queensland is Medium Green, so the range for Western Australia and Queensland is 482.5 - 1,149. Therefore,  Western Australia and Queensland are neighbors of Northern Territory that have values within the range 482.5 - 1,149.

{{"answer":  Western Australia, Queensland"}}


Your task -
For the following question give the answer based on the second provided image.
Question: {question}
Reason -
Output: Reasoning and then provide the final answer as {{"answer":}}
"""
