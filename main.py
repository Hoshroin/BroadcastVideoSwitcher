import cv2
import os, time
from random import randint

#可配置变量：
target_perfix = 'nwrt_idle' #这是视频文件的前缀名，比如：test_1.mp4，这里就填test_
target_path = './videos/' + target_perfix + '0.mp4' #这里是一打开程序就开始播放的视频文件相对路径
max_clip_index = 2 #这里填你所有片段数量减1的数值

cap = cv2.VideoCapture(target_path)
statulock = 0
ins_lock = 0
frame_counter = 0
clip_count = 0
idle_statu_repeats = 0
clip_index = 0
pre_clip_index = 0
MAX_FRAME = 0
clip_id_data = []

with open('./clip_id.virset', 'r') as f:
	tmp_fd = f.read()
	tmp_ar1 = tmp_fd.split("\n")
	for i in range(len(tmp_ar1)):
		if tmp_ar1[i] != "":
			clip_id_data.append([int(tmp_ar1[i].split(" ")[0]), tmp_ar1[i].split(" ")[1]])
	f.close()
print(clip_id_data)

print("Welcome! Now playing clip 0")
while 1:
	while cap.isOpened():
		ret, frame = cap.read()
		
		if statulock == 0:
			MAX_FRAME = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
			frame_counter = 0
			statulock = 1
		frame_counter += 1
		
		if ins_lock == 0:
			print("Clip " + str(clip_index) + " rolling - Frame " + str(frame_counter) + "/" + str(MAX_FRAME), end = '\r')
		else:
			print("Clip (" + str(ins_lock) + ") rolling - Frame " + str(frame_counter) + "/" + str(MAX_FRAME), end = '\r')
		
		if frame_counter == MAX_FRAME:
			#cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  #单片段循环
			break
			
		cv2.imshow('video', frame)
		
		k = cv2.waitKey(20)
		if k & 0xff == ord('q'):
			trgid = int(input("\nType your target clip id: "))
			if trgid != 0:
				ins_lock = trgid
				tmp_l1 = 0
				for i in range(len(clip_id_data)):
					if clip_id_data[i][0] == ins_lock:
						target_path = './videos/' + clip_id_data[i][1]
						tmp_l1 = 1
				if tmp_l1 != 1:
					ins_lock = 0
					print("*ERROR: Insert error! There are no clips that matches this id!")
			break
			
	cap.release()
	clip_count += 1
	if clip_count > 1:
		print("*COUNTER: " + str(clip_count) + " clips have been played this time!")
	else:
		print("*COUNTER: " + str(clip_count) + " clip has been played this time!")
	if ins_lock == 0:
		pre_clip_index = clip_index
		if clip_index == 0:
			if idle_statu_repeats < 1:
				clip_index = randint(1, max_clip_index)
				while 1:
					if pre_clip_index == clip_index:
						clip_index = randint(1, max_clip_index)
					else:
						break
			else:
				idle_statu_repeats -= 1
				clip_index = 0
			target_path = './videos/' + target_perfix + str(clip_index) +'.mp4'
		else:
			clip_index = 0
			idle_statu_repeats = randint(0, 1)
			if idle_statu_repeats > 1:
				print("*INFO: Repeating clip 0 for " + str(idle_statu_repeats) + " times")
			else:
				print("*INFO: Repeating clip 0 for " + str(idle_statu_repeats) + " time")
			target_path = './videos/' + target_perfix + '0.mp4'
		print("*INFO: Now playing clip " + str(clip_index))
	else:
		print("*WARN: Inserted clip (" + str(ins_lock) + ")")
		ins_lock = 0
		clip_index = 0
	cap = cv2.VideoCapture(target_path)
	statulock = 0

cap.release()
cv2.destroyAllWindows()
