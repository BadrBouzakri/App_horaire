from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horaires.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Horaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    matin_debut = db.Column(db.Time, nullable=False)
    matin_fin = db.Column(db.Time, nullable=False)
    apres_midi_debut = db.Column(db.Time, nullable=False)
    apres_midi_fin = db.Column(db.Time, nullable=False)
    total_heures = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Horaire {self.date}>'

def calculer_duree(debut, fin):
    """Calcule la durée entre deux heures"""
    debut_delta = timedelta(hours=debut.hour, minutes=debut.minute)
    fin_delta = timedelta(hours=fin.hour, minutes=fin.minute)
    duree = fin_delta - debut_delta
    return duree.total_seconds() / 3600

def format_duree(heures):
    """Formate la durée en heures:minutes"""
    h = int(heures)
    m = int((heures - h) * 60)
    return f"{h}:{m:02d}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/horaires', methods=['GET'])
def get_horaires():
    # Récupérer la semaine demandée ou la semaine actuelle
    semaine = request.args.get('semaine')
    if semaine:
        date_debut = datetime.strptime(semaine, '%Y-%m-%d').date()
    else:
        today = datetime.now().date()
        date_debut = today - timedelta(days=today.weekday())
    
    date_fin = date_debut + timedelta(days=6)
    
    horaires = Horaire.query.filter(
        Horaire.date >= date_debut,
        Horaire.date <= date_fin
    ).order_by(Horaire.date).all()
    
    result = []
    total_semaine = 0
    
    for h in horaires:
        result.append({
            'id': h.id,
            'date': h.date.strftime('%Y-%m-%d'),
            'jour': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'][h.date.weekday()],
            'matin_debut': h.matin_debut.strftime('%H:%M'),
            'matin_fin': h.matin_fin.strftime('%H:%M'),
            'apres_midi_debut': h.apres_midi_debut.strftime('%H:%M'),
            'apres_midi_fin': h.apres_midi_fin.strftime('%H:%M'),
            'total_heures': format_duree(h.total_heures),
            'total_heures_decimal': h.total_heures
        })
        total_semaine += h.total_heures
    
    heures_normales = 36.5
    heures_supplementaires = max(0, total_semaine - heures_normales)
    
    return jsonify({
        'horaires': result,
        'total_semaine': format_duree(total_semaine),
        'total_semaine_decimal': total_semaine,
        'heures_normales': heures_normales,
        'heures_supplementaires': format_duree(heures_supplementaires),
        'depasse_limite': total_semaine > heures_normales
    })

@app.route('/api/horaires', methods=['POST'])
def add_horaire():
    data = request.json
    
    # Parser les données
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    matin_debut = datetime.strptime(data['matin_debut'], '%H:%M').time()
    matin_fin = datetime.strptime(data['matin_fin'], '%H:%M').time()
    apres_midi_debut = datetime.strptime(data['apres_midi_debut'], '%H:%M').time()
    apres_midi_fin = datetime.strptime(data['apres_midi_fin'], '%H:%M').time()
    
    # Calculer le total d'heures
    duree_matin = calculer_duree(matin_debut, matin_fin)
    duree_apres_midi = calculer_duree(apres_midi_debut, apres_midi_fin)
    total_heures = duree_matin + duree_apres_midi
    
    # Vérifier si un horaire existe déjà pour cette date
    horaire_existant = Horaire.query.filter_by(date=date).first()
    
    if horaire_existant:
        # Mettre à jour l'horaire existant
        horaire_existant.matin_debut = matin_debut
        horaire_existant.matin_fin = matin_fin
        horaire_existant.apres_midi_debut = apres_midi_debut
        horaire_existant.apres_midi_fin = apres_midi_fin
        horaire_existant.total_heures = total_heures
    else:
        # Créer un nouvel horaire
        nouvel_horaire = Horaire(
            date=date,
            matin_debut=matin_debut,
            matin_fin=matin_fin,
            apres_midi_debut=apres_midi_debut,
            apres_midi_fin=apres_midi_fin,
            total_heures=total_heures
        )
        db.session.add(nouvel_horaire)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'total_jour': format_duree(total_heures),
        'message': f'Horaire enregistré pour le {date.strftime("%d/%m/%Y")}. Total du jour: {format_duree(total_heures)}'
    })

@app.route('/api/horaires/<int:id>', methods=['DELETE'])
def delete_horaire(id):
    horaire = Horaire.query.get_or_404(id)
    db.session.delete(horaire)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Horaire supprimé'})

@app.route('/api/export/csv')
def export_csv():
    # Récupérer tous les horaires
    horaires = Horaire.query.order_by(Horaire.date.desc()).all()
    
    # Créer le CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # En-têtes
    writer.writerow(['Date', 'Jour', 'Matin Début', 'Matin Fin', 'Après-midi Début', 'Après-midi Fin', 'Total Heures'])
    
    # Données
    for h in horaires:
        jour = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'][h.date.weekday()]
        writer.writerow([
            h.date.strftime('%d/%m/%Y'),
            jour,
            h.matin_debut.strftime('%H:%M'),
            h.matin_fin.strftime('%H:%M'),
            h.apres_midi_debut.strftime('%H:%M'),
            h.apres_midi_fin.strftime('%H:%M'),
            format_duree(h.total_heures)
        ])
    
    # Préparer la réponse
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'horaires_{datetime.now().strftime("%Y%m%d")}.csv'
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)