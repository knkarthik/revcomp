from __future__ import absolute_import
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .check_sequence import check_sequence, reverse_complement, handle_uploaded_file
import io
from .forms import FastaForm


def home(request):
    return render(request, 'rcomp/home.html')

def index(request):
    if request.method == 'POST':
        form = FastaForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                ufile = request.FILES['fastafile']
                content = io.TextIOWrapper(request.FILES['fastafile'].file)
                seq = handle_uploaded_file(ufile, content)
                request.session['val'] = seq
                return HttpResponseRedirect(reverse('rcomp:result'))
            elif request.POST['seq']:
                seq = form.cleaned_data['seq']
                seq = check_sequence(seq)
                request.session['val'] = seq
                return HttpResponseRedirect(reverse('rcomp:result'))
            else:
                return render(request, 'rcomp/index.html', {'form': form})
    else:
        form = FastaForm()
        return render(request, 'rcomp/index.html', {'form': form})


def result(request):
    myval = request.session['val']
    return render(request, 'rcomp/results.html', {'seq': myval})
