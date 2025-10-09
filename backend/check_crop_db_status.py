#!/usr/bin/env python3
"""
Quick check for crop prediction database integration status.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.crop_predictions import CropRecommendation, CropYieldPrediction

def check_database_status():
    """Check if crop prediction tables exist and have data."""
    app = create_app()
    
    with app.app_context():
        # Check if tables exist
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        print('=== DATABASE TABLES STATUS ===')
        print('Total tables:', len(existing_tables))
        print('Crop tables status:')
        crop_recommendations_exists = 'crop_recommendations' in existing_tables
        crop_yield_predictions_exists = 'crop_yield_predictions' in existing_tables
        
        print(f'- crop_recommendations: {crop_recommendations_exists}')
        print(f'- crop_yield_predictions: {crop_yield_predictions_exists}')
        
        # Check if models are accessible and count records
        if crop_recommendations_exists and crop_yield_predictions_exists:
            try:
                count_rec = CropRecommendation.query.count()
                count_yield = CropYieldPrediction.query.count()
                print(f'\n=== RECORD COUNTS ===')
                print(f'- Crop recommendations: {count_rec}')
                print(f'- Yield predictions: {count_yield}')
                
                # Show latest records if any exist
                if count_rec > 0:
                    latest_rec = CropRecommendation.query.order_by(CropRecommendation.created_at.desc()).first()
                    print(f'Latest recommendation: {latest_rec.predicted_crop} (confidence: {latest_rec.confidence})')
                
                if count_yield > 0:
                    latest_yield = CropYieldPrediction.query.order_by(CropYieldPrediction.created_at.desc()).first()
                    print(f'Latest yield prediction: {latest_yield.predicted_yield} {latest_yield.unit} for {latest_yield.crop}')
                    
            except Exception as e:
                print(f'Error querying tables: {e}')
        else:
            print('\n❌ Tables not found! Need to run migrations or create_crop_tables.py')
            
if __name__ == "__main__":
    check_database_status()