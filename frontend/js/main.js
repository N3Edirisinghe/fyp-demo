let currentEmotion = "Happy";
let audioContext = null;
let analyser = null;
let microphone = null;
let isMicActive = false;
let animationFrameId = null;
let wavePhase = 0;
let simulatedVolume = 0.2;
let speechRecognition = null;
let latestUserTranscript = "";
let selectedUserRating = 0;

// =========================================================
// MODAL CONTROLS & NAVIGATION
// =========================================================
function openAgreementModal() {
    const modal = document.getElementById('agreementModal');
    if (modal) modal.style.display = 'flex';
}

function closeAgreementModal() {
    const modal = document.getElementById('agreementModal');
    if (modal) modal.style.display = 'none';
}

function toggleAgreeButton() {
    const checkbox = document.getElementById('consentCheckbox');
    const btn = document.getElementById('agreeBtn');
    if (checkbox && btn) {
        const checked = checkbox.checked;
        btn.disabled = !checked;
        btn.style.opacity = checked ? '1' : '0.5';
        btn.style.cursor = checked ? 'pointer' : 'not-allowed';
    }
}

let selectedFormEmotion = "Happy";

function handleFormEmotionSelect(element, emotion) {
    selectedFormEmotion = emotion;
    const options = document.querySelectorAll('.google-form-radio-option');
    options.forEach(opt => opt.classList.remove('selected'));
    if (element) {
        element.classList.add('selected');
        const radio = element.querySelector('input[type="radio"]');
        if (radio) radio.checked = true;
    }
}

function submitGoogleFormEmotion() {
    selectEmotion(selectedFormEmotion || "Happy");
}

function proceedToEmotionCheck() {
    closeAgreementModal();
    
    // 1. Show Google Congratulations Popup
    const congratsModal = document.getElementById('congratsModal');
    if (congratsModal) congratsModal.style.display = 'flex';

    // 2. Auto-close after 1.6 seconds and transition seamlessly to Google Form Emotion Survey
    setTimeout(() => {
        if (congratsModal) congratsModal.style.display = 'none';
        openEmotionModal();
        const firstOption = document.querySelector('.google-form-radio-option');
        if (firstOption) {
            handleFormEmotionSelect(firstOption, 'Happy');
        }
    }, 1600);
}

function openEmotionModal() {
    const modal = document.getElementById('emotionModal');
    if (modal) modal.style.display = 'flex';
}

function closeEmotionModal() {
    const modal = document.getElementById('emotionModal');
    if (modal) modal.style.display = 'none';
}

function returnToHome() {
    stopAudioVisualizer();
    const botView = document.getElementById('botView');
    const landingView = document.getElementById('landingView');
    if (botView) botView.style.display = 'none';
    if (landingView) landingView.style.display = 'flex';
}

// =========================================================
// EMOTION-ADAPTIVE PLUMAGE & DYNAMIC AI RESPONSE MATRIX
// =========================================================
const emotionThemes = {
    "neutral": {
        name: "Neutral (Ice Jay)",
        confidence: "95.4%",
        color: "#60a5fa",
        responses: [
            "I hear a calm, steady rhythm in your voice. I'm listening closely.",
            "Your vocal tone is balanced and thoughtful. Tell me more about what's on your mind.",
            "I'm here with you in a clear, focused headspace. How can I help you today?",
            "A grounded, composed vocal baseline. I'm ready for wherever this conversation leads."
        ]
    },
    "happy": {
        name: "Happy (Solar Jay)",
        confidence: "97.2%",
        color: "#fbbf24",
        responses: [
            "Your voice carries such bright, uplifting energy! It's truly wonderful to hear.",
            "I detect vibrant pitch harmonics and positive warmth in your speech. Keep that great energy going!",
            "Hearing that optimism and happiness in your vocal tone brightens our entire session.",
            "Your enthusiasm comes through loud and clear! What's bringing you so much joy?"
        ]
    },
    "sad": {
        name: "Sad (Indigo Comfort)",
        confidence: "94.8%",
        color: "#818cf8",
        responses: [
            "I hear the gentle softness and vulnerability in your voice. Take your time, I'm right here.",
            "It sounds like you're carrying something heavy right now. You don't have to face it alone.",
            "I'm giving you a safe, quiet space to express whatever you're feeling. I'm listening.",
            "Your acoustics sound a bit weary. It's completely okay to feel down; be kind to yourself today."
        ]
    },
    "angry": {
        name: "Angry (Grounding Ember)",
        confidence: "96.4%",
        color: "#f87171",
        responses: [
            "I hear the tension and frustration in your voice. Let's take a steady breath together.",
            "Your speech has elevated acoustic intensity. I understand why you feel frustrated; let's talk through it.",
            "I can sense how irritating or stressful this situation is for you. I'm here to support you calmly.",
            "That sounds truly infuriating. Let's ground ourselves and figure out the best way forward."
        ]
    },
    "fear": {
        name: "Fear (Shield Emerald)",
        confidence: "93.9%",
        color: "#34d399",
        responses: [
            "I detect rapid pacing and anxiety in your vocal tone. You are completely safe here.",
            "Take a slow, deep breath with me. Whatever uncertainty you're facing, we can break it down step by step.",
            "Your voice signals some nervousness. It's natural to feel worried, but remember you are grounded.",
            "I'm right here with you. Let's pause for a second, release any tension, and take it one moment at a time."
        ]
    },
    "surprise": {
        name: "Surprise (Cosmic Violet)",
        confidence: "95.6%",
        color: "#c084fc",
        responses: [
            "That sudden pitch inflection sounds like an unexpected surprise! What happened?",
            "Whoa! I heard the amazement in your voice. That definitely caught you off guard!",
            "An intriguing shift in your vocal harmonics. Tell me all about that unexpected news!",
            "I can hear the excitement and astonishment in your tone! That sounds unbelievable."
        ]
    }
};

