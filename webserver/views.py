from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models.functions import ExtractHour,ExtractDay
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F




def home(request):
     if request.user.is_authenticated:
         return redirect('index')
     return redirect('login')
 
 
     
def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            arrivee_retour_employe_list = ArriveeRetourEmploye.objects.filter(date__gte=startDate, date__lte=endDate)
            # Pass the queryset to the template for rendering
            context = {
                'arrivee_retour_employe_list': arrivee_retour_employe_list
            }
            return render(request, 'index.html', context)
            
           
        last_month = ArriveeRetourEmploye.objects.latest('date').date.month
        arrivee_retour_employe_list = ArriveeRetourEmploye.objects.filter(date__month=last_month).order_by('-date', '-heure_arrive')
        # Pass the queryset to the template for rendering
        context = {
            'arrivee_retour_employe_list': arrivee_retour_employe_list
        }
        return render(request, 'index.html', context)
    return redirect("login")
 
 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Replace 'home' with the URL name for your home page
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')  # Replace 'home' with your actual URL name

    
def logout_view(request):
    logout(request)
    return redirect("home")




def insertArriveRetour(request):
    if request.method == 'GET':
        matricule = request.GET.get('matricule')
        type = request.GET.get('type')
        current_date = request.GET.get('date')
        current_time = request.GET.get('time')

        if type == 'stagiaire':
            ArriveeRetourModel = ArriveeRetourStagiaire
            model_instance = Stagiaire.objects.get(matricule=matricule)
            try:
                instance = ArriveeRetourModel.objects.get(date=current_date, stagiaire=model_instance)
                current_time_formatted = datetime.strptime(current_time, '%H:%M:%S').time()                # Check if the hour and minute are the same
                     #if instance.heure_arrive.strftime('%H:%M') != current_time_formatted:
                     
                last_hour_minute = instance.heure_retour
                if last_hour_minute != None:
                    if last_hour_minute.hour != current_time_formatted.hour or last_hour_minute.minute != current_time_formatted.minute:
                        instance.heure_retour = current_time
                        instance.save()
                        record = DetailsAccess(date=current_date, heure=current_time, employe=model_instance)
                        record.save()
                else:
                    last_hour_minute = instance.heure_arrive
                    if last_hour_minute.hour != current_time_formatted.hour or last_hour_minute.minute != current_time_formatted.minute:
                        instance.heure_retour = current_time
                        instance.save()
                        record = DetailsAccess(date=current_date, heure=current_time, employe=model_instance)
                        record.save()

            except ArriveeRetourModel.DoesNotExist:
                instance = ArriveeRetourModel(date=current_date, heure_arrive=current_time, stagiaire=model_instance)
                instance.save()
                record = DetailsAccess(date=current_date, heure=current_time, employe=model_instance)
                record.save()

        elif type == 'employe':
            ArriveeRetourModel = ArriveeRetourEmploye
            model_instance = Employe.objects.get(matricule=matricule)
            try:
                instance = ArriveeRetourModel.objects.get(date=current_date, employe=model_instance)
                current_time_formatted = datetime.strptime(current_time, '%H:%M:%S').time()                # Check if the hour and minute are the same
                     #if instance.heure_arrive.strftime('%H:%M') != current_time_formatted:
                     
                last_hour_minute = instance.heure_retour
                if last_hour_minute != None:
                    if last_hour_minute.hour != current_time_formatted.hour or last_hour_minute.minute != current_time_formatted.minute:
                        instance.heure_retour = current_time
                        instance.save()
                        record = DetailsAccess(date=current_date, heure=current_time, employe=model_instance)
                        record.save()
                else:
                    last_hour_minute = instance.heure_arrive
                    if last_hour_minute.hour != current_time_formatted.hour or last_hour_minute.minute != current_time_formatted.minute:
                        instance.heure_retour = current_time
                        instance.save()
                        record = DetailsAccess(date=current_date, heure=current_time, employe=model_instance)
                        record.save()
            except ArriveeRetourModel.DoesNotExist:
                instance = ArriveeRetourModel(date=current_date, heure_arrive=current_time, employe=model_instance)
                instance.save()
                record = DetailsAccess(date=current_date, heure=current_time, employe=model_instance)
                record.save()

        else:
            return JsonResponse({'error': 'Invalid type specified!'}, status=400)

        return JsonResponse({'status': 'successfully inserted'})

    return JsonResponse({'error': 'Invalid request method!'}, status=405)



def detailsAccess(request):
    matricule = request.GET.get('matricule')
    date = request.GET.get('date')
    model_instance = Employe.objects.get(matricule=matricule)
    accesses = DetailsAccess.objects.filter(employe=model_instance, date=date)
    print('\n****************',date,'****************\n')
    return render(request, 'detailsAccess.html', {'accesses': accesses})


