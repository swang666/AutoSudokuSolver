from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from . import forms
import cv2 
from PIL import Image
import base64
import numpy as np
import solver.modules.puzzlescan as ps
from solver.modules.puzzle_solving import read_and_solve
from django.http import HttpResponse


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
            decoded = 'data:image/jpg;base64,' + decoded
            lt, lb, rb, rt, x_factor, y_factor, processed_img = ps.find_corners(encoded)
            #sol = read_and_solve(processed_img)
            points = [lt,lb,rb,rt]
            #payload['sol'] = sol
            keys = ['lt','lb','rb','rt']
            for i in range(4):
                payload[keys[i] + 'x'] = points[i][0]
                payload[keys[i] + 'y'] = points[i][1]
            payload['x_factor'] = x_factor
            payload['y_factor'] = y_factor
            payload['imgb64'] = decoded
            request.session['processed_img'] = processed_img.tolist()
    payload['form'] = form     

    return render(request, 'solver/read_image.html', context = payload)

def render_output(request):
    payload = {}
    if request.method == 'POST':
        points = []
        data = request.POST
        
        x_factor = float(data['x_factor'])
        y_factor = float(data['y_factor'])
        for i in range(4):
            x = float(data[f'points[{i}][x]'])
            y = float(data[f'points[{i}][y]'])
            points.append((x/x_factor,y/y_factor))
        
        processed_img = np.array(request.session.get('processed_img'),np.uint8)
        #print(processed_img)
        smooth = ps.puzzle_process(points[0],points[1],points[2],points[3], processed_img)
        sol = read_and_solve(smooth)
        payload['sol'] = sol
        print(sol)
    return HttpResponse(sol)