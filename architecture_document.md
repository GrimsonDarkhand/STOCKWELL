# MAZEBOT // POSTMASTER - Architectural Design Document

## 1. Introduction

This document outlines the architectural design and data flow for the MAZEBOT // POSTMASTER system. The system is designed to autonomously manage, create, schedule, and publish multimedia content across various social media platforms, repurpose existing material, and redirect high-priority messages or comments. The architecture leverages a modular approach, integrating various specialized tools and APIs orchestrated by Make.com to ensure efficiency, scalability, and maintainability.

## 2. Core Principles

*   **Modularity**: The system is broken down into distinct functional modules, each responsible for a specific set of tasks. This promotes reusability, simplifies development, and allows for independent updates or replacements of components.
*   **Automation-Centric**: Make.com serves as the central orchestration layer, enabling seamless data flow and automated workflows between different services and APIs.
*   **Scalability**: The architecture is designed to handle increasing volumes of content and social media interactions by leveraging cloud-based services and APIs.
*   **Data Flow Transparency**: Clear definitions of data inputs, outputs, and transformations between modules ensure a comprehensive understanding of the system's operations.
*   **User-Centric Control**: While autonomous, the system provides mechanisms for user oversight, input, and redirection of critical information.

## 3. Overall Architecture Diagram

```mermaid
graph TD
    A[User Input/Existing Content] --> B{Content Brain}
    B --> C[Content Queue/Asset Manager]
    C --> D{Postmaster Scheduler}
    D --> E[Social Media Platforms]
    D --> F[Google Calendar]
    E --> G{CommentRadar}
    G --> H[WhatsApp (User)]
    C --> I{MailMaze}
    I --> J[Email List (Mailchimp)]
    E --> K{Analytics Brain}
    J --> K
    K --> L[Google Sheets]
    L --> A
    G --> A
    H --> A

    subgraph Core Automation (Make.com)
        B -- API Calls --> M[Gemini 1.5 Pro / GPT-4.5]
        D -- API Calls --> N[Publer]
        I -- API Calls --> O[Mailchimp]
        G -- API Calls --> P[Meta API / X API / Twilio]
        C -- API Calls --> Q[Google Drive]
        K -- API Calls --> R[Publer / Mailchimp / Google Sheets]
    end

    M --> B
    N --> D
    O --> I
    P --> G
    Q --> C
    R --> K

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#f9f,stroke:#333,stroke-width:2px
    style I fill:#bbf,stroke:#333,stroke-width:2px
    style J fill:#f9f,stroke:#333,stroke-width:2px
    style K fill:#bbf,stroke:#333,stroke-width:2px
    style L fill:#f9f,stroke:#333,stroke-width:2px
    style M fill:#ccf,stroke:#333,stroke-width:1px
    style N fill:#ccf,stroke:#333,stroke-width:1px
    style O fill:#ccf,stroke:#333,stroke-width:1px
    style P fill:#ccf,stroke:#333,stroke-width:1px
    style Q fill:#ccf,stroke:#333,stroke-width:1px
    style R fill:#ccf,stroke:#333,stroke-width:1px
```

## 4. Data Flow and Module Interactions

### 4.1. Content Brain (Creation & Repurposing Engine)

*   **Inputs**: Past magazine content (PDFs, articles, posts) from Google Drive (Asset Manager), user-defined prompts/themes, current week’s promotion goals.
*   **Process**: Make.com orchestrates calls to Google Gemini 1.5 Pro and OpenAI GPT-4.5 APIs. Gemini 1.5 Pro analyzes and summarizes long-form content (PDFs, articles) and extracts key information. GPT-4.5 generates various content formats (captions, tweet threads, carousel text, AI-generated posts) based on the extracted information and user prompts. For visual content repurposing (reels, memes), Gemini 1.5 Pro's multimodal capabilities are leveraged to understand existing video/image assets and guide the generation of new visual content.
*   **Outputs**: Generated captions, repurposed reels, AI-generated posts, carousel post text, tweet threads, meme formats. These outputs are then pushed to the Content Queue/Asset Manager.

### 4.2. Asset Manager

*   **Inputs**: Newly generated content from the Content Brain, existing brand assets (visuals, audio) from Google Drive.
*   **Process**: This module primarily interacts with Google Drive via Make.com. It stores and organizes all content and assets. It also serves as a central repository for the 


Content Brain and other modules to retrieve necessary assets.
*   **Outputs**: Organized and accessible content and assets for other modules.

### 4.3. Postmaster Scheduler (Auto Publishing Engine)

*   **Inputs**: Content from the Content Queue/Asset Manager.
*   **Process**: Make.com pulls content from the Asset Manager. It then uses Publer API to schedule posts across various social media platforms (Instagram, TikTok, Threads, X, Facebook, Medium). The scheduling logic within Make.com determines the best posting times per platform, based on predefined rules or insights from the Analytics Brain. It also manages automatic reposting of high-performing content after a specified period (e.g., 2-3 weeks). Google Calendar API is used to log scheduled posts for user oversight. Make.com also monitors engagement metrics (via Publer or direct social media APIs) and sends WhatsApp alerts via Twilio if engagement spikes, as defined by the CommentRadar module.
*   **Outputs**: Scheduled social media posts, updated Google Calendar entries, WhatsApp alerts for engagement spikes.

### 4.4. MailMaze (Email Composer & Blaster)

*   **Inputs**: Curated content from the Content Queue/Asset Manager (e.g., weekly digest content).
*   **Process**: Make.com retrieves relevant content for the weekly digest from the Asset Manager. It then interacts with the Mailchimp API to compose and send weekly digest-style emails to the user's email list. The system ensures the tone and voice match the ART MAZE brand. Mailchimp handles the actual email blasting and provides tracking for opens, clicks, and forwards. Make.com can also be configured to send previews of upcoming issues or community features.
*   **Outputs**: Sent weekly digest emails, email campaign performance data (tracked by Mailchimp).

