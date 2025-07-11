# Sistema Informativo Aziendale – Elettronica Iovine srl

Questo progetto documenta lo sviluppo di una piattaforma web realizzata come traccia d’esame per un corso di sistemi informativi.  
L’obiettivo è progettare e implementare un **sistema integrato** basato su un **database relazionale (SQL)** per supportare i principali servizi aziendali di **Elettronica Iovine srl**, operante nel settore della vendita e assistenza di prodotti elettronici e informatici.

---
## Tecnologie Utilizzate

### Backend
- **Python** – Linguaggio principale del progetto  
- **Django** – Framework per la gestione della logica, sicurezza e routing lato server  
- **Pillow** – Libreria per la gestione di immagini utente

###  Database
- **SQLite** (in locale, semplice da configurare)

### Frontend
- **HTML/CSS** – Utilizzati per costruire l’interfaccia utente

### Varie ed eventuali
- **SHA256** (hashing password)
- **Git+GitHub** (versionamento codice)
---

## Clonazione e Avvio del Progetto

```bash
# Clona il repository
git clone https://github.com/Antoman24/ProgettoElettronicaIovine
cd ProgettoElettronicaIovine

# Crea e attiva un ambiente virtuale
python -m venv venv

# Installa le dipendenze
pip install -r requirements.txt

# Esegui le migrazioni del database
python manage.py migrate

# Avvia il server di sviluppo
python manage.py runserver


```
Il progetto sarà disponibile all’indirizzo:
http://127.0.0.1:8000/

## Pagina iniziale
Se il processo ha restituito un esito positivo, la piattaforma dovrebbe presentarsi:
<img width="1004" height="410" alt="image" src="https://github.com/user-attachments/assets/2486bd01-28b5-4816-ba3c-6afdd89b75a8" />


## Obiettivi del Progetto
La piattaforma è stata concepita per offrire un ambiente centralizzato e modulare in grado di gestire:

E-commerce
Gestione completa del catalogo prodotti, carrello, ordini e acquisti online.

Assistenza Clienti
Sistema ticketing per la segnalazione di guasti o richieste di supporto tecnico.

Area Riservata
Accesso limitato al personale autorizzato per la gestione dei prodotti, clienti, ordini e interventi di assistenza.
ipologie di Utenti e Funzionalità
# Clienti
<img width="756" height="396" alt="image" src="https://github.com/user-attachments/assets/bcf8c349-a840-4553-92ee-7a2ee5cb63e2" />

* Visualizzazione e acquisto dei prodotti disponibili

* Apertura ticket di assistenza tecnica

* Accesso ai dati personali e saldo disponibile

* Inserimento di recensioni sugli interventi ricevuti

 Credenziali utenti demo
| Nome          | Email                                                   | Password  |
| ------------- | ------------------------------------------------------- | --------- |
| Mario Rossi   | [mario.rossi@email.it](mailto:mario.rossi@email.it)     | `pass123` |
| Luigi Bianchi | [luigi.bianchi@email.it](mailto:luigi.bianchi@email.it) | `pass456` |
| Anna Verdi    | [anna.verdi@email.it](mailto:anna.verdi@email.it)       | `pass789` |

# Tecnici
<img width="631" height="609" alt="image" src="https://github.com/user-attachments/assets/bece6590-8031-48fc-a7ce-43e24f83e032" />

* Aggiunta/rimozione prodotti dal catalogo e-commerce

* Presa in carico dei ticket di assistenza

* Accesso alle informazioni sugli ordini e sui clienti

 Credenziali utenti demo
| Nome             | Email                                                         | Password   |
| ---------------- | ------------------------------------------------------------- | ---------- |
| Giuseppe Ferrari | [giuseppe.ferrari@email.it](mailto:giuseppe.ferrari@email.it) | `admin123` |
| Marco Romano     | [marco.romano@email.it](mailto:marco.romano@email.it)         | `admin456` |
| Paolo Esposito   | [paolo.esposito@email.it](mailto:paolo.esposito@email.it)     | `admin789` |


Tutte le credenziali fornite sono a scopo dimostrativo e possono essere modificate nel database.

## 📄 Licenza

Questo progetto è rilasciato sotto licenza [MIT](LICENSE).

