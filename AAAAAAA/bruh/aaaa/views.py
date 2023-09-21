from django.shortcuts import render, HttpResponse
from aaaa.models import User, Product, Status, Access, Lesson
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

# Create your views here.

def bruh(request):
    userID = request.GET.get('user')
    accesses = Access.objects.filter(user = userID)
    setOfLessons = set()
    for access in accesses:
        lessons = Lesson.objects.filter(productID = access.product)
        setOfLessons.update(lessons)

    response = ""

    for lesson in setOfLessons:
        status = Status.objects.filter(user = userID, lesson = lesson).first()
        if status == None:
            response += f"Название: {lesson.name}, статус просмотра: {False}"
        else:
            response += f"Название: {lesson.name}, статус просмотра: {status.isWathed}, время просмотра: {status.timestamp}"
    
    return HttpResponse(response)

def bruh2(request):
    user = request.GET.get('user')
    product_id = request.GET.get('product_id')

    product = get_object_or_404(Product, pk=product_id)

    lessons = Lesson.objects.filter(productID=product)

    lessons_data = []

    for lesson in lessons:
        status = Status.objects.filter(user=user, lesson=lesson).first()
        if status is not None:
            status_data = {
                'is_watched': status.isWathed,
                'timestamp': status.timestamp,
            }
        else:
            status_data = {
                'is_watched': False,
                'timestamp': None,
            }

        lesson_data = {
            'lesson_name': lesson.name,
            'status': status_data,
        }

        lessons_data.append(lesson_data)

    return JsonResponse({'lessons': lessons_data})

def bruh3(request):
    products = Product.objects.all()

    product_stats = []

    for product in products:
        total_watched_lessons = Status.objects.filter(lesson__productID=product, isWathed=True).count()

        total_time_watched = Status.objects.filter(lesson__productID=product, isWathed=True).aggregate(Sum('timecode'))['timecode__sum']

        total_students = Access.objects.filter(product=product).count()

        total_users = User.objects.count()
        product_access_count = Access.objects.filter(product=product).count()
        acquisition_percentage = (product_access_count / total_users) * 100 if total_users > 0 else 0

        product_stat = {
            'product_name': product.name,
            'total_watched_lessons': total_watched_lessons,
            'total_time_watched': total_time_watched,
            'total_students': total_students,
            'acquisition_percentage': acquisition_percentage,
        }

        product_stats.append(product_stat)

    return JsonResponse({'product_stats': product_stats})