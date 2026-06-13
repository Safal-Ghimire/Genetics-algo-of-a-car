import math

import pygame

from car_class import Car
from common import *
from functions import (
    calculate_angle,
    calculate_points,
    create_road_body,
    distance,
    draw_before_updating,
    draw_finish_point,
    fill_empty_spaces,
    get_max_index,
    get_road_body_center,
    render_text,
    split_list,
)

car = []
parentcar = Car([200, 200], 0)
for i in range(20):
    car.append(Car([200, 200], 0, parent_status=parentcar))

car_points = []
car_cord = [200, 200]
# pygame setup
pygame.init()
pygame.font.init()

running = True
drawing = False
erase = False
draw_session = 0
erase_session = 0
road = []
total_clicks = 0
all_road = []
road_body_centre = []
finish_point = (-200, -200)
f_count = 0
play = False
frame = 0
generation = 0
while running:
    for event in pygame.event.get():
        # poll for events
        if event.type == pygame.QUIT:
            running = False

        # event handling for drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # listen for left click
                drawing = not drawing
                if draw_session % 2 != 0:  # every odd mouse click is for drawing
                    all_road.append(road)
                    road = []
                draw_session += 1
                erase = False
                erase_session = 2

            if (
                event.button == 3
            ):  # listen for right click ? #i can retouch this not necessary tho
                erase = not erase

                erase_session += 1
                drawing = False
                draw_session = 4

        # steering
        keys = pygame.key.get_pressed()
        for i in range(20):
            if car[i].coolision == False:
                if keys[pygame.K_d]:  # rotate clockwise
                    car[i].update_axis(1)
                if keys[pygame.K_a]:  # rotate counter clockwise
                    car[i].update_axis(-1)
                if draw_session == 0:
                    cord = pygame.mouse.get_pos()
                    car[i].pos = list(
                        cord
                    )  # new center of car is of the position of mouse
                    car[i].car_rect.center = cord
                    car_cord = cord
        if keys[pygame.K_f] or f_count == 0:  # for finish point
            cord = pygame.mouse.get_pos()
            finish_point = tuple(cord)
            f_count += 1
        if keys[pygame.K_p]:
            play = True

    screen.fill("white")

    ############                  this is for testing only          ###############################################
    """""if f_count >=1:
        cord=pygame.mouse.get_pos()

        check_angle=calculate_angle(finish_point,cord)

        pygame.draw.line(screen,(0,255,0),finish_point,cord,4)

        render_text(str(check_angle)+"angle",(20,60))"""

    ###################           testing ends here                   ###############################################################

    # drawing road logic

    if drawing == True and draw_session >= 2:
        cord = pygame.mouse.get_pos()

        # updating the road body of the current list of drawing session
        if len(road) == 0:
            road.append(cord)

        if len(road) > 0 and distance(cord, road[-1]) > 2:
            road.append(cord)

        render_text("Drawing", (20, 50), (0, 255, 0))

        # -------------------------------------------------------------------------------------------------------------------------

    road_body = create_road_body(all_road)
    road_body_centre = get_road_body_center(road_body)
    # erasing road logic
    # this might need retouching
    if erase:
        if erase_session % 2 != 0:  # odd click
            cords = pygame.mouse.get_pos()
            cord_rect = pygame.Rect(cords[0], cords[1], 20, 20)
            collision = False

            new_road = []  # new list to store updated blocks
            for unfiltered_road_cord_bloak in all_road:
                road_cord_block = []
                for road_cord in unfiltered_road_cord_bloak:
                    if cord_rect.collidepoint(road_cord[0], road_cord[1]):
                        road_cord_block = split_list(
                            unfiltered_road_cord_bloak, road_cord
                        )
                        collision = True

                for filtered_block in road_cord_block:
                    new_road.append(filtered_block)
            if collision:
                all_road = new_road
                collision = False

            pygame.draw.rect(screen, (0, 255, 0), cord_rect)
            render_text("Erasing", (20, 50), (0, 255, 0))

    #################################################################################################-----------------
    # rendering below alll

    # all car logics
    # creating vision
    for i in range(20):
        car[i].road_in_vision(road_body_centre)
        car[i].cast_ray(ray_count)
        car[i].detect_collison(car[i].seen_road)

        # car takes action:
        if play == True and car[i].coolision == False:
            car[i].get_input_list(finish_point)
            if len(car[i].input_list_array) > 0:
                action = car[i].brain()

            if action == 0:
                car[i].update_posn(1)  # forward
            if action == 1:
                car[i].update_posn(-1)  # backward
            if action == 2:
                car[i].update_axis(1)
                # rotate_clockwise
            if action == 3:
                car[i].update_axis(-1)  # roatate_counter_clockwise

        # drawing car stuffs

        car[i].draw_car()
        car[i].draw_ray()

    # new generation every 600 frames
    if frame == int(600 / n):
        for i in range(20):
            car_points.append(
                calculate_points(
                    car_cord, finish_point, car[i].pos, car[i].total_forward
                )
                - car[i].total_backward
            )
        frame = 0
        generation += 1
        index = get_max_index(car_points)
        parentcar = car[index]
        car = []
        car_points = []

        for i in range(200):
            car.append(Car(car_cord, 0, parent_status=parentcar))

    # rendering------------------------------------------------------------------------------------------------------

    # draw while the all_road list is yet to be updated
    draw_before_updating(road)

    fill_empty_spaces(all_road)

    draw_finish_point(finish_point)

    # all text
    fps = clock.get_fps()
    fps_str = f"FPS: {fps:.2f}"

    render_text(fps_str, (20, 20))

    gen_str = f"GEN:{generation}"
    render_text(gen_str, (20, 30))

    pygame.display.flip()
    if play == True:
        frame += 1

    clock.tick(200)

pygame.quit()
