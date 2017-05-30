from django.shortcuts import redirect, render

def index(request):
    if request.method == "POST":
        print(request.POST.get('dvhdata'))
    return render(request, 'myapp/index.html', {})


def analyse_dvh(request):
    dvh_data = request.dvh-data
    print(dvh_data)
    return render(request, 'myapp/index.html',{})
