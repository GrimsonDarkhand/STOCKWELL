import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class PostmasterSchedulerService:
    """
    Service class for the Postmaster Scheduler module.
    Handles content scheduling and publishing across social media platforms.
    """
    
    def __init__(self):
        self.publer_api_key = os.getenv('PUBLER_API_KEY')
        self.google_calendar_credentials = os.getenv('GOOGLE_CALENDAR_CREDENTIALS')
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('WHATSAPP_NUMBER')
        
        # Platform-specific optimal posting times (in hours, 24-hour format)
        self.optimal_times = {
            "instagram": [9, 11, 13, 17, 19],
            "tiktok": [6, 10, 19, 20],
            "x": [8, 12, 17, 19],
            "facebook": [9, 13, 15],
            "linkedin": [8, 12, 17],
            "medium": [7, 12, 20]
        }
        
        # Platform-specific posting limits per day
        self.daily_limits = {
            "instagram": 2,
            "tiktok": 3,
            "x": 5,
            "facebook": 2,
            "linkedin": 1,
            "medium": 1
        }
        
        # Engagement spike thresholds (percentage increase from average)
        self.engagement_thresholds = {
            "likes": 150,  # 150% of average
            "comments": 200,  # 200% of average
            "shares": 300,  # 300% of average
            "saves": 250   # 250% of average
        }
    
    def schedule_content(self, content_data: Dict[str, Any], 
                        schedule_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Schedule content for publishing on specified platforms.
        
        Args:
            content_data: Content information including text, media, platforms
            schedule_time: Optional specific time to schedule (ISO format)
            
        Returns:
            Dictionary containing scheduling results
        """
        try:
            platforms = content_data.get('platforms', [])
            content_text = content_data.get('content_text', '')
            media_urls = content_data.get('media_urls', [])
            
            if not platforms:
                return {
                    "success": False,
                    "error": "No platforms specified for scheduling"
                }
            
            scheduled_posts = []
            
            for platform in platforms:
                # Determine optimal posting time if not specified
                if not schedule_time:
                    optimal_time = self._get_next_optimal_time(platform)
                else:
                    optimal_time = schedule_time
                
                # Schedule post via Publer API (simulated)
                post_result = self._schedule_via_publer(
                    platform=platform,
                    content_text=content_text,
                    media_urls=media_urls,
                    schedule_time=optimal_time
                )
                
                if post_result['success']:
                    scheduled_posts.append({
                        "platform": platform,
                        "scheduled_time": optimal_time,
                        "post_id": post_result['post_id'],
                        "status": "scheduled"
                    })
                    
                    # Add to Google Calendar
                    self._add_to_calendar(platform, content_text, optimal_time)
                else:
                    scheduled_posts.append({
                        "platform": platform,
                        "error": post_result['error'],
                        "status": "failed"
                    })
            
            return {
                "success": True,
                "scheduled_posts": scheduled_posts,
                "total_scheduled": len([p for p in scheduled_posts if p.get('status') == 'scheduled']),
                "scheduled_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def schedule_bulk_content(self, content_list: List[Dict[str, Any]], 
                             distribution_strategy: str = "optimal") -> Dict[str, Any]:
        """
        Schedule multiple pieces of content with intelligent distribution.
        
        Args:
            content_list: List of content items to schedule
            distribution_strategy: Strategy for distributing content ("optimal", "even", "burst")
            
        Returns:
            Dictionary containing bulk scheduling results
        """
        try:
            results = []
            
            for i, content_data in enumerate(content_list):
                if distribution_strategy == "optimal":
                    # Schedule at optimal times for each platform
                    result = self.schedule_content(content_data)
                elif distribution_strategy == "even":
                    # Distribute evenly throughout the day
                    schedule_time = self._calculate_even_distribution_time(i, len(content_list))
                    result = self.schedule_content(content_data, schedule_time)
                elif distribution_strategy == "burst":
                    # Schedule in bursts with gaps
                    schedule_time = self._calculate_burst_time(i)
                    result = self.schedule_content(content_data, schedule_time)
                
                results.append(result)
            
            successful_schedules = [r for r in results if r.get('success')]
            
            return {
                "success": True,
                "total_content": len(content_list),
                "successful_schedules": len(successful_schedules),
                "failed_schedules": len(content_list) - len(successful_schedules),
                "results": results,
                "strategy_used": distribution_strategy
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def monitor_engagement(self, post_ids: List[str]) -> Dict[str, Any]:
        """
        Monitor engagement for specified posts and trigger alerts if spikes detected.
        
        Args:
            post_ids: List of post IDs to monitor
            
        Returns:
            Dictionary containing engagement monitoring results
        """
        try:
            engagement_data = []
            alerts_triggered = []
            
            for post_id in post_ids:
                # Get engagement metrics from Publer API (simulated)
                metrics = self._get_engagement_metrics(post_id)
                
                if metrics['success']:
                    engagement_data.append({
                        "post_id": post_id,
                        "metrics": metrics['data'],
                        "checked_at": datetime.utcnow().isoformat()
                    })
                    
                    # Check for engagement spikes
                    spike_detected = self._detect_engagement_spike(metrics['data'])
                    
                    if spike_detected:
                        alert_result = self._send_engagement_alert(post_id, metrics['data'])
                        alerts_triggered.append({
                            "post_id": post_id,
                            "spike_type": spike_detected,
                            "alert_sent": alert_result['success']
                        })
            
            return {
                "success": True,
                "monitored_posts": len(post_ids),
                "engagement_data": engagement_data,
                "alerts_triggered": alerts_triggered,
                "monitored_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def repost_high_performing_content(self, performance_threshold: float = 1.5) -> Dict[str, Any]:
        """
        Identify and repost high-performing content after specified period.
        
        Args:
            performance_threshold: Minimum performance multiplier to qualify for reposting
            
        Returns:
            Dictionary containing reposting results
        """
        try:
            # Get high-performing content from the last 2-3 weeks
            cutoff_date = datetime.utcnow() - timedelta(weeks=3)
            high_performers = self._get_high_performing_content(cutoff_date, performance_threshold)
            
            reposted_content = []
            
            for content in high_performers:
                # Modify content slightly for reposting
                modified_content = self._modify_content_for_repost(content)
                
                # Schedule repost
                repost_result = self.schedule_content(modified_content)
                
                if repost_result['success']:
                    reposted_content.append({
                        "original_post_id": content['post_id'],
                        "repost_result": repost_result,
                        "performance_score": content['performance_score']
                    })
            
            return {
                "success": True,
                "candidates_found": len(high_performers),
                "content_reposted": len(reposted_content),
                "reposted_content": reposted_content,
                "threshold_used": performance_threshold
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_posting_schedule(self, days_ahead: int = 7) -> Dict[str, Any]:
        """
        Get the current posting schedule for the next specified days.
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            Dictionary containing schedule information
        """
        try:
            # Simulate getting schedule from Publer API
            schedule = self._get_schedule_from_publer(days_ahead)
            
            return {
                "success": True,
                "schedule": schedule,
                "days_ahead": days_ahead,
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_next_optimal_time(self, platform: str) -> str:
        """Get the next optimal posting time for a platform."""
        optimal_hours = self.optimal_times.get(platform, [12])  # Default to noon
        now = datetime.utcnow()
        
        # Find next optimal hour
        for hour in optimal_hours:
            next_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if next_time > now:
                return next_time.isoformat()
        
        # If no optimal time today, use first optimal time tomorrow
        tomorrow = now + timedelta(days=1)
        next_time = tomorrow.replace(hour=optimal_hours[0], minute=0, second=0, microsecond=0)
        return next_time.isoformat()
    
    def _schedule_via_publer(self, platform: str, content_text: str, 
                           media_urls: List[str], schedule_time: str) -> Dict[str, Any]:
        """Schedule post via Publer API (simulated)."""
        # Simulate API call to Publer
        return {
            "success": True,
            "post_id": f"publer_{platform}_{datetime.utcnow().timestamp()}",
            "scheduled_time": schedule_time,
            "platform": platform
        }
    
    def _add_to_calendar(self, platform: str, content_text: str, schedule_time: str) -> bool:
        """Add scheduled post to Google Calendar."""
        # Simulate adding to Google Calendar
        # In production, this would use Google Calendar API
        return True
    
    def _get_engagement_metrics(self, post_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a post (simulated)."""
        # Simulate engagement metrics
        return {
            "success": True,
            "data": {
                "likes": 150,
                "comments": 25,
                "shares": 12,
                "saves": 8,
                "reach": 1200,
                "impressions": 2500
            }
        }
    
    def _detect_engagement_spike(self, metrics: Dict[str, Any]) -> Optional[str]:
        """Detect if there's an engagement spike."""
        # Simulate spike detection logic
        # In production, this would compare against historical averages
        if metrics.get('likes', 0) > 200:  # Simplified threshold
            return "likes_spike"
        return None
    
    def _send_engagement_alert(self, post_id: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Send WhatsApp alert for engagement spike."""
        try:
            message = f"🚀 Engagement spike detected!\n\nPost ID: {post_id}\nLikes: {metrics.get('likes', 0)}\nComments: {metrics.get('comments', 0)}\nShares: {metrics.get('shares', 0)}"
            
            # Simulate sending WhatsApp message via Twilio
            # In production, this would use Twilio WhatsApp API
            return {
                "success": True,
                "message_sent": True,
                "alert_time": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_high_performing_content(self, cutoff_date: datetime, 
                                   threshold: float) -> List[Dict[str, Any]]:
        """Get high-performing content for reposting."""
        # Simulate getting high-performing content
        return [
            {
                "post_id": "high_performer_1",
                "content_text": "Amazing digital art showcase",
                "platforms": ["instagram"],
                "performance_score": 2.1,
                "original_date": cutoff_date.isoformat()
            }
        ]
    
    def _modify_content_for_repost(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Modify content slightly for reposting."""
        modified = content.copy()
        modified['content_text'] = f"🔄 {content['content_text']} #ThrowbackThursday"
        return modified
    
    def _calculate_even_distribution_time(self, index: int, total: int) -> str:
        """Calculate evenly distributed posting time."""
        hours_span = 12  # Distribute over 12 hours
        interval = hours_span / total
        target_hour = 8 + (index * interval)  # Start at 8 AM
        
        target_time = datetime.utcnow().replace(
            hour=int(target_hour), 
            minute=int((target_hour % 1) * 60),
            second=0,
            microsecond=0
        )
        
        return target_time.isoformat()
    
    def _calculate_burst_time(self, index: int) -> str:
        """Calculate burst posting time."""
        # Post in bursts of 3 with 2-hour gaps
        burst_group = index // 3
        burst_position = index % 3
        
        base_hour = 9 + (burst_group * 2)  # 2-hour gaps between bursts
        target_hour = base_hour + (burst_position * 0.5)  # 30-minute intervals within burst
        
        target_time = datetime.utcnow().replace(
            hour=int(target_hour),
            minute=int((target_hour % 1) * 60),
            second=0,
            microsecond=0
        )
        
        return target_time.isoformat()
    
    def _get_schedule_from_publer(self, days_ahead: int) -> List[Dict[str, Any]]:
        """Get posting schedule from Publer API (simulated)."""
        schedule = []
        
        for day in range(days_ahead):
            date = datetime.utcnow() + timedelta(days=day)
            
            # Simulate scheduled posts for each day
            for platform in ["instagram", "tiktok", "x"]:
                for time_slot in self.optimal_times.get(platform, [12])[:2]:  # Max 2 posts per platform
                    schedule.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "time": f"{time_slot:02d}:00",
                        "platform": platform,
                        "content_preview": f"Scheduled {platform} post",
                        "status": "scheduled"
                    })
        
        return schedule

