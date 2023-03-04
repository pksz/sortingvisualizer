import pygame
import random
import time
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	INDIGO =75,0,130
	YELLOW=(255,255,0)
	ORANGE=255, 165, 0
	BACKGROUND_COLOR = INDIGO

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]
	FONT = pygame.font.SysFont('comicsans', 20)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	SIDE_PAD = 300
	TOP_PAD = 150

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
		self.block_height = int((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD  //10
	
#button class
class Button():
	def __init__(self,color,x,y,width,height,text):
		self.width=width
		self.height=height
		self.x=x
		self.y=y
		self.text=text
		self.color=color

	#draw button on screen
	def draw_button(self,draw_info,outline=None):
		win=draw_info.window
		if outline:
			pygame.draw.rect(win,outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height),0)
		buttontext=draw_info.FONT.render(self.text,1,draw_info.GREEN)
		draw_info.window.blit(buttontext,(self.x,self.y))
	
		
	def isOver(self,pos):
		if pos[0] > self.x and pos[0] < self.x  + self.width :
			if pos[1] > self.y  and pos[1] < self.y  + self.height:
				return True
			return False
	

	

def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.ORANGE)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	#controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	#draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	#sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	#draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))
	b1=Button(draw_info.INDIGO,1015,55,120,50,"Bubble Sort")
	b2=Button(draw_info.INDIGO,1015,115,150,50,"Insertion Sort")
	b3=Button(draw_info.INDIGO,1015,175,150,50,"Selection Sort")
	b4=Button(draw_info.INDIGO,1015,235,150,50,"Merge Sort")
	b5=Button(draw_info.INDIGO,1015,295,120,50,"Heap Sort")
	b6=Button(draw_info.INDIGO,1015,355,120,50,"Quick Sort")
	
	orderselectA=Button(draw_info.INDIGO,1015,415,120,50,"Ascending")
	orderselectB=Button(draw_info.INDIGO,1015,475,120,50,"Descending")

	randomizevalues=Button(draw_info.INDIGO,1015,535,120,50,"New List")
	sortbutton=Button(draw_info.INDIGO,1015,615,120,50,"Sort values")
	
	b1.draw_button(draw_info,(0,0,0))
	b2.draw_button(draw_info,(0,0,0))
	b3.draw_button(draw_info,(0,0,0))
	b4.draw_button(draw_info,(0,0,0))
	b5.draw_button(draw_info,(0,0,0))
	b6.draw_button(draw_info,(0,0,0))
	orderselectA.draw_button(draw_info,(0,0,0))
	orderselectB.draw_button(draw_info,(0,0,0))
	randomizevalues.draw_button(draw_info,(0,0,0))
	sortbutton.draw_button(draw_info,(0,0,0))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst
	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//10, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, (draw_info.block_height*(val))))

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst

#bubble sort

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

#insertion sort

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
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

#selection sort
def selection_Sort(draw_info, ascending=True):
	lst=draw_info.lst

	for step in range(len(lst)):
		min_idx = step

		for i in range(step+1, len(lst)):
         
            # to sort in descending order, change > to < in this line
            # select the minimum element in each loop
			
			if lst[i] < lst[min_idx] and ascending:
				min_idx = i
			else:
				if lst[i] > lst[min_idx] and  not ascending:
					min_idx = i
			draw_list(draw_info, {step: draw_info.GREEN, min_idx: draw_info.RED}, True)
		
			
        # put min at the correct position
		(lst[step], lst[min_idx]) = (lst[min_idx], lst[step])
		
		yield True
	return lst

#selection sort end

#merge sort
def merge(draw_info,arr, l, m, r, ascending):

	n1 = m - l + 1
	n2 = r - m

# create temp arrays
	L = [0] * (n1)
	R = [0] * (n2)

# Copy data to temp arrays L[] and R[]
	for i in range(0, n1):
		L[i] = arr[l + i]

	for j in range(0, n2):
		R[j] = arr[m + 1 + j]

	# Merge the temp arrays back into arr[l..r]
	i = 0     # Initial index of first subarray
	j = 0     # Initial index of second subarray
	k = l     # Initial index of merged subarray

	while i < n1 and j < n2:
		if(ascending):
			if L[i] <= R[j]:
				arr[k] = L[i]
				c = l+i
				i += 1
			else:
				arr[k] = R[j]
				c = m + l + j
				j += 1
			k += 1

		elif(not ascending):
			if L[i] >= R[j]:
				arr[k] = L[i]
				c = l+i
				i += 1
			else:
				arr[k] = R[j]
				c = m + l + j
				j += 1
			k += 1
		draw_list(draw_info, {k: draw_info.GREEN, c-1: draw_info.RED}, True)
		time.sleep(0.04)

# Copy the remaining elements of L[], if there
# are any
	while i < n1:
		arr[k] = L[i]
		c=l+i
		i += 1
		k += 1
		draw_list(draw_info, {k: draw_info.GREEN, c: draw_info.RED}, True)
		time.sleep(0.04)
