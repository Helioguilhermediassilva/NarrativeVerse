using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

namespace NarrativeVerse
{
    /// <summary>
    /// DialogueTrigger handles the interaction between Unity game objects and the NarrativeVerse dialogue system.
    /// It can be attached to NPCs, objects, or trigger zones to initiate dialogue when the player interacts with them.
    /// </summary>
    public class DialogueTrigger : MonoBehaviour
    {
        [Header("NPC Configuration")]
        [Tooltip("The unique identifier for this NPC in the npc_profiles.json file")]
        public string npcId;
        
        [Tooltip("The context for this dialogue interaction (e.g., greeting, quest_offer, etc.)")]
        public string interactionContext = "greeting";
        
        [Header("Dialogue UI References")]
        [Tooltip("Reference to the dialogue panel UI element")]
        public GameObject dialoguePanel;
        
        [Tooltip("Reference to the text component that displays the NPC's name")]
        public TextMeshProUGUI nameText;
        
        [Tooltip("Reference to the text component that displays the dialogue content")]
        public TextMeshProUGUI dialogueText;
        
        [Tooltip("Reference to the NPC's portrait image (optional)")]
        public Image npcPortrait;
        
        [Header("Dialogue Options")]
        [Tooltip("Parent object containing the player response option buttons")]
        public GameObject responseOptionsContainer;
        
        [Tooltip("Button prefab for response options")]
        public GameObject responseButtonPrefab;
        
        [Header("Interaction Settings")]
        [Tooltip("Whether dialogue can be triggered automatically when player enters trigger zone")]
        public bool autoTrigger = false;
        
        [Tooltip("Whether this dialogue can be triggered multiple times")]
        public bool repeatable = true;
        
        [Tooltip("Interaction prompt text (e.g., 'Press E to talk')")]
        public string interactionPrompt = "Press E to talk";
        
        // Reference to the NarrativeVerse manager that handles dialogue generation
        private NarrativeVerseManager narrativeManager;
        
        // Tracks whether this dialogue has been triggered before
        private bool hasTriggered = false;
        
        // Tracks whether player is in range to trigger dialogue
        private bool playerInRange = false;
        
        // Reference to the player's game object
        private GameObject player;
        
        // Current dialogue data
        private DialogueData currentDialogue;
        
        // List of current response options
        private List<ResponseOption> currentResponses = new List<ResponseOption>();
        
        // UI elements for interaction prompt
        private GameObject promptCanvas;
        private TextMeshProUGUI promptText;
        
        void Start()
        {
            // Find the NarrativeVerse manager in the scene
            narrativeManager = FindObjectOfType<NarrativeVerseManager>();
            
            if (narrativeManager == null)
            {
                Debug.LogError("NarrativeVerseManager not found in scene! DialogueTrigger requires a NarrativeVerseManager to function.");
            }
            
            // Initialize the interaction prompt UI
            InitializePromptUI();
            
            // Hide dialogue panel at start
            if (dialoguePanel != null)
            {
                dialoguePanel.SetActive(false);
            }
        }
        
        void Update()
        {
            // Check for player input to trigger dialogue
            if (playerInRange && !autoTrigger && Input.GetKeyDown(KeyCode.E))
            {
                TriggerDialogue();
            }
        }
        
