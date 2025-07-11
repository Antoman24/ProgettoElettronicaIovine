from django.contrib import admin
from django.urls import path, include
from ElettronicaIovine import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    # URL per i tecnici
    path('tecnico/', views.tecnico_login, name='tecnico_login'),
    path('tecnico/dashboard/', views.homepage_tecnico, name='homepage_tecnico'),

    path('tecnico/clienti/', views.elenco_clienti, name='elenco_clienti'),
    # URL per i clienti
    path('tecnico/prodotti/', views.prodotti_acquistabili_tecnici, name='prodotti_acquistabili_tecnici'),
    path('tecnico/prodotti/modifica/<int:id_prodotto>/', views.modifica_prodotto, name='modifica_prodotto'),
    path('tecnico/prodotti/elimina/<int:id_prodotto>/', views.elimina_prodotto, name='elimina_prodotto'),
    path('tecnico/aggiungi-prodotto/', views.aggiungi_prodotto, name='aggiungi_prodotto'),
    path('tecnico/recensioni/', views.recensioni_ricevute, name='recensioni_ricevute'),
    path('tecnico/richieste/', views.richieste_ricevute, name='richieste_ricevute'),

    path('cliente/', views.cliente_login, name='cliente_login'),
    path('cliente/dashboard/', views.homepage_cliente, name='homepage_cliente'),
    path('cliente/prodotti/', views.prodotti_acquistabili_cliente, name='prodotti_acquistabili_cliente'),
    path('cliente/assistenza/', views.assistenza, name='invia_assistenza'),
    path('cliente/carrello/', views.carrello, name='carrello'),
    path('cliente/aggiungi-al-carrello/<int:prodotto_id>/', views.aggiungi_al_carrello, name='aggiungi_al_carrello'),
    path('cliente/rimuovi-dal-carrello/<int:prodotto_id>/', views.rimuovi_dal_carrello, name='rimuovi_dal_carrello'),
    path('cliente/profilo/', views.profilo_cliente, name='profilo_cliente'),

    path('logout_tecnico/', views.logout_tecnico, name='logout_tecnico'),
    path('logout_cliente/', views.logout_cliente, name='logout_cliente'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
