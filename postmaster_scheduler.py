from flask import Blueprint, request, jsonify
from src.services.postmaster_scheduler_service import PostmasterSchedulerService
from datetime import datetime

postmaster_scheduler_bp = Blueprint('postmaster_scheduler', __name__)
scheduler_service = PostmasterSchedulerService()

@postmaster_scheduler_bp.route('/schedule', methods=['POST'])
def schedule_content():
    """
    Schedule content for publishing on specified platforms.
    
    Expected JSON payload:
    {
        "content_text": "string",
        "platforms": ["instagram", "tiktok", "x", "facebook"],
        "media_urls": ["url1", "url2"],
        "schedule_time": "optional ISO datetime string"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('content_text') or not data.get('platforms'):
            return jsonify({"error": "content_text and platforms are required"}), 400
        
        result = scheduler_service.schedule_content(
            content_data=data,
            schedule_time=data.get('schedule_time')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@postmaster_scheduler_bp.route('/schedule/bulk', methods=['POST'])
def schedule_bulk_content():
    """
    Schedule multiple pieces of content with intelligent distribution.
    
    Expected JSON payload:
    {
        "content_list": [
            {
                "content_text": "string",
                "platforms": ["instagram", "tiktok"],
                "media_urls": ["url1"]
            }
        ],
        "distribution_strategy": "optimal|even|burst"
    }
    """
    try:
        data = request.get_json()
        
        content_list = data.get('content_list', [])
        if not content_list:
            return jsonify({"error": "content_list is required and cannot be empty"}), 400
        
        distribution_strategy = data.get('distribution_strategy', 'optimal')
        
        result = scheduler_service.schedule_bulk_content(
            content_list=content_list,
            distribution_strategy=distribution_strategy
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@postmaster_scheduler_bp.route('/monitor', methods=['POST'])
def monitor_engagement():
    """
    Monitor engagement for specified posts.
    
    Expected JSON payload:
    {
        "post_ids": ["post_id_1", "post_id_2"]
    }
    """
    try:
        data = request.get_json()
        
        post_ids = data.get('post_ids', [])
        if not post_ids:
            return jsonify({"error": "post_ids is required and cannot be empty"}), 400
        
        result = scheduler_service.monitor_engagement(post_ids)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@postmaster_scheduler_bp.route('/repost', methods=['POST'])
def repost_high_performing():
    """
    Identify and repost high-performing content.
    
    Expected JSON payload:
    {
        "performance_threshold": 1.5
    }
    """
    try:
        data = request.get_json() or {}
        
        performance_threshold = data.get('performance_threshold', 1.5)
        
        result = scheduler_service.repost_high_performing_content(performance_threshold)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@postmaster_scheduler_bp.route('/schedule', methods=['GET'])
def get_posting_schedule():
    """
    Get the current posting schedule.
    
    Query parameters:
    - days_ahead: Number of days to look ahead (default: 7)
    """
    try:
        days_ahead = request.args.get('days_ahead', 7, type=int)
        
        if days_ahead < 1 or days_ahead > 30:
            return jsonify({"error": "days_ahead must be between 1 and 30"}), 400
        
        result = scheduler_service.get_posting_schedule(days_ahead)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@postmaster_scheduler_bp.route('/optimal-times', methods=['GET'])
def get_optimal_times():
    """Get optimal posting times for all platforms."""
    try:
        return jsonify({
            "success": True,
            "optimal_times": scheduler_service.optimal_times,
            "daily_limits": scheduler_service.daily_limits
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@postmaster_scheduler_bp.route('/platforms', methods=['GET'])
def get_supported_platforms():
    """Get list of supported platforms."""
    try:
        platforms = list(scheduler_service.optimal_times.keys())
        return jsonify({
            "success": True,
            "supported_platforms": platforms,
            "platform_details": {
                platform: {
                    "optimal_times": scheduler_service.optimal_times[platform],
                    "daily_limit": scheduler_service.daily_limits[platform]
                }
                for platform in platforms
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

