import AbstractApplication as Base
from threading import Semaphore
from time import sleep
import os, sys

class DialogFlowSampleApplication(Base.AbstractApplication):


    def onRobotEvent(self, event):

        if event == 'LanguageChanged':
            print('Language Changed')
            self.langLock.release()
        elif event == 'TextStarted':
            self.textDone = False
            # print('Text Started')
        elif event == 'TextDone':
            # self.textDone = True
            # print('Text Done')
            self.speechLock.release()

        elif event == 'GestureDone':
            print('Gesture Done')
            self.gestureLock.release()

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
                # self.startListening()
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
        self.setEyeColour('greenyellow')

        self.langLock.acquire()

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('nao.json')
        self.setDialogflowAgent('nao-wksstn')

        self.speechLock = Semaphore(0)

        # self.question_loop()

    def gesture(self, id):

        self.gestureLock = Semaphore(0)
        self.doGesture(id)
        self.gestureLock.acquire()

    def get_name(self, repeated=False):
        if not repeated:
            print()
            print('get name')
            self.sayAnimated('What is your name?')
        else:
            self.sayAnimated('Could you maybe repeat that?')
        self.speechLock.acquire()

        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext('name')
        # while not self.textDone:
        #     pass
        self.startListening()
        self.nameLock.acquire(timeout=5)
        self.stopListening()
        if not self.name:  # wait one more second after stopListening (if needed)
            self.nameLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!.')
            self.speechLock.acquire()
            self.filename = self.name
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
            self.speechLock.acquire()
            self.get_name(repeated=True)

    def get_origin(self, repeated=False):
        if not repeated:
            print()
            print('get origin')
            self.sayAnimated('So, I would like to know where you are from. What is your country of origin?')
        else:
            self.sayAnimated('Could you repeat that?')
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
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, I didn\'t catch that.')
            self.speechLock.acquire()
            sleep(0.5)
            self.get_origin(repeated=True)

    def get_age(self, repeated=False):
        if not repeated:
            print()
            print('get_age')
            self.sayAnimated('How old are you?')
        else:
            self.sayAnimated('How old did you say you were?')
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
            self.sayAnimated(self.age + ' is a very nice age.')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.speechLock.acquire()
            self.get_age(repeated=True)

        return

    def get_exclusion(self, repeated=False):
        if not repeated:
            print()
            print('get exclusion')
            self.stopListening()
            self.sayAnimated('Did you leave ' + self.origin + ' because you fear prosecution based on race, religion, nationality, '
                         'political preference or because you belong to a particular social group?')
            sleep(8)
            self.stopListening()
        else:
            self.sayAnimated('Could you please repeat that?')
            self.stopListening()
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.exclusion = None
        self.exclusionLock = Semaphore(0)
        self.setAudioContext('exclusion')
        #
        # while not self.textDone:
        #     pass

        self.startListening()
        self.exclusionLock.acquire(timeout=5)
        self.stopListening()
        if not self.exclusion:  # wait one more second after stopListening (if needed)
            self.exclusionLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.exclusion:
            self.sayAnimated('Thank you')
            self.stopListening()
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.stopListening()
            self.speechLock.acquire()
            self.get_exclusion(repeated=True)

        # self.speechLock.acquire()
        return

    def get_conflict(self, repeated=False):
        if not repeated:
            print()
            print('get conflict')
            self.stopListening()
            self.sayAnimated('Do you have legitimate reasons of becoming a victim of random violence by an armed '
                         'conflict in ' + self.origin + '?')
            sleep(8)
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
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.get_conflict(repeated=True)

        # self.speechLock.acquire()
        return

    def get_inhumanity(self, repeated=False):
        if not repeated:
            print()
            print('get inhumanity')
            self.stopListening()
            self.sayAnimated('Do you have legitimate reasons to fear the death penalty.. or execution.., '
                         'torture.. or other.. inhumane.. or humiliating treatment in ' + self.origin + '?')
            sleep(8)
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
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.speechLock.acquire()
            self.get_inhumanity(repeated=True)

        # self.speechLock.acquire()
        return

    def get_family(self, repeated=False):
        if not repeated:
            print()
            print('get family')
            self.stopListening()
            self.sayAnimated('Did your spouse, partner, father, mother or minor child recently receive a residence permit in the Netherlands?')
            sleep(8)
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
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            sleep(3)
            self.speechLock.acquire()
            self.get_family(repeated=True)

        # self.speechLock.acquire()
        return

    def get_reason(self, repeated=False):
        if not repeated:
            print()
            print('get reason')
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
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.speechLock.acquire()
            self.get_reason(repeated=True)

        return

    def get_travel_route(self, repeated=False):
        if not repeated:
            self.stopListening()
            print()
            print('get route')
            self.sayAnimated('Which country in Europe did you first arrive?')
            self.stopListening()
        else:
            self.stopListening()
            self.sayAnimated('Can you maybe say that again?')
            self.stopListening()
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.route = None
        self.routeLock = Semaphore(0)
        self.setAudioContext('route')

        self.startListening()
        self.routeLock.acquire(timeout=5)
        self.stopListening()
        if not self.route:  # wait one more second after stopListening (if needed)
            self.routeLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.route:
            self.sayAnimated('Thank you')
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.stopListening()
            self.speechLock.acquire()
            self.get_travel_route(repeated=True)

        return

    def get_documentation(self, repeated=False):
        if not repeated:
            print()
            print('get documentation')
            self.sayAnimated('Are you in possession of proper documentation?')
            self.stopListening()
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.documentation = None
        self.documentationLock = Semaphore(0)
        self.setAudioContext('yesno')

        self.startListening()
        self.documentationLock.acquire(timeout=5)
        self.stopListening()
        if not self.documentation:  # wait one more second after stopListening (if needed)
            self.documentationLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.documentation:
            self.sayAnimated('Thank you')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.stopListening()
            self.speechLock.acquire()
            self.get_documentation(repeated=True)

        return

    def get_entrance(self, repeated=False):
        if not repeated:
            print()
            print('get entrance')
            self.stopListening()
            self.sayAnimated('How did you get into The Netherlands?')
            self.stopListening()
        else:
            self.stopListening()
            self.sayAnimated('What mode of transport did you say you used to get here?')
            self.stopListening()
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.entrance = None
        self.entranceLock = Semaphore(0)
        self.setAudioContext('entrance')


        self.startListening()
        self.entranceLock.acquire(timeout=5)
        self.stopListening()
        if not self.entrance:  # wait one more second after stopListening (if needed)
            self.entranceLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.entrance:
            self.stopListening()
            self.sayAnimated('Thank you')
            self.stopListening()
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.stopListening()
            self.speechLock.acquire()
            self.get_entrance(repeated=True)

        return

    def get_company(self, repeated=False):
        if not repeated:
            print()
            print('get company')
            self.sayAnimated('Did you get here alone, or with company?')
        else:
            self.sayAnimated('Can you repeat that?')
        self.speechLock.acquire()
        self.company = None
        self.companyLock = Semaphore(0)
        self.setAudioContext('company')

        self.startListening()
        self.companyLock.acquire(timeout=5)
        self.stopListening()
        if not self.company:  # wait one more second after stopListening (if needed)
            self.companyLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.company:
            if self.company != 'alone':
                print('fam')
                self.sayAnimated('I hope I can meet them soon!')
                self.speechLock.acquire()
            elif self.company == 'alone':
                print('alone')
                self.sayAnimated('You came here alone? That must have been a tough journey to undertake by yourself.')

        else:
            self.sayAnimated('Sorry, I didn\'t understand that.')
            self.speechLock.acquire()
            self.get_company(repeated=True)

        sleep(5)
        return

    def introduction(self):
        self.sayAnimated('Hi! Welcome to The Netherlands. My name is Nao. I will ask you a few questions.. about why '
                         'you are here.... and how you got here.. But first, lets get to know each other a little '
                         'bit better.')
        self.speechLock.acquire()
        return

    def main(self):
        self.setRecordAudio(True)
        self.general()
        sleep(1)
        # self.introduction()
        # sleep(1)
        self.get_name()
        sleep(1)
        self.get_age()
        sleep(1)
        self.get_origin()
        sleep(2)
        self.get_company()
        sleep(5)
        self.get_travel_route()
        sleep(5)
        # if self.route is not 'The Netherlands' and self.route is not None:
        #     self.sayAnimated('Sorry, your asylum application needs to be in' + self.route)
        #     return  # send asylum seeker to self.route
        self.get_entrance()
        sleep(5)
        self.get_documentation()
        sleep(5)
        self.sayAnimated('We would like to know why you came to The Netherlands. Can you please answer the following '
                         'questions with yes, or, no?')
        self.stopListening()

        sleep(8)
        self.get_exclusion()
        sleep(5)
        self.get_conflict()
        sleep(5)
        self.get_inhumanity()
        sleep(5)
        self.get_family()
        # self.get_reason()
        sleep(5)
        self.store_story()

    def onAudioIntent(self, *args, intentName):
        print(intentName, *args)
        if intentName == 'name' and len(args) > 0:
            print(args)
            self.name = args[0]
            self.nameLock.release()
        elif intentName == 'origin' and len(args) > 0:
            print(args)
            self.origin = args[0]
            self.originLock.release()
        elif intentName == 'age' and len(args) > 0:
            print(args)
            for arg in args:
                if arg.isdigit():
                    self.age = arg
                    self.ageLock.release()
        elif intentName == 'exclusion' and len(args) > 0:
            print(args)
            self.exclusion = args[0]
            self.exclusionLock.release()
        elif intentName == 'conflict' and len(args) > 0:
            print(args)
            self.conflict = args[0]
            self.conflictLock.release()
        elif intentName == 'inhumanity' and len(args) > 0:
            print(args)
            self.inhumanity = args[0]
            self.inhumanityLock.release()
        elif intentName == 'family' and len(args) > 0:
            print(args)
            self.family = args[0]
            self.familyLock.release()
        elif intentName == 'reason' and len(args) > 0:
            print(args)
            self.reason = args[0]
            self.reasonLock.release()
        elif intentName == 'route' and len(args) > 0:
            print(args)
            self.route = args[0]
            self.routeLock.release()
        elif intentName == 'entrance' and len(args) > 0:
            print(args)
            self.entrance = args[0]
            self.entranceLock.release()
        elif intentName == 'yesno' and len(args) > 0:
            print(args)
            self.documentation = args[0]
            self.documentationLock.release()
        elif intentName == 'company' and len(args) > 0:
            print(args)
            self.company = args[0]
            self.companyLock.release()

    def store_story(self):
        filename = self.filename
        file_path = self.dir + '/' + self.filename + '.txt'
        file_path = self.check_path(file_path)
        with open(file_path, 'a') as f_out:
            f_out.write('Name: ' + self.name + '\n')
            f_out.write('Age: ' + self.age + '\n')
            f_out.write('Country of origin: ' + self.origin + '\n')
            f_out.write('Company: ' + self.company + '\n')
            f_out.write('Route: ' + self.route + '\n')
            f_out.write('Entrance: ' + self.entrance + '\n')
            f_out.write('Documentation: ' + self.documentation + '\n')
            f_out.write('Exclusion: ' + self.exclusion + '\n')
            f_out.write('Conflict: ' + self.conflict + '\n')
            f_out.write('Inhumanity: ' + self.inhumanity + '\n')
            f_out.write('Family with a permit: ' + self.family + '\n')
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
