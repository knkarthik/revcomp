from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .check_sequence import check_sequence, reverse_complement, handle_uploaded_file
import io

# Create your views here.


def index(request):
    if request.method == 'POST':
        if request.POST['seq']:
            seq = request.POST['seq']
            seq = check_sequence(seq)
            # saving the value of seq in 'val' to be passed between views
            request.session['val'] = seq
        elif request.FILES:
            # ufile is InMemoryUploadedFile object, we can not read its
            # contents as strings directly
            ufile = request.FILES['upload_flle']
            # InMemoryUploadedFile as a file object that is in BytesIO, so convert it to string
            content = io.TextIOWrapper(request.FILES['upload_flle'].file)
            seq = handle_uploaded_file(ufile, content)
            request.session['val'] = seq
        else:
            return render(request, 'revcomp/index.html')
        if seq:
                return HttpResponseRedirect(reverse('revcomp:rcomp'))
        else:
            return render(request, 'revcomp/index.html')
    else:
        return render(request, 'revcomp/index.html')


def rcomp(request):
    myval = request.session['val']
    return render(request, 'revcomp/results.html', {'seq': myval})
