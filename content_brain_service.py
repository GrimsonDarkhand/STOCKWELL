import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

class ContentBrainService:
    """
    Service class for the Content Brain module.
    Handles content generation and repurposing using AI models.
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.openai_base_url = "https://api.openai.com/v1"
        
        # Brand voice and style guidelines for ART MAZE
        self.brand_voice = {
            "tone": "creative, inspiring, authentic",
            "style": "contemporary art focused, community-driven",
            "hashtags": ["#ArtMaze", "#ContemporaryArt", "#ArtCommunity", "#CreativeExpression"],
            "website": "amazedigimag.wordpress.com",
            "cta_examples": [
                "Read more at amazedigimag.wordpress.com",
                "Join our creative community",
                "Discover more artists",
                "Share your art with us"
            ]
        }
    
    def generate_content(self, prompt: str, content_type: str, platform: str, 
                        source_material: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate new content based on prompt and requirements.
        
        Args:
            prompt: User prompt or theme
            content_type: Type of content (caption, post, thread, meme, reel)
            platform: Target platform (instagram, tiktok, x, facebook, etc.)
            source_material: Optional source material to reference
            
        Returns:
            Dictionary containing generated content
        """
        try:
            # Choose AI model based on content type and requirements
            if content_type in ['reel', 'meme'] or source_material:
                # Use Gemini for multimodal content
                return self._generate_with_gemini(prompt, content_type, platform, source_material)
            else:
                # Use GPT-4.5 for text-heavy content
                return self._generate_with_openai(prompt, content_type, platform)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def repurpose_content(self, original_content: str, target_platform: str, 
                         target_format: str) -> Dict[str, Any]:
        """
        Repurpose existing content for a different platform or format.
        
        Args:
            original_content: The original content to repurpose
            target_platform: Target platform for repurposed content
            target_format: Target format (caption, post, thread, etc.)
            
        Returns:
            Dictionary containing repurposed content
        """
        try:
            prompt = f"""
            Repurpose the following content for {target_platform} as a {target_format}.
            
            Original content: {original_content}
            
            Requirements:
            - Adapt the tone and style for {target_platform}
            - Maintain the core message and value
            - Include appropriate hashtags for {target_platform}
            - Add a call-to-action linking to amazedigimag.wordpress.com
            - Keep the ART MAZE brand voice: {self.brand_voice['tone']}
            """
            
            return self._generate_with_openai(prompt, target_format, target_platform)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def _generate_with_gemini(self, prompt: str, content_type: str, platform: str, 
                             source_material: Optional[str] = None) -> Dict[str, Any]:
        """Generate content using Google Gemini 1.5 Pro."""
        if not self.gemini_api_key:
            return {
                "success": False,
                "error": "Gemini API key not configured",
                "content": None
            }
        
        # Construct the prompt with brand guidelines
        system_prompt = f"""
        You are the Content Brain for ART MAZE, a contemporary art magazine.
        
        Brand Voice: {self.brand_voice['tone']}
        Style: {self.brand_voice['style']}
        Website: {self.brand_voice['website']}
        
        Generate a {content_type} for {platform} based on the following prompt.
        Include relevant hashtags and a call-to-action.
        """
        
        full_prompt = f"{system_prompt}\n\nPrompt: {prompt}"
        if source_material:
            full_prompt += f"\n\nSource Material: {source_material}"
        
        # Simulate Gemini API call (replace with actual API call)
        content = self._simulate_ai_response(full_prompt, content_type, platform)
        
        return {
            "success": True,
            "content": content,
            "model_used": "gemini-1.5-pro",
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _generate_with_openai(self, prompt: str, content_type: str, platform: str) -> Dict[str, Any]:
        """Generate content using OpenAI GPT-4.5."""
        if not self.openai_api_key:
            return {
                "success": False,
                "error": "OpenAI API key not configured",
                "content": None
            }
        
        # Construct the prompt with brand guidelines
        system_prompt = f"""
        You are the Content Brain for ART MAZE, a contemporary art magazine.
        
        Brand Voice: {self.brand_voice['tone']}
        Style: {self.brand_voice['style']}
        Website: {self.brand_voice['website']}
        
        Generate a {content_type} for {platform}.
        Include relevant hashtags from: {', '.join(self.brand_voice['hashtags'])}
        Add an appropriate call-to-action.
        """
        
        # Simulate OpenAI API call (replace with actual API call)
        content = self._simulate_ai_response(f"{system_prompt}\n\n{prompt}", content_type, platform)
        
        return {
            "success": True,
            "content": content,
            "model_used": "gpt-4.5",
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _simulate_ai_response(self, prompt: str, content_type: str, platform: str) -> Dict[str, str]:
        """
        Simulate AI response for development/testing purposes.
        Replace this with actual API calls in production.
        """
        
        # Platform-specific content templates
        templates = {
            "instagram": {
                "caption": "🎨 {content} ✨\n\n{hashtags}\n\n{cta}",
                "post": "{content}\n\n{hashtags}\n\n{cta}",
                "reel": "🎬 {content}\n\n{hashtags}\n\n{cta}"
            },
            "tiktok": {
                "caption": "{content} 🔥\n\n{hashtags}",
                "reel": "{content}\n\n{hashtags}"
            },
            "x": {
                "post": "{content}\n\n{hashtags}\n\n{cta}",
                "thread": "🧵 {content}\n\n{hashtags}\n\n{cta}"
            },
            "facebook": {
                "post": "{content}\n\n{hashtags}\n\n{cta}"
            }
        }
        
        # Sample content based on type
        sample_content = {
            "caption": "Exploring the intersection of digital art and human emotion in today's contemporary landscape",
            "post": "The power of art lies in its ability to transform perspectives and challenge conventional thinking. Today's featured artist demonstrates this beautifully through their innovative approach to mixed media.",
            "thread": "1/ Art has always been a reflection of society's evolution. In our digital age, artists are finding new ways to express timeless themes through contemporary mediums.",
            "reel": "Watch as this artist transforms ordinary materials into extraordinary expressions of creativity",
            "meme": "When you finally understand that abstract piece you've been staring at for 20 minutes"
        }
        
        content_text = sample_content.get(content_type, "Creative content for ART MAZE community")
        hashtags = " ".join(self.brand_voice['hashtags'][:3])
        cta = "Discover more at amazedigimag.wordpress.com"
        
        template = templates.get(platform, {}).get(content_type, "{content}\n\n{hashtags}\n\n{cta}")
        
        formatted_content = template.format(
            content=content_text,
            hashtags=hashtags,
            cta=cta
        )
        
        return {
            "text": formatted_content,
            "hashtags": hashtags,
            "call_to_action": cta,
            "media_suggestions": self._get_media_suggestions(content_type, platform)
        }
    
    def _get_media_suggestions(self, content_type: str, platform: str) -> List[str]:
        """Get media suggestions based on content type and platform."""
        suggestions = {
            "reel": ["video", "animation", "timelapse"],
            "meme": ["image", "graphic", "illustration"],
            "caption": ["photo", "artwork", "gallery_image"],
            "post": ["photo", "artwork", "infographic"],
            "thread": ["carousel", "infographic", "photo_series"]
        }
        
        return suggestions.get(content_type, ["image"])
    
    def get_content_suggestions(self, theme: str) -> List[Dict[str, str]]:
        """Get content suggestions based on a theme."""
        suggestions = [
            {
                "type": "instagram_post",
                "title": f"Featured Artist: {theme}",
                "description": "Showcase an artist working in this theme"
            },
            {
                "type": "tiktok_reel",
                "title": f"{theme} Process Video",
                "description": "Behind-the-scenes creation process"
            },
            {
                "type": "x_thread",
                "title": f"The History of {theme}",
                "description": "Educational thread about the theme"
            },
            {
                "type": "facebook_post",
                "title": f"Community Spotlight: {theme}",
                "description": "Highlight community members working in this area"
            }
        ]
        
        return suggestions

