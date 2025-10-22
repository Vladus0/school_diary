from datacenter.models import Schoolkid, Mark, Commendation, Lesson, Chastisement
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random

praise = [
	"Молодец!",
	"Ты растешь над собой!",
	"С каждым разом у тебя получается всё лучше!",
	"Это как раз то, что нужно!", "Замечательно!",
	"Очень хороший ответ!", "Ты меня очень обрадовал!",
	"Ты меня приятно удивил!"
]


def fix_marks():
	child = get_schoolkid()
	Mark.objects.filter(schoolkid=child, points__lt=4).update(points=5)


def remove_chastisements():
	child = get_schoolkid()
	comments = Chastisement.objects.filter(schoolkid=child)
	comments.delete()


def create_commendation(school_subject):
	child = get_schoolkid()
	lesson = random.choice(Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter, subject__title__contains=school_subject).order_by("-date"))
	if not lesson:
		print("Урок не найден")
		return
	else:
		Commendation.objects.create(schoolkid=child, subject=lesson.subject, teacher=lesson.teacher, created=lesson.date, text=random.choice(praise))


def get_schoolkid():
	try:
		child = Schoolkid.objects.get(full_name__contains="Фролов Иван")
		return child
	except ObjectDoesNotExist:
		print("Ученик не найден.")
		return
	except MultipleObjectsReturned:
		print("Найдено несколько учеников с таким именем.")
		return