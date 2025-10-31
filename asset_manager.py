from flask import Blueprint, request, jsonify
from src.services.asset_manager_service import AssetManagerService

asset_manager_bp = Blueprint('asset_manager', __name__)
asset_manager_service = AssetManagerService()

@asset_manager_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available asset categories."""
    try:
        categories = asset_manager_service.asset_categories
        return jsonify({
            "success": True,
            "categories": categories
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/assets/<category>', methods=['GET'])
def get_assets_by_category(category):
    """
    Get assets by category.
    
    Query parameters:
    - limit: Maximum number of assets to return (default: 20)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        
        result = asset_manager_service.get_assets_by_category(category, limit)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/search', methods=['GET'])
def search_assets():
    """
    Search for assets.
    
    Query parameters:
    - q: Search query (required)
    - type: Asset type filter (images, videos, audio, documents)
    - category: Category filter
    """
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Search query 'q' is required"}), 400
        
        asset_type = request.args.get('type')
        category = request.args.get('category')
        
        result = asset_manager_service.search_assets(query, asset_type, category)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/suggestions', methods=['GET'])
def get_asset_suggestions():
    """
    Get asset suggestions for content creation.
    
    Query parameters:
    - content_type: Type of content (required)
    - platform: Target platform (required)
    - theme: Optional theme
    """
    try:
        content_type = request.args.get('content_type')
        platform = request.args.get('platform')
        
        if not content_type or not platform:
            return jsonify({"error": "content_type and platform are required"}), 400
        
        theme = request.args.get('theme')
        
        result = asset_manager_service.get_asset_suggestions(content_type, platform, theme)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/upload', methods=['POST'])
def upload_asset():
    """
    Upload a new asset.
    
    Expected form data:
    - file: The file to upload
    - category: Asset category
    - metadata: Optional JSON metadata
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        category = request.form.get('category')
        if not category:
            return jsonify({"error": "Category is required"}), 400
        
        metadata = request.form.get('metadata')
        if metadata:
            try:
                import json
                metadata = json.loads(metadata)
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid metadata JSON"}), 400
        
        # Read file data
        file_data = file.read()
        
        result = asset_manager_service.upload_asset(
            file_data=file_data,
            filename=file.filename,
            category=category,
            metadata=metadata
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/organize', methods=['POST'])
def organize_assets():
    """
    Reorganize assets based on specified rules.
    
    Expected JSON payload:
    {
        "rules": {
            "move_by_date": true,
            "create_category_folders": true,
            "update_metadata": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'rules' not in data:
            return jsonify({"error": "Reorganization rules are required"}), 400
        
        result = asset_manager_service.organize_assets(data['rules'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/analytics', methods=['GET'])
def get_asset_analytics():
    """
    Get asset analytics.
    
    Query parameters:
    - period: Time period (7d, 30d, 90d) - default: 30d
    """
    try:
        time_period = request.args.get('period', '30d')
        
        # Validate time period
        valid_periods = ['7d', '30d', '90d']
        if time_period not in valid_periods:
            return jsonify({"error": f"Invalid time period. Must be one of: {valid_periods}"}), 400
        
        result = asset_manager_service.get_asset_analytics(time_period)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@asset_manager_bp.route('/formats', methods=['GET'])
def get_supported_formats():
    """Get supported file formats by type."""
    try:
        formats = asset_manager_service.supported_formats
        return jsonify({
            "success": True,
            "supported_formats": formats
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

