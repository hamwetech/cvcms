from django.shortcuts import render
from django.views import View

from messaging.forms import SMSForm


class SendSMSView(View):

    template_name = 'admin/messaging/send_message.html'

    def get(self, request, *args, **kwargs):
        form = SMSForm()
        context = {
            'form': form
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SMSForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            # process SMS sending...
            print(phone, message)
        else:
            form = SMSForm()

        return render(request, "sms_form.html", {"form": form})
