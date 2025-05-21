from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import (
    Student,Thesis,Memory,Commentaire

)
from itertools import chain
from operator import attrgetter
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


def is_admin(user):
    return user.is_superuser


# Create your views here.

@login_required
@user_passes_test(is_admin)
def dashboard(request):

    user = request.user # l'utilisateur connecté
    document_title = 'dashboard-page'

    total_user = User.objects.all().count()
    total_thesis = Thesis.objects.all().count()
    total_memory = Memory.objects.all().count()
    total_document = total_thesis + total_memory

    total_comment = Commentaire.objects.all().count()
    total_othor = User.objects.filter(Q(thesis__isnull=False)|Q(memory__isnull=False)).distinct().count()


    # les cinqs derniere document
    thesis = Thesis.objects.all().order_by('-date_publication')
    memories = Memory.objects.all().order_by('-date_publication')


    #combinaison de deux query set
    publications = sorted(chain(thesis,memories),
    key=attrgetter('date_publication'))
    



    context = {
        'document_title':document_title,
        'user' : user,
        'active_dashboard':'active',
        'total_user':total_user,
        'total_document':total_document,
        'total_comment':total_comment,
        'total_othor':total_othor,
        'documents':publications,
    }
    return render(request, 'app/admin/pages/index.html',context=context)

@login_required
def home(request):
    document_title = 'home-page'
    count_search = None

    thesis = Thesis.objects.filter(prouve=True)
    memories = Memory.objects.filter(prouve=True)


    #combinaison de deux query set
    publications = sorted(chain(thesis,memories),
    key=attrgetter('date_publication'))
    latest_publications = publications[:12]
    print(latest_publications)

    search = request.GET.get('search')

    if search:
        result_thesis = Thesis.objects.filter(Q(title__icontains=search)|
                                              Q(resume__icontains=search)|
                                              Q(description__icontains=search)|
                                              Q(author__username__icontains=search)|
                                              Q(author__last_name__icontains=search)|
                                              Q(author__first_name__icontains=search)
                                              )
        
        result_memory = Memory.objects.filter(Q(title__icontains=search)|
                                              Q(resume__icontains=search)|
                                              Q(description__icontains=search)|
                                              Q(author__username__icontains=search)|
                                              Q(author__last_name__icontains=search)|
                                              Q(author__first_name__icontains=search)
                                              )
        latest_publications = sorted(chain(result_thesis,result_memory),
    key=attrgetter('date_publication'))
        
        count_s = len(latest_publications)
        count_search = f'{count_s} resultats trouvés' if (count_s > 1)  else f'{count_s} resultat trouvé'

    context = {
        'document_title':document_title,
        'documents':latest_publications,
        'active_home':'active',
        'count_search':count_search
    }
    return render(request, 'app/site/pages/home.html',context=context)

def view_thesis(request):
    thesis = Thesis.objects.filter(prouve=True)
    document_title = 'thèse-page'

    context = {
        'document_title':document_title,
        'documents':thesis,
        'active_thesis':'active',
    }
    return render(request, 'app/site/pages/view_these.html',context=context)

def view_memories(request):
    memories = Memory.objects.filter(prouve=True)
    document_title = 'mémoire-page'

    context = {
        'document_title':document_title,
        'documents':memories,
        'active_memory':'active',
    }
    return render(request, 'app/site/pages/view_memories.html',context=context)

def document_details(request, document_type, document_id): 
    document_title = "details-page"
    comments = None
    if document_type == 'thesis':
        document = get_object_or_404(Thesis,id=document_id)
    elif document_type == 'memory':
        document = get_object_or_404(Memory,id=document_id)
    else:
        document = None
    if document:
        # on récupère le content_type pour la thèse et mémoire
        content_type = ContentType.objects.get_for_model(document)

        comments = Commentaire.objects.filter(content_type=content_type, object_id=document.id)
        

        print(comments)

    context = {
        'document_title':document_title,
        'document':document,
        'comments':comments,
        
    }
    return render(request,'app/site/pages/document_details.html',context)



def add_comment(request,document_type,document_id):

    content = request.POST.get('comment')
    if document_type == 'thesis':
        document = get_object_or_404(Thesis,id=document_id)
    elif document_type == 'memory':
        document = get_object_or_404(Memory,id=document_id)
    else:
        document = None
    if document:
        # on récupère le content_type pour la thèse et mémoire
        content_type = ContentType.objects.get_for_model(document)
        comment = Commentaire.objects.create(
            contenu=content,
            user=request.user,
            content_type=content_type,
            object_id=document.id,

        )
        print(comment)
        if comment:
            messages.success(request,"Votre commentaire a été ajouté avec succès")
            return redirect('app:document_details',document_type=document_type,document_id=document_id)
        else:
            messages.error(request,"Commentaire non envoyé")
            return redirect('app:document_details',document_type=document_type,document_id=document_id)

    return HttpResponse('Impossible')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Commentaire, id=comment_id)

    comment.delete()
    messages.success(request,"Votre commentaire a été supprimé avec succès")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def add_thesis(request):
    document_title='ajouter-thèse'
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        resume = request.POST.get('resume')
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        new_thesis = Thesis.objects.create(
            title=title,
            description=description,
            resume=resume,
            image=image,
            author=request.user,
            file=file
            )
        
        messages.success(request,"Votre publication est en attente de l'approbation de l'admin")
        return redirect('app:home')
        
    context = {
        'document_title':document_title,
    }
    return render(request,'app/site/pages/add_thesis.html',context)

def add_memory(request):
    document_title='ajouter-memoire'

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        resume = request.POST.get('resume')
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        new_memory = Memory.objects.create(
            title=title,
            description=description,
            resume=resume,
            image=image,
            author=request.user,
            file=file
            )
        messages.success(request,"Votre publication est en attente de l'approbation de l'admin")
        return redirect('app:home')
        
    context = {
        'document_title':document_title,
    }
    return render(request,'app/site/pages/add_memory.html',context)

def blog(request):
     return HttpResponse("Cette page sera disponible dans les versions à venir , L'essentiel était de concevoir une application qui répond aux attentes des étudiant et chercheur (par Binda)" )

def about(request):
     return HttpResponse("Cette page sera disponible dans les versions à venir , L'essentiel était de concevoir une application qui répond aux attentes des étudiant et chercheur (par Binda)" )

def contact(resquest):
    return HttpResponse("Cette page sera disponible dans les versions à venir , L'essentiel était de concevoir une application qui répond aux attentes des étudiant et chercheur (par Binda)" )

    






