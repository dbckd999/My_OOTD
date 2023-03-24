from django.shortcuts import render, redirect

from .models import Clothes

def post(request):
    if request.method == 'POST':
        #Clothes.objects.all().delete()
        post = Clothes()
        post.cloth_name = request.POST['cloth_name']
        post.cloth_var = request.POST['cloth_var']
        post.cloth_col_1 = request.POST['cloth_col_1']
        post.cloth_col_2 = request.POST['cloth_col_2']

        post.save()

        return redirect('post')
    else:
        post = Clothes.objects.all()
        return render(request, 'index.html', {'post':post})
    

# Create your views here.
