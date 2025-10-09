#!/usr/bin/env python3
"""
Script to manually create crop prediction tables if migration fails.
Run this script from the backend directory.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.crop_predictions import CropRecommendation, CropYieldPrediction

def create_crop_tables():
    """Create the crop prediction tables manually."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if tables exist
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            tables_to_create = []
            if 'crop_recommendations' not in existing_tables:
                tables_to_create.append('crop_recommendations')
            if 'crop_yield_predictions' not in existing_tables:
                tables_to_create.append('crop_yield_predictions')
            
            if not tables_to_create:
                print("✅ Crop prediction tables already exist!")
                return True
            
            # Create only the new tables
            print(f"Creating tables: {', '.join(tables_to_create)}")
            
            # Create the tables
            CropRecommendation.__table__.create(db.engine, checkfirst=True)
            CropYieldPrediction.__table__.create(db.engine, checkfirst=True)
            
            print("✅ Crop prediction tables created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False

if __name__ == "__main__":
    create_crop_tables()