def delArrivEmp(request):
    id = int(request.GET.get('id'))
    try:
        instance = ArriveeRetourEmploye.objects.get(id=id)
        instance.delete()
        return JsonResponse({'success': True})
    except ArriveeRetourEmploye.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Instance not found'})
    

def delUser(request):
    id = int(request.GET.get('id'))
    try:
        instance = User.objects.get(id=id)
        instance.delete()
        return JsonResponse({'success': True})
    except ArriveeRetourEmploye.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Instance not found'})
    
def auth(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        password = request.GET.get('password')

        try:
            profile = Profil.objects.get(id=id)
            stored_password = profile.password
        except Profil.DoesNotExist:
            return JsonResponse({'mes': 'failed'})

        if check_password(password, stored_password):
            return JsonResponse({'mes': id})
        else:
            return JsonResponse({'mes': 'failed'})


def get_all_data(request):
    employee_data = list(Employe.objects.all().values())
    stagiaire_data = list(Stagiaire.objects.all().values())

    response_data = {
        'employees': employee_data,
        'stagiaires': stagiaire_data,
    }

    return JsonResponse(response_data)


def tasks_list (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    arrivee_retour_employe_list = ArriveeRetourEmploye.objects.all()

    # Pass the queryset to the template for rendering
    context = {
        'arrivee_retour_employe_list': arrivee_retour_employe_list
    }
    return render(request, 'tasks-list.html', context)

def task_edit (request):
    if not request.user.is_authenticated:
         return redirect('login') 
     
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        arrivee_retour_employe = ArriveeRetourEmploye.objects.get(id=id)
        date = request.POST.get('date')
        heure_arrive = request.POST.get('heure_arrivee')
        heure_retour = request.POST.get('heure_retour')
        if not heure_retour:
            heure_retour = None
        arrivee_retour_employe.heure_arrive=heure_arrive
        arrivee_retour_employe.heure_retour=heure_retour
        arrivee_retour_employe.date=date
        arrivee_retour_employe.save()
        return redirect('index')
    
    id = int(request.GET.get('id'))
    arrivee_retour_employe = ArriveeRetourEmploye.objects.get(id=id)   
    return render(request, 'task-edit.html', {'arrivee_retour_employe': arrivee_retour_employe})

def user_edit (request):
    if not request.user.is_authenticated:
         return redirect('login') 
     
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        user = User.objects.get(id=id)
        status = request.POST.get('status')
        nom = request.POST.get('nom')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password!= password2:
            return render(request, 'userform.html',{'error':'Les mots de passes ne correspondent pas'})
        if password != None and password2 != None:  
            user.set_password(password)
        user.username = nom
        if status == 'user':
            user.is_staff = False
            user.is_superuser = False
            user.save()
        else:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return redirect('userlist')
    
    id = int(request.GET.get('id'))
    user =  User.objects.get(id=id)   
    return render(request, 'user-edit.html', {'Actualuser': user})

def datatable (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    employes = Employe.objects.all()
    return render(request, 'datatable.html', {'employes': employes})

def form_wizard (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        fonction = request.POST.get('fonction') 
        new_emp = Employe(nom=nom, prenom=prenom, fonction=fonction)
        new_emp.save()
    return render(request, 'form-wizard.html')


def userform (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    if request.method == 'POST':
        status = request.POST.get('status')
        nom = request.POST.get('nom')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password!= password2:
            return render(request, 'userform.html',{'error':'Les mots de passes ne correspondent pas'})
        if status == 'user':
            new_user = User.objects.create_user(username=nom, password=password)
            new_user.save()
        else:
            new_user = User.objects.create_superuser(username=nom, password=password)
            new_user.save()
        return redirect('userlist')
    return render(request, 'userform.html')


def chartdata(request):
    resp = {}
    
    # Retrieve the most recent month with records in the database
    last_month = ArriveeRetourEmploye.objects.latest('date').date.month

    # Query the database to get the day, hour, and count of scans registered on each hour
    data = ArriveeRetourEmploye.objects.filter(date__month=last_month) \
                                      .annotate(day=ExtractDay('date'),
                                                hour=ExtractHour('heure_arrive')) \
                                      .values('day', 'hour') \
                                      .annotate(scan_count=Count('id'))

    # Prepare the response data
    for entry in data:
        day = entry['day']
        hour = entry['hour']
        scan_count = entry['scan_count']


        if day not in resp:
            resp[day] = {
                'hours': [],
                'scans': []
            }

        resp[day]['hours'].append(hour)
        resp[day]['scans'].append(scan_count)

    # Add missing hours and set scan count to 0 if there is no corresponding scan
    for day_data in resp.values():
        for hour in range(7, 13):
            if hour not in day_data['hours']:
                day_data['hours'].append(hour)
                day_data['scans'].append(0)


    return JsonResponse(resp)

def userlist(request):
    if not request.user.is_authenticated:
         return redirect('login') 
    accounts = User.objects.all()
    return render(request, 'userlist.html', {'accounts': accounts})

def about (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'about.html')
def accordion (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'accordion.html')
def alerts (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'alerts.html')
def avatar (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'avatar.html')
def background (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'background.html')
def badge (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'badge.html')
def blog_details (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'blog-details.html')
def blog_edit (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'blog-edit.html')
def blog (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'blog.html')
def border (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'border.html')
def breadcrumbs (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'breadcrumbs.html')
def buttons (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'buttons.html')
def calendar2 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'calendar2.html')
def cards (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'cards.html')
def carousel (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'carousel.html')
def cart (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'cart.html')
def chart_chartjs (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'chart-chartjs.html')
def chart_echart (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'chart-echart.html')
def chart_flot (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'chart-flot.html')
def chart_morris (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'chart-morris.html')
def chart_nvd3 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'chart-nvd3.html')
def chat (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'chat.html')
def checkout (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'checkout.html')
def client_create (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'client-create.html')
def clients (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'clients.html')
def colors (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'colors.html')
def construction (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'construction.html')
def counters (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'counters.html')

def display (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'display.html')
def dropdown (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'dropdown.html')
def empty (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'empty.html')
def error404 (request, string):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'error404.html', status=404)
def error500 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'error500.html')
def error501 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'error501.html')
def faq (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'faq.html')
def file_attachments (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'file-attachments.html')
def file_manager_1 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'file-manager-1.html')
def file_manager_2 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'file-manager-2.html')
def file_manager (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'file-manager.html')
def flex (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'flex.html')
def footers (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'footers.html')
def forgot_password (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'forgot-password.html')
def form_advanced (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'form-advanced.html')
def form_editable (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'form-editable.html')
def form_elements (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'form-elements.html')
def form_layouts (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'form-layouts.html')
def form_validation (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'form-validation.html')
def gallery (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'gallery.html')
def height (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'height.html')
def icons (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons.html')
def icons2 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons2.html')
def icons3 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons3.html')
def icons4 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons4.html')
def icons5 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons5.html')
def icons6 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons6.html')
def icons7 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons7.html')
def icons8 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons8.html')
def icons9 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons9.html')
def icons10 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'icons10.html')
    


