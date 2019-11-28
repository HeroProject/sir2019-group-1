import AbstractApplication as Base
from threading import Semaphore
import os, sys

class DialogFlowSampleApplication(Base.AbstractApplication):


    def make_questions(self):
        self.name = ''
        self.age = ''
        self.origin = ''

        # set question, variable name and response
        self.questions = {0: ['Hello, what is your name?', 'name', 'Nice to meet you ' + self.name + '!.'],
                          2: ['Where do you come from', 'get_origin', 'Ah! I have heard of ' + self.origin + '.'],
                          1: ['What is your age?', 'get_age', self.age + ' is a very nice age. I myself am a robot, I do not have an age']}

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
        self.filename = self.name
        self.store_story()

    def general(self):
        self.dir = 'Stories'
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')

        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('nao.json')
        self.setDialogflowAgent('nao-wksstn')

        self.speechLock = Semaphore(0)

        # self.question_loop()

    def get_name(self):
        # self.speechLock = Semaphore(0)
        self.sayAnimated('Hello, what is your name?')
        self.speechLock.acquire()
        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext('name')
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
            self.get_name()

        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        # self.gestureLock = Semaphore(0)
        # self.doGesture('<gestureID>/behavior_1')
        # self.gestureLock.acquire()

        # check where the person is from

    def get_origin(self):
        self.sayAnimated('So, I would like to know where you are from')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.origin = None
        self.originLock = Semaphore(0)
        self.setAudioContext('origin')
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
            self.get_origin()

        self.speechLock.acquire()

    def get_age(self):
        self.sayAnimated('How old are you?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.age = None
        self.ageLock = Semaphore(0)
        self.setAudioContext('age')
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
            self.get_age()

        self.speechLock.acquire()

    def get_exclusion(self):
        self.sayAnimated('Did you leave' + self.origin + 'because you fear prosecution based on race, religion, nationality, '
                         'political preference or because you belong to a particular social group?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.exclusion = None
        self.exclusionLock = Semaphore(0)
        self.setAudioContext('exclusion')
        self.startListening()
        self.exclusionLock.acquire(timeout=5)
        self.stopListening()
        if not self.exclusion:  # wait one more second after stopListening (if needed)
            self.exclusionLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.exclusion:
            self.sayAnimated('Thank you')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.get_exclusion()

        self.speechLock.acquire()

    def get_conflict(self):
        self.sayAnimated('Do you have legitimate reasons of becoming a victim of random violence by an armed '
                         'conflict in ' + self.origin + '?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.conflict = None
        self.conflictLock = Semaphore(0)
        self.setAudioContext('conflict')
        self.startListening()
        self.conflictLock.acquire(timeout=5)
        self.stopListening()
        if not self.conflict:  # wait one more second after stopListening (if needed)
            self.conflictLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.conflict:
            self.sayAnimated('Thank you')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.get_conflict()

        self.speechLock.acquire()

    def get_inhumanity(self):
        self.sayAnimated('Do you have legitimate reasons to fear the death penalty or execution, '
                         'torture or other inhumane or humiliating treatment in ' + self.origin + '?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.inhumanity = None
        self.inhumanityLock = Semaphore(0)
        self.setAudioContext('inhumanity')
        self.startListening()
        self.inhumanityLock.acquire(timeout=5)
        self.stopListening()
        if not self.inhumanity:  # wait one more second after stopListening (if needed)
            self.inhumanityLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.inhumanity:
            self.sayAnimated('Thank you')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.get_inhumanity()

        self.speechLock.acquire()

    def get_family(self):
        self.sayAnimated('Did your spouse, partner, father, mother or minor child recently receive a residence permit in the Netherlands?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.family = None
        self.familyLock = Semaphore(0)
        self.setAudioContext('family')
        self.startListening()
        self.familyLock.acquire(timeout=5)
        self.stopListening()
        if not self.family:  # wait one more second after stopListening (if needed)
            self.familyLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.family:
            self.sayAnimated('Thank you')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.get_family()

        self.speechLock.acquire()

    def get_reason(self):
        self.sayAnimated('Can you please explain why you want to ask for asylum?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.reason = None
        self.reasonLock = Semaphore(0)
        self.setAudioContext('reason')
        self.startListening()
        self.reasonLock.acquire(timeout=5)
        self.stopListening()
        if not self.reason:  # wait one more second after stopListening (if needed)
            self.reasonLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.reason:
            self.sayAnimated('Thank you')
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.get_reason()

        self.speechLock.acquire()

    def main(self):
        self.general()

        self.get_name()
        self.get_age()
        self.get_origin()
        self.get_exclusion()
        if self.exclusion == 'no':
            self.get_conflict()
        self.get_inhumanity()
        self.get_family()
        self.get_reason()



        self.store_story()




    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            print('Language Changed')
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            print('Gesture Done')
            self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        print(intentName, *args)
        if intentName == 'name' and len(args) > 0:
            print(args)
            self.name = args[0]
            self.nameLock.release()
        if intentName == 'origin' and len(args) > 0:
            print(args)
            self.origin = args[0]
            self.originLock.release()
        if intentName == 'age' and len(args) > 0:
            print(args)
            for arg in args:
                if arg.isdigit():
                    self.age = arg
                    self.ageLock.release()
        if intentName == 'exclusion' and len(args) > 0:
            print(args)
            self.exclusion = args[0]
            self.exclusionLock.release()
        if intentName == 'conflict' and len(args) > 0:
            print(args)
            self.conflict = args[0]
            self.conflictLock.release()

        if intentName == 'inhumanity' and len(args) > 0:
            print(args)
            self.inhumanity = args[0]
            self.inhumanityLock.release()
        if intentName == 'family' and len(args) > 0:
            print(args)
            self.family = args[0]
            self.familyLock.release()
        if intentName == 'reason' and len(args) > 0:
            print(args)
            self.reason = args[0]
            self.reasonLock.release()

    def store_story(self):
        filename = self.filename
        file_path = self.dir + '/' + self.filename + '.txt'
        file_path = self.check_path(file_path)
        with open(file_path, 'a') as f_out:
            f_out.write('Name: ' + self.name + '\n')
            f_out.write('Age: ' + self.age + '\n')
            f_out.write('Country of origin: ' + self.origin + '\n')
            f_out.write('Exclusion: ' + self.exclusion + '\n')
            f_out.write('Conflict: ' + self.conflict + '\n')
            f_out.write('Inhumanity: ' + self.inhumanity + '\n')
            f_out.write('Family: ' + self.family + '\n')
            f_out.write('Reason: ' + self.reason + '\n')
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
