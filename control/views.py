import io
import mimetypes
from threading import Thread

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import User
from control.forms import sendMessageForm
from control.models import Tasks
from control.tasks import sendMessageTask
from sponsors.models import Sponsors


# fayil turini olish uchun
def get_file_mime_type(file):
    file_name = file.name
    mime_type, _ = mimetypes.guess_type(file_name)
    mime_type = mime_type.split("/")[0]
    return mime_type


class HomePage(LoginRequiredMixin,View):

    def get(self, request):
        context = {
            "users": User.objects.all().count(),
            "sponsors": Sponsors.objects.all().count(),
            "tasks": Tasks.objects.order_by("id").reverse().all()
        }

        return render(request, "dashboard.html", context=context)


class sendMessagePage(LoginRequiredMixin,View):

    def get(self, request):
        form = sendMessageForm()
        context = {
            "form": form
        }

        return render(request, "control/send-message.html", context)

    def post(self, request):
        global kbs
        form = sendMessageForm(data=request.POST)

        context = {
            "form": form
        }

        if not form.is_valid():
            return render(request, "control/send-message.html", context)

        file = request.FILES.get("file", None)

        message = form.data.get("message")

        mime_type = "text"
        try:
            mime_type = get_file_mime_type(file)
        except Exception as e:
            print(e)

        keyboards = form.data.get("keyboards", None)
        if keyboards is not None:
            validator = URLValidator()
            keyboards = str(keyboards).replace("\r", "").split("\n")
            kbs = []
            for keyboard in keyboards:
                keyboard = keyboard.split("=")
                if len(keyboard) != 2:
                    continue

                url = keyboard[1].replace(" ", "")
                try:
                    validator(url)
                except ValidationError as e:
                    form.add_error("keyboards", "Tugma nato'g'ri formatda kiritildi")
                    return render(request, "control/send-message.html", context)

                kbs.append({"title": keyboard[0], "url": url})

        if len(kbs) == 0:
            kbs = None
        if kbs is None and (keyboards is not None and "" != str(keyboards[0]).replace(" ", "")):
            form.add_error("keyboards", "Tugma nato'g'ri formatda kiritildi")
            return render(request, "control/send-message.html", context)

        bio = None

        if file is not None:
            content = file.read()

            bio = io.BytesIO(content)

        task = Tasks()
        task.save()

        task = Thread(target=sendMessageTask,
                      kwargs={'type': mime_type, "keyboards": kbs, "file": bio, "message": message, "task": task.id})
        task.start()

        messages.success(request, "Foydalanuvchilarga xabar yuborish boshlandi")
        return redirect(reverse("adm:home"))


class taskStatusApi(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Tasks, id=pk)
        context = {
            "task": task.id,
            "total": task.total,
            "done": task.done,
            "error": task.error,
            "success": task.success,
        }
        return Response(context)
