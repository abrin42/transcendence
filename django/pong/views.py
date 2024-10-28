from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

@csrf_exempt
def get_csrf_token(request):
    print(request)
    if request.method == 'POST':
        csrf_token = get_token(request)
        response = JsonResponse({'message': 'CSRF token generated'})
        response.set_cookie('csrftoken', csrf_token)
        return response
    return JsonResponse({'error': 'Invalid request la'}, status=400)
