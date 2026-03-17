"""Seed data for PromptLab — populates initial collections and prompts."""

from app.models import Collection, Prompt, get_current_time
from app.storage import storage


def seed_data():
    """Populate storage with 5 collections and 10 prompts."""
    if storage.get_all_collections() or storage.get_all_prompts():
        return  # already seeded

    # Collections
    c1 = Collection(id="c-writing", name="Writing", description="Prompts for content writing, copywriting, and creative writing tasks.")
    c2 = Collection(id="c-coding", name="Software Engineering", description="Prompts for code generation, debugging, and architecture decisions.")
    c3 = Collection(id="c-marketing", name="Marketing", description="Prompts for ad copy, social media, SEO, and campaign strategies.")
    c4 = Collection(id="c-education", name="Education", description="Prompts for lesson planning, tutoring, and educational content.")
    c5 = Collection(id="c-design", name="Design", description="Prompts for UI/UX feedback, design briefs, and creative direction.")

    for c in [c1, c2, c3, c4, c5]:
        storage.create_collection(c)

    # Prompts
    prompts = [
        Prompt(
            title="Blog Post Outline Generator",
            content="You are a professional content strategist. Given a topic and target audience, generate a detailed blog post outline with an engaging title, introduction hook, 5-7 main sections with subpoints, and a compelling conclusion with a call to action.",
            description="Generates structured blog post outlines for any topic.",
            collection_id="c-writing",
            tags=["writing", "blog", "content"],
        ),
        Prompt(
            title="Python Code Reviewer",
            content="You are a senior Python developer performing a code review. Analyze the provided code for: 1) Bugs and logical errors, 2) Performance bottlenecks, 3) PEP 8 compliance, 4) Security vulnerabilities, 5) Suggestions for more Pythonic patterns. Provide specific line references and improved code snippets.",
            description="Reviews Python code for bugs, performance, and best practices.",
            collection_id="c-coding",
            tags=["python", "code-review", "engineering"],
        ),
        Prompt(
            title="Social Media Campaign Planner",
            content="You are a social media marketing expert. Create a 2-week campaign plan for the given product/service. Include: platform-specific post ideas for Instagram, Twitter, and LinkedIn, posting schedule, hashtag strategy, engagement tactics, and KPIs to track. Format as a day-by-day calendar.",
            description="Plans a full 2-week social media campaign across platforms.",
            collection_id="c-marketing",
            tags=["social-media", "campaign", "marketing"],
        ),
        Prompt(
            title="Lesson Plan Creator",
            content="You are an experienced educator. Design a 60-minute lesson plan for the given subject and grade level. Include: learning objectives (using Bloom's taxonomy), warm-up activity (5 min), main instruction (20 min), guided practice (15 min), independent activity (15 min), and assessment/wrap-up (5 min). Add differentiation strategies for advanced and struggling learners.",
            description="Creates detailed lesson plans with differentiation strategies.",
            collection_id="c-education",
            tags=["teaching", "lesson-plan", "education"],
        ),
        Prompt(
            title="UI/UX Heuristic Evaluator",
            content="You are a senior UX designer conducting a heuristic evaluation. Analyze the described interface using Nielsen's 10 usability heuristics. For each heuristic, rate severity (0-4), describe the issue found, and provide a specific actionable recommendation. Summarize the top 3 critical issues at the end.",
            description="Evaluates UI designs against Nielsen's usability heuristics.",
            collection_id="c-design",
            tags=["ux", "usability", "design"],
        ),
        Prompt(
            title="API Documentation Writer",
            content="You are a technical writer specializing in API documentation. Given an API endpoint description, generate comprehensive documentation including: endpoint URL and method, request headers, path/query parameters with types, request body schema with examples, response schema for success and error cases, curl example, and common error codes with troubleshooting tips.",
            description="Generates comprehensive REST API documentation from endpoint specs.",
            collection_id="c-coding",
            tags=["api", "documentation", "engineering"],
        ),
        Prompt(
            title="Email Subject Line A/B Tester",
            content="You are an email marketing specialist. Given the email content and target audience, generate 10 subject line variations using different psychological triggers: curiosity, urgency, personalization, social proof, benefit-driven, question-based, number-based, fear of missing out, humor, and direct. Rate each for expected open rate (low/medium/high) and explain why.",
            description="Generates 10 email subject line variations with psychological triggers.",
            collection_id="c-marketing",
            tags=["email", "copywriting", "a-b-testing"],
        ),
        Prompt(
            title="Creative Story Starter",
            content="You are a creative writing coach. Generate 3 unique story starters for the given genre. Each starter should include: an opening paragraph (50-75 words) with a strong hook, a brief character sketch of the protagonist, the central conflict or mystery, and the setting description. Make each starter tonally distinct — one dark, one humorous, one literary.",
            description="Creates three tonally distinct story starters for any genre.",
            collection_id="c-writing",
            tags=["creative-writing", "fiction", "storytelling"],
        ),
        Prompt(
            title="Quiz Question Generator",
            content="You are an assessment design expert. Create a 10-question quiz for the given topic and difficulty level. Include a mix of: 4 multiple choice (with plausible distractors), 3 true/false (with explanation), 2 short answer, and 1 scenario-based question. Provide an answer key with detailed explanations for each answer.",
            description="Generates balanced quizzes with multiple question types and answer keys.",
            collection_id="c-education",
            tags=["quiz", "assessment", "education"],
        ),
        Prompt(
            title="Design System Color Palette",
            content="You are a design systems architect. Given a brand's primary color and mood/personality keywords, generate a complete color palette including: primary (3 shades), secondary (3 shades), neutral (5 shades from near-white to near-black), semantic colors (success, warning, error, info), and surface/background colors for light and dark themes. Provide hex values and WCAG contrast ratios for text combinations.",
            description="Generates accessible color palettes for design systems.",
            collection_id="c-design",
            tags=["color", "design-system", "accessibility"],
        ),
    ]

    for p in prompts:
        storage.create_prompt(p)
