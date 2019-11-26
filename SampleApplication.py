import AbstractApplication as Base
from threading import Semaphore
import os, sys

class DialogFlowSampleApplication(Base.AbstractApplication):


    def make_questions(self):
        self.answer_name = ''
        self.get_age = ''
        self.get_origin = ''

        # set question, variable name and response
        self.questions = {0: ['Hello, what is your name?', 'answer_name', 'Nice to meet you ' + self.answer_name + '!.'],
                          2: ['Where do you come from', 'get_origin', 'Ah! I have heard of ' + self.get_origin + '.'],
                          1: ['What is your age?', 'get_age', self.get_age + ' is a very nice age. I myself am a robot, I do not have an age']}

    def question_loop(self):
        self.make_questions()
        for i in range(len(self.questions)):
            question = self.questions[i][0]
            variable = self.questions[i][1]
            variableLock = variable + 'Lock'
            response = self.questions[i][2]
            while True:
                self.sayAnimated(question)
                self.speechLock.acquire()
                print(i)

                setattr(self, variableLock, Semaphore(0))

                self.setAudioContext(variable)
                self.startListening()
                getattr(self, variableLock).acquire(timeout=5)
                self.stopListening()
                print('getatrrr ', getattr(self, variable))

                if getattr(self, variable) is not '':
                    print('break', getattr(self, variable))
                    break
                else:
                    self.sayAnimated('Sorry, I didn\'t catch that.')


            print(response)
            self.sayAnimated(response)
            self.speechLock.acquire()


        # store story in stories
        self.filename = self.answer_name
        self.store_story()

    def get_name(self):
        self.answer_name = None
        self.answer_nameLock = Semaphore(0)
        self.setAudioContext('answer_name')
        self.startListening()
        self.answer_nameLock.acquire(timeout=5)
        self.stopListening()
        if not self.answer_name:  # wait one more second after stopListening (if needed)
            self.answer_nameLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.answer_name:
            self.sayAnimated('Nice to meet you ' + self.answer_name + '!.')
            self.filename = self.answer_name
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
    def get_origin(self):
        self.sayAnimated('So, I would like to know where you are from')
        self.speechLock.acquire()
        print('6')

        # Listen for an answer for at most 5 seconds
        self.get_origin = None
        self.get_originLock = Semaphore(0)
        self.setAudioContext('get_origin')
        self.startListening()
        self.get_originLock.acquire(timeout=5)
        self.stopListening()
        if not self.get_origin:  # wait one more second after stopListening (if needed)
            self.get_originLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.get_origin:
            self.sayAnimated('Ah! I have heard of ' + self.get_origin + '.')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that.')
            sys.exit(1)

        self.speechLock.acquire()
        print('7')
    def get_age(self):
        # age
        self.sayAnimated('How old are you?')
        self.speechLock.acquire()
        print('6')

        # Listen for an answer for at most 5 seconds
        self.get_age = None
        self.get_ageLock = Semaphore(0)
        self.setAudioContext('get_age')
        self.startListening()
        self.get_ageLock.acquire(timeout=5)
        self.stopListening()
        if not self.get_age:  # wait one more second after stopListening (if needed)
            self.get_ageLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.get_age:
            self.sayAnimated(self.get_age + ' is a very nice age. I myself am a robot, I do not have an age')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            sys.exit(1)

        self.speechLock.acquire()
        print('7')


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


        # self.question_loop()
        # return

        self.sayAnimated('Hello, what is your name?')
        self.speechLock.acquire()
        print('3')

        self.get_name()
        self.get_age()
        self.get_origin()

        self.store_story()




    def onRobotEvent(self, event):
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
        print(intentName, *args)
        if intentName == 'answer_name' and len(args) > 0:
            print(args)
            self.answer_name = args[0]
            self.answer_nameLock.release()
        if intentName == 'get_origin' and len(args) > 0:
            print(args)
            self.get_origin = args[0]
            self.get_originLock.release()
        if intentName == 'get_age' and len(args) > 0:
            print(args)
            for arg in args:
                if arg.isdigit():
                    self.get_age = arg
                    self.get_ageLock.release()

    def store_story(self):
        filename = self.filename
        file_path = self.dir + '/' + self.filename + '.txt'
        file_path = self.check_path(file_path)
        with open(file_path, 'a') as f_out:
            f_out.write('Name: ' + self.answer_name + '\n')
            f_out.write('Age: ' + self.get_age + '\n')
            f_out.write('Country of origin: ' + self.get_origin + '\n')
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
