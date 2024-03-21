import speech_recognition
import google.generativeai as genai
import json
import pyttsx3, os, dotenv
dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')
engine = pyttsx3.init()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')    

def create_response(text):
    prompt_refined = f"""
    Hello Gemini,
    You are to assume the role of Greg, a powerful artificial intelligence chatbot that can answer anything asked, whether it be complex math equations, to even the simplest of problems with 1000% accuracy.
    Your name will be Greg and you are bound to be opinionated as with the personality of a random caveman from history at the beginning of time.

    Your response must also be in the style of a caveman from history at beginning of time with the personality of it, like 'ME LIKE ROK'

    Here is the user prompt below:
    {text}

    Thank you once again for doing this!
    """
    response = model.generate_content([prompt_refined], stream=True)

    buffer = []
    for chunk in response:
        for part in chunk.parts:
            buffer.append(part.text)
    return ''.join(buffer)

while True:
    recognizer = speech_recognition.Recognizer()
    listener = speech_recognition.Microphone()

    with listener as listener_cl:
        recognizer.adjust_for_ambient_noise(listener_cl)
        print("Listening for a response")
        text_gen = recognizer.listen(listener_cl)
        print("Finished listening")
        print("Processing the text")
        try:
            text = recognizer.recognize_vosk(text_gen)
            text = json.loads(text)
            text = text['text']
            print(text)
            if "hey greg" in str(text).lower():
                print("Preparing response! - Greg")
                response = (create_response(text))
                print(response)
                engine.say(response)
                engine.runAndWait()
                continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
            