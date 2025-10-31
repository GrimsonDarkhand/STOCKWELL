from flask import Blueprint, request, jsonify
from src.models.content import db, ContentItem, GenerationRequest
from src.services.content_brain_service import ContentBrainService
from datetime import datetime

content_brain_bp = Blueprint('content_brain', __name__)
content_brain_service = ContentBrainService()

@content_brain_bp.route('/generate', methods=['POST'])
def generate_content():
    """
    Generate new content based on prompt and requirements.
    
    Expected JSON payload:
    {
        "prompt": "string",
        "content_type": "caption|post|thread|meme|reel",
        "platform": "instagram|tiktok|x|facebook|medium",
        "source_material": "optional string"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['prompt', 'content_type', 'platform']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        prompt = data['prompt']
        content_type = data['content_type']
        platform = data['platform']
        source_material = data.get('source_material')
        
        # Create generation request record
        generation_request = GenerationRequest(
            request_type='generate',
            prompt=prompt,
            source_content=source_material,
            target_platform=platform,
            target_format=content_type,
            status='processing'
        )
        db.session.add(generation_request)
        db.session.commit()
        
        # Generate content using Content Brain service
        result = content_brain_service.generate_content(
            prompt=prompt,
            content_type=content_type,
            platform=platform,
            source_material=source_material
        )
        
        if result['success']:
            # Create content item
            content_item = ContentItem(
                title=f"Generated {content_type} for {platform}",
                content_type=content_type,
                platform=platform,
                content_text=result['content']['text'],
                hashtags=result['content']['hashtags'],
                call_to_action=result['content']['call_to_action'],
                source_material=source_material,
                status='draft'
            )
            db.session.add(content_item)
            
            # Update generation request
            generation_request.status = 'completed'
            generation_request.result_content_id = content_item.id
            generation_request.completed_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "content": content_item.to_dict(),
                "generation_request_id": generation_request.id,
                "model_used": result.get('model_used'),
                "media_suggestions": result['content'].get('media_suggestions', [])
            }), 201
        else:
            # Update generation request with error
            generation_request.status = 'failed'
            generation_request.error_message = result['error']
            generation_request.completed_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                "success": False,
                "error": result['error'],
                "generation_request_id": generation_request.id
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_brain_bp.route('/repurpose', methods=['POST'])
def repurpose_content():
    """
    Repurpose existing content for a different platform or format.
    
    Expected JSON payload:
    {
        "content_id": "integer (optional)",
        "original_content": "string (required if no content_id)",
        "target_platform": "instagram|tiktok|x|facebook|medium",
        "target_format": "caption|post|thread|meme|reel"
    }
    """
    try:
        data = request.get_json()
        
        # Get original content
        original_content = None
        source_content_id = data.get('content_id')
        
        if source_content_id:
            content_item = ContentItem.query.get(source_content_id)
            if not content_item:
                return jsonify({"error": "Content not found"}), 404
            original_content = content_item.content_text
        elif 'original_content' in data:
            original_content = data['original_content']
        else:
            return jsonify({"error": "Either content_id or original_content is required"}), 400
        
        target_platform = data.get('target_platform')
        target_format = data.get('target_format')
        
        if not target_platform or not target_format:
            return jsonify({"error": "target_platform and target_format are required"}), 400
        
        # Create generation request record
        generation_request = GenerationRequest(
            request_type='repurpose',
            prompt=f"Repurpose for {target_platform} as {target_format}",
            source_content=original_content,
            target_platform=target_platform,
            target_format=target_format,
            status='processing'
        )
        db.session.add(generation_request)
        db.session.commit()
        
        # Repurpose content using Content Brain service
        result = content_brain_service.repurpose_content(
            original_content=original_content,
            target_platform=target_platform,
            target_format=target_format
        )
        
        if result['success']:
            # Create new content item
            content_item = ContentItem(
                title=f"Repurposed {target_format} for {target_platform}",
                content_type=target_format,
                platform=target_platform,
                content_text=result['content']['text'],
                hashtags=result['content']['hashtags'],
                call_to_action=result['content']['call_to_action'],
                source_material=f"Repurposed from content_id: {source_content_id}" if source_content_id else "Repurposed content",
                status='draft'
            )
            db.session.add(content_item)
            
            # Update generation request
            generation_request.status = 'completed'
            generation_request.result_content_id = content_item.id
            generation_request.completed_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "content": content_item.to_dict(),
                "generation_request_id": generation_request.id,
                "model_used": result.get('model_used')
            }), 201
        else:
            # Update generation request with error
            generation_request.status = 'failed'
            generation_request.error_message = result['error']
            generation_request.completed_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                "success": False,
                "error": result['error'],
                "generation_request_id": generation_request.id
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_brain_bp.route('/suggestions/<theme>', methods=['GET'])
def get_content_suggestions(theme):
    """Get content suggestions based on a theme."""
    try:
        suggestions = content_brain_service.get_content_suggestions(theme)
        return jsonify({
            "success": True,
            "theme": theme,
            "suggestions": suggestions
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_brain_bp.route('/content', methods=['GET'])
def get_content():
    """Get all generated content with optional filtering."""
    try:
        # Get query parameters for filtering
        platform = request.args.get('platform')
        content_type = request.args.get('content_type')
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        
        # Build query
        query = ContentItem.query
        
        if platform:
            query = query.filter(ContentItem.platform == platform)
        if content_type:
            query = query.filter(ContentItem.content_type == content_type)
        if status:
            query = query.filter(ContentItem.status == status)
        
        # Order by creation date (newest first) and limit
        content_items = query.order_by(ContentItem.created_at.desc()).limit(limit).all()
        
        return jsonify({
            "success": True,
            "content": [item.to_dict() for item in content_items],
            "count": len(content_items)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_brain_bp.route('/content/<int:content_id>', methods=['GET'])
def get_content_by_id(content_id):
    """Get specific content by ID."""
    try:
        content_item = ContentItem.query.get(content_id)
        if not content_item:
            return jsonify({"error": "Content not found"}), 404
        
        return jsonify({
            "success": True,
            "content": content_item.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_brain_bp.route('/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    """Update content item."""
    try:
        content_item = ContentItem.query.get(content_id)
        if not content_item:
            return jsonify({"error": "Content not found"}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['title', 'content_text', 'hashtags', 'call_to_action', 'status']
        for field in allowed_fields:
            if field in data:
                setattr(content_item, field, data[field])
        
        content_item.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "content": content_item.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_brain_bp.route('/requests', methods=['GET'])
def get_generation_requests():
    """Get generation requests with optional filtering."""
    try:
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        
        query = GenerationRequest.query
        
        if status:
            query = query.filter(GenerationRequest.status == status)
        
        requests = query.order_by(GenerationRequest.created_at.desc()).limit(limit).all()
        
        return jsonify({
            "success": True,
            "requests": [req.to_dict() for req in requests],
            "count": len(requests)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

