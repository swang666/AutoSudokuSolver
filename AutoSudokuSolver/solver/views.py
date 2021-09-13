from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from . import forms
import cv2 
from PIL import Image
import base64
import numpy as np
import solver.modules.puzzlescan as ps
import solver.modules.puzzle_solving as pzs
from django.http import HttpResponse


# Create your views here.
def index(request):
    form = forms.ImageForm()
    payload = {}
    if request.method == 'POST':

        form = forms.ImageForm(request.POST, request.FILES)

            
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
            lt, lb, rb, rt, factor, canvas_height, processed_img = ps.find_corners(encoded)
            #sol = read_and_solve(processed_img)
            points = [lt,lb,rb,rt]
            #payload['sol'] = sol
            keys = ['lt','lb','rb','rt']
            for i in range(4):
                payload[keys[i] + 'x'] = points[i][0]
                payload[keys[i] + 'y'] = points[i][1]
            payload['factor'] = factor
            payload['canvas_height'] = canvas_height
            payload['imgb64'] = decoded
            request.session['processed_img'] = processed_img.tolist()
    payload['form'] = form     

    return render(request, 'solver/read_image.html', context = payload)

def process_image(request):
    payload = {}
    if request.method == 'POST':
        points = []
        data = request.POST
        
        factor = float(data['factor'])
        for i in range(4):
            x = float(data[f'points[{i}][x]'])
            y = float(data[f'points[{i}][y]'])
            points.append((x/factor,y/factor))
        
        processed_img = np.array(request.session.get('processed_img'),np.uint8)
        #print(processed_img)
        smooth = ps.puzzle_process(points[0],points[1],points[2],points[3], processed_img)
        puzzle = pzs.read_puzzle(smooth)
        
        html = "<table id = 'process_puzzle'>"
        for row in puzzle:
            html += "<tr>"
            for cell in row:
                if cell != 0:
                    html += "<td><input value = '" + str(cell) + "' type = 'number'></td>"
                else:
                    html += "<td><input type = 'number'></td>"
            html += "</tr>"
        html += "</table>"

    return HttpResponse(html)

def render_output(request):
    if request.method == 'POST':
        data = request.POST
        puzzle = []
        for i in range(9):
            row = data.getlist(f'puzzle[{i}][]')
            row = [int(x) for x in row]
            puzzle.append(row)

        sol = pzs.solve_puzzle(puzzle)
        if sol:
            html = "<table id = 'output'>"
            for row in sol:
                html += "<tr>"
                for cell in row:
                    html += "<td><input value = '" + str(cell) + "' type = 'number' disabled></td>"
                html += "</tr>"
            html += "</table>"
        else:
            html = "Oops, I can't solve the puzzle with what you provided"

    return HttpResponse(html)