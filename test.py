import math
import pygame
import numpy
from common import screen ,vision_threshold,ray_count,elite_count
from functions import distance,relu,mutate_weights,render_text
import random


class Car():
    def __init__(self, pos,angle,elite_rank=None,):
        self.pos = list(pos)
        self.angle = math.radians(angle)
        self.resvel = 6
        self.vel_x = math.sin(self.angle) * self.resvel
        self.vel_y = math.cos(self.angle) * self.resvel
        self.elite_rank=elite_rank
        self.coolision=False
        self.total_forward=0
        self.total_backward=0

        self.image = pygame.image.load("car.png")
        self.scaled_imgae=pygame.transform.scale(self.image,(70,50))
        self.image=self.scaled_imgae
        self.car_rect = self.image.get_rect()
        self.car_rect.center = self.pos
        self.car_mesh=pygame.mask.from_surface(self.scaled_imgae)
          # Set the starting position of the car


        #defining the fixed vertical axis of the car
        self.fixed_top=(self.pos[0],self.car_rect.top)
        self.fixed_bottom=(self.pos[0],self.car_rect.bottom)


        self.seen_road=[]
        self.vision_threshold=vision_threshold
        self.ray_count=ray_count
        self.seen_list=[]
        self.input_list_array=numpy.array(self.seen_list)

        #brain stuff
        input_size = 5 + ray_count * 2
        hidden1_size = 9
        hidden2_size = 6
        output_size = 4
        self.mutation_rate=0.1
        self.mutation_strength=0.3




        self.w_ih1 = numpy.random.uniform(-1, 1, (input_size, hidden1_size))  # shape: (17, 10)
        self.w_h1h2 = numpy.random.uniform(-1, 1, (hidden1_size, hidden2_size))  # (10, 6)
        self.w_h2o = numpy.random.uniform(-1, 1, (hidden2_size, output_size))  # (6, 4)



    def update_axis(self, rotate_condn):

        if rotate_condn < 0:  # Rotate counter-clockwise (left)
            self.angle += math.radians(7)
        elif rotate_condn > 0:  # Rotate clockwise (right)
            self.angle -= math.radians(7)

        # Normalize the angle
        self.angle %= 2 * math.pi

        # Recalculate velocity
        self.vel_x = math.sin(self.angle) * self.resvel
        self.vel_y = math.cos(self.angle) * self.resvel

    def update_posn(self, condn):

        if condn == 1:  # 1 for forward
            self.pos[0] += self.vel_x
            self.pos[1] += self.vel_y
            self.total_forward+=1
        elif condn == -1:  # -1 for backward
            self.pos[0] -= self.vel_x
            self.pos[1] -= self.vel_y
            self.total_backward+=1

        self.car_rect.center = self.pos

    def draw_car(self):
        # Rotate the car image
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.angle)+90)
        rotated_rect = rotated_image.get_rect(center=self.car_rect.center)
        screen.blit(rotated_image, rotated_rect.topleft)


    def road_in_vision(self,road):
        self.seen_road=[]
        for road_coordinate in road:
            if len(road_coordinate)>1:
                if distance(self.pos,road_coordinate)<self.vision_threshold:
                    self.seen_road.append(road_coordinate)

    def cast_ray(self,ray_count):
        sector_points = [[] for _ in range(ray_count)]
        sector_count=0
        self.seen_list=[]
        set_angle=360/ray_count
        for check_cordinates in self.seen_road:
            dx=self.pos[0]-check_cordinates[0]
            dy=self.pos[1]-check_cordinates[1]
            angle=math.atan2(-dy,dx) #- because of coordinate system of pygame
            angle=math.degrees(angle)
            if angle<0:
                angle+=360
            sector=int(angle/set_angle)
            sector_points[sector].append(check_cordinates)

            #getting average of each point in the sector
        for each_sector in sector_points:
            avgx,avgy=0,0
            n=len(each_sector)
            if n>0:
                for each_point in each_sector:
                    avgx+=each_point[0]
                    avgy+=each_point[1]
                avgx=(avgx)/n
                avgy=(avgy)/n
            if n>=1:
                self.seen_list.append([avgx,avgy])
            if n==0:

                self.seen_list.append([self.pos[0]+vision_threshold*math.sin(math.radians(set_angle*(sector_count+1)+180)), self.pos[1]+vision_threshold*math.cos(math.radians(set_angle*(sector_count+1)+180))])
            sector_count+=1


    def draw_ray(self):
        i=1
        for element in self.seen_list:

            pygame.draw.line(screen,(255,0,0),self.pos,element,2)
            pygame.draw.circle(screen, (0,0,255), element, 4, width=0)
            render_text(str(i),element)
            i+=1

    def get_input_list(self,finish):
        input_list=[]
        for each_val in self.seen_list:
            for each_coordinate in each_val:
                input_list.append(each_coordinate)
        input_list.append(self.pos[0])
        input_list.append(self.pos[1])
        input_list.append(self.angle)

        input_list.append(finish[0])
        input_list.append(finish[1])


        self.input_list_array=numpy.array(input_list)






    def brain(self):
        i_h1_prod=numpy.dot(self.input_list_array,self.w_ih1)
        activated_i_h1_prod=relu(i_h1_prod)

        h1_h2_product=numpy.dot(activated_i_h1_prod,self.w_h1h2)

        activated_h1_h2_product=relu(h1_h2_product)

        h2_o_prod=numpy.dot(activated_h1_h2_product,self.w_h2o)
        activated_h2_o_product=relu(h2_o_prod)
        max_index=0
        #choosing the action to do
        for i in range(4):
            if activated_h2_o_product[max_index]<activated_h2_o_product[i]:
                max_index=i

        return max_index #it is action to take place


    def breed(self,parent):
        parent_x=random.randint(0,len(parent)-1)
        parent_y=parent_x
        while parent_x== parent_y:#prevents both parent to be the same (or cloning)
            parent_y=random.randint(0,len(parent)-1)




        #adding random mutation

        if self.elite_rank ==None:
            mask = (numpy.random.random(self.w_ih1.shape) < 0.5).astype(int)
            self.w_ih1 = mask * parent[parent_x].w_ih1 + (1 - mask) * parent[parent_y].w_ih1
            mask = (numpy.random.random(self.w_h1h2.shape) < 0.5).astype(int)
            self.w_h1h2 = mask * parent[parent_x].w_h1h2 + (1 - mask) * parent[parent_y].w_h1h2
            mask = (numpy.random.random(self.w_h2o.shape) < 0.5).astype(int)
            self.w_h2o = mask * parent[parent_x].w_h2o + (1 - mask) * parent[parent_y].w_h2o


            self.w_ih1 = mutate_weights(self.w_ih1, self.mutation_rate,self.mutation_strength)
            self.w_h1h2 = mutate_weights(self.w_h1h2, self.mutation_rate,self.mutation_strength)
            self.w_h2o = mutate_weights(self.w_h2o, self.mutation_rate,self.mutation_strength)

        else:
            self.w_ih1=parent[self.elite_rank].w_ih1
            self.w_h1h2=parent[self.elite_rank].w_h1h2
            self.w_h2o=parent[self.elite_rank].w_h2o
















    def detect_collison(self,road):
        for coordinate in road:
            if self.car_rect.collidepoint(coordinate):
                self.coolision=True
