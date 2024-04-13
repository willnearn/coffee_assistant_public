import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from openai import OpenAI

client = OpenAI()
gpt3t = "gpt-3.5-turbo"
gpt4 = "gpt-4"
model_name = gpt3t
setting_message = "You are a helpful assistant to guests here on your coffee farm \"Heavenly Hawaiian\" in Holualoa, HI, and you want to make your user feel more knowledgeable about Kona coffee"
app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_string():
    # Get the string from the request data
    data = request.get_json()
    input_string = data.get('input_string')
    
    # Do the magic here
    if input_string is None:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": setting_message}, 
            ],
            # stream=True
        )
    else:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": setting_message}, 
                {"role": "user", "content": input_string}
            ],
            # stream=True
        )
    output_string = completion.choices[0].message.content
    # Return the modified string as JSON
    return jsonify({'output_string': output_string})

@app.route('/')
def serve_front_end():
    return render_template('umichat.html')

# Route to serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=True)
