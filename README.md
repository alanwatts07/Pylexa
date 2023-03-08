# Pylexa
A python alexa using openai, replicate, and gtts to create a better version of alexa.

Features
1) A text file transcription of what is heard and replied.
2) Transcribes audio to text with openai whisper and feeds it into openai for a response.
3) Detects the word image and returns a generated image using replicate and stable-diffusion.
4) Remembers as many lines of the conversation as you want (edit in the pylexa.py)
5) Change record length also in the pylexa.py file.
6) Recommended use is with VisualStudio with a split window. One can be open to image.png and one to trans.txt to watch everything.

Setup
1) Get openai and replicate api keys.
2) OpenAi key goes on pylexa.py where is says 'YOUR_API_KEY'
3) Load your replicate api key as an environment variable exacatly like so in terminal:
export REPLICATE_API_TOKEN='YOUR_API_KEY'
4) Now you just run python3 pylexa.py and be ready to record your audio=]
