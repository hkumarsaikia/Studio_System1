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

    @staticmethod
    def generate_narration(topic: str, scene_label: str, category: str, mood: str) -> str:
        """Generate a 1-2 sentence narration script for one 10-second segment."""
        if scene_label == 'Topic frame':
            templates = [
                f"Today we're breaking down {topic} — how it actually works, and why it matters.",
                f"Let's take apart {topic}, piece by piece, and see what's really going on.",
                f"What if everything you knew about {topic} was only part of the story?",
            ]
            return random.choice(templates)

        if scene_label == 'Hook':
            if mood == 'stressed':
                templates = [
                    f"Right now, the system behind {topic} is under enormous pressure. Here's why that affects you.",
                    f"Most people never see how {topic} shapes their daily decisions. That changes today.",
                ]
            else:
                templates = [
                    f"You interact with {topic} every single day — you just don't realize it yet.",
                    f"Here's the thing about {topic} that nobody is talking about.",
                ]
            return random.choice(templates)

        if scene_label == 'System boundary':
            templates = [
                "First, let's define where this system starts and where it stops.",
                "Every system has edges. Let's map the boundaries of this one.",
            ]
            return random.choice(templates)

        if scene_label == 'Cause layer 1':
            templates = [
                f"At its foundation, {topic} is driven by a single core mechanism.",
                "This is the primary engine. Everything else flows from here.",
            ]
            return random.choice(templates)

        if scene_label == 'Cause layer 2':
            templates = [
                "Now, watch how the effect propagates outward through the network.",
                "The secondary mechanisms amplify the initial trigger across the system.",
            ]
            return random.choice(templates)

        if scene_label == 'Cause layer 3':
            templates = [
                "Here's where feedback loops take over — amplifying or dampening the signal.",
                "At the deepest layer, variables interact in ways that are hard to predict.",
            ]
            return random.choice(templates)

        if scene_label == 'Data lens':
            templates = [
                f"Let's look at what the data actually says about {topic}.",
                "When you quantify this system, the patterns become unmistakable.",
            ]
            return random.choice(templates)

        if scene_label == 'Real world scene':
            templates = [
                "This is what it looks like on the ground, in real life, right now.",
                "Step outside the model. Here's how this plays out in the real world.",
            ]
            return random.choice(templates)

        if scene_label == 'Ecology/externalities':
            templates = [
                "But there are hidden costs that the standard model doesn't account for.",
                "The externalities of this system are significant — and largely invisible.",
            ]
            return random.choice(templates)

        if scene_label == 'Macro trend':
            templates = [
                "Zoom out. Where is this trajectory heading over the next decade?",
                "At the macro scale, the trend line points in one clear direction.",
            ]
            return random.choice(templates)

        if scene_label == 'Actionable takeaway':
            if mood == 'happy':
                return "So what can you actually do with this knowledge? Here's the play."
            return "Understanding this architecture gives you a strategic advantage. Here's how to use it."

        if scene_label == 'Closing':
            templates = [
                f"That's {topic} — decoded, mapped, and laid bare. Now you see the system.",
                "Systems thinking isn't about knowing everything. It's about seeing the connections.",
            ]
            return random.choice(templates)

        return f"Let's examine {topic} from this angle."

    @staticmethod
    def generate_visual_direction(topic: str, scene_label: str, visual: str, action: str) -> str:
        """Generate a visual/animation direction note for one 10-second segment."""
        directions = {
            'Topic frame':           f"Open on a crowd scene with a {action} camera. Title '{topic}' fades in with accent glow.",
            'Hook':                  f"Icon grid animates in with a {action} motion. Category-relevant icons pulse sequentially.",
            'System boundary':       f"Network graph materializes node by node. Camera holds {action}. Connections draw themselves.",
            'Cause layer 1':         f"Mathematical notation writes itself on a chalkboard. {action} camera builds tension.",
            'Cause layer 2':         f"Flow diagram arrows animate left to right. Labels appear with staggered timing. {action} camera.",
            'Cause layer 3':         f"Generative data lattice pulses with feedback energy. {action} camera reveals depth.",
            'Data lens':             f"Neural core visualization rotates slowly. Data streams converge. {action} camera.",
            'Real world scene':      f"City street parallax scene. Weather effects active. {action} camera across the urban landscape.",
            'Ecology/externalities': f"Animal silhouettes move across a natural backdrop. {action} camera tracks the motion.",
            'Macro trend':           f"Globe visualization rotates showing macro data overlays. {action} camera.",
            'Actionable takeaway':   f"Icon grid returns with action-oriented icons. {action} camera emphasizes key takeaways.",
            'Closing':               f"Crowd scene returns, mood shifts to positive. {action} camera for final reflection.",
        }
        return directions.get(scene_label, f"Render {visual} component with {action} camera movement.")
