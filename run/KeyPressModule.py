import pygame


def init():
    pygame.init()
    win = pygame.display.set_mode((100, 100))


def get_key(key_name):
    answer = False
    for eve in pygame.event.get():pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame,'K_{}'.format(key_name))
    if key_input [my_key]:
        answer = True
    pygame.display.update()
    return answer


def main():
    if get_key('UP'):
        print('UP Key was pressed')

    if get_key('DOWN'):
        print('DOWN Key was pressed')

    if get_key('LEFT'):
        print('LEFT Key was pressed')

    if get_key('RIGHT'):
        print('RIGHT Key was pressed')

if __name__ == "__main__":
    init()
    while True:
        main()