from openai import OpenAI
from datetime import datetime
import sys, os

class OpenaiClient:
    def __init__(self, history=[]):
        """
        Initializes the OpenaiClient instance.

        Args:
            history (list, optional): A list to store the history of completions and responses. Defaults to an empty list.
        """
        self.client = OpenAI(
            organization=os.environ.get('OPENAI_ORGANIZATION')
        )
        self.history = history

    def generate_completion(
        self, user_input=None, image_url=None, n_choices=1,
        max_tokens=300, temperature=0.0, model="gpt-4o-mini"
    ):
        """
        A method that generates completions using a OpenAI model.

        Documentation: https://platform.openai.com/docs/api-reference/chat/create?lang=python

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

        Example usage:
        client = OpenaiClient()
        client.generate_completion(
            "Enter prompt here...",
            max_tokens=300
            )
        """
        if user_input is None:
            user_input = "What's in this image?"
        if model is None:
            model = 'gpt-4o-mini'
        if image_url is not None:
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
            messages = [{
                "role": "user",
                "content": user_input
            }]
        if (n_choices > 1) & (temperature == 0):
            temperature = 0.7
        if (n_choices > 1) & (temperature == 0):
            temperature = 0.7
        try:
            print(f'Sending request to Open AI...')
            response = self.client.chat.completions.create(
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
        try:
            print('Time completed:', datetime.now())
            if n_choices == 1:
                response_string = response.choices[0].message.content.strip()
                self.history.append(response.choices[0].message)
            else:
                response_string = [choice.message.content.strip() for choice in response.choices]
                self.history.append([dict(choice.message) for choice in response.choices])
            return self.history
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