### 4.5. CommentRadar (Engagement Redirector)

*   **Inputs**: Real-time comments and messages from various social media platforms (Facebook, Instagram, X, Threads).
*   **Process**: Make.com continuously monitors incoming comments and messages via Meta API, X/Threads API, and potentially other social media APIs. It applies filtering logic to identify high-priority messages (e.g., sales inquiries, urgent questions) and flags trolls/spam. High-priority messages are immediately redirected to the user's WhatsApp via Twilio (using the WhatsApp Business API) as webhooks. For frequently asked questions, Make.com triggers auto-responses using predefined saved replies. This module is critical for ensuring timely and effective engagement with the audience.
*   **Outputs**: Redirected high-priority messages to WhatsApp, auto-responses to FAQs, flagged trolls/spam for review.

### 4.6. Analytics Brain

*   **Inputs**: Performance data from Publer (social media analytics), Mailchimp (email campaign analytics), and potentially other sources.
*   **Process**: Make.com pulls weekly reports from Publer (top-performing content, follower growth, engagement spikes) and Mailchimp (opens, clicks, forwards). This data is then aggregated and pushed into Google Sheets for comprehensive analysis. The Analytics Brain, through Make.com, can be configured to generate insights and suggest actions, such as which content to boost or repost, based on predefined metrics and thresholds. This module provides the feedback loop necessary for continuous optimization of content strategy.
*   **Outputs**: Weekly performance reports in Google Sheets, insights and suggestions for content optimization.

## 5. Automation Flow Examples (Orchestrated by Make.com)

### 5.1. Daily Content Publishing

1.  **Trigger**: Daily at 7:30 AM (scheduled in Make.com).
2.  **Action - Content Selection**: Make.com selects content from the Content Queue/Asset Manager based on the weekly theme or archives.
3.  **Action - Content Generation (if needed)**: If new content is required, Make.com triggers the Content Brain (Gemini 1.5 Pro / GPT-4.5) to generate captions and select appropriate assets.
4.  **Action - Scheduling**: Make.com sends the content and captions to Publer via API. Publer then schedules the post for Instagram, Threads, and X, optimizing for best times per platform.

### 5.2. Daily Engagement Monitoring

1.  **Trigger**: Daily at 1:00 PM (scheduled in Make.com).
2.  **Action - Data Pull**: Make.com pulls post comments and DMs from Meta API and X/Threads API.
3.  **Action - Filtering**: Make.com filters messages for high-priority interactions (e.g., sales inquiries) and flags trolls/spam.
4.  **Action - Redirection/Auto-response**: High-priority messages are sent to the user via WhatsApp (Twilio). Auto-responses are triggered for FAQs.

### 5.3. Weekly Email Digest

1.  **Trigger**: Weekly on Sunday (scheduled in Make.com).
2.  **Action - Content Compilation**: Make.com compiles content for the weekly digest from the Content Queue/Asset Manager.
3.  **Action - Email Draft Generation**: Make.com interacts with Mailchimp API to auto-generate an email draft.
4.  **Action - Campaign Queuing**: The email campaign is queued in Mailchimp for Monday send.

### 5.4. On-Demand Content Repurposing

1.  **Trigger**: User input (e.g., via a simple form or direct message to Make.com webhook).
2.  **Action - Prompt Processing**: Make.com receives a prompt like 


"Repurpose Week 2 WhatsApp post for TikTok".
3.  **Action - Content Brain Execution**: Make.com triggers the Content Brain (Gemini 1.5 Pro / GPT-4.5) to process the request, accessing the original content from the Asset Manager.
4.  **Output**: The Content Brain returns a new video (or instructions for creating one) and a caption optimized for TikTok, which can then be delivered to the user or pushed to the Postmaster Scheduler.

## 6. Security Considerations

*   **API Key Management**: All API keys for Google Gemini, GPT-4.5, Publer, Mailchimp, Twilio, and Google services will be securely stored and managed within Make.com, leveraging its built-in credential management features. Direct exposure of API keys in code or public repositories will be avoided.
*   **Data Privacy**: User data and content will be handled in accordance with relevant data privacy regulations. Access to sensitive information will be restricted to authorized modules and personnel.
*   **Authentication**: Secure authentication mechanisms will be implemented for all user-facing interactions and API calls.
*   **Input Validation**: All inputs to the system, especially those from external sources or user prompts, will be validated to prevent injection attacks or malformed data processing.

## 7. Future Enhancements

*   **Visual Remixing Integration**: Explore integration with advanced visual remixing tools like RunwayML or Pika Labs for more sophisticated video and image generation, potentially as an extension to the Content Brain.
*   **Community Content Publishing**: Develop a Discord server bot to facilitate the publishing of community-generated content, integrating with the Postmaster Scheduler.
*   **WhatsApp Autoresponder AI Agent**: Enhance the CommentRadar with a more sophisticated AI agent for WhatsApp auto-responses, capable of handling more complex queries and maintaining conversational context.
*   **Voice Note Responder**: Implement a voice note responder for DMs, leveraging speech-to-text and text-to-speech capabilities to provide audio replies.
*   **Advanced Analytics & Reporting**: Develop custom dashboards and more in-depth reporting within Google Sheets or a dedicated BI tool, leveraging the aggregated data from the Analytics Brain.
*   **Dynamic Content Optimization**: Implement machine learning models within the Analytics Brain to dynamically adjust posting schedules and content types based on real-time engagement data.

---

**Author**: Manus AI
**Date**: June 17, 2025


