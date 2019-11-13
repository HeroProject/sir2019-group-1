import AbstractApplication as Base
from threading import Semaphore


class DialogFlowSampleApplication(Base.AbstractApplication):
    def main(self):

        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')

        self.langLock.acquire()
        print('1')

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('nao-axsltp-05aa80c86129.json')
        self.setDialogflowAgent('NAO')
        print('2')

        # Make the robot ask the question, and wait until it is done speaking
        self.speechLock = Semaphore(0)
        self.sayAnimated('Hello, what is your name?')
        self.speechLock.acquire()
        print('3')


        # Listen for an answer for at most 5 seconds
        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext('answer_name')
        self.startListening()
        self.nameLock.acquire(timeout=5)
        self.stopListening()
        if not self.name:  # wait one more second after stopListening (if needed)
            self.nameLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!')
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
        self.speechLock.acquire()
        print('5')
        # Display a gesture (replace <gestureID> with your gestureID)
        # self.gestureLock = Semaphore(0)
        # self.doGesture('<gestureID>/behavior_1')
        # self.gestureLock.acquire()

    def onRobotEvent(self, event):
        print('onRobotEvent')
        if event == 'LanguageChanged':
            print('Language Changed')
            self.langLock.release()
        elif event == 'TextDone':
            print('Text Done')
            self.speechLock.release()
        elif event == 'GestureDone':
            print('Gesture Done')
            self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        print('onAudioIntent')
        if intentName == 'answer_name' and len(args) > 0:
            print('if ')
            self.name = args[0]
            self.nameLock.release()


# Run the application
sample = DialogFlowSampleApplication()

sample.main()
sample.stop()
