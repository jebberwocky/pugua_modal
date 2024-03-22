
from __future__ import annotations

from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, asgi_app

import urllib.request
import urllib.parse
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from pugua_keys import *

def get_links(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    return html

class TheBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        chat_model = ChatOpenAI(temperature=1,
                                model_name="gpt-4",
                                openai_api_key=get_openai_key())
        messages = []
        gua = ""
        for message in request.query:
            if message.role == "bot":
                messages.append(AIMessage(content=message.content))
            elif message.role == "system":
                messages.append(SystemMessage(content=message.content))
            elif message.role == "user":
                gua = get_links("http://colbt.cc:8686/suangua?seed"+urllib.parse.quote(message.content))
                the_prompt = "你是一个只解释易经卦像的bot, 关连"+message.content+"为主题来解释以下易经卦像:"+gua
                print(the_prompt)
                messages.append(HumanMessage(content=the_prompt))

        response = chat_model.invoke(messages).content
        print(response)
        if isinstance(response, str):
            response = "卦: " +" ".join(json.loads(gua)[4])+ "解读: "+ response
            yield fp.PartialResponse(text=response)
        else:
            yield fp.PartialResponse(text="There was an issue processing your query.")

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(
            introduction_message="请随意输入些文字, 将从输入的文字请卦. "
        )


REQUIREMENTS = ["fastapi-poe==0.0.36", "langchain==0.1.13", "openai==1.14.2","langchain-openai==0.1.0","langchain-core==0.1.33"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("gua")

def get_openai_key():
    return OPENAI_API_KEY



@stub.function(image=image)
@asgi_app()
def fastapi_app():
    # Optionally, provide your Poe access key here:
    # 1. You can go to https://poe.com/create_bot?server=1 to generate an access key.
    # 2. We strongly recommend using a key for a production bot to prevent abuse,
    # but the starter examples disable the key check for convenience.
    # 3. You can also store your access key on modal.com and retrieve it in this function
    # by following the instructions at: https://modal.com/docs/guide/secrets
    bot = TheBot()
    POE_ACCESS_KEY = POE_ACCCESS_KEY
    # app = make_app(bot, access_key=POE_ACCESS_KEY)
    app = fp.make_app(bot, access_key=POE_ACCESS_KEY)
    return app