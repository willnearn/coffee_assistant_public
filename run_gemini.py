import os
import pathlib
import textwrap
from flask import Flask, request, jsonify, render_template, send_from_directory

import google.generativeai as genai
from google.generativeai.types.generation_types import BlockedPromptException
from google.generativeai.types import generation_types

from IPython.display import Markdown
# Used to securely store your API key
#from google.colab import userdata #I can't pip install google.colab. Not sure what's up with this. TODO: Look into this later

def to_markdown(text): #Not sure why they include this before some of the more important setup stuff
  text = text.replace('•', '  *')
  return Markdown(text) #Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
app = Flask(__name__)


# CONFIGURATION
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)
line_separator = "\n\n====================================================================================================\n\n"
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
chat = model.start_chat()
with open("heavenly_background_information.txt","r") as f:
  setting_message = f.read()


#RUN THE CHAT
#chat = model.start_chat(history=[{
#    "role": "user",
#    "parts": ["Can you generate a good welcome message for me? But don't comment that you're giving a welcome message, just give it naturally"]
#  },])
@app.route('/', methods=['POST'])
def process_string():
  data = request.get_json()
  user_message = data.get('input_string')
  try: 
    response = chat.send_message(user_message) #TODO: Stream functionality in the future. #TODO: Accept pictures as well? Let gemini-pro-vision and UmiChat develop first.
    output_string = to_markdown(response.text).data
  except generation_types.StopCandidateException as e:
    output_string = f"I'm sorry, the generation stopped due to a StopCandidateException. We have to hold high safety standards here to avoid misuse, so I hope that this doesn't bother you. If you believe that this was an error, try your question again!"
  except BlockedPromptException as e: #Handle offensive user inputs so that the program won't stop execution
    for f in e.args[0].safety_ratings:
      if f.probability > f.HarmProbability.MEDIUM.value:
        output_string = "Sorry, we couldn't process the request because the prompt was deemed unsafe in "+f.category.name +" with a "+f.probability.name+" risk. We have to keep our safety settings very conservative to avoid law suits, so I hope you understand :)"
  except Exception as e: # Fall-through
     output_string = "I'm sorry, but there's been an error in our system. Please try again in a bit"
  return jsonify({'output_string':output_string})

@app.route('/initial_message')
def get_initial_message():
    try:
      response = chat.send_message(setting_message)
      output_string = to_markdown(response.text).data
    except ValueError as e: #Handle offensive responses from Gemini so that the program won't stop execution
      for f in response.prompt_feedback.safety_ratings:
        if f.probability > f.HarmProbability.MEDIUM.value:
          output_string = "Sorry, we couldn't process the request because the answer was deemed unsafe in "+f.category.name +" with a "+f.probability.name+" risk. We have to keep our safety settings very conservative to avoid law suits, so I hope you understand :)"
    return jsonify({'initialMessage': output_string})


@app.route('/')
def serve_front_end():
    return render_template('umichat.html')

# Route to serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=True)