def invoice_create (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'invoice-create.html')
def invoice_details (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'invoice-details.html')
def invoice_edit (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'invoice-edit.html')
def invoice_list (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'invoice-list.html')
def invoice_timelog (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'invoice-timelog.html')
def landing (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'landing.html')
def loaders (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'loaders.html')
def lockscreen (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'lockscreen.html')

def mail_compose (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'mail-compose.html')
def mail_inbox (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'mail-inbox.html')
def mail_read (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'mail-read.html')
def mail_settings (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'mail-settings.html')
def maps (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'maps.html')
def maps1 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'maps1.html')
def maps2 (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'maps2.html')
def margin (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'margin.html')
def mediaobject (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'mediaobject.html')
def modal (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'modal.html')
def navigation (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'navigation.html')
def notify (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'notify.html')
def offcanvas (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'offcanvas.html')
def opacity (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'opacity.html')
def padding (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'padding.html')
def pagination (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'pagination.html')
def panels (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'panels.html')
def position (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'position.html')
def pricing (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'pricing.html')
def product_details (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'product-details.html')
def products (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'products.html')
def profile (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'profile.html')
def progress (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'progress.html')
def project_details (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'project-details.html')
def project_edit (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'project-edit.html')
def project_new (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'project-new.html')
def projects_list (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'projects-list.html')
def projects (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'projects.html')
def rangeslider (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'rangeslider.html')
def rating (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'rating.html')
def register (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'register.html')
def scroll (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'scroll.html')
def services (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'services.html')
def settings (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'settings.html')
def sweetalert (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'sweetalert.html')
def switcherpage (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'switcherpage.html')
def table_editable (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'table-editable.html')
def tables (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'tables.html')
def tabs (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'tabs.html')
def tags (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'tags.html')
def task_create (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'task-create.html')

def terms (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'terms.html')
def thumbnails (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'thumbnails.html')
def ticket_details (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'ticket-details.html')
def timeline (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'timeline.html')
def tooltipandpopover (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'tooltipandpopover.html')
def treeview (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'treeview.html')
def typography (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'typography.html')
def users_list (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'users-list.html')
def width (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'width.html')
def wishlist (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'wishlist.html')
def wysiwyag (request):
    if not request.user.is_authenticated:
         return redirect('login') 
    return render(request, 'wysiwyag.html')