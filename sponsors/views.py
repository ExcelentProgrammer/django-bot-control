import asyncio

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from bot.management.commands.loader import bot
from sponsors.models import Sponsors


class HomePage(ListView):
    template_name = "sponsors/list.html"
    model = Sponsors


class UpdatePage(UpdateView):
    template_name = "sponsors/edit.html"
    model = Sponsors
    fields = "__all__"
    success_url = reverse_lazy("sponsors:list")


class DeletePage(DeleteView):
    template_name = "sponsors/delete.html"
    model = Sponsors
    success_url = reverse_lazy("sponsors:list")


class CreatePage(CreateView):
    template_name = "sponsors/create.html"
    model = Sponsors
    fields = ['link']
    success_url = reverse_lazy("sponsors:list")

    def form_valid(self, form):
        link = self.request.POST.get("link")

        try:
            chat = bot.get_chat(link)
            name = chat.title
            me = bot.get_me()
            form.instance.name = name

            check = bot.get_chat_member(chat.id, me.id)

            if check.status != "administrator":
                messages.error(self.request, "Bot kanalda admin emas")
                return redirect(reverse("sponsors:create"))



        except Exception as e:
            print(e)
            messages.error(self.request,
                           "Kanal topilmadi yoki nato'g'ri formatda kiritdingiz example: @channel_user_name agarda bu ishlamasa kanal id raqamini yuboring")
            return redirect(reverse("sponsors:create"))

        form.save()

        return redirect(reverse("sponsors:list"))
