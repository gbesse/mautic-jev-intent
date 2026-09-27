# Mautic Jev Intent

Experimental community alpha v0.1.0 · MIT.

## Français

Un service reçoit les soumissions de formulaire Mautic, vérifie HMAC SHA256 et écrit l’intention dans un champ Contact personnalisé.

Installation :

```sh
python3 app.py
```

Variables serveur : `TYPESAFE_API_KEY, MAUTIC_WEBHOOK_SECRET, MAUTIC_URL, MAUTIC_API_USER, MAUTIC_API_PASSWORD, MAUTIC_INTENT_FIELD (optional; default: jev_intent), MAUTIC_MESSAGE_FIELD (optional; default: message)`. Garder les secrets hors du dépôt et de la configuration visible par les utilisateurs.

Créer un champ Contact `jev_intent`, activer l’API et configurer l’événement webhook `mautic.form_on_submit` vers `/webhook`. L’API Basic doit être activée sur l’instance.

## English

A service receives Mautic form submissions, verifies HMAC SHA256, and writes intent to a custom Contact field.

Setup:

```sh
python3 app.py
```

Server variables: `TYPESAFE_API_KEY, MAUTIC_WEBHOOK_SECRET, MAUTIC_URL, MAUTIC_API_USER, MAUTIC_API_PASSWORD, MAUTIC_INTENT_FIELD (optional; default: jev_intent), MAUTIC_MESSAGE_FIELD (optional; default: message)`. Keep secrets outside the repository and user-visible configuration.

Create a `jev_intent` Contact field, enable the API, and configure the `mautic.form_on_submit` webhook event to `/webhook`. Basic API authentication must be enabled on the instance.

## Español

Un servicio recibe envíos de formularios de Mautic, verifica HMAC SHA256 y escribe la intención en un campo personalizado del contacto.

Instalación:

```sh
python3 app.py
```

Variables del servidor: `TYPESAFE_API_KEY, MAUTIC_WEBHOOK_SECRET, MAUTIC_URL, MAUTIC_API_USER, MAUTIC_API_PASSWORD, MAUTIC_INTENT_FIELD (optional; default: jev_intent), MAUTIC_MESSAGE_FIELD (optional; default: message)`. Mantén los secretos fuera del repositorio y de la configuración visible para usuarios.

Crea un campo de Contacto `jev_intent`, activa la API y configura el evento webhook `mautic.form_on_submit` hacia `/webhook`. Debe estar activa la autenticación Basic de la API.

## Verification / Vérification / Verificación

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic Jev responses and host event fixtures. Threshold `0.9` in `policy.json` is an example and must be calibrated on labeled data before automatic actions. No live host or Jev service has been exercised. / Les tests utilisent des réponses synthétiques et le seuil doit être calibré ; aucun hôte ni service Jev réel n’a été testé. / Las pruebas usan respuestas sintéticas y el umbral debe calibrarse; no se ha probado un host ni un servicio Jev real.

Host reference / Référence de l’hôte / Referencia del host: https://devdocs.mautic.org/en/6.0/webhooks/getting_started.html

The receiver listens on `127.0.0.1:8080` by default; use a TLS reverse proxy for remote webhooks. `LISTEN_HOST` and `PORT` can override the bind address. / Le service écoute par défaut sur `127.0.0.1:8080` ; utiliser un proxy TLS pour les webhooks distants. / El servicio escucha por defecto en `127.0.0.1:8080`; usa un proxy TLS para webhooks remotos.
