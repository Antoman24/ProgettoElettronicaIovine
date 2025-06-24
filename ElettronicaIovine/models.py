from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    class TipoUtente(models.TextChoices):
        CLIENTE = 'Cliente', _('Cliente')
        TECNICO = 'Tecnico', _('Tecnico')

    id_user = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, unique=True )
    tipo = models.CharField(
        max_length=10,
        choices=TipoUtente.choices,
        default=TipoUtente.CLIENTE
    )
    saldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True )
    residenza = models.CharField(max_length=200, null=True, blank=True)
    specializzazione = models.CharField(max_length=100, null=True, blank=True)



class Recensione(models.Model):
    id_cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recensioni_date')
    id_tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recensioni_ricevute')
    voto = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Il voto deve essere almeno 1"),
            MaxValueValidator(5, message="Il voto non può essere superiore a 5")
        ]
    )
    descrizione = models.TextField()

    class Meta:
        unique_together = ('id_cliente', 'id_tecnico')



class Assistenza(models.Model):
    class StatoAssistenza(models.TextChoices):
        ACCOLTO = 'Accolto', _('Accolto')
        IN_LAVORAZIONE = 'In lavorazione', _('In lavorazione')
        DA_RITIRARE = 'Da ritirare', _('Da ritirare')

    id_cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistenze_richieste')
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistenze_fornite')
    stato = models.CharField(max_length=20, choices=StatoAssistenza.choices, default=StatoAssistenza.ACCOLTO)
    data = models.DateTimeField(auto_now_add=True)
    intestazione = models.CharField(max_length=200)
    descrizione = models.TextField(null=True, blank=True)



class ProdottoAcquistabile(models.Model):
    id_prodotto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200 )
    immagine = models.ImageField(upload_to='prodotti/')
    descrizione = models.TextField(null=True, blank=True)
    prezzo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Il prezzo non può essere negativo")]
    )
    quantita_rimasta = models.PositiveIntegerField(
        validators=[MinValueValidator(0, message="La quantità non può essere negativa")]
    )
    id_tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prodotti')




class Ordine(models.Model):
    class StatoOrdine(models.TextChoices):
        ACCOLTO = 'Accolto', _('Accolto')
        IN_LAVORAZIONE = 'In lavorazione', _('In lavorazione')
        DA_RITIRARE = 'Da ritirare', _('Da ritirare')

    id_ordine = models.AutoField(primary_key=True)
    stato = models.CharField(
        max_length=20,
        choices=StatoOrdine.choices,
        default=StatoOrdine.ACCOLTO,
        null=False
    )
    data_ordine = models.DateTimeField(auto_now_add=True)
    prezzo_totale = models.DecimalField(max_digits=10, decimal_places=2)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordini')



class DettaglioOrdine(models.Model):
    id_prodotto = models.ForeignKey(ProdottoAcquistabile, on_delete=models.CASCADE)
    id_ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, related_name='dettagli')
    quantita = models.PositiveIntegerField()
    prezzo_quantita = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('id_prodotto', 'id_ordine')

