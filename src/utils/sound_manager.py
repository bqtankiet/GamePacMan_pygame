import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}  # Lưu trữ âm thanh
        self.music_volume = 0.1  # Âm lượng mặc định của nhạc nền
        self.sound_volume = 0.2  # Âm lượng mặc định của hiệu ứng âm thanh
        self.channels = [pygame.mixer.Channel(i) for i in
                         range(pygame.mixer.get_num_channels())]  # Tạo các kênh âm thanh

    def load_sound(self, name, filepath):
        """Tải một hiệu ứng âm thanh."""
        self.sounds[name] = pygame.mixer.Sound(filepath)
        self.sounds[name].set_volume(self.sound_volume)

    def play_sound(self, name, loops=0):
        """Phát một hiệu ứng âm thanh."""
        if name in self.sounds:
            self.sounds[name].play(loops=loops)
        else:
            print(f"Sound '{name}' not found!")

    def stop_sound(self, name):
        """Dừng một hiệu ứng âm thanh."""
        if name in self.sounds:
            self.sounds[name].stop()
        else:
            print(f"Sound '{name}' not found!")

    def load_music(self, filepath):
        """Tải nhạc nền."""
        pygame.mixer.music.load(filepath)

    def play_music(self, loops=-1):
        """Phát nhạc nền."""
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        """Dừng nhạc nền."""
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        """Điều chỉnh âm lượng nhạc nền."""
        self.music_volume = max(0, min(1, volume))  # Đảm bảo giá trị từ 0 đến 1
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):
        """Điều chỉnh âm lượng hiệu ứng âm thanh."""
        self.sound_volume = max(0, min(1, volume))  # Đảm bảo giá trị từ 0 đến 1
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def fadeout_music(self, time_ms):
        """Tắt nhạc nền từ từ."""
        pygame.mixer.music.fadeout(time_ms)

    def stop_all(self):
        """Tắt tất cả âm thanh (nhạc nền và hiệu ứng âm thanh)."""
        # Dừng nhạc nền
        self.stop_music()

        # Dừng tất cả các kênh âm thanh
        for channel in self.channels:
            if channel.get_busy():  # Kiểm tra nếu kênh đang phát
                channel.stop()