        /// <summary>
        /// Initializes the floating interaction prompt UI
        /// </summary>
        private void InitializePromptUI()
        {
            // Create a canvas for the prompt if it doesn't exist
            if (promptCanvas == null)
            {
                promptCanvas = new GameObject("PromptCanvas");
                promptCanvas.transform.SetParent(transform);
                promptCanvas.transform.localPosition = new Vector3(0, 2, 0); // Position above the NPC
                
                Canvas canvas = promptCanvas.AddComponent<Canvas>();
                canvas.renderMode = RenderMode.WorldSpace;
                canvas.worldCamera = Camera.main;
                
                RectTransform rectTransform = promptCanvas.GetComponent<RectTransform>();
                rectTransform.sizeDelta = new Vector2(2, 0.5f);
                rectTransform.localScale = new Vector3(0.01f, 0.01f, 0.01f);
                
                // Add a background image
                GameObject background = new GameObject("Background");
                background.transform.SetParent(promptCanvas.transform);
                Image bgImage = background.AddComponent<Image>();
                bgImage.color = new Color(0, 0, 0, 0.7f);
                
                RectTransform bgRectTransform = background.GetComponent<RectTransform>();
                bgRectTransform.anchorMin = Vector2.zero;
                bgRectTransform.anchorMax = Vector2.one;
                bgRectTransform.sizeDelta = Vector2.zero;
                
                // Add text for the prompt
                GameObject textObj = new GameObject("PromptText");
                textObj.transform.SetParent(promptCanvas.transform);
                promptText = textObj.AddComponent<TextMeshProUGUI>();
                promptText.text = interactionPrompt;
                promptText.color = Color.white;
                promptText.alignment = TextAlignmentOptions.Center;
                promptText.fontSize = 36;
                
                RectTransform textRectTransform = textObj.GetComponent<RectTransform>();
                textRectTransform.anchorMin = Vector2.zero;
                textRectTransform.anchorMax = Vector2.one;
                textRectTransform.sizeDelta = Vector2.zero;
                textRectTransform.offsetMin = new Vector2(10, 5);
                textRectTransform.offsetMax = new Vector2(-10, -5);
            }
            
            // Hide prompt initially
            promptCanvas.SetActive(false);
        }
        
        /// <summary>
        /// Triggers the dialogue interaction with this NPC
        /// </summary>
        public void TriggerDialogue()
        {
            if (!repeatable && hasTriggered)
            {
                return;
            }
            
            // Request dialogue from the NarrativeVerse manager
            RequestDialogueFromManager();
            
            // Show the dialogue UI
            ShowDialogueUI();
            
            // Mark as triggered
            hasTriggered = true;
        }
        
        /// <summary>
        /// Requests dialogue data from the NarrativeVerse manager
        /// </summary>
        private void RequestDialogueFromManager()
        {
            if (narrativeManager != null)
            {
                // Get dialogue data from the manager
                currentDialogue = narrativeManager.GetDialogue(npcId, interactionContext);
                
                // Get response options
                currentResponses = narrativeManager.GetResponseOptions(npcId, interactionContext, 3);
            }
            else
            {
                // Fallback for testing without manager
                currentDialogue = new DialogueData
                {
                    npcName = "Missing Manager",
                    dialogueText = "NarrativeVerseManager not found. Please add one to your scene."
                };
                
                currentResponses = new List<ResponseOption>();
            }
        }
        
        /// <summary>
        /// Shows the dialogue UI with the current dialogue data
        /// </summary>
        private void ShowDialogueUI()
        {
            if (dialoguePanel != null)
            {
                dialoguePanel.SetActive(true);
                
                // Set NPC name
                if (nameText != null)
                {
                    nameText.text = currentDialogue.npcName;
                }
                
                // Set dialogue text
                if (dialogueText != null)
                {
                    dialogueText.text = currentDialogue.dialogueText;
                }
                
                // Set portrait if available
                if (npcPortrait != null && currentDialogue.portraitSprite != null)
                {
                    npcPortrait.sprite = currentDialogue.portraitSprite;
                    npcPortrait.gameObject.SetActive(true);
                }
                else if (npcPortrait != null)
                {
                    npcPortrait.gameObject.SetActive(false);
                }
                
                // Create response options
                CreateResponseOptions();
            }
        }
        
        /// <summary>
        /// Creates UI buttons for each response option
        /// </summary>
        private void CreateResponseOptions()
        {
            if (responseOptionsContainer != null)
            {
                // Clear existing options
                foreach (Transform child in responseOptionsContainer.transform)
                {
                    Destroy(child.gameObject);
                }
                
                // Create new option buttons
                for (int i = 0; i < currentResponses.Count; i++)
                {
                    ResponseOption option = currentResponses[i];
                    GameObject buttonObj = Instantiate(responseButtonPrefab, responseOptionsContainer.transform);
                    
                    // Set button text
                    TextMeshProUGUI buttonText = buttonObj.GetComponentInChildren<TextMeshProUGUI>();
                    if (buttonText != null)
                    {
                        buttonText.text = option.text;
                    }
                    
                    // Set button click action
                    Button button = buttonObj.GetComponent<Button>();
                    if (button != null)
                    {
                        int optionIndex = i; // Capture the index for the lambda
                        button.onClick.AddListener(() => SelectResponse(optionIndex));
                    }
                }
            }
        }
        
