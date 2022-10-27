from array import array
from ast import Yield
from pickle import TRUE
import pygame
import random
import math
import multiprocessing
import os
import time
pygame.init()
class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = BLACK

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('bahnschrift', 10)
    LARGE_FONT = pygame.font.SysFont('bahnschrift', 30)

    SIDE_PAD = 100
    TOP_PAD = 90

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render(
        "SPACE - Start Sorting", 1, draw_info.WHITE)
    draw_info.window.blit(
        controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | S- Selection Sort | Q - Quick Sort | H - Heap Sort | M - Merge Sort ", 1, draw_info.WHITE)
    draw_info.window.blit(
        sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,
                         draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * \
            draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color,
                         (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

#---------------------------------------------------------------Bubble Sort---------------------------------------------------------
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN,
                          j + 1: draw_info.RED}, True)
                yield True

    return lst

#--------------------------------------------------------------Selection Sort--------------------------------------------------------
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for step in range(len(lst)):
        min_idx = step
        for i in range(step + 1, len(lst)):
            
            if (lst[i] < lst[min_idx] and ascending) or (lst[i] > lst[min_idx] and not ascending):
                min_idx = i
        (lst[step], lst[min_idx]) = (lst[min_idx], lst[step])
        draw_list(draw_info, {step: draw_info.GREEN,min_idx: draw_info.RED}, True)
        yield True

    

    return lst

#--------------------------------------------------------------Insertion Sort--------------------------------------------------------
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN,i: draw_info.RED}, True)
            yield True

    return lst
#----------------------------------------------------------------Quick Sort----------------------------------------------------------
def partition(draw_info,array, low, high):
  pivot = array[high]
  i = low - 1
  for j in range(low, high):
    if array[j] <= pivot:
      i = i + 1
      
      (array[i], array[j]) = (array[j], array[i])
      draw_list(draw_info, {j: draw_info.GREEN,i: draw_info.RED}, True)
  (array[i + 1], array[high]) = (array[high], array[i + 1])
  return i + 1
def quickSort(draw_info,array, low, high):
    
  if low < high:
    pi = partition(draw_info,array, low, high)
    quickSort(draw_info,array, low, pi - 1)
    quickSort(draw_info,array, pi + 1, high)
def callQuicksort(draw_info, ascending=True):
    quickSort(draw_info,draw_info.lst,0,len(draw_info.lst)-1)
    yield True
    return draw_info.lst

#----------------------------------------------------------------Heap Sort-----------------------------------------------------------
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        (arr[i], arr[largest]) = (arr[largest], arr[i])  # swap
 
        heapify(arr, n, largest) 
def heapSort(draw_info,ascending):
    arr=draw_info.lst
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
 
    for i in range(n - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])  # swap
        draw_list(draw_info, {i: draw_info.GREEN,0: draw_info.RED}, True)
        yield True
        heapify(arr, i, 0)
        
    return arr

#----------------------------------------------------------------Merge Sort----------------------------------------------------------
def merge(draw_info,arr, start, mid, end):
    start2 = mid + 1
    if (arr[mid] <= arr[start2]):
        return
    while (start <= mid and start2 <= end):
        if (arr[start] <= arr[start2]):
            start += 1
        else:
            value = arr[start2]
            index = start2
            while (index != start):
                arr[index] = arr[index - 1]
                index -= 1
                draw_list(draw_info, {index: draw_info.GREEN,index-1: draw_info.RED}, True)

            arr[start] = value
            start += 1
            mid += 1
            start2 += 1 
def mergeSort(draw_info,arr, l, r):
    if (l < r):
        m = l + (r - l) // 2
        mergeSort(draw_info,arr, l, m)
        mergeSort(draw_info,arr, m + 1, r)
        merge(draw_info,arr, l, m, r)
def callMergeSort(draw_info, ascending:True):
    mergeSort(draw_info,draw_info.lst,0,len(draw_info.lst)-1)
    yield True


def main():
    run = True
    clock = pygame.time.Clock()
    n = 100
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(400, 300, lst)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
  #  c_time=pygame.time.get_ticks()   #i tried this, but this hanged the windws
   # print(c_time)   #
    while run:
        
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = callQuicksort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heapSort
                sorting_algo_name = "Heap Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = callMergeSort
                sorting_algo_name = "Merge Sort"

    pygame.quit()


if __name__ == "__main__":

    p1 = multiprocessing.Process(target=main, args=())
    p1.start()
    p2 = multiprocessing.Process(target=main, args=())
    p2.start()
    p3 = multiprocessing.Process(target=main, args=())
    p3.start()
    p4 = multiprocessing.Process(target=main, args=())
    p4.start()
    p5 = multiprocessing.Process(target=main, args=())
    p5.start()
    p6 = multiprocessing.Process(target=main, args=())
    p6.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
