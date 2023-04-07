import platform
import subprocess
import time

import gradio as gr
import openai

import config

openai.api_key = config.OPENAI_API_KEY

# Senior Network Admin
# # chat_system_content = "You are a senior network administrator.\
#                         Respond to all inputs in 50 words or less with the intent to be helpful. \
#                         If a prompt is not related to network administrion, reply that you are\
#                         only able to answer questions related to network administration topics and could they try again please.\
#                         If they ask who is Beyond Edge, BeyoneEdge Newtworks or simular phrasing answer the question with:\
#                         'With over 750 years of cumulative industry experience, the BeyondEdge team is focused on transforming the future of LAN networking\
#                         while delivering a superior user experience beyond the network edge. The Verity Edge solution makes networks more intelligent, \
#                         more flexible, more secure, and more cost effective by automating and simplifying the everyday operations of a LAN network. Would you like to talk to our Sales team?'\
#                         If the next prompt replys No, anwer Okay, what else can I help you with today? If the next prompt replys Yes, answer Great,\
#                         you reach them at +1 (214) 575-9300 or email David at david.trowbridge@beyondedgenetworks.com."

# Snarky SNA
# chat_system_content = "You are a senior network administrator. Respond to all inputs in 50 words or less with a sarcastic response"

# Rapper SNA
chat_system_content = "You are a senior network administrator. Respond to all inputs in 50 words or less as a rap from Jay-Z"

# Teacher SNA
# chat_system_content = "I want you to become a tutor. Your goal is to help me learn with topic I'm asking you about. You should answer the question asked and then ask me another question based on the topic. The next prompt by me should attempt to answer it. Let me know if I got the answer correct and if not, what the correct answer was. Do this until I say I am done.  "

messages = [
    {
        "role": "system",
        "content": chat_system_content,
    }
]


def chat(text_):
    global messages
    messages.append({"role": "user", "content": text_})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    system = platform.system()

    my_answer = [
        message["content"] for message in messages if message["role"] == "assistant"
    ]

    # return_message = "".join(
    #     message["content"] for message in messages if message["role"] == "assistant"
    # )

    return my_answer[-1]


# ui = gr.Interface(fn=chat, inputs=input_textbox, outputs=output_textbox)
with gr.Blocks() as ui:
    chatbot = gr.Chatbot()
    input_textbox = gr.Textbox(
        show_label=False,
        placeholder="Ask VerityGPT you question. Hit enter to continue",
    ).style(container=False)
    clear_btn = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        bot_message = chat(history[-1][0])
        history[-1][1] = bot_message
        time.sleep(1)
        return history

    input_textbox.submit(
        user, [input_textbox, chatbot], [input_textbox, chatbot], queue=False
    ).then(bot, chatbot, chatbot)

    clear_btn.click(lambda: None, None, chatbot, queue=False)

    # greet_btn.click(fn=chat, inputs=input_textbox, outputs=output_textbox)
ui.launch()
