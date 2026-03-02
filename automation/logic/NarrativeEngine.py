import random

class NarrativeEngine:
    """
    Procedural Narrative Generator for Studio System videos.
    Replaces static dictionary lookups with dynamic, context-aware, and varied
    sentence structures based on the scene's mood, category, and topic.
    """

    @staticmethod
    def generate_subtext(topic: str, scene_label: str, category: str, mood: str) -> str:
        # 1. Base mappings based on the scene's architectural purpose
        if scene_label == 'Topic frame':
            templates = [
                "A systems explainer in 2 minutes.",
                "Deconstructing the invisible machinery.",
                f"How {topic} actually functions.",
                "A deep dive into the underlying architecture.",
            ]
            return random.choice(templates)

        if scene_label == 'Hook':
            if mood == 'stressed':
                templates = [
                    f"Why the mechanisms behind {topic} are reaching a breaking point.",
                    f"The critical vulnerabilities hidden within {topic}.",
                    f"How the architecture of {topic} impacts your daily life.",
                ]
            else:
                templates = [
                    f"Why {topic} matters more now than ever.",
                    f"The surprising truth about how {topic} operates.",
                ]
            return random.choice(templates)

        if scene_label == 'System boundary':
            templates = [
                "Where does the jurisdiction of this system begin and end?",
                "Mapping the outer limits of the network.",
                "Defining the strict boundaries of the architecture.",
            ]
            return random.choice(templates)

        if scene_label == 'Cause layer 1':
            templates = [
                f"The primary engine driving {topic}.",
                "The foundational layer holding the structure together.",
                "At its core, this is what fuels the entire process.",
            ]
            return random.choice(templates)

        if scene_label == 'Cause layer 2':
            templates = [
                "How these mechanisms propagate through the network.",
                "The secondary effects rippling outward.",
                "Tracing the flow of cause and effect.",
            ]
            return random.choice(templates)

        if scene_label == 'Cause layer 3':
            templates = [
                "Feedback loops that exponentially amplify or dampen the baseline.",
                "The mathematical convergence of these variables.",
                "Complex interactions emerging at the deepest layer.",
            ]
            return random.choice(templates)

        if scene_label == 'Data lens':
            templates = [
                f"What the raw metrics reveal about {topic}.",
                "Quantifying the impact through statistical analysis.",
                "The numbers tell a distinctly different story.",
            ]
            return random.choice(templates)

        if scene_label == 'Real world scene':
            if category == 'MONEY & ECONOMICS':
                return "How this institutional flow dictates market realities."
            elif category == 'POWER & INSTITUTIONS':
                return "How policy translates into physical execution."
            else:
                return "How this abstract model plays out on the ground."

        if scene_label == 'Ecology/externalities':
            templates = [
                "The hidden costs externalized by the system.",
                "What the frictionless model fails to account for.",
                "Tracing the unintended environmental consequences.",
            ]
            return random.choice(templates)

        if scene_label == 'Macro trend':
            templates = [
                "Where this trajectory implies we are headed next.",
                "Zooming out to the planetary scale over the next decade.",
                "The inevitable mathematical conclusion on a macro level.",
            ]
            return random.choice(templates)

        if scene_label == 'Actionable takeaway':
            if mood == 'happy':
                return "Leveraging this architecture for positive outcomes."
            elif mood == 'stressed':
                return "Mitigating the asymmetric risks involved."
            else:
                return "How to strategically navigate these mechanisms."

        if scene_label == 'Closing':
            templates = [
                f"{topic}, demystified and mapped.",
                "The system, fully rendered.",
                "Understanding the architecture of our reality.",
            ]
            return random.choice(templates)

        # Fallback
        return f"Exploring the parameters of {topic}."
