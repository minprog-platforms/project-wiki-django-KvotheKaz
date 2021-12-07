import markdown2
from django.shortcuts import redirect, render
from django import forms
import random
from django.db import models
from . import util


class NewEntryForm(forms.Form):
    new_title = forms.CharField(label="Title")
    new_content = forms.CharField(label="Content")

def index(request):
    return render (request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    return render (request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(util.get_entry(title))
    })

def random_page(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return entry(request, random_page)

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_title"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new_entry_error.html")
            else:    
                content = form.cleaned_data["new_content"]
                new_entry = util.save_entry(title, content)
                return render(request, "encyclopedia/new.html", {
                    "new_entry": new_entry,
            })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "")
    if util.get_entry(query):
        return redirect('entry', title = query)
    else:
        substring_entries = []
        for entry in entries:
            if query.upper() in entry.upper():
                substring_entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": substring_entries,
    })

