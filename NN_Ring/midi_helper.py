# 00 - Import Dependencies
import pygame.midi

def get_wave_device_info():
    pygame.midi.init()

    for i in range(pygame.midi.get_count()):
        interf, name, is_input, output, opened = pygame.midi.get_device_info(i)

        name_decoded = name.decode()
        if is_input and "Wave" in name_decoded:
            result = i, name_decoded

    return result


    pygame.midi.quit()