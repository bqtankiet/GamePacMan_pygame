import pygame

class SoundManager:
    pygame.mixer.init()
    BackgroundMusic = pygame.mixer.Sound("../resource/sounds/background_qaqxCP52.mp3")
    BackgroundMusic.set_volume(0.5)

    ButtonSound = pygame.mixer.Sound("../resource/sounds/sound-effect/credit.wav")

