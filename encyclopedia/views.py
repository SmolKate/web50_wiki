from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
import re
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import secrets
import markdown2
from markdown2 import Markdown


from . import util



class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title:", required=True, widget= forms.TextInput(attrs={'style': "width:80%"}))
    content = forms.CharField(label="Content:", required=True, widget=forms.Textarea)
    field_order = ["title", "content"]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
    })

def get(request, title):
    markdowner=Markdown()
    cont=util.get_entry(title)
    if cont == None:
        return render(request, "encyclopedia/get.html", {
        "content": cont,
        "title":title,
        })
    else:
        return render(request, "encyclopedia/get.html", {
        "content": markdowner.convert(cont),
        "title":title,
        
    })
  
def search(request):
    q = request.GET.get('q', ' ')
    markdowner=Markdown()
    cont=util.get_entry(q)
    if util.get_entry(q) is not None:
        return render(request, "encyclopedia/get.html", {
            "content": markdowner.convert(cont),
            "title":q })
    else:
        searchresults = []
        for entry in util.list_entries():
            if q.upper() in entry.upper():
                searchresults.append(entry)
               
        return render(request, "encyclopedia/index.html", {"entries": searchresults})
            
def new(request):
    
    if request.method=="POST":
        form=NewTaskForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            for entry in util.list_entries():
                if title.upper() == entry.upper():
                    return render (request, "encyclopedia/error.html")
            util.save_entry(title, content)
            
            markdowner=Markdown()
            cont=util.get_entry(title)
            return render(request, "encyclopedia/get.html", {
                "content": markdowner.convert(cont),
                "title":title
                })
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
                })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewTaskForm()
            })

def edit(request, ent):
    form=NewTaskForm()
    form.fields["title"].initial=ent
    form.fields["content"].initial=util.get_entry(ent)
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": ent
        })
    
def change(request):
    if request.method=="POST":
        form=NewTaskForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            util.save_entry(title, content)
            markdowner=Markdown()
            cont=util.get_entry(title)
            return render(request, "encyclopedia/get.html", {
                "content": markdowner.convert(cont),
                "title":title
                })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
                })
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": NewTaskForm()
            })

def random(request):
    list=util.list_entries()
    randompage=secrets.choice(list)
    markdowner=Markdown()
    cont=util.get_entry(randompage)
    return render(request, "encyclopedia/get.html", {
        "content": markdowner.convert(cont),
                "title":randompage
    })