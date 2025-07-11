from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from ElettronicaIovine.models import Utente, ProdottoAcquistabile
from django.db.models import Q
from .models import Recensione
import time
from functools import wraps

def index(request):
    return render(request, 'index.html')

# Funzione generale per verificare se l'utente è loggato
def is_logged_in(request):
    return 'user_id' in request.session and 'user_type' in request.session

# Decoratore per verificare se l'utente è loggato
def login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not is_logged_in(request):
            # Redirect alla pagina di login appropriata
            if request.path.startswith('/tecnico'):
                return redirect('tecnico_login')
            else:
                return redirect('cliente_login')
        return function(request, *args, **kwargs)
    return wrapper

# Funzioni per i clienti
def is_cliente(request):
    return request.session.get('user_type') == 'Cliente'

import hashlib

def hash_password_sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def cliente_login(request):
    max_tentativi = 5
    blocco_minuti = 2
    blocco_fino = request.session.get('blocco_cliente', 0)

    if time.time() < blocco_fino:

        secondi_restanti = int(blocco_fino - time.time())
        messages.error(request, f'Troppi tentativi falliti. Riprova tra {secondi_restanti} secondi.')
        return render(request, 'Cliente/cliente_login.html')


    request.session['tentativi_cliente'] = 0
    request.session['blocco_cliente'] = 0

    if request.method == 'POST':
        tentativi = request.session.get('tentativi_cliente', 0)
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hash_password_sha256(password)
        try:
            utente = Utente.objects.get(email=email, password=password_hash, tipo='Cliente')
            request.session['user_id'] = utente.id_utente
            request.session['user_type'] = 'Cliente'
            request.session['tentativi_cliente'] = 0
            request.session['blocco_cliente'] = 0
            return redirect(request.GET.get('next', 'homepage_cliente'))
        except Utente.DoesNotExist:
            tentativi += 1
            request.session['tentativi_cliente'] = tentativi
            if tentativi >= max_tentativi:
                request.session['blocco_cliente'] = time.time() + blocco_minuti * 60
                messages.error(request, 'Troppi tentativi falliti. Attendi 2 minuti prima di riprovare.')
            else:
                messages.error(request, f'Credenziali non valide. Tentativo {tentativi} di {max_tentativi}.')
            return render(request, 'Cliente/cliente_login.html')
    return render(request, 'Cliente/cliente_login.html')

def cliente_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not is_logged_in(request):
            return redirect('cliente_login')
        if not is_cliente(request):
            return redirect('cliente_login')
        return function(request, *args, **kwargs)
    return wrapper

@cliente_required
def homepage_cliente(request):
    try:
        utente = Utente.objects.get(id_utente=request.session['user_id'])
        context = {
            'utente': utente
        }
        return render(request, 'Cliente/homepage_cliente.html', context)
    except Utente.DoesNotExist:
        return redirect('cliente_login')
@cliente_required
def prodotti_acquistabili_cliente(request):
    try:
        utente = Utente.objects.get(id_utente=request.session['user_id'])

        # Gestione ricerca
        query = request.GET.get('q', '')

        if query:
            prodotti = ProdottoAcquistabile.objects.filter(
                Q(nome__icontains=query) |
                Q(marca__icontains=query) |
                Q(categoria__icontains=query) |
                Q(descrizione__icontains=query)
            )
        else:
            prodotti = ProdottoAcquistabile.objects.all()

        context = {
            'utente': utente,
            'prodotti': prodotti,
            'query': query
        }
        return render(request, 'Cliente/prodotti_acquistabili_cliente.html', context)
    except Utente.DoesNotExist:
        return redirect('cliente_login')

# Funzioni per i tecnici
def is_tecnico(request):
    return request.session.get('user_type') == 'Tecnico'

