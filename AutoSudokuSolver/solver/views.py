from django.shortcuts import render
from . import forms
import cv2 
from PIL import Image
import base64
from solver.modules.puzzlescan import puzzle_process
from solver.modules.puzzle_solving import read_and_solve

# Create your views here.
def index(request):
    form = forms.ImageForm()
    payload = {}
    if request.method == 'POST':

        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upFile = request.FILES['img']
            data = upFile.read()
            
            encoded = base64.b64encode(data)
            processed_img = puzzle_process(encoded)
            sol = read_and_solve(processed_img)
            payload['sol'] = sol

            
    payload['form'] = form     

    return render(request, 'solver/index.html', context = payload)

def read_image(request):
    form = forms.ImageForm()
    payload = {}
    if request.method == 'POST':

        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upFile = request.FILES['img']
            data = upFile.read()
            
            encoded = base64.b64encode(data)
            decoded = encoded.decode('utf8')
            #processed_img = puzzle_process(encoded)
            #sol = read_and_solve(processed_img)
            #payload['sol'] = sol
            payload['imgb64'] = decoded

            
    payload['form'] = form     

    return render(request, 'solver/index.html', context = payload)