import tkinter as tk
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import random
from transformers import BertTokenizer, TFBertForSequenceClassification
from twilio.rest import Client
from Modules.home_control import home_control_module
from Modules.news_module import news_module
from Modules.weather_module import weather_module
from Modules.news_module.science_decouverte import science_decouverte
import os
class VoiceAssistant:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
        self.model = TFBertForSequenceClassification.from_pretrained("bert-base-multilingual-cased")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.mute_mode = False
        self.autonomous_module = science_decouverte.ScienceDecouverte()

        # Initialisation du modèle de traitement du langage naturel
        self.nlp_model = self.load_nlp_model()
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")

    def speak(self, text):
        if not self.mute_mode:
            self.engine.say(text)
            self.engine.runAndWait()

    def process_command(self, text):
        if "heure" in text:
            return datetime.datetime.now().strftime("Il est %H heures et %M minutes.")
        elif "date" in text:
            return datetime.date.today().strftime("Aujourd'hui, nous sommes le %d/%m/%Y.")
        elif "météo" in text:
            return weather_module.get_weather()
        elif "actualités" in text:
            return news_module.get_news()
        elif "allumer" in text or "éteindre" in text:
            return home_control_module.control_home_device(text)
        elif "muet" in text:
            self.mute_mode = True
            return "Mode muet activé."
        elif "réactiver" in text:
            self.mute_mode = False
            return "Mode muet désactivé."
        elif "comment ça va" in text:
            return random.choice(["Je vais bien, merci!", "Tout va bien de mon côté.", "Je suis là pour vous aider!"])
        elif "remercie" in text:
            return random.choice(["De rien!", "Toujours là pour vous!", "A votre service!"])
        elif "découvert" in text:
            return self.discover()
        elif "recherche" in text:
            return self.wikipedia_search(text)
        elif "ouvre" in text:
            return self.open_website(text)
        elif "envoie un email" in text:
            return self.send_email()
        elif "rappelle-moi" in text:
            return self.set_reminder(text)
        elif "envoie un SMS" in text:
            return self.send_sms()
        else:
            return self.autonomous_module.get_autonomous_response(text)

    def discover(self):
        return self.autonomous_module.get_random_response()

    def wikipedia_search(self, query):
        try:
            summary = wikipedia.summary(query)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return "La recherche est ambiguë. Veuillez préciser votre question."
        except wikipedia.exceptions.PageError as e:
            return "Aucune information trouvée sur Wikipedia."

    def open_website(self, text):
        try:
            website = text.split("ouvre")[-1].strip()
            webbrowser.open(website)
            return f"Ouverture de {website}"
        except Exception as e:
            return "Impossible d'ouvrir le site web."

    def send_email(self):
        try:
            # Configuration du serveur SMTP et envoi de l'email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("votre_email@gmail.com", "votre_mot_de_passe")
            server.sendmail("votre_email@gmail.com", "destinataire@example.com", "Ceci est un email envoyé depuis l'assistant vocal.")
            server.quit()
            return "Email envoyé avec succès."
        except Exception as e:
            return "Échec de l'envoi de l'email."

    def set_reminder(self, text):
        try:
            # Analyse de la phrase pour extraire la date/heure du rappel
            # Code pour planifier un rappel
            return "Rappel programmé avec succès."
        except Exception as e:
            return "Échec de la programmation du rappel."

    def send_sms(self):
        try:
            # Configuration du client Twilio et envoi du SMS
            client = Client("YOUR_TWILIO_ACCOUNT_SID", "YOUR_TWILIO_AUTH_TOKEN")
            message = client.messages.create(to="", from_="", body="Ceci est un SMS envoyé depuis l'assistant vocal.")
            return "SMS envoyé avec succès."
        except Exception as e:
            return "Échec de l'envoi du SMS."

    def get_live_stream_url(self):
        # Suppose que vous avez une méthode pour obtenir l'URL du flux vidéo
        pass

    def load_nlp_model(self):
        # Charger le modèle BERT pré-entraîné pour classification de séquence
        nlp_model = TFBertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)
        return nlp_model

    def preprocess_text(self, text):
        # Prétraitement du texte avant de le passer au modèle NLP (BERT)
        # Tokenisation et padding du texte
        inputs = self.tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=128)
        return inputs

    def start(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.speak("Bonjour")

        while True:
            with self.microphone as source:
                audio = self.recognizer.listen(source)

                try:
                    text = self.recognizer.recognize_google(audio, language="fr-FR")
                    print("Vous avez dit:", text)

                    if "comment" in text and "domotique" in text:
                        response = self.process_command(text)
                        print("Réponse:", response)
                        self.speak(response)
                    elif not self.mute_mode:
                        response = self.process_command(text)
                        print("Réponse:", response)
                        self.speak(response)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Échec de la demande au service de reconnaissance vocale : {e}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")  # Taille de la fenêtre
        self.title("Assistant vocal")
        self.assistant = VoiceAssistant()

    def start_listening(self):
        self.assistant.start()

def main():
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    app = App()
    app.start_listening()
    app.mainloop()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