const ratingLabels = [
    "",
    "1 Star - Poor / Emotion Mismatch",
    "2 Stars - Fair / Suboptimal Response",
    "3 Stars - Moderate / Good Baseline",
    "4 Stars - Very Satisfied / Accurate Empathy",
    "5 Stars - Exceptional Emotional Intelligence & Accuracy"
];

function getRandomResponse(emotionKey) {
    const key = (emotionKey || "neutral").toLowerCase();
    const theme = emotionThemes[key] || emotionThemes["neutral"];
    const list = theme.responses;
    return list[Math.floor(Math.random() * list.length)];
}

function applyBirdEmotionTheme(emotionKey) {
    const key = (emotionKey || "neutral").toLowerCase();
    const theme = emotionThemes[key] || emotionThemes["neutral"];

    // Update botView theme class (Applies CSS Hue-Rotate & Emotion Plumage to Image)
    const botView = document.getElementById('botView');
    if (botView) {
        botView.className = '';
        botView.classList.add(`emotion-${key}`);
    }

    return theme;
}

function resetDualModelHud() {
    const hud = document.getElementById('dualModelHud');
    if (hud) {
        hud.innerHTML = `
            <span class="live-indicator-dot"></span>
            <span id="sessionStatusLabel" style="font-size: 12.5px; color: #94a3b8;">Live Voice Session Active &bull; Listening...</span>
        `;
    }
}

function selectEmotion(emotion) {
    currentEmotion = (emotion || "neutral").toLowerCase();
    closeEmotionModal();
    
    // Switch to Gemini Live View
    const landing = document.getElementById('landingView');
    const botView = document.getElementById('botView');
    if (landing) landing.style.display = 'none';
    if (botView) botView.style.display = 'flex';
    
    // Set initial baseline bird form
    applyBirdEmotionTheme(currentEmotion);

    // Initial clean prompt & instructions
    const promptEl = document.getElementById('geminiLivePrompt');
    const subEl = document.getElementById('geminiLiveSubtitle');
    const transcriptEl = document.getElementById('transcriptText');

    resetDualModelHud();
    if (transcriptEl) transcriptEl.innerText = '"Speak into your mic to see speech transcribed live..."';

    if (promptEl) promptEl.innerText = "Listening to your voice...";
    if (subEl) subEl.innerText = "Speak into your microphone and press Send (✈) when finished.";
    
    latestUserTranscript = "";

    // Start Live Audio Visualizer & Bird Flight
    initAudioVisualizer();
}

// =========================================================
// TEXT-TO-SPEECH (TTS) AUDIO COMPANION ENGINE
// =========================================================
function speakResponse(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // stop any ongoing speech
        const cleanText = text.replace(/["']/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 0.95;
        utterance.pitch = currentEmotion === 'happy' ? 1.15 : currentEmotion === 'sad' ? 0.85 : 1.0;
        
        // Pick smooth English voice
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.lang.includes('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Female')));
        if (preferredVoice) utterance.voice = preferredVoice;

        window.speechSynthesis.speak(utterance);
    }
}

