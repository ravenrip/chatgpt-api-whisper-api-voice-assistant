import gradio as gr

def capitalize_text(input_text):
    return input_text.capitalize()

input_textbox = gr.inputs.Textbox(lines=1, label="Enter text")
output_textbox = gr.outputs.Textbox(label="Capitalized text")

interface = gr.Interface(fn=capitalize_text, inputs=input_textbox, outputs=output_textbox)
interface.launch()