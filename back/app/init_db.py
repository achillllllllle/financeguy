from sqlalchemy.orm import Session
from . import models

def init_general_categories(db: Session):
    # Liste des catégories générales par défaut
    general_categories = [
        {
            "name": "Alimentation",
            "description": "Dépenses liées à la nourriture et aux boissons",
            "is_general": True
        },
        {
            "name": "Transport",
            "description": "Dépenses de transport (essence, tickets, etc.)",
            "is_general": True
        },
        {
            "name": "Logement",
            "description": "Dépenses liées au logement (loyer, charges, etc.)",
            "is_general": True
        },
        {
            "name": "Factures",
            "description": "Factures mensuelles (électricité, eau, etc.)",
            "is_general": True
        },
        {
            "name": "Loisirs",
            "description": "Dépenses de loisirs et divertissement",
            "is_general": True
        },
        {
            "name": "Santé",
            "description": "Dépenses de santé et médicaments",
            "is_general": True
        },
        {
            "name": "Shopping",
            "description": "Achats divers",
            "is_general": True
        },
        {
            "name": "Salaire",
            "description": "Revenus salariaux",
            "is_general": True
        },
        {
            "name": "Autres revenus",
            "description": "Autres sources de revenus",
            "is_general": True
        }
    ]

    # Vérifier si les catégories générales existent déjà
    existing_categories = db.query(models.Category).filter(
        models.Category.is_general == True
    ).all()

    if not existing_categories:
        for category_data in general_categories:
            db_category = models.Category(**category_data)
            db.add(db_category)
        db.commit()
        print("Catégories générales initialisées avec succès")
    else:
        print("Les catégories générales existent déjà") 