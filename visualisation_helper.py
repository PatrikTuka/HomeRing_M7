import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
PURPLE = (169, 67, 247)
BLUE = (67, 136, 247)
PINK = (252, 0, 244)
GREEN = (93, 252, 0)
ORANGE = (252, 143, 0)

volume_set = [
    pygame.image.load("visual_assets/volume_set/speaker_mute.png"),
    pygame.image.load("visual_assets/volume_set/speaker_one.png"),
    pygame.image.load("visual_assets/volume_set/speaker_two.png"),
    pygame.image.load("visual_assets/volume_set/speaker_three.png"),
    pygame.image.load("visual_assets/volume_set/speaker_red.png")
]

album_set = [
    pygame.image.load("visual_assets/album_set/fast_car.png"),
    pygame.image.load("visual_assets/album_set/friends.png"),
    pygame.image.load("visual_assets/album_set/mamma_mia.png"),
    pygame.image.load("visual_assets/album_set/up_town_funk.png"),
    pygame.image.load("visual_assets/album_set/what_about_us.png"),
    pygame.image.load("visual_assets/album_set/with_or_without_you.png"),
]

movie_set = [
    pygame.image.load("visual_assets/movie_set/friends.png"),
    pygame.image.load("visual_assets/movie_set/queens_gambit.png"),
    pygame.image.load("visual_assets/movie_set/full_house.png"),
    pygame.image.load("visual_assets/movie_set/inception.png"),
    pygame.image.load("visual_assets/movie_set/ready_player_one.png"),
    pygame.image.load("visual_assets/movie_set/maestro_in_blue.png"),
]



def draw_tv(screen, pos_x, pos_y, is_on, volume, movie):
    #310,140
    size_outer = (390, 230)
    size_inner = (360, 200)
    border = 15

    pygame.draw.rect(screen, GRAY, (pos_x, pos_y, size_outer[0], size_outer[1]))

    if is_on:

        match volume:
            case 0.00:
                screen.blit(volume_set[0], (pos_x + 400, pos_y))
            case 0.25:
                screen.blit(volume_set[1], (pos_x + 400, pos_y))
            case 0.5:
                screen.blit(volume_set[2], (pos_x + 400, pos_y))
            case 0.75:
                screen.blit(volume_set[3], (pos_x + 400, pos_y))
            case 1.00:
                screen.blit(volume_set[4], (pos_x + 400, pos_y))

        screen.blit(movie_set[movie], (pos_x + border, pos_y + border))


    else:
        pygame.draw.rect(screen, BLACK, (pos_x+border,pos_y+border,size_inner[0],size_inner[1]))

def draw_speaker(screen, pos_x, pos_y, is_on, volume, song):
    size = (110, 350)
    large_radius = 30
    small_radius = 20
    gap = 20
    pygame.draw.rect(screen, GRAY, (pos_x, pos_y, size[0], size[1]))

    if is_on:
        pygame.draw.circle(screen, WHITE, (pos_x+(size[0]/2), pos_y + large_radius + gap), large_radius)
        pygame.draw.circle(screen, WHITE, (pos_x+(size[0]/2), pos_y + 2 * large_radius + small_radius + 2*gap), small_radius)
        pygame.draw.circle(screen, WHITE, (pos_x+(size[0]/2), pos_y + 2 * large_radius + 3 * small_radius + 3*gap), small_radius)

        match volume:
            case 0.00:
                screen.blit(volume_set[0], (pos_x + 22, pos_y - 90))
            case 0.25:
                screen.blit(volume_set[1], (pos_x + 22, pos_y - 90))
            case 0.5:
                screen.blit(volume_set[2], (pos_x + 22, pos_y - 90))
            case 0.75:
                screen.blit(volume_set[3], (pos_x + 22, pos_y - 90))
            case 1.00:
                screen.blit(volume_set[4], (pos_x + 22, pos_y - 90))

        screen.blit(album_set[song], (pos_x + 20, pos_y + 250))

    else:
        pygame.draw.circle(screen, BLACK, (pos_x + (size[0] / 2), pos_y + large_radius + gap), large_radius)
        pygame.draw.circle(screen, BLACK, (pos_x + (size[0] / 2), pos_y + 2 * large_radius + small_radius + 2 * gap), small_radius)
        pygame.draw.circle(screen, BLACK,(pos_x + (size[0] / 2), pos_y + 2 * large_radius + 3 * small_radius + 3 * gap), small_radius)


def calculate_color_value(color, brightness):
    #brightness between 0 and 1
    return (color[0]*brightness, color[1]*brightness, color[2]*brightness)

def draw_lamp(screen, pos_x, pos_y, is_on, lamp_color, brightness):
    center_point = (pos_x, pos_y)
    lamp_color_list = [WHITE, PURPLE, BLUE, GREEN, ORANGE, PINK]
    pygame.draw.rect(screen, GRAY, (pos_x, pos_y, 30, 15))
    pygame.draw.rect(screen, GRAY, (pos_x+7.5, pos_y, 15, 230))
    pygame.draw.rect(screen, GRAY, (pos_x-10, pos_y+215, 50, 15))

    if is_on:
        lamp_color = calculate_color_value(lamp_color_list[lamp_color], brightness)

    else:
        lamp_color = BLACK

    # Lamp Section
    top_left = (pos_x - 9, pos_y - 90)
    top_right = (pos_x + 39, pos_y - 90)
    bottom_left = (pos_x - 42.5, pos_y)
    bottom_right = (pos_x + 72.5, pos_y)

    vertices = [top_left, top_right, bottom_right, bottom_left]

    pygame.draw.polygon(screen, lamp_color, vertices)


def display_scene(screen, SPEAKER_controls, TV_controls, LAMP_controls):
    draw_speaker(screen, 80,220, is_on=SPEAKER_controls[0], volume=SPEAKER_controls[2], song=SPEAKER_controls[1])
    draw_tv(screen, 310, 140, is_on=TV_controls[0], volume=TV_controls[2], movie=TV_controls[1])
    draw_lamp(screen, 837, 341,is_on=LAMP_controls[0],  brightness=LAMP_controls[2], lamp_color=LAMP_controls[1])

