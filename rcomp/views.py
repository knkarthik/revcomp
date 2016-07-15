from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .check_sequence import check_sequence, reverse_complement, rtst

# Create your views here.


def index(request):
    if request.method == 'POST':
        seq = request.POST.get('seq', False)
        request.session['val'] = check_sequence(seq)
        if seq:
            return HttpResponseRedirect(reverse('rcomp:result'))
        else:
            return render(request, 'rcomp/index.html')
    else:
        return render(request, 'rcomp/index.html')


def result(request):
    myval = request.session['val']
    return render(request, 'rcomp/results.html', {'seq': myval})
