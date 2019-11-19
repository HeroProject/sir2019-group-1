import AbstractApplication as Base
from threading import Semaphore
import os, sys

class DialogFlowSampleApplication(Base.AbstractApplication):
    # def __init__(self):
    #     # self.filename = ''
    #     self.dir = 'Stories'
    #     # if not os.path.isdir(self.dir):
    #     #     os.mkdir(self.dir)


    def main(self):
        self.dir = 'Stories'
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')

        self.langLock.acquire()
        print('1')

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('nao.json')
        self.setDialogflowAgent('nao-wksstn')
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
            self.sayAnimated('Nice to meet you ' + self.name + '!.')
            self.filename = self.name
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
            sys.exit(1)

        self.speechLock.acquire()
        print('5')

        # Display a gesture (replace <gestureID> with your gestureID)
        # self.gestureLock = Semaphore(0)
        # self.doGesture('<gestureID>/behavior_1')
        # self.gestureLock.acquire()

        # check where the person is from

        self.sayAnimated('So, I would like to know where you are from')
        self.speechLock.acquire()
        print('6')

        # Listen for an answer for at most 5 seconds
        self.origin = None
        self.originLock = Semaphore(0)
        self.setAudioContext('get_origin')
        self.startListening()
        self.originLock.acquire(timeout=5)
        self.stopListening()
        if not self.origin:  # wait one more second after stopListening (if needed)
            self.originLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.origin:
            self.sayAnimated('Ah! I have heard of ' + self.origin + '.')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that.')
            sys.exit(1)

        self.speechLock.acquire()
        print('7')

        # age
        self.sayAnimated('How old are you?')
        self.speechLock.acquire()
        print('6')

        # Listen for an answer for at most 5 seconds
        self.age = None
        self.ageLock = Semaphore(0)
        self.setAudioContext('get_age')
        self.startListening()
        self.ageLock.acquire(timeout=5)
        self.stopListening()
        if not self.age:  # wait one more second after stopListening (if needed)
            self.ageLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.age:
            self.sayAnimated(self.age + ' is a very nice age. I myself am a robot, I do not have an age')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            sys.exit(1)

        self.speechLock.acquire()
        print('7')

        self.store_story()








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
        print(intentName, *args)
        if intentName == 'answer_name' and len(args) > 0:
            print(args)
            self.name = args[0]
            self.nameLock.release()
        if intentName == 'get_origin' and len(args) > 0:
            print(args)
            self.origin = args[0]
            self.originLock.release()
        if intentName == 'get_age' and len(args) > 0:
            print(args)
            for arg in args:
                if arg.isdigit():
                    self.age = arg
                    self.ageLock.release()

    def store_story(self):
        filename = self.filename
        file_path = self.dir + '/' + self.filename + '.txt'
        file_path = self.check_path(file_path)
        with open(file_path, 'a') as f_out:
            f_out.write('Name: ' + self.name + '\n')
            f_out.write('Age: ' + self.age + '\n')
            f_out.write('Country of origin: ' + self.origin + '\n')
        return

    def check_path(self, file_path):
        i = 1
        while os.path.isfile(file_path):
            file_path = self.dir + '/' + self.filename + '_' + '{i}'.format(i=i) + '.txt'
            i += 1
        return file_path



# Run the application
sample = DialogFlowSampleApplication()

sample.main()
sample.stop()
