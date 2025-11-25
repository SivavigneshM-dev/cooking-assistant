from django.shortcuts import render, redirect
from .forms import FeedbackForm

def feedback_view(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect("/")
    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback_form.html", {"form": form})
