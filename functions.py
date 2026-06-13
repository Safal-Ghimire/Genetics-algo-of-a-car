import math

import numpy
import pygame

from common import *


def magnitude(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def dotprdct(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def anglef(line1, line2):
    """fids the angle between tow lines"""
    vec1 = (line1[0][0] - line1[1][0], line1[0][1] - line1[1][1])
    vec2 = (line2[0][0] - line2[1][0], line2[0][1] - line2[1][1])
    mag_vec1 = magnitude(vec1)
    mag_vect2 = magnitude(vec2)

    angle = math.acos(dotprdct(vec2, vec1) / (mag_vec1 * mag_vect2))


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def create_road_body(all_road_body):
    all_rect_body = []
    for all_cords in all_road_body:
        for cords in all_cords:
            new_rect = pygame.Rect(cords[0], cords[1], 2, 2)

            all_rect_body.append(new_rect)

    return all_rect_body


def get_road_body_center(road_body):
    center = []
    for body in road_body:
        center.append(body.center)
    return center


def fill_empty_spaces(all_road_body):
    for all_coords in all_road_body:
        if len(all_coords) > 0:
            for i in range(0, len(all_coords) - 1):
                pygame.draw.line(screen, (0, 0, 0), all_coords[i], all_coords[i + 1], 4)


def draw_before_updating(coords):
    """#draw while the all_road list is yet to be updated the road is drawn first"""
    if len(coords) > 0:
        for i in range(0, len(coords) - 1):
            pygame.draw.line(screen, (0, 0, 0), coords[i], coords[i + 1], 4)


def road_in_vision(road, position):
    seen_road = []
    for road_list in road:
        for road_coordinate in road_list:
            if distance(position, road) < vision_threshold:
                seen_road.append(road_coordinate)


def draw_finish_point(finish_point):
    pygame.draw.circle(screen, (23, 255, 255), finish_point, 20, width=1)


def relu(vals):
    n = len(vals)
    for i in range(n):
        if vals[i] < 0:
            vals[i] = 0
    return vals


def mutate_weights_old(weights, mutation_rate):
    # Add small Gaussian noise as mutation
    mutation = numpy.random.normal(0, mutation_rate, weights.shape)
    new_weights = weights + mutation

    return new_weights


def mutate_weights(weights, mutation_rate, mutation_strength):
    # Add small  noise as mutation first by producing a mask
    # a mask is a set of random events happening based on the probanility given

    mask = (numpy.random.random(weights.shape) < mutation_rate).astype(
        int
    )  # first generate a random probability score between 0 and 1 if it is less then the mutation rate or (in simple terms probability) set it to 1 else 0 it generate a random true event based on the probability given

    mutation = numpy.random.normal(0, mutation_strength, weights.shape)

    new_weights = weights + mutation * mask

    return new_weights


def calculate_points(start, end, position, total_forward_press):
    dist_to_end = distance(position, end)
    dist_from_start = distance(position, start)
    if dist_to_end == 0:
        dist_to_end = 0.0001  # prevent division by zero
    score = -5 * (dist_to_end) + 0.6 * dist_from_start + 0.2 * total_forward_press

    print(f"forward:{total_forward_press}")
    return score


def get_max_index(vals):
    n = len(vals)
    max_index = 0
    # choosing the action to do
    for i in range(n):
        if vals[max_index] < vals[i]:
            max_index = i

    return max_index


def render_text(val, place, color=(0, 0, 0)):
    text_surface = font.render(val, True, color)
    screen.blit(text_surface, place)


def calculate_angle(position, check_cordinates):
    dx = position[0] - check_cordinates[0]
    dy = position[1] - check_cordinates[1]
    angle = math.atan2(-dy, dx)  # - because of coordinate system of pygame
    angle = math.degrees(angle)
    return angle


def split_list(given_list, value):
    First_list = []
    Second_list = []
    index = given_list.index(value)
    for i in range(0, index):
        First_list.append(given_list[i])
    for i in range(index + 1, 0):
        Second_list.append(given_list[i])
    final = [First_list, Second_list]
    return final


# pygame.draw.circle(surface, color, center, radius, width=0)
