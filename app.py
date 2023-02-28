import os
import openai
from flask import Flask, redirect, render_template, request, url_for, session
from speech_recognition import recognize_from_microphone, generate_prompt
import azure.cognitiveservices.speech as speechsdk
import uuid

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
app.config['SECRET_KEY'] = 'une-chaîne-aléatoire-et-secrète'
speech_key = os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')

speech_synthesizers = {}

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = recognize_from_microphone()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(question),
            temperature=0.6,
            max_tokens=4000,
            n=1,
            stop=None
        )
        response_text = response.choices[0].text

        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        speech_config.speech_synthesis_voice_name = 'fr-CH-ArianeNeural'

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesizer.speak_text_async(response_text)
        
        # Génère une clé aléatoire pour cet objet speech_synthesizer
        key = str(uuid.uuid4())

        # Stocke l'objet speech_synthesizer dans le dictionnaire avec la clé associée
        speech_synthesizers[key] = speech_synthesizer

        # Stocke la clé dans la session pour pouvoir récupérer l'objet speech_synthesizer plus tard
        session['speech_synthesizer_key'] = key

        # Vérifiez si la variable de session "questions" existe et initialisez-la à une liste vide si elle n'existe pas
        if 'questions' not in session:
            session['questions'] = []

        # Ajoutez la question actuelle à la liste des questions stockées dans la variable de session "questions"
        session['questions'].append(question)
        session.modified = True

        # Vérifiez si la variable de session "responses" existe et initialisez-la à une liste vide si elle n'existe pas
        if 'responses' not in session:
            session['responses'] = []

        # Ajoutez la réponse à la liste des réponses stockées dans la variable de session "responses"
        session['responses'].append(response_text)
        session.modified = True
        
        return redirect(url_for("index"))

    # Obtenez les questions et les réponses stockées dans les variables de session pour les afficher dans la vue
    questions = session.get("questions")
    responses = session.get("responses")

    if questions:
        chat = zip(questions, responses)
    else:
        chat = []
        
    return render_template("index.html", chat=chat)

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("index"))



@app.route("/stop", methods=["POST"])
def stop():
    if 'speech_synthesizer_key' in session:
        key = session['speech_synthesizer_key']
        if key in speech_synthesizers:
            speech_synthesizer = speech_synthesizers[key]
            speech_synthesizer.stop_speaking()
            return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True) 