# Pylexa
A python alexa using openai, replicate, and gtts to create a better version of alexa.

![Screenshot](https://user-images.githubusercontent.com/98160685/223595759-ab60ba6d-a3de-47d6-9d8f-ed8b2c8038b8.png)

# Features
1) A text file transcription of what is heard and replied.
2) Transcribes audio to text with openai whisper and feeds it into openai for a response.
3) Detects the word image and returns a generated image using replicate and stable-diffusion.
4) When image is created, response will use a model that creates text descriptions of images from the generated image. (It actually knows what is in the image it is sending back to you)
5) Remembers as many lines of the conversation as you want (edit in the pylexa.py)
6) Change record length also in the pylexa.py file.
7) Recommended use is with VisualStudio with a split window. One can be open to image.png and one to trans.txt to watch everything.

# Setup
1) Get openai and replicate api keys.
2) Clone the repository
3) pip install -r requirements.txt
4) OpenAi key goes on pylexa.py where is says 'YOUR_API_KEY'
5) Load your replicate api key as an environment variable exacatly like so in terminal:
export REPLICATE_API_TOKEN='YOUR_API_KEY'
6) Now you just run python3 pylexa.py and be ready to record your audio=]

