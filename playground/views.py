from django.shortcuts import render

def calculate():
    x =1
    y = 2
    return x
# Request handler (action)
def say_hello(request):
    # return HttpResponse("Hello World")
    x = calculate()
    return render(request, "hello.html", {"name": "Mosh"})
