import hashlib

class NarrativeEngine:
    """
    Procedural Narrative Generator for Studio System videos.
    Replaces static dictionary lookups with dynamic, context-aware, and varied
    sentence structures based on the scene's mood, category, and topic.
    """

    @staticmethod
    def _pick(templates: list[str], topic: str, scene_label: str, category: str, mood: str) -> str:
        seed = f'{topic}|{scene_label}|{category}|{mood}'.encode('utf-8')
        digest = hashlib.sha256(seed).hexdigest()
        index = int(digest[:8], 16) % len(templates)
        return templates[index]

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
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

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
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        if scene_label == 'System boundary':
            templates = [
                "Where does the jurisdiction of this system begin and end?",
                "Mapping the outer limits of the network.",
                "Defining the strict boundaries of the architecture.",
            ]
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        if scene_label == 'Cause layer 1':
            templates = [
                f"The primary engine driving {topic}.",
                "The foundational layer holding the structure together.",
                "At its core, this is what fuels the entire process.",
            ]
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        if scene_label == 'Cause layer 2':
            templates = [
                "How these mechanisms propagate through the network.",
                "The secondary effects rippling outward.",
                "Tracing the flow of cause and effect.",
            ]
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        if scene_label == 'Cause layer 3':
            templates = [
                "Feedback loops that exponentially amplify or dampen the baseline.",
                "The mathematical convergence of these variables.",
                "Complex interactions emerging at the deepest layer.",
            ]
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        if scene_label == 'Data lens':
            templates = [
                f"What the raw metrics reveal about {topic}.",
                "Quantifying the impact through statistical analysis.",
                "The numbers tell a distinctly different story.",
            ]
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

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
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        if scene_label == 'Macro trend':
            templates = [
                "Where this trajectory implies we are headed next.",
                "Zooming out to the planetary scale over the next decade.",
                "The inevitable mathematical conclusion on a macro level.",
            ]
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

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
            return NarrativeEngine._pick(templates, topic, scene_label, category, mood)

        # Fallback
        return f"Exploring the parameters of {topic}."

    @staticmethod
    def generate_narration(topic: str, scene_label: str, category: str, mood: str) -> str:
        if scene_label == 'Topic frame':
            return f'{topic} looks simple on the surface, but it is really a system of incentives, rules, and feedback loops.'

        if scene_label == 'Hook':
            return f'This matters because {topic.lower()} changes what people can afford, access, or influence in everyday life.'

        if scene_label == 'System boundary':
            return 'To understand it, start by mapping the main actors, the rules they follow, and the limits of the system.'

        if scene_label == 'Cause layer 1':
            return f'The first layer is the core driver that keeps {topic.lower()} moving even when the outcomes look unfair or inefficient.'

        if scene_label == 'Cause layer 2':
            return 'Then that driver flows through institutions, prices, behavior, and public expectations.'

        if scene_label == 'Cause layer 3':
            return 'Over time, feedback loops reinforce the pattern and make the system harder to change.'

        if scene_label == 'Data lens':
            return 'The data lens helps separate intuition from measurement and shows which pressures are actually growing.'

        if scene_label == 'Real world scene':
            return 'What looks abstract in theory appears in the real world as daily constraints, tradeoffs, and visible pressure points.'

        if scene_label == 'Ecology/externalities':
            return 'Every system pushes some costs outward, and those hidden externalities are often what people notice last.'

        if scene_label == 'Macro trend':
            return 'At a larger scale, the same forces shape long-term trends across regions, industries, and institutions.'

        if scene_label == 'Actionable takeaway':
            return 'The practical takeaway is to focus on leverage points where small rule changes or behavior changes alter the whole system.'

        if scene_label == 'Closing':
            return f'Once you see how {topic.lower()} works as a system, the outcomes stop looking random.'

        return f'This segment explains one part of how {topic.lower()} works.'
