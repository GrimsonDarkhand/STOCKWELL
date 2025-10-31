import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class MailMazeService:
    """
    Service class for the MailMaze module.
    Handles email composition, sending, and campaign management.
    """
    
    def __init__(self):
        self.mailchimp_api_key = os.getenv('MAILCHIMP_API_KEY')
        self.mailchimp_server = os.getenv('MAILCHIMP_SERVER', 'us1')  # e.g., us1, us2, etc.
        self.mailchimp_list_id = os.getenv('MAILCHIMP_LIST_ID')
        self.mailchimp_base_url = f"https://{self.mailchimp_server}.api.mailchimp.com/3.0"
        
        # Email template configurations
        self.email_templates = {
            "weekly_digest": {
                "subject_template": "🎨 ART MAZE Weekly Digest - {week_theme}",
                "from_name": "ART MAZE",
                "from_email": "hello@amazedigimag.wordpress.com",
                "template_sections": [
                    "header",
                    "featured_content",
                    "community_highlights", 
                    "upcoming_events",
                    "artist_spotlight",
                    "footer"
                ]
            },
            "community_feature": {
                "subject_template": "🌟 Community Feature: {artist_name}",
                "from_name": "ART MAZE",
                "from_email": "hello@amazedigimag.wordpress.com"
            },
            "event_announcement": {
                "subject_template": "📅 Upcoming: {event_name}",
                "from_name": "ART MAZE",
                "from_email": "hello@amazedigimag.wordpress.com"
            }
        }
        
        # Brand styling for emails
        self.brand_styling = {
            "primary_color": "#2C3E50",
            "secondary_color": "#E74C3C",
            "accent_color": "#F39C12",
            "font_family": "Arial, sans-serif",
            "website_url": "https://amazedigimag.wordpress.com",
            "social_links": {
                "instagram": "https://instagram.com/artmaze",
                "tiktok": "https://tiktok.com/@artmaze",
                "x": "https://x.com/artmaze"
            }
        }
    
    def compose_weekly_digest(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compose a weekly digest email from provided content.
        
        Args:
            content_data: Dictionary containing content for different sections
            
        Returns:
            Dictionary containing composed email data
        """
        try:
            week_theme = content_data.get('theme', 'Creative Expressions')
            featured_content = content_data.get('featured_content', [])
            community_highlights = content_data.get('community_highlights', [])
            upcoming_events = content_data.get('upcoming_events', [])
            artist_spotlight = content_data.get('artist_spotlight', {})
            
            # Generate email subject
            subject = self.email_templates['weekly_digest']['subject_template'].format(
                week_theme=week_theme
            )
            
            # Compose email HTML content
            html_content = self._generate_weekly_digest_html(
                theme=week_theme,
                featured_content=featured_content,
                community_highlights=community_highlights,
                upcoming_events=upcoming_events,
                artist_spotlight=artist_spotlight
            )
            
            # Generate plain text version
            text_content = self._generate_weekly_digest_text(
                theme=week_theme,
                featured_content=featured_content,
                community_highlights=community_highlights,
                upcoming_events=upcoming_events,
                artist_spotlight=artist_spotlight
            )
            
            return {
                "success": True,
                "email_data": {
                    "subject": subject,
                    "html_content": html_content,
                    "text_content": text_content,
                    "from_name": self.email_templates['weekly_digest']['from_name'],
                    "from_email": self.email_templates['weekly_digest']['from_email'],
                    "template_type": "weekly_digest"
                },
                "composed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_campaign(self, email_data: Dict[str, Any], 
                     send_immediately: bool = False) -> Dict[str, Any]:
        """
        Send email campaign via Mailchimp.
        
        Args:
            email_data: Email content and configuration
            send_immediately: Whether to send immediately or schedule
            
        Returns:
            Dictionary containing campaign results
        """
        try:
            # Create campaign in Mailchimp (simulated)
            campaign_result = self._create_mailchimp_campaign(email_data)
            
            if not campaign_result['success']:
                return campaign_result
            
            campaign_id = campaign_result['campaign_id']
            
            if send_immediately:
                # Send campaign immediately
                send_result = self._send_mailchimp_campaign(campaign_id)
                
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "status": "sent" if send_result['success'] else "failed",
                    "sent_at": datetime.utcnow().isoformat() if send_result['success'] else None,
                    "error": send_result.get('error')
                }
            else:
                # Schedule for later (default: next Monday at 9 AM)
                schedule_time = self._get_next_monday_9am()
                schedule_result = self._schedule_mailchimp_campaign(campaign_id, schedule_time)
                
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "status": "scheduled",
                    "scheduled_for": schedule_time.isoformat(),
                    "error": schedule_result.get('error')
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_campaign_analytics(self, campaign_id: str) -> Dict[str, Any]:
        """
        Get analytics for a specific email campaign.
        
        Args:
            campaign_id: Mailchimp campaign ID
            
        Returns:
            Dictionary containing campaign analytics
        """
        try:
            # Get analytics from Mailchimp API (simulated)
            analytics = self._get_mailchimp_analytics(campaign_id)
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "analytics": analytics,
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def manage_subscribers(self, action: str, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manage email subscribers (add, remove, update).
        
        Args:
            action: Action to perform ('add', 'remove', 'update')
            email_data: Subscriber information
            
        Returns:
            Dictionary containing operation results
        """
        try:
            if action == 'add':
                result = self._add_subscriber(email_data)
            elif action == 'remove':
                result = self._remove_subscriber(email_data['email'])
            elif action == 'update':
                result = self._update_subscriber(email_data)
            else:
                return {
                    "success": False,
                    "error": f"Invalid action: {action}"
                }
            
            return {
                "success": True,
                "action": action,
                "result": result,
                "processed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_subscriber_analytics(self) -> Dict[str, Any]:
        """Get subscriber list analytics."""
        try:
            analytics = self._get_subscriber_analytics()
            
            return {
                "success": True,
                "analytics": analytics,
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def preview_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate email preview for testing.
        
        Args:
            email_data: Email content and configuration
            
        Returns:
            Dictionary containing preview data
        """
        try:
            return {
                "success": True,
                "preview": {
                    "subject": email_data.get('subject'),
                    "from": f"{email_data.get('from_name')} <{email_data.get('from_email')}>",
                    "html_preview": email_data.get('html_content', '')[:500] + "...",
                    "text_preview": email_data.get('text_content', '')[:500] + "...",
                    "estimated_send_time": self._estimate_send_time()
                },
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_weekly_digest_html(self, theme: str, featured_content: List[Dict], 
                                   community_highlights: List[Dict], 
                                   upcoming_events: List[Dict],
                                   artist_spotlight: Dict) -> str:
        """Generate HTML content for weekly digest."""
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ART MAZE Weekly Digest</title>
            <style>
                body {{ font-family: {self.brand_styling['font_family']}; margin: 0; padding: 0; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                .header {{ background-color: {self.brand_styling['primary_color']}; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ color: {self.brand_styling['primary_color']}; border-bottom: 2px solid {self.brand_styling['secondary_color']}; padding-bottom: 10px; }}
                .featured-item {{ background-color: #f9f9f9; padding: 15px; margin-bottom: 15px; border-left: 4px solid {self.brand_styling['accent_color']}; }}
                .footer {{ background-color: {self.brand_styling['primary_color']}; color: white; padding: 20px; text-align: center; }}
                .social-links a {{ color: white; text-decoration: none; margin: 0 10px; }}
                .cta-button {{ background-color: {self.brand_styling['secondary_color']}; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎨 ART MAZE</h1>
                    <p>Weekly Digest - {theme}</p>
                </div>
                
                <div class="content">
                    <div class="section">
                        <h2>✨ Featured Content</h2>
                        {self._format_featured_content_html(featured_content)}
                    </div>
                    
                    <div class="section">
                        <h2>🌟 Community Highlights</h2>
                        {self._format_community_highlights_html(community_highlights)}
                    </div>
                    
                    <div class="section">
                        <h2>🎭 Artist Spotlight</h2>
                        {self._format_artist_spotlight_html(artist_spotlight)}
                    </div>
                    
                    <div class="section">
                        <h2>📅 Upcoming Events</h2>
                        {self._format_upcoming_events_html(upcoming_events)}
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.brand_styling['website_url']}" class="cta-button">Visit ART MAZE</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Follow us on social media:</p>
                    <div class="social-links">
                        <a href="{self.brand_styling['social_links']['instagram']}">Instagram</a>
                        <a href="{self.brand_styling['social_links']['tiktok']}">TikTok</a>
                        <a href="{self.brand_styling['social_links']['x']}">X (Twitter)</a>
                    </div>
                    <p style="margin-top: 20px; font-size: 12px;">
                        You're receiving this because you subscribed to ART MAZE updates.<br>
                        <a href="#" style="color: white;">Unsubscribe</a> | <a href="#" style="color: white;">Update Preferences</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _generate_weekly_digest_text(self, theme: str, featured_content: List[Dict], 
                                   community_highlights: List[Dict], 
                                   upcoming_events: List[Dict],
                                   artist_spotlight: Dict) -> str:
        """Generate plain text content for weekly digest."""
        
        text_content = f"""
ART MAZE Weekly Digest - {theme}
{'=' * 50}

✨ FEATURED CONTENT
{self._format_featured_content_text(featured_content)}

🌟 COMMUNITY HIGHLIGHTS  
{self._format_community_highlights_text(community_highlights)}

🎭 ARTIST SPOTLIGHT
{self._format_artist_spotlight_text(artist_spotlight)}

📅 UPCOMING EVENTS
{self._format_upcoming_events_text(upcoming_events)}

Visit us at: {self.brand_styling['website_url']}

Follow us:
Instagram: {self.brand_styling['social_links']['instagram']}
TikTok: {self.brand_styling['social_links']['tiktok']}
X: {self.brand_styling['social_links']['x']}

---
You're receiving this because you subscribed to ART MAZE updates.
To unsubscribe or update preferences, visit our website.
        """
        
        return text_content.strip()
    
    def _format_featured_content_html(self, content: List[Dict]) -> str:
        """Format featured content for HTML email."""
        if not content:
            return "<p>No featured content this week.</p>"
        
        html = ""
        for item in content[:3]:  # Limit to 3 items
            html += f"""
            <div class="featured-item">
                <h3>{item.get('title', 'Untitled')}</h3>
                <p>{item.get('description', 'No description available.')}</p>
                <a href="{item.get('url', '#')}">Read More</a>
            </div>
            """
        return html
    
    def _format_community_highlights_html(self, highlights: List[Dict]) -> str:
        """Format community highlights for HTML email."""
        if not highlights:
            return "<p>No community highlights this week.</p>"
        
        html = ""
        for highlight in highlights[:2]:  # Limit to 2 items
            html += f"""
            <div class="featured-item">
                <h4>{highlight.get('title', 'Community Feature')}</h4>
                <p>{highlight.get('description', 'Amazing work from our community!')}</p>
            </div>
            """
        return html
    
    def _format_artist_spotlight_html(self, spotlight: Dict) -> str:
        """Format artist spotlight for HTML email."""
        if not spotlight:
            return "<p>No artist spotlight this week.</p>"
        
        return f"""
        <div class="featured-item">
            <h3>{spotlight.get('name', 'Featured Artist')}</h3>
            <p><strong>Medium:</strong> {spotlight.get('medium', 'Mixed Media')}</p>
            <p>{spotlight.get('bio', 'Talented artist creating amazing work.')}</p>
            <a href="{spotlight.get('portfolio_url', '#')}">View Portfolio</a>
        </div>
        """
    
    def _format_upcoming_events_html(self, events: List[Dict]) -> str:
        """Format upcoming events for HTML email."""
        if not events:
            return "<p>No upcoming events.</p>"
        
        html = ""
        for event in events[:2]:  # Limit to 2 events
            html += f"""
            <div class="featured-item">
                <h4>{event.get('name', 'Art Event')}</h4>
                <p><strong>Date:</strong> {event.get('date', 'TBA')}</p>
                <p>{event.get('description', 'Exciting art event coming up!')}</p>
            </div>
            """
        return html
    
    def _format_featured_content_text(self, content: List[Dict]) -> str:
        """Format featured content for plain text email."""
        if not content:
            return "No featured content this week."
        
        text = ""
        for i, item in enumerate(content[:3], 1):
            text += f"{i}. {item.get('title', 'Untitled')}\n"
            text += f"   {item.get('description', 'No description available.')}\n"
            text += f"   Link: {item.get('url', 'N/A')}\n\n"
        return text
    
    def _format_community_highlights_text(self, highlights: List[Dict]) -> str:
        """Format community highlights for plain text email."""
        if not highlights:
            return "No community highlights this week."
        
        text = ""
        for i, highlight in enumerate(highlights[:2], 1):
            text += f"{i}. {highlight.get('title', 'Community Feature')}\n"
            text += f"   {highlight.get('description', 'Amazing work from our community!')}\n\n"
        return text
    
    def _format_artist_spotlight_text(self, spotlight: Dict) -> str:
        """Format artist spotlight for plain text email."""
        if not spotlight:
            return "No artist spotlight this week."
        
        return f"""
{spotlight.get('name', 'Featured Artist')}
Medium: {spotlight.get('medium', 'Mixed Media')}
{spotlight.get('bio', 'Talented artist creating amazing work.')}
Portfolio: {spotlight.get('portfolio_url', 'N/A')}
        """.strip()
    
    def _format_upcoming_events_text(self, events: List[Dict]) -> str:
        """Format upcoming events for plain text email."""
        if not events:
            return "No upcoming events."
        
        text = ""
        for i, event in enumerate(events[:2], 1):
            text += f"{i}. {event.get('name', 'Art Event')}\n"
            text += f"   Date: {event.get('date', 'TBA')}\n"
            text += f"   {event.get('description', 'Exciting art event coming up!')}\n\n"
        return text
    
    def _create_mailchimp_campaign(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create campaign in Mailchimp (simulated)."""
        # Simulate Mailchimp API call
        return {
            "success": True,
            "campaign_id": f"mc_campaign_{datetime.utcnow().timestamp()}"
        }
    
    def _send_mailchimp_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Send Mailchimp campaign (simulated)."""
        return {"success": True}
    
    def _schedule_mailchimp_campaign(self, campaign_id: str, schedule_time: datetime) -> Dict[str, Any]:
        """Schedule Mailchimp campaign (simulated)."""
        return {"success": True}
    
    def _get_mailchimp_analytics(self, campaign_id: str) -> Dict[str, Any]:
        """Get Mailchimp campaign analytics (simulated)."""
        return {
            "emails_sent": 1247,
            "opens": 312,
            "clicks": 89,
            "open_rate": 25.02,
            "click_rate": 7.14,
            "unsubscribes": 3,
            "bounces": 12
        }
    
    def _add_subscriber(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add subscriber to Mailchimp list (simulated)."""
        return {"success": True, "subscriber_id": f"sub_{datetime.utcnow().timestamp()}"}
    
    def _remove_subscriber(self, email: str) -> Dict[str, Any]:
        """Remove subscriber from Mailchimp list (simulated)."""
        return {"success": True}
    
    def _update_subscriber(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update subscriber in Mailchimp list (simulated)."""
        return {"success": True}
    
    def _get_subscriber_analytics(self) -> Dict[str, Any]:
        """Get subscriber analytics (simulated)."""
        return {
            "total_subscribers": 1247,
            "subscribed": 1198,
            "unsubscribed": 49,
            "cleaned": 0,
            "pending": 0,
            "growth_rate": 5.2,
            "avg_open_rate": 24.8,
            "avg_click_rate": 6.9
        }
    
    def _get_next_monday_9am(self) -> datetime:
        """Get next Monday at 9 AM for scheduling."""
        now = datetime.utcnow()
        days_ahead = 0 - now.weekday()  # Monday is 0
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        
        next_monday = now + timedelta(days=days_ahead)
        return next_monday.replace(hour=9, minute=0, second=0, microsecond=0)
    
    def _estimate_send_time(self) -> str:
        """Estimate email send time."""
        return "Approximately 15-30 minutes for full list delivery"

