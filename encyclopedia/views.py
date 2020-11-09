from django.shortcuts import render

from . import util

import random

from django.http import HttpResponseRedirect

from django.urls import reverse

#import re

import markdown2

from django import forms


class EditEntryForm(forms.Form):
    draft = forms.CharField(widget=forms.Textarea)


class AddEntryForm(forms.Form):
    entry = forms.CharField()
    article = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, entry):
    print(entry)

    if entry == "randomEntry":
        entry = random.choice(util.list_entries())
        return HttpResponseRedirect(entry)

    elif entry == "searchEntry":
        # a list of action needed for caseinsensetive search
        queryArr = []
        query = request.GET.get('q')
        queryArr.append(query)

        queryUpp = request.GET.get('q').upper()
        queryArr.append(queryUpp)

        queryCap = request.GET.get('q').capitalize()
        queryArr.append(queryCap)

        queryLow = request.GET.get('q').lower()
        queryArr.append(queryLow)

        if query in util.list_entries():
            return HttpResponseRedirect(query)
        elif queryUpp in util.list_entries():
            return HttpResponseRedirect(queryUpp)
        elif queryCap in util.list_entries():
            return HttpResponseRedirect(queryCap)
        elif queryLow in util.list_entries():
            return HttpResponseRedirect(queryLow)   
        ###

        # here we work with search by subsrting
        else:
            matches =[]
            for entry in util.list_entries():
                for elem in queryArr:
                    if elem in entry:
                        matches.append(entry)
                        break
        
            if matches:
                return render(request, "wiki/searchResult.html",{
                    "results": matches
                    })
            else:
                return render(request, "wiki/noSuchArticle.html",{
                    "entry": query
                    })
        ###
    elif not util.get_entry(entry):
        return render(request, "wiki/noSuchArticle.html",{
            "entry": entry
        })
        
    return render(request, "wiki/article.html", {
        "entry": entry,
        "article": markdown2.markdown(util.get_entry(entry))
        })   


def edit(request, entry):
    #print(entry)
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            title = entry
            content = form.cleaned_data["draft"]

            # the hack needed for correct work with cyrylic symbols
            content = content.encode('utf-8')

            util.save_entry(title, content)
        
            #litle hack here, which alows redirect user to the page with edited article
            return HttpResponseRedirect(reverse("index")+"wiki/"+title)

        else:
            return render(request, "wiki/editArticle.html", {
                "form": form
                }) 

    return render(request, "wiki/editArticle.html", {
        "entry": entry,
        "article": util.get_entry(entry),
        "form": EditEntryForm({"draft": util.get_entry(entry) })
        })   


def add(request):
    #print(entry)
    if request.method == "POST":
        form = AddEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry"]

            # this 'if' neded to check is such article alredy exist or not
            if title in util.list_entries():
                return render(request, "wiki/addArticle.html", {
                "form": form,
                "wrong_title": "Such entry title already exist. Please provide new one!"
                }) 
            ###
            content = form.cleaned_data["article"]

            # the hack needed for correct work with cyrylic symbols
            content = content.encode('utf-8')

            util.save_entry(title, content)

            #litle hack here, which alows redirect user to the page with new article:
            return HttpResponseRedirect(reverse("index")+"wiki/"+title)
            
        else:
            return render(request, "wiki/addArticle.html", {
                "form": form
                })  
        

    return render(request, "wiki/addArticle.html", {
        "form": AddEntryForm()
        })  