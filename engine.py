#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
manus_engine.py

This module simulates prompt orchestration for intelligent NPCs in NarrativeVerse,
adapting dialogues based on player decisions and character personalities.
"""

import json
import random
from typing import Dict, List, Optional, Tuple, Any


class Engine:
    """
    Main engine for adaptive prompt orchestration for NPCs.
    Manages the generation of dialogues and behaviors based on game context,
    interaction history, and character profiles.
    """

    def __init__(self, npc_profiles_path: str = "npc_profiles.json"):
        """
        Initializes the Manus engine with NPC profiles and prompt templates.

        Args:
            npc_profiles_path: Path to the JSON file containing NPC profiles
        """
        self.npc_profiles = self._load_npc_profiles(npc_profiles_path)
        self.player_history = {}
        self.relationship_states = {}
        self.conversation_context = {}
        self.prompt_templates = self._initialize_prompt_templates()
        
    def _load_npc_profiles(self, profile_path: str) -> Dict:
        """Loads NPC profiles from the JSON file."""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Profile file not found: {profile_path}")
            return {"npcs": []}
        except json.JSONDecodeError:
            print(f"Error decoding JSON file: {profile_path}")
            return {"npcs": []}
    
    def _initialize_prompt_templates(self) -> Dict:
        """Initializes prompt templates for different contexts and interaction styles."""
        return {
            "greeting": {
                "formal": "Greetings, traveler. I am {npc_name}, {npc_title}. {custom_intro}",
                "friendly": "Hello! Great to see you here! I'm {npc_name}. {custom_intro}",
                "cautious": "Hmm... {hesitation} I'm {npc_name}. {custom_intro}",
                "excited": "Wow! A new face! I'm {npc_name}! {custom_intro}"
            },
            "quest_offer": {
                "urgent": "I need your help immediately. {quest_description} Time is running out!",
                "mysterious": "I have an... interesting proposal. {quest_description} There's more to this than meets the eye.",
                "casual": "If you have time, could you help me with something? {quest_description} No rush.",
                "challenging": "I'm looking for someone with your skills. {quest_description} Few could manage this."
            },
            "response_to_player_choice": {
                "approval": "Excellent choice! {approval_response}",
                "disappointment": "{disappointment_response} I expected more from you.",
                "surprise": "Interesting... {surprise_response} I didn't expect that.",
                "neutral": "I understand your decision. {neutral_response}"
            },
            "mood_modifiers": {
                "happy": {
                    "word_choices": ["wonderful", "excellent", "fantastic", "amazing"],
                    "sentence_endings": ["!", "! That's great!", "! How delightful!"],
                    "speech_patterns": "expansive and enthusiastic"
                },
                "sad": {
                    "word_choices": ["unfortunately", "sadly", "regrettably", "with sorrow"],
                    "sentence_endings": ["...", ". *sigh*", ". Such is life..."],
                    "speech_patterns": "slow and melancholic"
                },
                "angry": {
                    "word_choices": ["irritating", "absurd", "unacceptable", "outrageous"],
                    "sentence_endings": [".", ". Understood?", "!"],
                    "speech_patterns": "short and intense"
                },
                "curious": {
                    "word_choices": ["interesting", "fascinating", "intriguing", "curious"],
                    "sentence_endings": ["?", "... don't you think?", "... I wonder why."],
                    "speech_patterns": "questioning and reflective"
                }
            }
        }
    
    def generate_dialogue(self, 
                         npc_name: str, 
                         context: str, 
                         player_history: Optional[Dict] = None,
                         player_choice: Optional[str] = None) -> str:
        """
        Generates adaptive dialogue for an NPC based on context and history.
        
        Args:
            npc_name: Name of the NPC to generate dialogue for
            context: Current interaction context (greeting, quest, etc)
            player_history: Optional history of interactions with the player
            player_choice: Recent player choice that may influence the response
            
        Returns:
            Generated dialogue text for the NPC
        """
        # Find the NPC profile
        npc_profile = next((npc for npc in self.npc_profiles["npcs"] 
                           if npc["name"] == npc_name), None)
        
        if not npc_profile:
            return f"[NPC '{npc_name}' not found in system]"
        
        # Determine interaction style based on context and personality
        interaction_style = self._determine_interaction_style(npc_profile, context, player_history)
        
        # Select appropriate base template
        template = self._select_template(context, interaction_style, player_choice)
        
        # Apply mood and personality modifiers
        mood = self._determine_mood(npc_profile, player_history, player_choice)
        modified_template = self._apply_mood_modifiers(template, mood)
        
        # Fill the template with NPC information and context
        return self._fill_template(modified_template, npc_profile, context, player_choice)
    
    def _determine_interaction_style(self, 
                                    npc_profile: Dict, 
                                    context: str, 
                                    player_history: Optional[Dict]) -> str:
        """Determines the appropriate interaction style based on profile and context."""
        # Simplified implementation - in a real system, this would be more complex
        if context == "greeting":
            return "friendly" if npc_profile["alignment"].split()[1] == "Good" else "cautious"
        elif context == "quest_offer":
            if "urgency" in context.lower():
                return "urgent"
            elif npc_profile["class"] in ["Techno-Mage Scientist", "Sentient Alien Pet"]:
                return "mysterious"
            else:
                return "casual"
        elif context == "response_to_player_choice":
            # Here we would use player history to determine the response
            if not player_history:
                return "neutral"
            # Additional logic based on history
            return "approval"  # Default for simulation
        
        return "friendly"  # Default style
    
    def _select_template(self, 
                        context: str, 
                        interaction_style: str, 
                        player_choice: Optional[str]) -> str:
        """Selects the appropriate base template for the context and style."""
        if context in self.prompt_templates and interaction_style in self.prompt_templates[context]:
            return self.prompt_templates[context][interaction_style]
        
        # Fallback to generic template if specific one not found
        return "Hello, I'm {npc_name}. How can I help?"
    
    def _determine_mood(self, 
                       npc_profile: Dict, 
                       player_history: Optional[Dict], 
                       player_choice: Optional[str]) -> str:
        """Determines the current mood of the NPC based on personality and context."""
        # In a real system, this would be based on a more complex model
        # Simplified simulation for demonstration
        moods = ["happy", "sad", "angry", "curious"]
        
        # Tendency based on personality traits
        personality_traits = npc_profile.get("personality_traits", {})
        
        if personality_traits:
            # Determine mood based on dominant trait
            max_trait = max(personality_traits.items(), key=lambda x: x[1])
            
            if max_trait[0] in ["optimism", "enthusiasm", "curiosity"]:
                return "happy" if random.random() < 0.7 else random.choice(moods)
            elif max_trait[0] in ["wisdom", "empathy", "compassion"]:
                return "curious" if random.random() < 0.6 else random.choice(moods)
            elif max_trait[0] in ["determination", "courage"]:
                # More varied, depending on situation
                return random.choice(moods)
        
        # Fallback to random mood with tendency toward curious
        return "curious" if random.random() < 0.4 else random.choice(moods)
    
    def _apply_mood_modifiers(self, template: str, mood: str) -> str:
        """Applies mood modifiers to the base template."""
        if mood not in self.prompt_templates["mood_modifiers"]:
            return template
        
        mood_data = self.prompt_templates["mood_modifiers"][mood]
        
        # Simple simulation - in a real system, we'd use more advanced NLP
        # Here we just add a prefix indicating the mood
        mood_prefix = f"[{mood_data['speech_patterns']}] "
        return mood_prefix + template
    
    def _fill_template(self, 
                      template: str, 
                      npc_profile: Dict, 
                      context: str, 
                      player_choice: Optional[str]) -> str:
        """Fills the template with specific NPC information and context."""
        filled_template = template
        
        # Basic replacements
        replacements = {
            "{npc_name}": npc_profile["name"],
            "{npc_title}": npc_profile["class"],
            "{custom_intro}": f"I am {npc_profile['alignment']} and {self._generate_intro_snippet(npc_profile)}",
            "{hesitation}": random.choice(["Who approaches?", "You seem... different.", "Hmm..."]),
            "{quest_description}": "[Quest description would be dynamically generated]",
            "{approval_response}": "This shows your character.",
            "{disappointment_response}": "This wasn't what I expected.",
            "{surprise_response}": "You continue to surprise me.",
            "{neutral_response}": "Let's see where this leads us."
        }
        
        for key, value in replacements.items():
            filled_template = filled_template.replace(key, value)
        
        return filled_template
    
    def _generate_intro_snippet(self, npc_profile: Dict) -> str:
        """Generates an introduction snippet based on the NPC's profile."""
        backstory = npc_profile.get("backstory", "")
        if backstory:
            # Extract a relevant sentence from the backstory
            sentences = backstory.split('.')
            if len(sentences) > 2:
                return sentences[1].strip() + "."
            return backstory.split('.')[0] + "."
        
        return "I have a story to tell."
    
    def update_player_relationship(self, 
                                  npc_name: str, 
                                  player_action: str, 
                                  context: str) -> None:
        """
        Updates the relationship state between the player and an NPC.
        
        Args:
            npc_name: Name of the NPC
            player_action: Description of the player's action
            context: Interaction context
        """
        if npc_name not in self.relationship_states:
            self.relationship_states[npc_name] = {
                "affinity": 50,  # Scale of 0-100
                "trust": 50,     # Scale of 0-100
                "interactions": []
            }
        
        # Simulated sentiment analysis of player action
        sentiment_score = self._analyze_player_action(player_action)
        
        # Update relationship metrics
        self.relationship_states[npc_name]["affinity"] += sentiment_score
        self.relationship_states[npc_name]["affinity"] = max(0, min(100, self.relationship_states[npc_name]["affinity"]))
        
        # Adjust trust based on context and history
        trust_change = sentiment_score * 0.5  # Trust changes more slowly than affinity
        self.relationship_states[npc_name]["trust"] += trust_change
        self.relationship_states[npc_name]["trust"] = max(0, min(100, self.relationship_states[npc_name]["trust"]))
        
        # Record interaction
        self.relationship_states[npc_name]["interactions"].append({
            "action": player_action,
            "context": context,
            "sentiment": sentiment_score,
            "timestamp": "simulated_timestamp"  # In a real system, we'd use actual timestamp
        })
    
    def _analyze_player_action(self, action: str) -> float:
        """
        Analyzes the player's action to determine its impact on the relationship.
        Returns a value between -10 and +10.
        
        In a real system, this would use natural language processing.
        """
        # Simplified simulation - positive and negative keywords
        positive_keywords = ["help", "save", "protect", "agree", "gift", "compliment"]
        negative_keywords = ["attack", "steal", "lie", "threaten", "insult", "refuse"]
        
        score = 0
        action_lower = action.lower()
        
        for word in positive_keywords:
            if word in action_lower:
                score += 2
        
        for word in negative_keywords:
            if word in action_lower:
                score -= 2
        
        return max(-10, min(10, score))
    
    def generate_response_options(self, 
                                 npc_name: str, 
                                 context: str, 
                                 player_statement: str,
                                 num_options: int = 3) -> List[str]:
        """
        Generates NPC response options to a player statement.
        
        Args:
            npc_name: Name of the NPC
            context: Conversation context
            player_statement: What the player said
            num_options: Number of options to generate
            
        Returns:
            List of possible NPC responses
        """
        npc_profile = next((npc for npc in self.npc_profiles["npcs"] 
                           if npc["name"] == npc_name), None)
        
        if not npc_profile:
            return [f"[NPC '{npc_name}' not found]"] * num_options
        
        # In a real system, this would use a language model to generate varied responses
        # Here we use simple templates for demonstration
        
        relationship = self.relationship_states.get(npc_name, {"affinity": 50, "trust": 50})
        affinity = relationship["affinity"]
        trust = relationship["trust"]
        
        # Adjust tone based on relationship
        tone = "friendly" if affinity > 70 else "neutral" if affinity > 30 else "cautious"
        
        # Generate options based on context and tone
        options = []
        
        # Option based on high affinity
        if affinity > 60:
            options.append(f"I completely understand, {self._get_player_nickname(affinity)}. "
                          f"Considering our history together, I suggest {self._generate_suggestion(npc_profile, context, True)}.")
        
        # Option based on low affinity
        if affinity < 40:
            options.append(f"Hmm. {self._generate_cautious_response(npc_profile)}. "
                          f"Perhaps we should {self._generate_suggestion(npc_profile, context, False)}.")
        
        # Option based on high trust
        if trust > 70:
            options.append(f"I trust you to make the right decision here. "
                          f"If you want my honest opinion, {self._generate_honest_opinion(npc_profile, context)}.")
        
        # Neutral/informative option
        options.append(f"Considering the facts, {self._generate_factual_response(npc_profile, context)}.")
        
        # Option based on NPC personality
        options.append(self._generate_personality_based_response(npc_profile, context))
        
        # Select and return the requested number of options
        if len(options) > num_options:
            return random.sample(options, num_options)
        
        # Fill with generic options if needed
        while len(options) < num_options:
            options.append(f"Interesting perspective. Let's consider {random.choice(['next steps', 'other options', 'alternatives'])}.")
        
        return options
    
    def _get_player_nickname(self, affinity: float) -> str:
        """Generates a nickname for the player based on affinity level."""
        if affinity > 90:
            return random.choice(["my dear friend", "partner", "adventure companion"])
        elif affinity > 70:
            return random.choice(["friend", "partner", "adventurer"])
        else:
            return "traveler"
    
    def _generate_suggestion(self, npc_profile: Dict, context: str, positive: bool) -> str:
        """Generates a suggestion based on the NPC's profile and context."""
        if "Explorer" in npc_profile["class"]:
            return "explore that less-traveled path" if positive else "follow the safer route this time"
        elif "Scientist" in npc_profile["class"]:
            return "analyze the patterns before deciding" if positive else "consider the unknown variables"
        elif "Guardian" in npc_profile["class"]:
            return "protect what's most valuable first" if positive else "retreat and reassess the situation"
        else:
            return "follow your intuition" if positive else "think more about the consequences"
    
    def _generate_cautious_response(self, npc_profile: Dict) -> str:
        """Generates a cautious response based on the NPC's profile."""
        alignment = npc_profile["alignment"].split()
        if alignment[0] == "Lawful":
            return "We need to consider the rules and traditions here"
        elif alignment[0] == "Chaotic":
            return "I don't much trust rigid plans in this situation"
        else:  # Neutral
            return "I see pros and cons on both sides"
    
    def _generate_honest_opinion(self, npc_profile: Dict, context: str) -> str:
        """Generates an honest opinion based on the NPC's profile."""
        personality_traits = npc_profile.get("personality_traits", {})
        
        if personality_traits:
            max_trait = max(personality_traits.items(), key=lambda x: x[1])
            trait_name = max_trait[0]
            
            if trait_name in ["optimism", "enthusiasm", "curiosity"]:
                return "I believe we should try the bolder approach"
            elif trait_name in ["wisdom", "patience"]:
                return "I suggest we observe more before acting"
            elif trait_name in ["determination", "courage"]:
                return "we should face this head-on, without hesitation"
        
        return "I think we should follow what seems most aligned with our goals"
    
    def _generate_factual_response(self, npc_profile: Dict, context: str) -> str:
        """Generates a factual response based on the NPC's profile and context."""
        npc_class = npc_profile["class"]
        
        if "Explorer" in npc_class:
            return "I've seen similar situations in my travels, and usually it's best to map all possible routes"
        elif "Scientist" in npc_class:
            return "the data suggests there are multiple variables to consider, especially the time factor"
        elif "Guardian" in npc_class:
            return "the natural balance suggests we should intervene minimally, but with precision"
        else:
            return "based on what we know, we have several viable options to consider"
    
    def _generate_personality_based_response(self, npc_profile: Dict, context: str) -> str:
        """Generates a response based on the NPC's unique personality."""
        # Use the NPC's interaction style to personalize the response
        interaction_style = npc_profile.get("interaction_style", {})
        
        if "under_stress" in interaction_style and "stress" in context.lower():
            return f"[Under pressure] {interaction_style['under_stress']}"
        elif "teaching_moments" in interaction_style and "learn" in context.lower():
            return f"[Teaching] {interaction_style['teaching_moments']}"
        elif "conflict_resolution" in interaction_style and ("conflict" in context.lower() or "disagree" in context.lower()):
            return f"[Resolving conflict] {interaction_style['conflict_resolution']}"
        elif "first_meeting" in interaction_style and "new" in context.lower():
            return f"[First meeting] {interaction_style['first_meeting']}"
        
        # Fallback to a generic response based on class
        return f"As a {npc_profile['class']}, my perspective is that {self._generate_class_perspective(npc_profile['class'])}"
    
    def _generate_class_perspective(self, npc_class: str) -> str:
        """Generates a perspective based on the NPC's class."""
        perspectives = {
            "Star Explorer": "each journey reveals new possibilities we couldn't imagine before setting out",
            "Techno-Mage Scientist": "the intersection between science and the unexplained often reveals the most elegant solutions",
            "Guardian of the Floating Forests": "all parts of a system are connected, and each action creates ripples through the whole",
            "Sentient Alien Pet": "communication goes far beyond words; sometimes the unspoken is more important",
            "Hero Apprentice": "the stories we hear shape the stories we live, and each of us is writing our own chapter"
        }
        
        for class_key, perspective in perspectives.items():
            if class_key in npc_class:
                return perspective
        
        return "each situation is unique and deserves careful consideration"


