from django.shortcuts import redirect


def check_admin(view_func):
    def waraper(request, *args, **kwargs):
        if request.user.is_admin == False:
            return redirect("/dashboard")
        else:
            return view_func(request, *args, **kwargs)
        
    return waraper



def check_auth(view_func):
    def waraper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard")
        else:
            return view_func(request, *args, **kwargs)
    
    return waraper



