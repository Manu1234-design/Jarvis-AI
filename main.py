import os
from groq import Groq
import speech_recognition as sr
import pyaudio
import pyttsx3
import datetime
import time
import speedtest



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 3
        audio = r.listen(source,timeout=2,phrase_time_limit=4)

    try:
        print("Recognizing.....")
        query =r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:

        return "none"
    return query

def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour>=0 and hour<=12:
        speak(f"good morning, its {tt}")
    elif hour>12 and hour<18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening,  its {tt}")
    speak("i am jarvis your personal ai assistant,  please tell me,  how can i help you")



os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# Set the system prompt
system_prompt = {
    "role": "system",
    "content":"You are jarvis my personal ai assisstant and not a language model. You reply with medium answer."

}

# Initialize the chat history
chat_history = [system_prompt]

def TaskExecution():
    wish()

    while True:
        # Get user input from the console

        query = takecommand()
        if query == "none":
            continue
        elif query == "check internet speed":
            st = speedtest.Speedtest()
            dl = st.download()
            correctDownload = int(dl/800000)
            up = st.upload()
            correctupload = int(up/800000)
            speak(f"sir we have {correctDownload} mega bytes per second downloading speed and {correctupload} mega bytes per second uploading speed")
        elif "quit" in query:
            speak("Thank you have a nice day")
            break
        else:
            chat_history.append({"role": "user", "content": query})

            response = client.chat.completions.create(model="llama3-70b-8192",
                                                      messages=chat_history,
                                                      max_tokens=1024,
                                                      temperature=1.2)
            # Append the response to the chat history
            chat_history.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            # Print the response
            speak(response.choices[0].message.content)
  # Append the user input to the chat history


if __name__ == "__main__":
    TaskExecution()