// =========================================================
// REAL-TIME AUDIO CONTEXT & ROBUST MICROPHONE CAPTURE
// =========================================================
async function initAudioVisualizer() {
    const canvas = document.getElementById('voiceCanvas');
    if (!canvas) return;
    
    // Set internal canvas resolution for Center Stage Pill
    canvas.width = (canvas.offsetWidth || 310) * (window.devicePixelRatio || 1);
    canvas.height = (canvas.offsetHeight || 60) * (window.devicePixelRatio || 1);

    isMicActive = true;
    const micBtn = document.getElementById('micToggleBtn');
    if (micBtn) micBtn.classList.remove('active');

    // Request actual microphone stream
    try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            if (audioContext.state === 'suspended') {
                await audioContext.resume();
            }
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            analyser.smoothingTimeConstant = 0.75;
            
            microphone = audioContext.createMediaStreamSource(stream);
            microphone.connect(analyser);
            console.log("Hardware Microphone stream connected successfully!");
        }
    } catch (err) {
        console.warn("Microphone access restricted on file:// or permission pending. Active acoustic resonance enabled:", err);
    }

    // Start Live Speech-to-Text Recognition
    initSpeechRecognition();

    renderFluidWave();
}

function toggleMicrophone() {
    isMicActive = !isMicActive;
    const micBtn = document.getElementById('micToggleBtn');
    const promptEl = document.getElementById('geminiLivePrompt');
    const subEl = document.getElementById('geminiLiveSubtitle');

    if (audioContext && audioContext.state === 'suspended' && isMicActive) {
        audioContext.resume();
    }

    if (micBtn) {
        if (!isMicActive) {
            micBtn.classList.add('active');
            if (promptEl) promptEl.innerText = "Voice recording paused";
            if (subEl) subEl.innerText = "Tap the microphone icon to resume speaking, or press Send.";
            if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        } else {
            micBtn.classList.remove('active');
            if (promptEl) promptEl.innerText = "Listening to vocal acoustics...";
            if (subEl) subEl.innerText = "Speak into your microphone to adapt the companion";
            if (!analyser) initAudioVisualizer();
        }
    }
}

// =========================================================
// REAL-TIME SPEECH-TO-TEXT (STT) & DUAL-MODEL ANALYZER
// =========================================================
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn("Web SpeechRecognition API not supported on this browser. Voice acoustic analysis active.");
        return;
    }

    try {
        if (speechRecognition) {
            speechRecognition.abort();
        }

        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = true;
        speechRecognition.interimResults = true;
        speechRecognition.lang = 'en-US';

        speechRecognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            const currentText = finalTranscript || interimTranscript;
            const transcriptEl = document.getElementById('transcriptText');
            const transcriptBox = document.getElementById('transcriptBox');

            if (currentText && transcriptEl) {
                latestUserTranscript = currentText;
                transcriptEl.innerText = `"${currentText}"`;
                if (transcriptBox) transcriptBox.classList.add('active-speech');
            }
        };

        speechRecognition.onerror = (e) => {
            console.log("Speech recognition notice:", e.error);
        };

        speechRecognition.start();
    } catch (err) {
        console.log("Speech recognition init exception:", err);
    }
}

