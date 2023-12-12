import pygame
from grid import *
from socketHandler import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("map_builder")
clock = pygame.time.Clock()
running = True

mouse_button = 0

keys =[pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4]


def data_receive_event(received_data):
    #print(received_data)
    data = list(map(str, received_data.split(';')))
    
    if data[0] == 'init':
        if(len(data[1]) != 0):
            data_ = data[1][1:-1]
            data__ = data_.replace(" ", "")
            data___ = list(map(int,data__.split(',')))
            grid.load_checked(data___)


    if data[0] == 'click':
        grid.check_by_grid_coordinate(int(data[2]),int(data[3]),int(data[1]),int(data[4]))


socketHandler = SocketHandler("127.0.0.1", 2000, receive_callback=data_receive_event)

def draw():
    grid.draw_grid(screen)
    pygame.display.flip()


def event_handler(e):
    global mouse_button

    if e.type == pygame.MOUSEBUTTONDOWN:
        mouse_button = e.button
        grid.check_by_click(e.pos, mouse_button)
        socketHandler.send_message('click;'+ str(mouse_button)+ ';' + str(grid.mouse_coordinate_to_grid_coordinate(e.pos)[0]) + ';' +str(grid.mouse_coordinate_to_grid_coordinate(e.pos)[1]) + ';' + str(grid.selected_color))
    if e.type == pygame.KEYDOWN:
        for i in range(len(keys) - 1):
            if e.key == keys[i]:
                if i <= len(grid.colors) - 1: 
                    grid.selected_color = i

def main():
    global grid
    global socketHandler
    grid = Grid(screen_size)
    grid.append_grid()
    socketHandler.connect()
    socketHandler.start_receive_thread()


def loop():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            event_handler(event)

        draw()
        clock.tick(60)


def exit():
    socketHandler.close()
    pygame.quit()


if __name__ == "__main__":
    main()
    loop()
    exit()
