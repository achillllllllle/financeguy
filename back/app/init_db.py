from sqlalchemy.orm import Session
from . import models
from sqlalchemy import select

def init_general_categories(db):
    """Initialize general categories if they don't exist"""
    general_categories = [
        {"name": "Salaire", "description": "Revenus salariaux"},
        {"name": "Loyer", "description": "Paiement du loyer"},
        {"name": "Épicerie", "description": "Courses alimentaires"},
        {"name": "Transport", "description": "Frais de transport"},
        {"name": "Loisirs", "description": "Dépenses de loisirs"},
        {"name": "Santé", "description": "Frais médicaux"},
        {"name": "Éducation", "description": "Frais d'éducation"},
        {"name": "Autres", "description": "Autres dépenses"}
    ]

    try:
        # Vérifier si les catégories existent déjà
        stmt = select(models.Category).where(models.Category.is_general == True)
        existing_categories = db.session.execute(stmt).scalars().all()
        existing_names = {cat.name for cat in existing_categories}

        # Ajouter les catégories manquantes
        for category in general_categories:
            if category["name"] not in existing_names:
                new_category = models.Category(
                    name=category["name"],
                    description=category["description"],
                    is_general=True
                )
                db.session.add(new_category)

        db.session.commit()
        print("Catégories générales initialisées avec succès")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing categories: {str(e)}")
        raise 