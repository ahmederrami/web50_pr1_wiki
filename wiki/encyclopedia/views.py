from django.shortcuts import render
from django.http import HttpResponse

from . import util

import markdown2 # to convert markdown content to html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#--------------By ahmederrami@gmail.com-----------------------------------------------------
def entry(request, title):
    # get markdown content of encyclopedia entry which title is title
    md= util.get_entry(title)
    if md:
        # convert the markdown content to html before sending it to entry.html
        html= markdown2.markdown(md)
    else:
        html= None
    return render(request, "encyclopedia/entry.html", {
        "entry": html,
        "title": title
    })

def search(request):
    if 'query' in request.GET and request.GET['query']:
        title= request.GET['query']
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

    entries= util.list_entries()
    # If the query matches the name of an encyclopedia entry, the user should
    # be redirected to that entry’s page.
    
    if title in entries:
        html= markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title
        })
    else:
        # If the query does not match the name of an encyclopedia entry, the user
        # should instead be taken to a search results page that displays a list of
        # all encyclopedia entries that have the query as a substring
        search_results=[]
        for entry in entries:
            if title.lower() in entry.lower():
                search_results.append(entry)
        return render(request, "encyclopedia/search.html", {
                "search_results": search_results,
                "size" : len(search_results),
                "title": title
            })

def add(request):
    if 'entry' in request.POST and request.POST['entry']:
        entryTitle= request.POST['entry']
        entryExists= util.get_entry(entryTitle)
        if entryExists:
            return HttpResponse("There is already an entry with the same title")
        else:
            util.save_entry(entryTitle, request.POST['content'])
            html= markdown2.markdown(util.get_entry(entryTitle))
            return render(request, "encyclopedia/entry.html", {
                "entry": html,
                "title": entryTitle
            })
    else:
        return render(request, "encyclopedia/add.html")