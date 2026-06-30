from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtWidgets import QApplication, QPushButton
from priceguessr.paths import audio_path
try:
    import pygame # თუ ვერ ვიწერთ pygame-ს მაინც იმუშაოს თამაშმა
except ImportError:
    pygame = None
# ეს კოდი აკონტროლებს ხმებს თამაში
##  საუნდ ეფექტებისთვის გამოვიყენეთ pygame თუნდაც შეიძლებოდა qt player გამოვიყენოთ უფრო მარტივი მომეჩვენა pygame
# audiomanager აკონტროლებს აუდიოს მთლიან კოდში click,background song,coorect,incorrect
class AudioManager(QObject): # იღებს QObject  რომ გამოვიყენოთ მისი შესაძლებლობები
    def __init__(self, parent=None): # Parent შეიძლება იყოს ობიექტი ქტსი
        super().__init__(parent) #იყენებს მშობელ  ფუნქციებს
        self.enabled = False  #ხდება True როცა ჩაიტვირთება ყველა ხმა
        self.click_sound = None
        self.correct_sound = None
        self.incorrect_sound = None
        if pygame is None:
            return
        try:
            pygame.mixer.init() # აუდიოსისტემის ინიციალიზაცია
            self.click_sound = pygame.mixer.Sound(audio_path("click.wav")) ## აქ ჩვენ ვანიჭებთ ხმებს
            self.correct_sound = pygame.mixer.Sound(audio_path("correct.mp3")) # 
            self.incorrect_sound = pygame.mixer.Sound(audio_path("incorrect.mp3"))#
            self.click_sound.set_volume(0.34)
            self.correct_sound.set_volume(0.67)
            self.incorrect_sound.set_volume(0.67)
            pygame.mixer.music.load(audio_path("background.mp3")) # background მუსიკა
            pygame.mixer.music.set_volume(0.20)
            pygame.mixer.music.play(-1, fade_ms=1000) # -1-ს გამო ის ლუპშია სულ  
            self.enabled = True # როცა ჩაიტვირთა ყველა ხმა ის გახდა True
            QApplication.instance().installEventFilter(self) # იღებს აპლიკაციის ინსტანს და აკეთებს ისე რომ audiomanager აკვირდება ივენთებს (36 ლაინი ai-დამაწერინა იმიტომ რომ არ მუშოაბდა სხვანაირად)
        except (OSError, pygame.error): # თუ ვერ ჩაიტვირთება ფაილი ან აუდი დევაისის ერრორი
            pygame.mixer.quit()

    def eventFilter(self, obj, event): # თუ ჩაიწერა ყველაფერი  თუ ევენთ არის დაჭერა და ეს არის მარცხენა დაჭერა
        if (self.enabled and event.type() == QEvent.MouseButtonPress and
                event.button() == Qt.LeftButton and
                (isinstance(obj, QPushButton) or obj.property("game_mode"))): # ამოწმებს თუ დაჭერილია QPushButton
            self.play_click() # დაკლიკვის ხმა
        return super().eventFilter(obj, event) #იმუშაოს როგორც უნდა ყოფილიყო

    def play_click(self):
        if self.enabled:
            self.click_sound.play()
    def play_correct(self): # სწორი არცევანი
        if self.enabled:
            self.correct_sound.play()
    def play_incorrect(self): #არასწორი არჩევანი
        if self.enabled:
            self.incorrect_sound.play()

    def shutdown(self): #გათიშვის კოდი
        if self.enabled:
            QApplication.instance().removeEventFilter(self)
            pygame.mixer.music.fadeout(300)
            pygame.mixer.quit()
            self.enabled = False
