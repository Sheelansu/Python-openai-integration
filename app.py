import gradio as gr
import openai

openai.api_key = open("key.txt", "r").read().strip("\n")

message_history = []

def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history
    )

    reply_content = completion.choices[0].message.content
    
    message_history.append({"role": "assistant", "content": f"{reply_content}"}) 
    
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]  # convert to tuples of list
    return response

# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo: 

    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot() 

    # creates a new Row component, which is a container for other components.
    with gr.Row(): 
        
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
  
    txt.submit(predict, txt, chatbot) 

    txt.submit(None, None, txt, _js="() => {''}") 
demo.launch()