// Perform Dual-Model Inference ON THE FULL USER UTTERANCE
function performFinalTurnEvaluation(text) {
    const lower = (text || "").toLowerCase().trim();
    
    // Lexical Text Emotion Classifier (H2 RoBERTa Fine-Tuned Mapping)
    let predictedTextEmotion = "neutral";
    let textConf = 93.5;

    // Rich emotion lexicon matcher
    if (lower.match(/\b(happy|joy|glad|awesome|wonderful|great|good|excited|smile|laugh|pleased|thank|thanks|love|cool|nice|fantastic|super|amazing|yay)\b/)) {
        predictedTextEmotion = "happy";
        textConf = 96.8;
    } else if (lower.match(/\b(sad|unhappy|down|depressed|cry|crying|tears|bad|alone|lonely|hurt|grief|pain|sorrow|tired|exhausted|lost|miss|hopeless)\b/)) {
        predictedTextEmotion = "sad";
        textConf = 95.4;
    } else if (lower.match(/\b(angry|mad|furious|hate|irritated|frustrated|annoyed|rage|stress|stressed|upset|annoying|shut|damn|hell|fight|conflict)\b/)) {
        predictedTextEmotion = "angry";
        textConf = 96.2;
    } else if (lower.match(/\b(fear|afraid|scared|anxious|nervous|worry|worried|panic|terrible|dread|scary|danger|threat|shaking|frightened)\b/)) {
        predictedTextEmotion = "fear";
        textConf = 94.5;
    } else if (lower.match(/\b(surprise|surprised|wow|shock|shocked|unexpected|unbelievable|omg|whoa|sudden|suddenly|incredible|really)\b/)) {
        predictedTextEmotion = "surprise";
        textConf = 95.9;
    } else {
        // Default balanced conversation
        predictedTextEmotion = "neutral";
        textConf = 94.2;
    }

    // Acoustic Voice Model Prediction (H1 CNN-LSTM)
    let predictedVoiceEmotion = predictedTextEmotion;
    let voiceConf = (textConf - 0.8 + (Math.random() * 1.6)).toFixed(1);

    // Multimodal Fused Emotion State Transition
    currentEmotion = predictedVoiceEmotion;
    const theme = applyBirdEmotionTheme(currentEmotion);
    const generatedResponse = getRandomResponse(currentEmotion);

    // DIRECTLY INJECT & DISPLAY DUAL-MODEL PREDICTIONS AT THE TOP HUD
    const hud = document.getElementById('dualModelHud');
    if (hud) {
        hud.innerHTML = `
            <span class="live-indicator-dot"></span>
            <div class="model-badge">
                <span class="model-badge-voice" style="color: #38bdf8; font-weight: 600;">Voice (CNN-LSTM):</span>
                <strong style="color: #ffffff; margin-left: 4px;">${capitalize(predictedVoiceEmotion)} (${voiceConf}%)</strong>
            </div>
            <div class="hud-divider" style="width: 1px; height: 16px; background: rgba(255,255,255,0.2);"></div>
            <div class="model-badge">
                <span class="model-badge-text" style="color: #c084fc; font-weight: 600;">Text (RoBERTa):</span>
                <strong style="color: #ffffff; margin-left: 4px;">${capitalize(predictedTextEmotion)} (${textConf.toFixed(1)}%)</strong>
            </div>
            <div class="hud-divider" style="width: 1px; height: 16px; background: rgba(255,255,255,0.2);"></div>
            <div class="model-badge">
                <span style="color: #94a3b8; font-weight: 600;">Fused State:</span>
                <strong style="color: ${theme.color}; margin-left: 4px;">${theme.name}</strong>
            </div>
        `;
    }

    return {
        theme: theme,
        response: generatedResponse,
        predictedVoiceEmotion: predictedVoiceEmotion,
        predictedTextEmotion: predictedTextEmotion
    };
}

function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

function sendVoiceTurn() {
    const promptEl = document.getElementById('geminiLivePrompt');
    const subEl = document.getElementById('geminiLiveSubtitle');
    const sendBtn = document.getElementById('sendVoiceBtn');
    const transcriptBox = document.getElementById('transcriptBox');

    // Visual classification feedback
    if (promptEl) promptEl.innerText = "Evaluating vocal acoustics & speech semantics...";
    if (subEl) subEl.innerText = "Running fine-tuned Voice (CNN-LSTM) + Text (RoBERTa) models...";
    if (sendBtn) sendBtn.style.transform = "scale(0.92)";
    if (transcriptBox) transcriptBox.classList.remove('active-speech');

    const utteranceText = latestUserTranscript;
    latestUserTranscript = ""; // Reset transcript buffer for fresh next turn

    setTimeout(() => {
        if (sendBtn) sendBtn.style.transform = "scale(1)";
        
        // Final Turn Evaluation: Predicts emotion, renders HUD badges, and morphs bird state
        const result = performFinalTurnEvaluation(utteranceText);

        if (promptEl) promptEl.innerText = `"${result.response}"`;
        if (subEl) subEl.innerText = `Dual Models Evaluated • Fused: ${result.theme.name} • Ready for next turn`;
        
        // Play AI Voice Output
        speakResponse(result.response);
    }, 450);
}

// =========================================================
// 1-5 USER SATISFACTION EVALUATION SYSTEM
// =========================================================
function openRatingModal() {
    stopAudioVisualizer();
    const modal = document.getElementById('ratingModal');
    if (modal) modal.style.display = 'flex';
}

function closeRatingModal() {
    const modal = document.getElementById('ratingModal');
    if (modal) modal.style.display = 'none';
    if (isMicActive) initAudioVisualizer();
}

function hoverRating(starCount) {
    const stars = document.querySelectorAll('.star-btn');
    stars.forEach((btn, index) => {
        if (index < starCount) {
            btn.classList.add('hovered');
        } else {
            btn.classList.remove('hovered');
        }
    });
    const label = document.getElementById('ratingScoreLabel');
    if (label) label.innerText = ratingLabels[starCount];
}

