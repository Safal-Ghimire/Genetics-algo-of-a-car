import pygame 
import math

from functions import distance,create_road_body,fill_empty_spaces,draw_before_updating,get_road_body_center,draw_finish_point
from car_class import Car
from common import *


car=Car([200,200],0)


#pygame setup
pygame.init()

running = True
drawing = False
draw_session=0
road = []
total_clicks=0
all_road=[]
road_body_centre=[]
finish_point=(-100,-100)
f_count=0

while running:
    for event in pygame.event.get():
        #poll for events
        if event.type == pygame.QUIT:
            running = False

        #event handling for drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1: #listen for left click
                drawing= not drawing
                if draw_session%2 is not 0: #every odd mouse click is for drawing
                    all_road.append(road)
                    road=[]
                draw_session+=1

        # steering
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: # move forward
            car.update_posn(1)
        if keys[pygame.K_s]: # move backward
            car.update_posn(-1)
        if keys[pygame.K_d]: # rotate clockwise
            car.update_axis(1)
        if keys[pygame.K_a]: # rotate counter clockwise
            car.update_axis(-1)
        
        if keys[pygame.K_f] and f_count==0: #for finish point
            cord=pygame.mouse.get_pos()
            finish_point=tuple(cord)
            f_count+=1

        
      #plaicing the car logic
    if draw_session==0:
        cord=pygame.mouse.get_pos()
        car.pos=list(cord)#new center of car is of the position of mouse
        car.car_rect.center=cord #new center of car is of the position of mouse





#drawing road logic


    if drawing == True and draw_session>=2 :
        cord = pygame.mouse.get_pos()
        
        #updating the road body of the current list of drawing session
        if len(road)==0:
            road.append(cord)

        if len(road) > 0 and  distance(cord,road[-1]) > 2:
            road.append(cord)
            print(cord)
        
            #-------------------------------------------------------------------------------------------------------------------------

    road_body = create_road_body(all_road)
    road_body_centre=get_road_body_center(road_body)
    

    #creating vision

    car.road_in_vision(road_body_centre)
    car.cast_ray(ray_count)
    
    
    screen.fill("white")

    

        



        

    











    

    #rendering------------------------------------------------------------------------------------------------------

    #draw while the all_road list is yet to be updated
    draw_before_updating(road)
    
    fill_empty_spaces(all_road)

    car.draw_car()
    car.draw_ray()
    draw_finish_point(finish_point)
    
    pygame.display.flip()

    clock.tick(80)

pygame.quit()

    