# Example usage of ManusEngine
if __name__ == "__main__":
    # Initialize the engine
    engine = ManusEngine()
    
    # Example dialogue generation
    print("\n=== Example Generated Dialogues ===\n")
    
    # Greeting dialogues for different NPCs
    npcs = ["Captain Lyra Novastella", "Dr. Elian Thaumatec", "Sylva Aerafrond", "Blip", "Mira Lumina"]
    
    for npc in npcs:
        print(f"\n--- Dialogue for {npc} ---")
        greeting = engine.generate_dialogue(npc, "greeting")
        print(f"Greeting: {greeting}")
        
        # Simulate a relationship update
        engine.update_player_relationship(
            npc, 
            "helping solve a difficult problem", 
            "cooperative mission"
        )
        
        # Generate response options
        print("\nResponse options for 'We need to find a creative solution to this challenge':")
        options = engine.generate_response_options(
            npc, 
            "problem solving", 
            "We need to find a creative solution to this challenge"
        )
        
        for i, option in enumerate(options, 1):
            print(f"  Option {i}: {option}")
    
    print("\n=== Mood Adaptation Demonstration ===\n")
    
    # Demonstrate how the same NPC responds in different moods
    test_npc = "Dr. Elian Thaumatec"
    moods = ["happy", "sad", "angry", "curious"]
    
    # Force different moods for demonstration
    original_determine_mood = engine._determine_mood
    try:
        for mood in moods:
            print(f"\n--- {test_npc} in '{mood}' mood ---")
            # Temporarily replace the mood determination method
            engine._determine_mood = lambda *args, **kwargs: mood
            
            dialogue = engine.generate_dialogue(test_npc, "greeting")
            print(dialogue)
            
            quest = engine.generate_dialogue(test_npc, "quest_offer")
            print(quest)
    finally:
        # Restore the original method
        engine._determine_mood = original_determine_mood
    
    print("\n=== End of Demonstration ===")
