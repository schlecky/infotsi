from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Epreuve, Code, Etudiant
from multiprocessing import Process, Queue
import queue as OQueue


def index(request):
    return HttpResponse("Page de challenge")


def majScoreEtudiant(etud):
    codes = Code.objects.filter(etudiant=etud)
    etud.score = sum(c.score for c in codes)
    etud.save()


def ajouteCode(request, epreuve_id):
    if request.user.is_authenticated:
        if 'code' not in request.POST:
            return redirect('challenge:accueil')
        code = request.POST['code']
        score, message = codeScore(code, epreuve_id)
        etud = request.user.etudiant
        e = Epreuve.objects.get(id=epreuve_id)
        c, created = Code.objects.get_or_create(epreuve=e,
                                                etudiant=etud)
        if created or score > c.score:
            c.code = code
            c.score = score
            c.save()

            majScoreEtudiant(etud)

        return render(request, 'challenge/ajouteCode.html',
                      {'epreuve': e,
                       'score': score,
                       'message': message,
                       'scoreTot': etud.score,
                       'listeJoueurs': listeJoueurs()})


def editeCode(request, epreuve_id):
    if request.user.is_authenticated:
        epreuve = get_object_or_404(Epreuve, pk=epreuve_id)
        code = Code.objects.filter(epreuve=epreuve,
                                etudiant=request.user.etudiant)
        if code:
            code = code.get()
            c = code.code
        else:
            c = ""
        return render(request, 'challenge/editecode.html',
                      {'epreuve': epreuve,
                       'listeJoueurs': listeJoueurs(),
                       'code': c,
                       })
    else:
        return redirect('challenge:loginView')


def codeScore(code, epreuve_id):
    epreuve = get_object_or_404(Epreuve, pk=epreuve_id)

    def runCode(q, code, testCode):
        exec(testCode, globals(), locals())
        try:
            score, message = scoreFunc(code)
            q.put(score)
            q.put(message)
        except Exception as e:
            q.put(-1)
            print(e)
            q.put(str(e))


    q = Queue()
    process = Process(target=runCode, args=(q, code, epreuve.test))
    process.start()
    try:
        score = q.get(True, 3)
        message = q.get(True, 3)
    except OQueue.Empty:
        score = -2
        message = ""
        process.terminate()

    return score, message


def classement(etudiant):
    if(etudiant.estClasse):
        l = list(Etudiant.objects.filter(estClasse=True).order_by('-score'))
        rang = l.index(etudiant)+1
        total = len(l)
    else:
        rang=-1
        total=-1
    return {'pos': rang, "tot": total}


def listeJoueurs():
    joueurs = []
    for e in Etudiant.objects.all().filter(estClasse=True).order_by('-score'):
        joueurs.append({
            'id': e.id,
            'first_name': e.user.first_name,
            'last_name': e.user.last_name,
            'score': e.score,
        }
        )
    return joueurs


def accueilView(request):
    if request.user.is_authenticated:
        user = request.user
        codes = Code.objects.filter(etudiant=user.etudiant)
        epreuves = Epreuve.objects.all().order_by('difficulte')
        listeEpreuves = []
        for e in epreuves:
            if codes.filter(epreuve=e) and codes.get(epreuve=e).score>0:
                r = True
            else:
                r = False
            listeEpreuves.append({
                'id': e.id,
                'reussie': r,
                'points': e.points,
                'titre': e.titre,
                'difficulte': list(range(e.difficulte)),
            })
        statEpreuves={'total': len(listeEpreuves),
                      'restantes': len(listeEpreuves)-len(codes)}
        return render(request, 'challenge/base.html',
                      {'listeEpreuves': listeEpreuves,
                       'statEpreuves': statEpreuves,
                       'classement': classement(user.etudiant),
                       'user': user,
                       'listeJoueurs': listeJoueurs()})
    else:
        return redirect('challenge:loginView')


def loginView(request):
    if request.user.is_authenticated:
        return redirect('challenge:accueil')
    if('username' in request.POST and 'password' in request.POST):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('challenge:accueil')
        else:
            return render(request, 'challenge/login.html', {'message': "echec"})
    else:
        return render(request, 'challenge/login.html')


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return loginView(request)
