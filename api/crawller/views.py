import logging
import os
import pickle
import random
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from crawller.models import User
from api.celery_app.crawller_task import user_queue

logger = logging.getLogger(__name__)

def handle_uploaded_file(file_name, percent=0.1):
    
    with open(os.path.join(settings.MEDIA_ROOT, file_name), 'rb+') as destination:
        users_id = pickle.load(destination)
    logger.error(f"Load Users ids")
    user_sample = random.sample(users_id, int(len(users_id) * percent))

    logger.error(f"{len(user_sample)} user's following and followers should be extracted!")
    return user_sample



def home(request):
    try:
        users_count = User.objects.all().count()
        latest_time = User.objects.order_by('-saved_at')[0]
        first_time = User.objects.order_by('saved_at')[0]
    except Exception as e:
        logger.error(e)
        users_count = 0
        latest_time = first_time = None

    return render(request, 'home.html', { 'users_count': users_count, 
            "starting_time":first_time.saved_at, "latest_time":latest_time.saved_at})



def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        logger.error("submit: " + str(request.POST.get("submit")))
        logger.error("crawl: " + str(request.POST.get("crawl")))
        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        logger.error("filename: "+ filename)
        uploaded_file_url = fs.url(filename)
        if request.POST.get("submit"):
        
            return render(request, 'simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })
        elif request.POST.get("crawl"):
            users_id = handle_uploaded_file(filename)
            user_queue.apply_async((users_id,))
            return render(request, 'simple_upload.html', {
                'user_id_set': str(filename)
            })


    return render(request, 'simple_upload.html')

