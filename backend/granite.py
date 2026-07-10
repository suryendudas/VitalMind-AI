import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters

load_dotenv()

_model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=Credentials(
        api_key=os.environ["IBM_API_KEY"],
        url=os.environ["IBM_URL"],
    ),
    project_id=os.environ["IBM_PROJECT_ID"],
)

_params = TextChatParameters(
    max_tokens=1024,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.05,
)


def generate_response(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    response = _model.chat(messages=messages, params=_params)
    return response["choices"][0]["message"]["content"]