        /// <summary>
        /// Handles player selection of a response option
        /// </summary>
        /// <param name="optionIndex">Index of the selected response option</param>
        public void SelectResponse(int optionIndex)
        {
            if (optionIndex >= 0 && optionIndex < currentResponses.Count)
            {
                ResponseOption selectedOption = currentResponses[optionIndex];
                
                // Inform the NarrativeVerse manager of the player's choice
                if (narrativeManager != null)
                {
                    narrativeManager.ProcessPlayerChoice(npcId, interactionContext, selectedOption);
                }
                
                // Handle any game-specific effects of this choice
                HandleResponseEffects(selectedOption);
                
                // Close dialogue or continue based on the response type
                if (selectedOption.endsDialogue)
                {
                    CloseDialogue();
                }
                else
                {
                    // Request follow-up dialogue
                    interactionContext = selectedOption.nextContext;
                    RequestDialogueFromManager();
                    UpdateDialogueUI();
                }
            }
        }
        
        /// <summary>
        /// Updates the dialogue UI with new content without closing and reopening
        /// </summary>
        private void UpdateDialogueUI()
        {
            // Update NPC name
            if (nameText != null)
            {
                nameText.text = currentDialogue.npcName;
            }
            
            // Update dialogue text
            if (dialogueText != null)
            {
                dialogueText.text = currentDialogue.dialogueText;
            }
            
            // Update portrait if available
            if (npcPortrait != null && currentDialogue.portraitSprite != null)
            {
                npcPortrait.sprite = currentDialogue.portraitSprite;
                npcPortrait.gameObject.SetActive(true);
            }
            
            // Update response options
            CreateResponseOptions();
        }
        
        /// <summary>
        /// Handles any game-specific effects of a selected response
        /// </summary>
        /// <param name="option">The selected response option</param>
        private void HandleResponseEffects(ResponseOption option)
        {
            // Example: Add items to inventory
            if (option.giveItems != null && option.giveItems.Length > 0)
            {
                foreach (string item in option.giveItems)
                {
                    // Call to inventory system would go here
                    Debug.Log($"Adding item to inventory: {item}");
                }
            }
            
            // Example: Update quest status
            if (!string.IsNullOrEmpty(option.questUpdate))
            {
                // Call to quest system would go here
                Debug.Log($"Updating quest: {option.questUpdate}");
            }
            
            // Example: Trigger events
            if (!string.IsNullOrEmpty(option.triggerEvent))
            {
                // Call event system or trigger game events
                Debug.Log($"Triggering event: {option.triggerEvent}");
            }
        }
        
        /// <summary>
        /// Closes the dialogue UI
        /// </summary>
        public void CloseDialogue()
        {
            if (dialoguePanel != null)
            {
                dialoguePanel.SetActive(false);
            }
        }
        
        /// <summary>
        /// Called when player enters the trigger zone
        /// </summary>
        /// <param name="other">The collider that entered the trigger</param>
        private void OnTriggerEnter(Collider other)
        {
            // Check if it's the player
            if (other.CompareTag("Player"))
            {
                playerInRange = true;
                player = other.gameObject;
                
                // Show interaction prompt if not auto-triggering
                if (!autoTrigger)
                {
                    promptCanvas.SetActive(true);
                }
                else
                {
                    // Auto-trigger dialogue
                    TriggerDialogue();
                }
            }
        }
        
        /// <summary>
        /// Called when player exits the trigger zone
        /// </summary>
        /// <param name="other">The collider that exited the trigger</param>
        private void OnTriggerExit(Collider other)
        {
            // Check if it's the player
            if (other.CompareTag("Player"))
            {
                playerInRange = false;
                player = null;
                
                // Hide interaction prompt
                promptCanvas.SetActive(false);
                
                // Close dialogue if open
                CloseDialogue();
            }
        }
    }
    
    /// <summary>
    /// Data structure for dialogue content
    /// </summary>
    [System.Serializable]
    public class DialogueData
    {
        public string npcName;
        public string dialogueText;
        public Sprite portraitSprite;
    }
    
    /// <summary>
    /// Data structure for response options
    /// </summary>
    [System.Serializable]
    public class ResponseOption
    {
        public string text;
        public string nextContext;
        public bool endsDialogue;
        public string[] giveItems;
        public string questUpdate;
        public string triggerEvent;
    }
}
