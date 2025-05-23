# Intégration Google Sheets (Optionnel)
# Pour utiliser ce module, vous devez :
# 1. Installer les dépendances : pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
# 2. Créer un projet Google Cloud et activer l'API Google Sheets
# 3. Télécharger les credentials et les placer dans le dossier

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheetsIntegration:
    def __init__(self, credentials_file='credentials.json', spreadsheet_id=None):
        """
        Initialise la connexion à Google Sheets
        
        Args:
            credentials_file: Chemin vers le fichier de credentials Google
            spreadsheet_id: ID de la feuille Google Sheets (peut être défini plus tard)
        """
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.service = None
        
        if os.path.exists(credentials_file):
            self.authenticate()
    
    def authenticate(self):
        """Authentifie l'accès à Google Sheets"""
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=creds)
    
    def create_spreadsheet(self, title="Horaires de Travail"):
        """Crée une nouvelle feuille Google Sheets"""
        spreadsheet = {
            'properties': {
                'title': title
            },
            'sheets': [{
                'properties': {
                    'title': 'Horaires',
                    'gridProperties': {
                        'rowCount': 1000,
                        'columnCount': 10
                    }
                }
            }]
        }
        
        result = self.service.spreadsheets().create(body=spreadsheet).execute()
        self.spreadsheet_id = result['spreadsheetId']
        
        # Ajouter les en-têtes
        headers = [['Date', 'Jour', 'Matin Début', 'Matin Fin', 'Après-midi Début', 
                   'Après-midi Fin', 'Total Heures', 'Total Décimal', 'Semaine']]
        
        self.update_values('A1:I1', headers)
        
        return self.spreadsheet_id
    
    def update_values(self, range_name, values):
        """Met à jour des valeurs dans la feuille"""
        body = {'values': values}
        
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        return result
    
    def append_horaire(self, horaire_data):
        """Ajoute un horaire à la feuille"""
        values = [[
            horaire_data['date'],
            horaire_data['jour'],
            horaire_data['matin_debut'],
            horaire_data['matin_fin'],
            horaire_data['apres_midi_debut'],
            horaire_data['apres_midi_fin'],
            horaire_data['total_heures'],
            horaire_data['total_heures_decimal'],
            horaire_data.get('semaine', '')
        ]]
        
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='A:I',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
        
        return result
    
    def get_all_horaires(self):
        """Récupère tous les horaires de la feuille"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='A2:I'
        ).execute()
        
        values = result.get('values', [])
        return values
    
    def clear_sheet(self):
        """Efface toutes les données sauf les en-têtes"""
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range='A2:I1000'
        ).execute()
    
    def sync_from_database(self, horaires_list):
        """Synchronise tous les horaires depuis la base de données vers Google Sheets"""
        # Effacer les données existantes
        self.clear_sheet()
        
        # Préparer toutes les données
        all_values = []
        for h in horaires_list:
            all_values.append([
                h['date'],
                h['jour'],
                h['matin_debut'],
                h['matin_fin'],
                h['apres_midi_debut'],
                h['apres_midi_fin'],
                h['total_heures'],
                h['total_heures_decimal'],
                h.get('semaine', '')
            ])
        
        # Envoyer toutes les données en une fois
        if all_values:
            self.update_values(f'A2:I{len(all_values)+1}', all_values)
        
        return len(all_values)

# Exemple d'utilisation dans app.py :
# 
# from google_sheets_integration import GoogleSheetsIntegration
# 
# # Initialiser l'intégration
# gs = GoogleSheetsIntegration('path/to/credentials.json')
# 
# # Créer une nouvelle feuille ou utiliser une existante
# spreadsheet_id = gs.create_spreadsheet("Mes Horaires 2025")
# # ou
# gs.spreadsheet_id = "ID_DE_VOTRE_FEUILLE_EXISTANTE"
# 
# # Ajouter un horaire
# gs.append_horaire({
#     'date': '23/05/2025',
#     'jour': 'Vendredi',
#     'matin_debut': '09:00',
#     'matin_fin': '13:00',
#     'apres_midi_debut': '14:00',
#     'apres_midi_fin': '16:00',
#     'total_heures': '6:00',
#     'total_heures_decimal': 6.0,
#     'semaine': 'Semaine 21'
# })