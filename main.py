import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import speech_recognition as sr
import pyttsx3
from kivy.utils import platform
from plyer import tts  # For Android

# Platform-specific imports
ANDROID = platform == 'android'
if ANDROID:
    try:
        from jnius import autoclass
        from android.permissions import request_permissions, Permission
        # Import Android-specific modules
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
    except ImportError:
        print("Android modules not available")
        ANDROID = False

from contact_utils import get_contact_number_by_name

class VoiceCommandApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None
        if not ANDROID:
            try:
                self.engine = pyttsx3.init()
            except:
                pass
        
        # Request Android permissions only on Android
        if ANDROID:
            self.request_android_permissions()

    def request_android_permissions(self):
        """Request Android permissions"""
        if not ANDROID:
            print("Not running on Android - permissions not required")
            return

        def callback(permissions, results):
            if all([res for res in results]):
                print("All permissions granted")
            else:
                print("Some permissions denied")

        try:
            request_permissions([
                Permission.INTERNET,
                Permission.CALL_PHONE,
                Permission.READ_CONTACTS,
                Permission.RECORD_AUDIO
            ], callback)
        except Exception as e:
            print(f"Error requesting permissions: {e}")

    def speak(self, text):
        try:
            if ANDROID:
                tts.speak(text)
            else:
                if self.engine:
                    self.engine.say(text)
                    self.engine.runAndWait()
        except Exception as e:
            self.ids.output.text += f"\nTTS error: {e}"

    def make_phone_call(self, number):
        if ANDROID:
            try:
                intent = Intent(Intent.ACTION_CALL)
                intent.setData(Uri.parse(f"tel:{number}"))
                activity.startActivity(intent)
                return True
            except Exception as e:
                print(f"Error making call: {e}")
                return False
        else:
            import webbrowser
            webbrowser.open(f"tel:{number}")
            return True

    def open_whatsapp(self, number, message):
        if ANDROID:
            try:
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(f"https://wa.me/91{number}?text={message}"))
                activity.startActivity(intent)
                return True
            except Exception as e:
                print(f"Error opening WhatsApp: {e}")
                return False
        else:
            import webbrowser, urllib.parse
            message = urllib.parse.quote(message)
            webbrowser.open(f"https://wa.me/91{number}?text={message}")
            return True

    def listen_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.ids.output.text = "Listening..."
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                self.ids.output.text = f"You said: {command}"
                self.process_command(command.lower())
            except sr.UnknownValueError:
                self.ids.output.text = "Sorry, I didn't understand."
            except sr.RequestError:
                self.ids.output.text = "Speech service unavailable."
            except Exception as e:
                self.ids.output.text = f"Error: {e}"

    def process_command(self, command):
        if "hello" in command:
            self.speak("Hi there! How can I help you?")
        elif "time" in command:
            from datetime import datetime
            now = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
        elif "call" in command:
            name = command.replace("call ", "").strip()
            number = get_contact_number_by_name(name)
            if number:
                if self.make_phone_call(number):
                    self.speak(f"Calling {name}")
                else:
                    self.speak("Failed to make the call")
            else:
                self.speak(f"Couldn't find number for {name}")
        elif "whatsapp" in command:
            import re
            name_match = re.search(r"whatsapp to (.+?) message", command, re.IGNORECASE)
            msg_match = re.search(r"message (.+)$", command, re.IGNORECASE)

            if name_match and msg_match:
                name = name_match.group(1).strip()
                message = msg_match.group(1).strip()
                number = get_contact_number_by_name(name)
                if number:
                    number_clean = ''.join(filter(str.isdigit, number))[-10:]
                    if self.open_whatsapp(number_clean, message):
                        self.speak(f"Opening WhatsApp chat with {name}")
                    else:
                        self.speak("Failed to open WhatsApp")
                else:
                    self.speak(f"Couldn't find WhatsApp number for {name}")
            else:
                self.speak("Please say: WhatsApp to [contact name] message [your message]")
        elif "exit" in command:
            self.speak("Goodbye!")
            App.get_running_app().stop()
        else:
            self.speak("Command not recognized.")

class VoiceApp(App):
    def build(self):
        return VoiceCommandApp()

if __name__ == '__main__':
    VoiceApp().run()
