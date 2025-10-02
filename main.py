from datacenter.models import Schoolkid, Mark, Commendation, Lesson, Chastisement
import random


def fix_marks(child):
	all_bad_marks = Mark.objects.filter(schoolkid=child, points__lt=4)
	print(Mark.objects.filter(schoolkid=child, points__lt=4).count())
	for bad_mark in all_bad_marks:
		bad_mark.points = 5
		bad_mark.save()
	print(Mark.objects.filter(schoolkid=child, points__lt=4).count())


def remove_chastisements(child):
	comments = Chastisement.objects.filter(schoolkid=child)
	comments.delete()


def create_commendation(child, school_subject, praise):
	lessons = Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter, subject__title__contains=school_subject).order_by("-date")
	lesson = random.choice(lessons)
	Commendation.objects.create(schoolkid=child, subject=lesson.subject, teacher=lesson.teacher, created=lesson.date, text=random.choice(praise))

def main():
    try:
        child = Schoolkid.objects.get(full_name__contains="Фролов Иван")
    except Schoolkid.DoesNotExist:
        print("Ученик не найден.")
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников с таким именем.")
		

if __name__ == '__main__':
	main()