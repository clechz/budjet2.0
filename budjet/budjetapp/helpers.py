from django.shortcuts import redirect

def session_required(request):
    if not request.session.session_key:
        request.session.create()
    return redirect(request.path)