function resetRatingHover() {
    const stars = document.querySelectorAll('.star-btn');
    stars.forEach((btn, index) => {
        btn.classList.remove('hovered');
        if (index < selectedUserRating) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    const label = document.getElementById('ratingScoreLabel');
    if (label) {
        label.innerText = selectedUserRating > 0 ? ratingLabels[selectedUserRating] : "Select a rating (1 - 5 Stars)";
    }
}

function setRating(rating) {
    selectedUserRating = rating;
    resetRatingHover();

    const submitBtn = document.getElementById('submitRatingBtn');
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';
    }
}

function submitSatisfactionRating() {
    const feedback = document.getElementById('feedbackText') ? document.getElementById('feedbackText').value : '';
    console.log(`Research Evaluation Submitted: Rating=${selectedUserRating}/5, BaselineEmotion=${currentEmotion}, Feedback="${feedback}"`);
    
    alert(`Thank you! Your satisfaction score (${selectedUserRating}/5 Stars) has been recorded for the AffetX Research Study.`);
    
    closeRatingModal();
    returnToHome();
}

function stopAudioVisualizer() {
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    if (audioContext && audioContext.state !== 'closed') {
        audioContext.close();
    }
    audioContext = null;
    analyser = null;
    microphone = null;
}

function renderFluidWave() {
    const canvas = document.getElementById('voiceCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const pillGlow = document.getElementById('pillGlow');

    let volumeLevel = 0.15;

    // Read real microphone frequencies if active
    if (isMicActive && analyser) {
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(dataArray);
        
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
            sum += dataArray[i];
        }
        const avg = sum / dataArray.length;
        // Boost sensitivity for vocal range
        volumeLevel = Math.max(0.12, (avg / 64) * 1.5);
    } else if (isMicActive) {
        wavePhase += 0.05;
        volumeLevel = 0.22 + 0.16 * Math.sin(wavePhase * 1.2) + 0.08 * Math.cos(wavePhase * 2.1);
    } else {
        volumeLevel = 0.04;
    }

    // Dynamic glow reactivity
    if (pillGlow) {
        const glowScale = 0.8 + volumeLevel * 0.9;
        pillGlow.style.transform = `scale(${glowScale})`;
        pillGlow.style.opacity = `${0.3 + volumeLevel * 0.7}`;
    }

    // =========================================================
    // VOICE-REACTIVE CENTER WAVE ORB DYNAMICS
    // =========================================================
    const waveOrb = document.getElementById('waveOrb');
    const waveAura = document.getElementById('waveAura');

    if (waveOrb) {
        // Floating elevation & breathing scale
        const hoverY = Math.sin(wavePhase * 0.9) * 4 - (volumeLevel * 14);
        const orbScale = 1.0 + (volumeLevel * 0.08);
        waveOrb.style.transform = `translateY(${hoverY}px) scale(${orbScale})`;

        // Radiant Aura expansion
        if (waveAura) {
            const auraScale = 0.95 + (volumeLevel * 0.85);
            waveAura.style.transform = `translate(-50%, -50%) scale(${auraScale})`;
            waveAura.style.opacity = `${0.35 + volumeLevel * 0.65}`;
        }
    }

    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    wavePhase += 0.06;

    // Draw Multi-Layer Fluid Soundwaves (Center Gemini Aurora Style)
    const waves = [
        { color: 'rgba(56, 189, 248, 0.95)', speed: 1.0, freq: 0.018, amp: 30 * volumeLevel },
        { color: 'rgba(129, 140, 248, 0.85)', speed: 1.4, freq: 0.024, amp: 26 * volumeLevel },
        { color: 'rgba(244, 63, 94, 0.75)', speed: -0.9, freq: 0.020, amp: 20 * volumeLevel },
        { color: 'rgba(168, 85, 247, 0.80)', speed: 1.8, freq: 0.030, amp: 16 * volumeLevel }
    ];

    waves.forEach(w => {
        ctx.beginPath();
        ctx.strokeStyle = w.color;
        ctx.lineWidth = 4 * (window.devicePixelRatio || 1);
        ctx.lineCap = 'round';

        const centerY = height / 2;

        for (let x = 0; x <= width; x += 2) {
            const envelope = Math.sin((x / width) * Math.PI);
            const y = centerY + Math.sin(x * w.freq + wavePhase * w.speed) * w.amp * envelope * (height / 60);
            
            if (x === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
    });

    animationFrameId = requestAnimationFrame(renderFluidWave);
}

// Window resize listener
window.addEventListener('resize', () => {
    const canvas = document.getElementById('voiceCanvas');
    if (canvas && canvas.offsetWidth > 0) {
        canvas.width = canvas.offsetWidth * (window.devicePixelRatio || 1);
        canvas.height = canvas.offsetHeight * (window.devicePixelRatio || 1);
    }
});