# Copy the remaining elements of R[], if there
# are any
	while j < n2:
		arr[k] = R[j]
		c = l + m +j
		j += 1
		k += 1
		draw_list(draw_info, {k: draw_info.GREEN, c: draw_info.RED}, True)
		time.sleep(0.04)
# l is for left index and r is right index of the
# sub-array of arr to be sorted


def mergeSort(draw_info,arr, l, r,ascending):
	if l < r:

# Same as (l+r)//2, but avoids overflow for
# large l and h
		m = l+(r-l)//2

# Sort first and second halves
		mergeSort(draw_info,arr, l, m,ascending)	
		mergeSort(draw_info,arr, m+1, r,ascending)
		merge(draw_info,arr, l, m, r,ascending)
	

def merge_Sort(draw_info,ascending=True):	
	arr=draw_info.lst
	lenarr=len(arr)-1
	mergeSort(draw_info,arr,0,lenarr,ascending)
	yield True


	

#mergesort end
	
# heap sort

# To heapify subtree rooted at index i.
# n is size of heap


def heapifyAsc(draw_info,arr, N, i):
	largest = i # Initialize largest as root
	smallest =i
	l = 2 * i + 1	 # left = 2*i + 1
	r = 2 * i + 2	 # right = 2*i + 2

	# See if left child of root exists and is
	# greater than root
	if l < N and arr[largest] < arr[l]:
		largest = l

	# See if right child of root exists and is
	# greater than root
	if r < N and arr[largest] < arr[r]:
		largest = r
		draw_list(draw_info, {r: draw_info.GREEN,i:draw_info.RED}, True)
	# Change root, if needed
	if largest != i:
		arr[i], arr[largest] = arr[largest], arr[i] # swap
		draw_list(draw_info, {i: draw_info.GREEN,i:draw_info.RED}, True)
		time.sleep(0.05)
		# Heapify the root.
		heapifyAsc(draw_info,arr, N, largest)

def heapifyDesc(draw_info,arr, n, i):
    smallest = i # Initialize smallest as root
    l = 2 * i + 1 # left = 2*i + 1
    r = 2 * i + 2 # right = 2*i + 2
 
    # If left child is smaller than root
    if l < n and arr[l] < arr[smallest]:
        smallest = l
 
    # If right child is smaller than
    # smallest so far
    if r < n and arr[r] < arr[smallest]:
        smallest = r
        draw_list(draw_info, {r: draw_info.GREEN,i:draw_info.RED}, True)
    # If smallest is not root
    if smallest != i:
        (arr[i],arr[smallest]) = (arr[smallest],arr[i])
        draw_list(draw_info, {i: draw_info.GREEN,i:draw_info.RED}, True)
        time.sleep(0.05)
 
        # Recursively heapify the affected
        # sub-tree
        heapifyDesc(draw_info,arr, n, smallest)

# The main function to sort an array of given size


def heapSort(draw_info, ascending=True):
	arr=draw_info.lst
	N = len(arr)
	if (ascending):
	# Build a maxheap.
		for i in range(N//2 - 1, -1, -1):
			heapifyAsc(draw_info,arr, N, i)

	# One by one extract elements
		for i in range(N-1, 0, -1):
			arr[i], arr[0] = arr[0], arr[i] # swap
			heapifyAsc(draw_info,arr, i, 0)
			draw_list(draw_info, {i: draw_info.GREEN,0:draw_info.RED}, True)
	if (not ascending):
	# Build a maxheap.
		for i in range(N//2 - 1, -1, -1):
			heapifyDesc(draw_info,arr, N, i)

	# One by one extract elements
		for i in range(N-1, 0, -1):
			arr[i], arr[0] = arr[0], arr[i] # swap
			heapifyDesc(draw_info,arr, i, 0)
			draw_list(draw_info, {i: draw_info.GREEN,0:draw_info.RED}, True)
		yield True
		yield True
	
#heap sort end

#quicksort
def quick_Sort(draw_info,ascending=True):
	arr=draw_info.lst
	start=0
	end=len(arr)-1
	quick_sort(draw_info,arr,start,end,ascending)
	yield True

def partition(draw_info,array, start, end,ascending):
    pivot = array[start]
    low = start + 1
    high = end
    val=array.index(pivot)
    if ascending:
        while True:
        # If the current value we're looking at is larger than the pivot
        # it's in the right place (right side of pivot) and we can move left,
        # to the next element.
        # We also need to make sure we haven't surpassed the low pointer, since that
        # indicates we have already moved all the elements to their correct side of the pivot
            while low <= high and array[high] >= pivot:
                high = high - 1
                draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED,end:draw_info.BLACK}, True)
                time.sleep(0.02)
        # Opposite process of the one above
            while low <= high and array[low] <= pivot:
                low = low + 1
                draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED,end:draw_info.BLACK}, True)
                time.sleep(0.02)
        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
            if low <= high:
                array[low], array[high] = array[high], array[low]
                draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED,end:draw_info.BLACK}, True)
                time.sleep(0.02)

            
            else:
                break


    if(not ascending):
        while True:
        
            while low <= high and array[high] <= pivot:
                high = high - 1
                draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED,end:draw_info.BLACK}, True)
                time.sleep(0.02)
        # Opposite process of the one above
            while low <= high and array[low] >= pivot:
                low = low + 1
                draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED,end:draw_info.BLACK}, True)
                time.sleep(0.02)
        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
            if low <= high:
                array[low], array[high] = array[high], array[low]
                draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED,end:draw_info.BLACK}, True)
                time.sleep(0.02)
            else:
                break
        		
    array[start], array[high] = array[high], array[start]
    #draw_list(draw_info, {val: draw_info.YELLOW,low:draw_info.GREEN,high:draw_info.RED}, True)
    #time.sleep(0.2)
    return high

