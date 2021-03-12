import cv2
import numpy as np
from collections import deque

def return_two_end_points(input_list):
    st_point = 0
    end_point = len(input_list)
    st_token = 0
    end_token = 0
    for i in range(end_point):
        if input_list[i] != 0 and st_token == 0:
            st_point = i
            st_token = 1
        if input_list[len(input_list) - 1 - i] != 0 and end_token == 0:
            end_point = len(input_list) - 1 - i
            end_token = 1
    if st_token == 0 and end_token == 0:
        return -1, -1
    else:
        return st_point, end_point

def find_edge(input_list):
    return_list = []
    for i in range(len(input_list)):
        vol_list = []
        st_point, end_point = return_two_end_points(input_list[i])
        if st_point != -1 and end_point != - 1:
            vol_list.append(i)
            vol_list.append(st_point)
            vol_list.append(end_point)
            return_list.append(vol_list)
    return_list = np.array(return_list)
    return return_list

def a4_to_serial(input_a4, cursor=np.array([0, 0])):
    return_serial = []
    vol_cursor = np.array(cursor)
    edge = find_edge(input_a4)
    y_num = 0
    state_token1 = 0

    """try start"""
    """initialize state"""
    if vol_cursor[1] == edge[y_num][0] and vol_cursor[0] == edge[y_num][1]:
        state_token1 = 1
    elif vol_cursor[1] == edge[y_num][0] and vol_cursor[0] == edge[y_num][2]:
        state_token1 = -1
    elif vol_cursor[1] == edge[y_num][0]:
        state_token1 = 3
    else:
        state_token1 = 4
    """initialize end"""

    while y_num < len(edge):

        if vol_cursor[1] == edge[y_num][0] and vol_cursor[0] == edge[y_num][1] and state_token1 == 0:
            state_token1 = 1

        elif vol_cursor[1] == edge[y_num][0] and vol_cursor[0] == edge[y_num][2] and state_token1 == 0:
            state_token1 = -1

        if state_token1 == 1:
            if input_a4[vol_cursor[1]][vol_cursor[0]] == 1:
                return_serial.append('p')
            if vol_cursor[0] < edge[y_num][2]:
                init_loc = vol_cursor
                new_loc = [vol_cursor[0] + 1, vol_cursor[1]]
                return_serial.append(direction_mov(vol_cursor, new_loc))
                vol_cursor = new_loc
            elif vol_cursor[0] == edge[y_num][2]:
                state_token1 = 4

        elif state_token1 == -1:
            if input_a4[vol_cursor[1]][vol_cursor[0]] == 1:
                return_serial.append('p')
            if vol_cursor[0] > edge[y_num][1]:
                init_loc = vol_cursor
                new_loc = [vol_cursor[0] - 1, vol_cursor[1]]
                return_serial.append(direction_mov(vol_cursor, new_loc))
                vol_cursor = new_loc
            elif vol_cursor[0] == edge[y_num][1]:
                state_token1 = 4

        elif state_token1 == 2:
            if vol_cursor[1] != edge[y_num][0]:
                init_loc = vol_cursor
                new_loc = [vol_cursor[0], vol_cursor[1] + 1]
                return_serial.append(direction_mov(vol_cursor, new_loc))
                vol_cursor = new_loc
            else:
                state_token1 = 3

        elif state_token1 == 3:
            if vol_cursor[0] - edge[y_num][1] < edge[y_num][2] - vol_cursor[0]:
                while vol_cursor[0] != edge[y_num][1]:
                    if vol_cursor[0] > edge[y_num][1]:
                        init_loc = vol_cursor
                        new_loc = [vol_cursor[0] - 1, vol_cursor[1]]
                        return_serial.append(direction_mov(vol_cursor, new_loc))
                        vol_cursor = new_loc
                    else:
                        init_loc = vol_cursor
                        new_loc = [vol_cursor[0] + 1, vol_cursor[1]]
                        return_serial.append(direction_mov(vol_cursor, new_loc))
                        vol_cursor = new_loc
            else:
                while vol_cursor[0] != edge[y_num][2]:
                    if vol_cursor[0] < edge[y_num][2]:
                        init_loc = vol_cursor
                        new_loc = [vol_cursor[0] + 1, vol_cursor[1]]
                        return_serial.append(direction_mov(vol_cursor, new_loc))
                        vol_cursor = new_loc
                    else:
                        init_loc = vol_cursor
                        new_loc = [vol_cursor[0] - 1, vol_cursor[1]]
                        return_serial.append(direction_mov(vol_cursor, new_loc))
                        vol_cursor = new_loc
            if vol_cursor[0] == edge[y_num][1] or vol_cursor[0] == edge[y_num][2]:
                state_token1 = 0

        elif state_token1 == 4:
            y_num += 1
            state_token1 = 2

        else:
            break
    """try end"""
    
    """except start"""
    """except end"""
    return return_serial