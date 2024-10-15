from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def layout(request):
    return render(request, 'layout.html')

@csrf_exempt
def csrf_test_view(request):
    print(request)
    if request.method == 'POST':
        csrf_token = get_token(request)
        response = JsonResponse({'message': 'CSRF token generated'})
        response.set_cookie('csrftoken', csrf_token)
        csrf_cook = request.COOKIES.get('jwt')
        print(csrf_cook)
        return response
    return JsonResponse({'error': 'Invalid request la'}, status=400)