from datetime import datetime, timedelta

"""Формирование списка свободных окон по 30 минут"""
busy = [
	{'start': '10:30',
  	'stop': '10:50'},

	{'start': '18:40',
  	'stop': '18:50'},

 	{'start': '14:40',
  	'stop': '15:50'},

	{'start': '16:40',
  	'stop': '17:20'},

	{'start': '20:05',
  	'stop': '20:20'}
]
# Добавляем начало и конец рабочего дня в список busy
busy.insert(0, {'start': '09:00', 'stop': '09:00'})
busy.append({'start': '21:00', 'stop': '21:00'})

#Сортировка по началу занятого времени
sorted_busy = sorted(busy, key=lambda x: x['start'])

def time_to_minutes(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M')
    return time_obj.hour * 60 + time_obj.minute

# Время начала и конца рабочего дня
working_day_start = time_to_minutes('09:00')
working_day_end = time_to_minutes('21:00')

#Размер окна приёма в минутах
window_size = 30

#Список свободных окон
free = []

def insert_into_free(current_stop,next_start,window_size):
	if current_stop <= next_start - window_size:
		#Перевод из минут в часы + минуты
		free_start_hours, free_start_minutes = divmod(timedelta(minutes=current_stop)// 60, 60)
		free_end_hours, free_end_minutes = divmod(timedelta(minutes=current_stop+30) // 60, 60)

		#Формирование строк с нужным форматом для начала и окончания свободного окна
		free_start = f'{free_start_hours}:{free_start_minutes}'
		free_end = f'{free_end_hours}:{free_end_minutes}'

		free.append({'start' : free_start, 'stop' : free_end})

		# Рекурсивный вызов для заполнения оставшегося между
  		# окончанием свободного окна и началом занятого промежутка времени
		insert_into_free(current_stop+30,next_start,window_size)

#Позиция текущего занятого времени в списке
j = 0

for i in range(working_day_start,working_day_end-30, window_size):
    #Проверка на окончание рабочего дня (последнего занятого времени)
	if j < 6:
		# Перевод времени в минуты у окончания текущего
  		# занятого времени и начала следующего занятого времени
		current_stop = time_to_minutes(sorted_busy[j]['stop'])
		next_start = time_to_minutes(sorted_busy[j + 1]['start'])

		insert_into_free(current_stop,next_start,window_size)
		j += 1

print(free)
