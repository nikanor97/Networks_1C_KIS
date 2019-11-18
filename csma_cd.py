import time
import random

FRAME_LENGTH = 20  # Длина кадра
TICK_LENGTH = 0.1  # Длительность тика (в секундах) (удобно для демонстрации)


class Node:

    def __init__(self, name):
        self.name = name  # Имя ноды (целое число)
        self.start_time = 0  # Внутреннее время начала отправки
        self.end_time = 0  # Предположительное время конца отправки
        self.num_collisions = 0  # Кол-во уже произошедших коллизий для данной ноды
        self.wait_until = None  # Момент времени (по внутренним часам), до которого нода будет ждать,
                                # прежде чем попытается отправить кадр

    def send_frame(self, start_time):
        self.start_time = start_time
        self.end_time = start_time + FRAME_LENGTH

    def update_waiting(self, current_time):
        self.wait_until = current_time + self.num_collisions * 2 + random.randint(1, 10)  # например, пусть ф-ла такая


def generate_nodes(num_nodes):
    """
    Сгенерировать массив нод
    :param num_nodes: кол-во нод
    :return: массив нод
    """
    node_list = []
    for i in range(num_nodes):
        node_list.append(Node(i))
    return node_list


def get_nodes(node_list, current_time):
    """
    Получить ноды, готовые к отправке
    :param node_list: массив нод
    :param current_time: текущее (внутреннее) время
    :return: массив нод, готовых к отправке кадров
    """
    res_nodes = []
    for node in node_list:
        if node.wait_until == current_time:
            res_nodes.append(node)
    return res_nodes


def csma_cd(N):
    """
    Реализация демонстрации работы протокола
    :param N: кол-во нод
    """
    start_time = time.time()
    current_time = 0
    channel_is_free = True
    sending_node = None
    node_list = generate_nodes(N)
    while len(node_list) > 0:
        time_passed = round(time.time() - start_time, 2)
        if time_passed % TICK_LENGTH == 0:
            current_time += 1
            print('current time: ', current_time)
            print('channel is free: ', channel_is_free)
            if not channel_is_free:
                if sending_node.end_time == current_time:
                    channel_is_free = True
                    sending_node = None
                    for node in node_list:
                        node.update_waiting(current_time)
            if channel_is_free:
                for node in node_list:
                    if node.wait_until is None:
                        node.update_waiting(current_time)
                ready_nodes = get_nodes(node_list, current_time)
                print('ready_nodes_names: ', [i.name for i in ready_nodes])
                # если готовых нод > 1, то произошла коллизия, они это за 1 такт поняли и поехало дальше
                if len(ready_nodes) > 1:
                    for node in ready_nodes:
                        node.num_collisions += 1
                        node.update_waiting(current_time)
                elif len(ready_nodes) == 1:
                    channel_is_free = False
                    sending_node = ready_nodes[0]
                    print('\tSENDING NODE NAME: ', sending_node.name)
                    node_list.remove(sending_node)
                    sending_node.send_frame(current_time)
        else:
            continue


csma_cd(N=10,  # Кол-во нод
        )
