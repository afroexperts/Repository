#!/usr/bin/env python3
"""
Seed Translations Script
Populates the translations table with default translations for English, French, Kinyarwanda, and Swahili
"""

from database import get_db, Translation
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default translations for core UI elements
default_translations = {
    # Dashboard
    "dashboard.title": {
        "en": "Dashboard",
        "fr": "Tableau de bord",
        "rw": "Imbonerahamwe",
        "sw": "Dashbodi"
    },
    "dashboard.welcome": {
        "en": "Welcome to Afro Experts ERP",
        "fr": "Bienvenue sur Afro Experts ERP",
        "rw": "Murakaza neza kuri Afro Experts ERP",
        "sw": "Karibu katika Afro Experts ERP"
    },
    "dashboard.stats": {
        "en": "Statistics",
        "fr": "Statistiques",
        "rw": "Imibare",
        "sw": "Takwimu"
    },
    
    # Navigation
    "nav.products": {
        "en": "Products",
        "fr": "Produits",
        "rw": "Ibicuruzwa",
        "sw": "Bidhaa"
    },
    "nav.orders": {
        "en": "Orders",
        "fr": "Commandes",
        "rw": "Amatungo",
        "sw": "Maagizo"
    },
    "nav.clients": {
        "en": "Clients",
        "fr": "Clients",
        "rw": "Abakiriya",
        "sw": "Wateja"
    },
    "nav.inventory": {
        "en": "Inventory",
        "fr": "Inventaire",
        "rw": "Ububiko",
        "sw": "Hifadhi"
    },
    "nav.finance": {
        "en": "Finance",
        "fr": "Finance",
        "rw": "Imari",
        "sw": "Fedha"
    },
    "nav.invoices": {
        "en": "Invoices",
        "fr": "Factures",
        "rw": "Imifatirwa",
        "sw": "Ankara"
    },
    "nav.reports": {
        "en": "Reports",
        "fr": "Rapports",
        "rw": "Raporo",
        "sw": "Ripoti"
    },
    "nav.settings": {
        "en": "Settings",
        "fr": "Paramètres",
        "rw": "Igenamiterere",
        "sw": "Mipangilio"
    },
    
    # Common Actions
    "action.save": {
        "en": "Save",
        "fr": "Enregistrer",
        "rw": "Kubika",
        "sw": "Hifadhi"
    },
    "action.cancel": {
        "en": "Cancel",
        "fr": "Annuler",
        "rw": "Kureka",
        "sw": "Ghairi"
    },
    "action.delete": {
        "en": "Delete",
        "fr": "Supprimer",
        "rw": "Gusiba",
        "sw": "Futa"
    },
    "action.edit": {
        "en": "Edit",
        "fr": "Modifier",
        "rw": "Guhindura",
        "sw": "Hariri"
    },
    "action.create": {
        "en": "Create",
        "fr": "Créer",
        "rw": "Kurema",
        "sw": "Unda"
    },
    "action.view": {
        "en": "View",
        "fr": "Voir",
        "rw": "Kureba",
        "sw": "Ona"
    },
    
    # Status Messages
    "status.success": {
        "en": "Success",
        "fr": "Succès",
        "rw": "Byakunze",
        "sw": "Mafanikio"
    },
    "status.error": {
        "en": "Error",
        "fr": "Erreur",
        "rw": "Ikosa",
        "sw": "Hitilafu"
    },
    "status.loading": {
        "en": "Loading...",
        "fr": "Chargement...",
        "rw": "Gupakurura...",
        "sw": "Inapakia..."
    },
    
    # Form Labels
    "form.name": {
        "en": "Name",
        "fr": "Nom",
        "rw": "Izina",
        "sw": "Jina"
    },
    "form.email": {
        "en": "Email",
        "fr": "E-mail",
        "rw": "Imeyili",
        "sw": "Barua pepe"
    },
    "form.phone": {
        "en": "Phone",
        "fr": "Téléphone",
        "rw": "Telefone",
        "sw": "Simu"
    },
    "form.address": {
        "en": "Address",
        "fr": "Adresse",
        "rw": "Aderesi",
        "sw": "Anwani"
    },
    "form.description": {
        "en": "Description",
        "fr": "Description",
        "rw": "Ibisobanuro",
        "sw": "Maelezo"
    },
    "form.price": {
        "en": "Price",
        "fr": "Prix",
        "rw": "Igiciro",
        "sw": "Bei"
    },
    "form.quantity": {
        "en": "Quantity",
        "fr": "Quantité",
        "rw": "Ingano",
        "sw": "Kiasi"
    },
    "form.date": {
        "en": "Date",
        "fr": "Date",
        "rw": "Itariki",
        "sw": "Tarehe"
    },
    
    # Roles
    "role.admin": {
        "en": "Administrator",
        "fr": "Administrateur",
        "rw": "Umuyobozi mukuru",
        "sw": "Msimamizi"
    },
    "role.manager": {
        "en": "Manager",
        "fr": "Gestionnaire",
        "rw": "Umuyobozi",
        "sw": "Meneja"
    },
    "role.cashier": {
        "en": "Cashier",
        "fr": "Caissier",
        "rw": "Umukoresha w'amafaranga",
        "sw": "Karani wa fedha"
    },
    "role.inventory_officer": {
        "en": "Inventory Officer",
        "fr": "Responsable d'inventaire",
        "rw": "Ushinzwe ububiko",
        "sw": "Afisa wa hifadhi"
    },
    "role.technician": {
        "en": "Technician",
        "fr": "Technicien",
        "rw": "Umunyanyabuhanga",
        "sw": "Fundi"
    },
    
    # Languages
    "language.english": {
        "en": "English",
        "fr": "Anglais",
        "rw": "Icyongereza",
        "sw": "Kiingereza"
    },
    "language.french": {
        "en": "French",
        "fr": "Français",
        "rw": "Igifaransa",
        "sw": "Kifaransa"
    },
    "language.kinyarwanda": {
        "en": "Kinyarwanda",
        "fr": "Kinyarwanda",
        "rw": "Ikinyarwanda",
        "sw": "Kinyarwanda"
    },
    "language.swahili": {
        "en": "Swahili",
        "fr": "Swahili",
        "rw": "Igiswahiri",
        "sw": "Kiswahili"
    }
}

def seed_translations():
    """Seed the database with default translations"""
    logger.info("Starting translations seeding...")
    
    db = next(get_db())
    
    try:
        # Delete existing translations to avoid duplicates
        db.query(Translation).delete()
        db.commit()
        
        # Seed translations
        total_translations = 0
        for key, languages in default_translations.items():
            for language, value in languages.items():
                translation = Translation(
                    key=key,
                    language=language,
                    value=value,
                    category="ui"
                )
                db.add(translation)
                total_translations += 1
        
        db.commit()
        logger.info(f"✅ Translations seeded successfully! Added {total_translations} translations")
        
        # Print summary by language
        for lang in ["en", "fr", "rw", "sw"]:
            count = db.query(Translation).filter(Translation.language == lang).count()
            logger.info(f"  {lang}: {count} translations")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error seeding translations: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_translations()