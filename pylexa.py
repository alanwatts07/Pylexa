import replicate
import openai
import subprocess
import pyaudio
import wave
from image import create_image
from termcolor import colored
from explain import explain_image
from gtts import gTTS

model = replicate.models.get("openai/whisper")
version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")
openai.api_key = "YOUR_API_KEY"

record_seconds=5
number_lines=-5
#before you start make sure you get your replicate.com api key and add as an env variable
#{type this into console} export REPLICATE_API_TOKEN='token'

def record_audio(record_time):
    # Set the parameters for recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = record_time

    # Create an instance of the PyAudio class
    audio = pyaudio.PyAudio()

    # Open a new stream to record audio
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print(colored("Recording audio...",'red'))

    # Create a list to store the audio frames
    frames = []

    # Record audio in chunks and append to frames list
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print(colored("Finished recording.",'green'))

    # Stop the stream and close the PyAudio instance
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio as a WAV file
    WAVE_OUTPUT_FILENAME = "recorded_audio.wav"
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    print("Audio saved as {}.".format(WAVE_OUTPUT_FILENAME))
    
    return WAVE_OUTPUT_FILENAME


def generate_text_completion(prompt):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f' {prompt}',
            max_tokens=80,
            n=1,
            stop=None,
            temperature=0.7,
        )

        message = completions.choices[0].text.strip()
        return message

def synthesize_text_with_gtts(text):
    # Create gTTS object
    tts = gTTS(text=text, lang='en')

    # Save audio stream to file
    filename = 'output.mp3'
    tts.save(filename)

    return filename

filename=record_audio(record_seconds)
# https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#input
inputs = {
    # Audio file
    'audio': open('recorded_audio.wav', "rb"),

    # Choose a Whisper model.
    'model': "base",

    # Choose the format for the transcription
    'transcription': "plain text",

    # Translate the text to English when set to True
    'translate': False,

    # language spoken in the audio, specify None to perform language
    # detection
    # 'language': ...,

    # temperature to use for sampling
    'temperature': 0,

    # optional patience value to use in beam decoding, as in
    # https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to
    # conventional beam search
    # 'patience': ...,

    # comma-separated list of token ids to suppress during sampling; '-1'
    # will suppress most special characters except common punctuations
    'suppress_tokens': "-1",

    # optional text to provide as a prompt for the first window.
    # 'initial_prompt': ...,

    # if True, provide the previous output of the model as a prompt for
    # the next window; disabling may make the text inconsistent across
    # windows, but the model becomes less prone to getting stuck in a
    # failure loop
    'condition_on_previous_text': False,

    # temperature to increase when falling back when the decoding fails to
    # meet either of the thresholds below
    'temperature_increment_on_fallback': 0.2,

    # if the gzip compression ratio is higher than this value, treat the
    # decoding as failed
    'compression_ratio_threshold': 2.4,

    # if the average log probability is lower than this value, treat the
    # decoding as failed
    'logprob_threshold': -1,

    # if the probability of the  token is higher than this
    # value AND the decoding has failed due to `logprob_threshold`,
    # consider the segment as silence
    'no_speech_threshold': 0.6,
}

# https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
output = version.predict(**inputs)

# Extract transcription from output
transcription = output["transcription"]

# Format transcription into a sentence string
sentence ='User: ' + transcription


if "image" in sentence:
    # Call another function or do something else
    print(colored("Image/Picture found!","blue"))
    synthesize_text_with_gtts("I am creating your image gimme one sec. I need my crayons. ")
    filename=create_image(transcription,'image')
    sentence1=explain_image(filename)
    #
    print(colored(sentence1,'light_blue','on_black'))
    subprocess.run(['mpg321','output.mp3'])
    # Save sentence to file
    with open("trans.txt", "a") as f:
        f.write(f'{sentence}\n')

    print(colored(sentence,'light_blue'))
    with open("trans.txt", "r") as f:
        prev = f.readlines()[number_lines:]
        last_3_lines = ''.join(prev)

    #sentence = 'Continue the conversation you are having: ' + last_3_lines
    #answer= generate_text_completion(sentence)
    #modified_string = answer.replace("AI:", "")
    #synthesize_text_with_polly(modified_string)
    #print(colored(modified_string,'green'))

    
    answer1= f'AI: See I generated an image of {sentence1}'
    answer=f'See I generated an image of {sentence1}'
    synthesize_text_with_gtts(answer)
    with open("trans.txt", "a") as f:
        f.write(f'{answer1}\n')
    print(answer1)
    subprocess.run(['mpg321','output.mp3'])

else:
    # Do something else
    print(colored("Image not found","yellow"))


# Save sentence to file
    with open("trans.txt", "a") as f:
        f.write(f'{sentence}\n')

    print(colored(sentence,'light_blue','on_green'))
    with open("trans.txt", "r") as f:
        prev = f.readlines()[-5:]
        last_3_lines = ''.join(prev)

    sentence = 'Continue the conversation you are having: ' + last_3_lines
    answer= generate_text_completion(sentence)
    modified_string = answer.replace("AI:", "")
    synthesize_text_with_gtts(modified_string)
    print(colored(modified_string,'green'))

    answer= 'AI: ' + modified_string
    with open("trans.txt", "a") as f:
        f.write(f'{answer}\n')
    subprocess.run(['mpg321','output.mp3'])