def tecnico_login(request):
    max_tentativi = 5
    blocco_minuti = 2
    tentativi = request.session.get('tentativi_tecnico', 0)
    blocco_fino = request.session.get('blocco_tecnico', 0)

    if time.time() < blocco_fino:
        messages.error(request, f'Troppi tentativi falliti. Riprova tra {int((blocco_fino - time.time()) // 1)} secondi.')
        return render(request, 'Tecnico/tecnico_login.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash = hash_password_sha256(password)
        try:
            utente = Utente.objects.get(email=email, password=password_hash, tipo='Tecnico')
            request.session['user_id'] = utente.id_utente
            request.session['user_type'] = 'Tecnico'
            request.session['tentativi_tecnico'] = 0
            return redirect(request.GET.get('next', 'homepage_tecnico'))
        except Utente.DoesNotExist:
            tentativi += 1
            request.session['tentativi_tecnico'] = tentativi
            if tentativi >= max_tentativi:
                request.session['blocco_tecnico'] = time.time() + blocco_minuti * 60
                messages.error(request, 'Troppi tentativi falliti. Attendi 2 minuti prima di riprovare.')
            else:
                messages.error(request, f'Credenziali non valide. Tentativo {tentativi} di {max_tentativi}.')
            # Mostra il messaggio nella stessa pagina senza redirect
            return render(request, 'Tecnico/tecnico_login.html')
    return render(request, 'Tecnico/tecnico_login.html')

def tecnico_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not is_logged_in(request):
            return redirect('tecnico_login')
        if not is_tecnico(request):
            return redirect('tecnico_login')
        return function(request, *args, **kwargs)
    return wrapper

@tecnico_required
def homepage_tecnico(request):
    try:
        utente = Utente.objects.get(id_utente=request.session['user_id'])
        context = {
            'utente': utente
        }
        return render(request, 'Tecnico/homepage_tecnico.html', context)
    except Utente.DoesNotExist:
        return redirect('tecnico_login')


@tecnico_required
def elenco_clienti(request):
    try:
        tecnico = Utente.objects.get(id_utente=request.session['user_id'])

        # Recupera il parametro di ricerca dalla query string
        query = request.GET.get('q', '')

        # Filtra i clienti in base alla query
        if query:
            clienti = Utente.objects.filter(
                tipo='Cliente'
            ).filter(
                Q(nome__icontains=query) |
                Q(cognome__icontains=query) |
                Q(email__icontains=query)
            )
        else:
            clienti = Utente.objects.filter(tipo='Cliente')

        context = {
            'utente': tecnico,
            'clienti': clienti,
            'query': query
        }
        return render(request, 'Tecnico/elenco_clienti.html', context)
    except Utente.DoesNotExist:
        return redirect('tecnico_login')

@tecnico_required
def prodotti_acquistabili_tecnici(request):
    try:
        tecnico = Utente.objects.get(id_utente=request.session['user_id'])

        # Gestione ricerca
        query = request.GET.get('q', '')

        if query:
            prodotti = ProdottoAcquistabile.objects.filter(
                Q(nome__icontains=query) |
                Q(marca__icontains=query) |
                Q(categoria__icontains=query)
            )
        else:
            prodotti = ProdottoAcquistabile.objects.all()

        context = {
            'utente': tecnico,
            'prodotti': prodotti,
            'query': query
        }
        return render(request, 'Tecnico/prodotti_acquistabili_tecnici.html', context)
    except Utente.DoesNotExist:
        return redirect('tecnico_login')

@tecnico_required
def modifica_prodotto(request, id_prodotto):
    try:
        # Verifica che l'utente sia un tecnico
        tecnico = Utente.objects.get(id_utente=request.session['user_id'])

        # Ottieni il prodotto
        prodotto = ProdottoAcquistabile.objects.get(id_prodotto=id_prodotto)

        if request.method == 'POST':
            # Aggiorna i dati del prodotto
            prodotto.nome = request.POST.get('nome')
            prodotto.marca = request.POST.get('marca')
            prodotto.categoria = request.POST.get('categoria')
            prodotto.prezzo = request.POST.get('prezzo')
            prodotto.quantita_disponibile = request.POST.get('quantita')
            prodotto.descrizione = request.POST.get('descrizione', '')
            prodotto.save()

            # Redirect alla pagina di visualizzazione prodotti
            return redirect('prodotti_acquistabili_tecnici')

        # Se non è una richiesta POST, redirige alla pagina prodotti
        return redirect('prodotti_acquistabili_tecnici')

    except Utente.DoesNotExist:
        return redirect('tecnico_login')
    except ProdottoAcquistabile.DoesNotExist:
        # Gestione errore se il prodotto non esiste
        return redirect('prodotti_acquistabili_tecnici')

@tecnico_required
def elimina_prodotto(request, id_prodotto):
    try:
        # Verifica che l'utente sia un tecnico
        tecnico = Utente.objects.get(id_utente=request.session['user_id'])

        # Elimina il prodotto
        prodotto = ProdottoAcquistabile.objects.get(id_prodotto=id_prodotto)
        prodotto.delete()

        # Redirect alla pagina di visualizzazione prodotti
        return redirect('prodotti_acquistabili_tecnici')

    except Utente.DoesNotExist:
        return redirect('tecnico_login')
    except ProdottoAcquistabile.DoesNotExist:
        # Gestione errore se il prodotto non esiste
        return redirect('prodotti_acquistabili_tecnici')

@tecnico_required
def aggiungi_prodotto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        prezzo = request.POST.get('prezzo')
        quantita_rimasta = request.POST.get('quantita_rimasta')
        descrizione = request.POST.get('descrizione')
        immagine = request.FILES.get('immagine')

        # Recupera il tecnico dalla sessione
        # Usa user_id invece di id_utente
        id_tecnico = request.session.get('user_id')
        tecnico = Utente.objects.get(id_utente=id_tecnico)

        # Crea il nuovo prodotto
        prodotto = ProdottoAcquistabile(
            nome=nome,
            prezzo=prezzo,
            quantita_rimasta=quantita_rimasta,
            descrizione=descrizione,
            id_tecnico=tecnico
        )

        # Se è stata caricata un'immagine, la salva
        if immagine:
            prodotto.immagine = immagine

        prodotto.save()

        return render(request, 'Tecnico/aggiunta_prodotti.html', {
            'success_message': 'Prodotto aggiunto con successo!'
        })

    return render(request, 'Tecnico/aggiunta_prodotti.html')


@cliente_required
def assistenza(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        oggetto = request.POST.get('oggetto')
        messaggio = request.POST.get('messaggio')
        # Qui puoi gestire la richiesta (salvare o inviare email)
        return render(request, 'Cliente/assistenza.html', {'success': True})
    return render(request, 'Cliente/assistenza.html')



@cliente_required
def aggiungi_al_carrello(request, prodotto_id):
    prodotto = get_object_or_404(ProdottoAcquistabile, id_prodotto=prodotto_id)
    if prodotto.quantita_rimasta > 0:
        carrello = request.session.get('carrello', {})
        carrello[str(prodotto_id)] = carrello.get(str(prodotto_id), 0) + 1
        request.session['carrello'] = carrello
        prodotto.quantita_rimasta -= 1
        prodotto.save()
    return redirect('prodotti_acquistabili_cliente')

@cliente_required
def carrello(request):
    carrello = request.session.get('carrello', {})
    prodotti = []
    totale = 0
    for prodotto_id, quantita in carrello.items():
        prodotto = ProdottoAcquistabile.objects.get(id_prodotto=prodotto_id)
        prodotti.append({'prodotto': prodotto, 'quantita': quantita})
        totale += prodotto.prezzo * quantita
    return render(request, 'Cliente/carrello.html', {'prodotti': prodotti, 'totale': totale})

@cliente_required
def rimuovi_dal_carrello(request, prodotto_id):
    carrello = request.session.get('carrello', {})
    prodotto_id_str = str(prodotto_id)
    if prodotto_id_str in carrello:
        prodotto = get_object_or_404(ProdottoAcquistabile, id_prodotto=prodotto_id)
        # Decrementa la quantità di 1
        if carrello[prodotto_id_str] > 1:
            carrello[prodotto_id_str] -= 1
            prodotto.quantita_rimasta += 1
            prodotto.save()
        else:
            # Se la quantità è 1, rimuovi il prodotto dal carrello
            prodotto.quantita_rimasta += 1
            prodotto.save()
            del carrello[prodotto_id_str]
        request.session['carrello'] = carrello
    return redirect('carrello')
def profilo_cliente(request):
    utente = request.session.get('utente')
    return render(request, 'Cliente/profilo_cliente.html', {'utente': utente})
# ElettronicaIovine/views.py

@cliente_required
def profilo_cliente(request):
    try:
        utente = Utente.objects.get(id_utente=request.session['user_id'])
        return render(request, 'Cliente/profilo_cliente.html', {'utente': utente})
    except Utente.DoesNotExist:
        return redirect('cliente_login')

@cliente_required
def prodotti_acquistabili_cliente(request):
    query = request.GET.get('q', '')
    if query:
        prodotti = ProdottoAcquistabile.objects.filter(nome__icontains=query)
    else:
        prodotti = ProdottoAcquistabile.objects.all()
    utente = Utente.objects.get(id_utente=request.session['user_id'])
    return render(request, 'Cliente/prodotti_acquistabili_cliente.html', {
        'prodotti': prodotti,
        'query': query,
        'utente': utente
    })

@tecnico_required
def recensioni_ricevute(request):
    tecnico_id = request.session.get('user_id')
    recensioni = Recensione.objects.filter(id_tecnico_id=tecnico_id)
    return render(request, 'Tecnico/recensioni_ricevute.html', {'recensioni': recensioni})



@tecnico_required
def richieste_ricevute(request):
    return render(request, 'Tecnico/richieste_ricevute.html')


def logout_cliente(request):
    request.session.flush()
    return redirect('cliente_login')

def logout_tecnico(request):
    request.session.flush()
    return redirect('tecnico_login')
