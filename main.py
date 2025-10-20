from datacenter.models import Schoolkid, Mark, Commendation, Lesson, Chastisement
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random
import argparse


def fix_marks(child):
	all_bad_marks = Mark.objects.filter(schoolkid=child, points__lt=4)
	for bad_mark in all_bad_marks:
		bad_mark.points = 5
		bad_mark.save()


def remove_chastisements(child):
	comments = Chastisement.objects.filter(schoolkid=child)
	comments.delete()


def create_commendation(child, school_subject, praise):
	lesson = random.choice(Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter, subject__title__contains=school_subject).order_by("-date"))
	if not lesson:
		print("Урок не найден")
		return
	else:
		Commendation.objects.create(schoolkid=child, subject=lesson.subject, teacher=lesson.teacher, created=lesson.date, text=random.choice(praise))


def main():
	praise = ["Молодец!", "Ты растешь над собой!", "С каждым разом у тебя получается всё лучше!", "Это как раз то, что нужно!", "Замечательно!", "Очень хороший ответ!", "Ты меня очень обрадовал!", "Ты меня приятно удивил!"]
	parser = argparse.ArgumentParser(description='Вместо плохих оценок ставит 5, удаляет плохие замечания и добавляет хорошие коментарии')
	parser.add_argument('--fullname', type=str, help='Имя ученика')
	args = parser.parse_args()
	fullname = args.fullname
	try:
		child = Schoolkid.objects.get(full_name__contains=fullname)
	except ObjectDoesNotExist:
		print("Ученик не найден.")
		return
	except MultipleObjectsReturned:
		print("Найдено несколько учеников с таким именем.")
		return
		

if __name__ == '__main__':
	main()