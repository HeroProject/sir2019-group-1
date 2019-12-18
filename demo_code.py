import AbstractApplication as Base
from threading import Semaphore
from time import sleep
import os


class DialogFlowSampleApplication(Base.AbstractApplication):

    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextStarted':
            self.textDone = False
        elif event == 'TextDone':
            # self.textDone = True
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()

    def general(self):
        """
        Initialise general settings like language, eye-color and the Google Dialogflow json-file.
        """
        self.dir = 'Stories'
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.setEyeColour('greenyellow')

        self.langLock.acquire()

        # pass Google Dialogflow parameters
        self.setDialogflowKey('nao.json')
        self.setDialogflowAgent('nao-wksstn')

        self.speechLock = Semaphore(0)

    def gesture(self, id):
        """
        Helper function for executing movements.
        """

        self.gestureLock = Semaphore(0)
        self.doGesture(id)
        self.gestureLock.acquire()

    def introduction(self):
        self.sayAnimated('Hi! Welcome to The Netherlands. My name is Nao. I will ask you a few questions.. about why '
                         'you are here.... and how you got here.. But first, lets get to know each other a little '
                         'bit better.')
        self.speechLock.acquire()
        return

    def get_name(self, repeated=False):
        if not repeated:
            self.sayAnimated('What is your name?')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Could you maybe repeat that?')
            self.speechLock.acquire()

        self.name = None
        self.nameLock = Semaphore(0)
        self.setAudioContext('name')
        self.startListening()
        self.nameLock.acquire(timeout=5)
        self.stopListening()

        # wait one more second after stopListening (if needed)
        if not self.name:
            self.nameLock.acquire(timeout=1)

        # respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!.')
            self.speechLock.acquire()
            self.filename = self.name
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
            self.speechLock.acquire()
            self.get_name(repeated=True)

    def get_age(self, repeated=False):
        if not repeated:
            self.sayAnimated('How old are you?')
            self.speechLock.acquire()

        else:
            self.sayAnimated('How old did you say you were?')
            self.speechLock.acquire()

        self.age = None
        self.ageLock = Semaphore(0)
        self.setAudioContext('age')

        self.startListening()
        self.ageLock.acquire(timeout=5)
        self.stopListening()

        if not self.age:
            self.ageLock.acquire(timeout=1)

        if self.age:
            self.sayAnimated(self.age + ' is a very nice age.')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, I didn\'t catch that')
            self.speechLock.acquire()
            self.get_age(repeated=True)

    def get_origin(self, repeated=False):
        if not repeated:
            self.sayAnimated('So, I would like to know where you are from. What is your country of origin?')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Could you repeat that?')
            self.speechLock.acquire()

        self.origin = None
        self.originLock = Semaphore(0)
        self.setAudioContext('origin')

        self.startListening()
        self.originLock.acquire(timeout=5)
        self.stopListening()

        if not self.origin:
            self.originLock.acquire(timeout=1)

        if self.origin:
            self.sayAnimated('Ah! I have heard of ' + self.origin + '.')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, I didn\'t catch that.')
            self.speechLock.acquire()
            self.get_origin(repeated=True)

    def get_company(self, repeated=False):
        if not repeated:
            self.sayAnimated('Did you get here alone, or with company?')
            self.speechLock.acquire()

        self.company = None
        self.companyLock = Semaphore(0)
        self.setAudioContext('company')

        self.startListening()
        self.companyLock.acquire(timeout=5)
        self.stopListening()

        if not self.company:
            self.companyLock.acquire(timeout=1)

        if self.company:
            if self.company != 'alone':
                self.sayAnimated('I hope I can meet them soon!')
                self.speechLock.acquire()
            elif self.company == 'alone':
                self.sayAnimated(
                    'You came here alone from ' + self.origin + '? That must have been a tough journey to undertake by yourself.')
                self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, I didn\'t understand that. Can you repeat that?')
            self.speechLock.acquire()
            self.get_company(repeated=True)

    def get_travel_route(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.stopListening()
            self.sayAnimated('Which country in Europe did you first arrive?')
            self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.route = None
        self.routeLock = Semaphore(0)
        self.setAudioContext('route')

        self.startListening()
        self.routeLock.acquire(timeout=5)
        self.stopListening()

        if not self.route:
            self.routeLock.acquire(timeout=1)

        if self.route:
            self.sayAnimated('Thank you')
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, I didn\'t catch that. Can you maybe say that again?')
            self.speechLock.acquire()
            self.get_travel_route(repeated=True)

    def get_entrance(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.sayAnimated('How did you get into The Netherlands?')
            self.speechLock.acquire()
            self.stopListening()
        else:
            self.stopListening()

        self.entrance = None
        self.entranceLock = Semaphore(0)
        self.setAudioContext('entrance')

        self.startListening()
        self.entranceLock.acquire(timeout=5)
        self.stopListening()

        if not self.entrance:
            self.entranceLock.acquire(timeout=1)

        if self.entrance:
            self.stopListening()
            self.sayAnimated('Thank you')
            self.speechLock.acquire()
            self.stopListening()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, I didn\'t catch that. What mode of transport did you say you used to get here?')
            self.speechLock.acquire()
            self.stopListening()
            self.get_entrance(repeated=True)

    def get_documentation(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.sayAnimated('Are you in possession of proper documentation?')
            self.speechLock.acquire()
            self.stopListening()

        self.documentation = None
        self.documentationLock = Semaphore(0)
        self.setAudioContext('yesno')

        self.startListening()
        self.documentationLock.acquire(timeout=5)
        self.stopListening()

        if not self.documentation:
            self.documentationLock.acquire(timeout=1)

        if self.documentation:
            self.sayAnimated('OK!.')
            self.speechLock.acquire()
        else:
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.speechLock.acquire()
            self.stopListening()
            self.get_documentation(repeated=True)

    def get_exclusion(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.sayAnimated(
                'Did you leave ' + self.origin + ' because you fear prosecution based on race, religion, nationality, '
                                                 'political preference or because you belong to a particular social group?')
            self.speechLock.acquire()
            self.stopListening()

        else:
            self.stopListening()

        self.exclusion = None
        self.exclusionLock = Semaphore(0)
        self.setAudioContext('exclusion')

        self.startListening()
        self.exclusionLock.acquire(timeout=5)
        self.stopListening()

        if not self.exclusion:
            self.exclusionLock.acquire(timeout=1)

        if self.exclusion:
            if self.exclusion == 'yes':
                self.say('Oh no I am sorry.')
            else:
                self.sayAnimated('Thanks.')
            self.speechLock.acquire()
            self.stopListening()
        else:
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.speechLock.acquire()
            self.stopListening()
            self.get_exclusion(repeated=True)

    def get_conflict(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.sayAnimated('Do you have legitimate reasons of becoming a victim of random violence by an armed '
                             'conflict in ' + self.origin + '?')
            self.speechLock.acquire()

        self.conflict = None
        self.conflictLock = Semaphore(0)
        self.setAudioContext('conflict')

        self.startListening()
        self.conflictLock.acquire(timeout=5)
        self.stopListening()

        if not self.conflict:
            self.conflictLock.acquire(timeout=1)

        if self.conflict:
            self.sayAnimated('Ok, thank you for sharing.')
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.speechLock.acquire()
            self.get_conflict(repeated=True)

    def get_inhumanity(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.sayAnimated('Do you have legitimate reasons to fear the death penalty.. or execution.., '
                             'torture.. or other.. inhumane.. or humiliating treatment in ' + self.origin + '?')
            self.speechLock.acquire()

        self.inhumanity = None
        self.inhumanityLock = Semaphore(0)
        self.setAudioContext('inhumanity')

        self.startListening()
        self.inhumanityLock.acquire(timeout=5)
        self.stopListening()

        if not self.inhumanity:
            self.inhumanityLock.acquire(timeout=1)

        if self.inhumanity:
            if self.inhumanity == 'yes':
                self.say('I am sorry to hear that.')
            else:
                self.sayAnimated('OK.')
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.speechLock.acquire()
            self.get_inhumanity(repeated=True)

    def get_family(self, repeated=False):
        if not repeated:
            self.stopListening()
            self.sayAnimated(
                'Did your spouse, partner, father, mother or minor child recently receive a residence permit in the Netherlands?')
            self.speechLock.acquire()

        self.stopListening()

        self.family = None
        self.familyLock = Semaphore(0)
        self.setAudioContext('family')

        self.startListening()
        self.familyLock.acquire(timeout=5)
        self.stopListening()

        if not self.family:
            self.familyLock.acquire(timeout=1)

        if self.family:
            self.sayAnimated('Thank you')
            self.speechLock.acquire()
        else:
            self.stopListening()
            self.sayAnimated('Sorry, could you please answer this question with, yes, or, no?')
            self.speechLock.acquire()
            self.get_family(repeated=True)

    def wrapup(self):
        self.sayAnimated('OK ' + self.name + ' !. I think I now have all the information I need!. Thank you very much!.'
                                             ' Within a few days we will invite you for a second interview. For now.., all I can do'
                                             ' Is wishing you a good stay here in this center. Good day')
        self.speechLock.acquire()

    def main(self):
        """
        Main function to be called when running the interview. Calls the question function in the right order.
        """

        self.setRecordAudio(True)
        self.general()
        sleep(1)
        self.introduction()
        sleep(1)
        self.get_name()
        sleep(1)
        self.get_age()
        sleep(1)
        self.get_origin()
        sleep(1)
        self.get_company()
        sleep(1)
        self.get_travel_route()
        sleep(1)
        self.get_entrance()
        sleep(1)
        self.get_documentation()
        sleep(1)
        self.sayAnimated(
            'OK ' + self.name + '. We would like to know why you came to The Netherlands. Can you please answer the following '
                                'questions with yes, or, no?')
        self.speechLock.acquire()
        self.stopListening()
        self.get_exclusion()
        sleep(1)
        self.get_conflict()
        sleep(1)
        self.get_inhumanity()
        sleep(1)
        self.get_family()
        sleep(1)

        #  end interview and save answers
        self.wrapup()
        self.store_story()

    def onAudioIntent(self, *args, intentName):
        """
        Is called whenever Google Dialogflow finds an intent in the audio and saves that to the corresponding variable.
        """

        print(intentName, *args)
        if intentName == 'name' and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()
        elif intentName == 'origin' and len(args) > 0:
            self.origin = args[0]
            self.originLock.release()
        elif intentName == 'age' and len(args) > 0:
            for arg in args:
                if arg.isdigit():
                    self.age = arg
                    self.ageLock.release()
        elif intentName == 'exclusion' and len(args) > 0:
            self.exclusion = args[0]
            self.exclusionLock.release()
        elif intentName == 'conflict' and len(args) > 0:
            self.conflict = args[0]
            self.conflictLock.release()
        elif intentName == 'inhumanity' and len(args) > 0:
            self.inhumanity = args[0]
            self.inhumanityLock.release()
        elif intentName == 'family' and len(args) > 0:
            self.family = args[0]
            self.familyLock.release()
        elif intentName == 'reason' and len(args) > 0:
            self.reason = args[0]
            self.reasonLock.release()
        elif intentName == 'route' and len(args) > 0:
            self.route = args[0]
            self.routeLock.release()
        elif intentName == 'entrance' and len(args) > 0:
            self.entrance = args[0]
            self.entranceLock.release()
        elif intentName == 'yesno' and len(args) > 0:
            self.documentation = args[0]
            self.documentationLock.release()
        elif intentName == 'company' and len(args) > 0:
            self.company = args[0]
            self.companyLock.release()

    def store_story(self):
        """
        Saves the answers of the interview in a txt-file.
        """

        file_path = self.dir + '/' + self.filename + '.txt'
        file_path = self.check_path(file_path)
        with open(file_path, 'a') as f_out:
            f_out.write('Name: ' + self.name + '\n')
            f_out.write('Age: ' + self.age + '\n')
            f_out.write('Country of origin: ' + self.origin + '\n')
            f_out.write('Company: ' + self.company + '\n')
            f_out.write('First country of arrival: ' + self.route)
            if self.route.lower() != 'the netherlands':
                f_out.write(' >>> DUBLIN PROCEDURE\n')
            else:
                f_out.write('\n')
            f_out.write('Entrance: ' + self.entrance + '\n')
            f_out.write('Documentation: ' + self.documentation + '\n')
            f_out.write('Exclusion: ' + self.exclusion + '\n')
            f_out.write('Conflict: ' + self.conflict + '\n')
            f_out.write('Inhumanity: ' + self.inhumanity + '\n')
            f_out.write('Family with a permit: ' + self.family + '\n')
        return

    def check_path(self, file_path):
        """
        Helper function for store_story() to save file correctly.
        """
        i = 1
        while os.path.isfile(file_path):
            file_path = self.dir + '/' + self.filename + '_' + '{i}'.format(i=i) + '.txt'
            i += 1
        return file_path


# run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