def quick_sort(draw_info,array, start, end,ascending):
    if start >= end:
        return

    p = partition(draw_info,array, start, end,ascending)
    quick_sort(draw_info,array, start, p-1,ascending)
    quick_sort(draw_info,array, p+1, end,ascending)


#quicksort end
		
	


def main():
	run = True
	clock = pygame.time.Clock()

	n = 100
	min_val = 1
	max_val = 200

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1200, 790, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None



	randomizevalues=Button(draw_info.INDIGO,550,70,200,60,"New List")
	sortbutton=Button(draw_info.INDIGO,15,120,200,60,"sort values")

	bubblebutton=Button(draw_info.INDIGO,1015,55,120,50,"Bubble Sort")
	insertionbutton=Button(draw_info.INDIGO,1015,115,150,50,"Insertion Sort")
	selectionbutton=Button(draw_info.INDIGO,1015,175,150,50,"Selection Sort")
	mergebutton=Button(draw_info.INDIGO,1015,235,150,50,"Merge Sort")
	heapbutton=Button(draw_info.INDIGO,1015,295,120,50,"Heap Sort")
	quickbutton=Button(draw_info.INDIGO,1015,355,120,50,"Quick Sort")
	
	orderselectA=Button(draw_info.INDIGO,1015,415,120,50,"Ascending")
	orderselectB=Button(draw_info.INDIGO,1015,475,120,50,"Descending")

	randomizevalues=Button(draw_info.INDIGO,1015,535,120,50,"New List")
	sortbutton=Button(draw_info.INDIGO,1015,615,120,50,"Sort values")
	while run:
		clock.tick(60)

		bubblebutton.draw_button(draw_info,(0,0,0))
		insertionbutton.draw_button(draw_info,(0,0,0))
		selectionbutton.draw_button(draw_info,(0,0,0))
		mergebutton.draw_button(draw_info,(0,0,0))
		heapbutton.draw_button(draw_info,(0,0,0))
		quickbutton.draw_button(draw_info,(0,0,0))
		orderselectA.draw_button(draw_info,(0,0,0))
		orderselectB.draw_button(draw_info,(0,0,0))
		randomizevalues.draw_button(draw_info,(0,0,0))
		sortbutton.draw_button(draw_info,(0,0,0))

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info,sorting_algo_name, ascending)

		for event in pygame.event.get():
			pos = pygame.mouse.get_pos()

			if event.type == pygame.QUIT:
				run = False
			if event.type != pygame.MOUSEBUTTONDOWN:
				continue
			if event.type == pygame.MOUSEBUTTONDOWN:
				if bubblebutton.isOver(pos):
					sorting_algorithm = bubble_sort
					sorting_algo_name = "Bubble Sort"
					print('bubble')
				elif insertionbutton.isOver(pos):
					sorting_algorithm = insertion_sort
					sorting_algo_name = "Insertion Sort"
					print('insert')
				elif selectionbutton.isOver(pos):
					sorting_algorithm=selection_Sort
					sorting_algo_name="Selection sort"
					print('select')
				elif mergebutton.isOver(pos):
					sorting_algorithm=merge_Sort
					sorting_algo_name="Merge Sort"
					print('merge')
				elif heapbutton.isOver(pos):
					sorting_algorithm=heapSort
					sorting_algo_name="Heap Sort"
					print('heap')
				elif quickbutton.isOver(pos):
					print('quick')
					sorting_algorithm=quick_Sort
					sorting_algo_name="quick Sort"
				elif orderselectA.isOver(pos):
					ascending = True
					print('ascending')
				elif orderselectB.isOver(pos):
					ascending = False
					print('descending')
				elif sortbutton.isOver(pos):
					sorting = True
					sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
				elif randomizevalues.isOver(pos):
					lst = generate_starting_list(n, min_val, max_val)
					draw_info.set_list(lst)
					sorting=False


	pygame.quit()


if __name__ == "__main__":
	main()