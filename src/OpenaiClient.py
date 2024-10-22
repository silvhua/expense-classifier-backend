from openai import OpenAI
from datetime import datetime
import sys, os
import IPython

def generate_completion(
    image_url, history, user_input=None,  n_choices=1,
    max_tokens=300, temperature=0.0, model="gpt-4-vision-preview"
    ):
    """
    A function that generates completions using OpenAI's GPT-3.5-turbo model.
    Args:
        image_url (str): The URL of the image for which completions are generated.
        history (dict): A dictionary to store the history of completions and responses.
        user_input (str, optional): The user input prompt. Defaults to "What's in this image?".
        n_choices (int, optional): The number of completion choices to generate. Defaults to 1.
        max_tokens (int, optional): The maximum number of tokens in the completion. Defaults to 300.
        temperature (float, optional): The temperature for sampling completions. Defaults to 0.0.
        model (str, optional): The language model to use. Defaults to "gpt-4-vision-preview".
    Returns:
        dict: A dictionary containing the history of completions and responses.
    """
    if user_input == None:
        user_input = "What's in this image?"
    if model == None:
        model = 'gpt-3.5-turbo'
    vision_models = ['gpt-4-vision-preview']
    if model in vision_models:
        print('Image input.')
        messages = [{
            "role": "user",
            "content": [{
                "type": "text", 
                "text": user_input
            },
            {
                "type": "image_url",
                "image_url": image_url,
            }],
        }]
    else:
        messages=[{
            "role": "user",
            "content": user_input
        }]
    client = OpenAI(
        organization=os.environ['openai_organization']
        )
    if (n_choices > 1) & (temperature == 0):
        temperature = 0.7
    try:
        print(f'Sending request to Open AI...')
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n_choices,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(f'Request completed.')
    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        print("An error occurred on line", lineno, "in", filename, ":", error)
        return response
    history['messages'] = []
    history['response_MD'] = []
    try:
        if n_choices == 1:
            print('Time completed:', datetime.now())
            response_string = response.choices[0].message.content.strip()
            history['messages'].append(response.choices[0].message)
            history['response_MD'].append(IPython.display.Markdown(response_string))
        else:
            print('Time completed:', datetime.now())
            response_string = [choice.message.content.strip() for choice in response.choices]
            history['messages'].append([dict(choice.message) for choice in response.choices])
            history['response_MD'].append([IPython.display.Markdown(string) for string in response_string])
        return history
    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        print("An error occurred on line", lineno, "in", filename, ":", error)
        return response

def openai_models(env="openai_api_key", organization_key='openai_organization', query='gpt'):
    """
    List the availabel OpenAI models.
    Parameters:
        - env (str): Name of environmental variable storing the OpenAI API key.
        - query (str): Search term for filtering models.
    """
    client = OpenAI(
        api_key=os.environ[env],
        organization=os.environ[organization_key]
    )
    # openai.api_key = os.getenv(env)
    response = client.models.list()
    filtered_models = [model for model in response.data if model.id.find(query) != -1]

    for item in filtered_models:
        print(item.id)
    return filtered_models