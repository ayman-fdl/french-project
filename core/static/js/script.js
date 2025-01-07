document.addEventListener("DOMContentLoaded", function () {
    const inputContainer = document.querySelector(".input-container");
    const sendMessageButton = document.querySelector("button[onclick='sendMessage()']");
    const userInput = document.getElementById("user-input");

     userInput.focus();

    // Au chargement, positionne le conteneur au centre
    inputContainer.classList.add("input-container-center");

    // Fonction pour déplacer le conteneur en bas
    function repositionInputContainer() {
        inputContainer.classList.remove("input-container-center"); // Retirer la classe de centrage
        inputContainer.classList.add("input-container-bottom");   // Ajouter la classe pour le bas

        // Sélectionne la div avec l'ID "logo-id"
        const logoDiv = document.getElementById("logo-id");

        // Vérifie si l'élément existe pour éviter les erreurs
        if (logoDiv) {
            logoDiv.style.display = "none"; // Masque la div
        }
    }

    // Événement pour le clic sur le bouton d'envoi
    sendMessageButton.addEventListener("click", function () {
        repositionInputContainer(); // Déplacer le conteneur en bas
    });

    // Événement pour la touche Entrée
    userInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Évite le comportement par défaut
            repositionInputContainer(); // Déplacer le conteneur en bas
        }
    });
});





// Function to send a message
function sendMessage() {
    const input = document.getElementById("user-input");
    const chatContainer = document.getElementById("chat-container");
    const userMessage = input.value.trim();

    if (userMessage) {
        let texte = userMessage.replace(/\/texte\s/g, "");
        if (userMessage.startsWith("/texte")) {
            localStorage.setItem("sharedData", texte);
        }
        // Display the user's message in the chat container
        displayUserMessage(userMessage, chatContainer);

        // Clear the input field
        input.value = "";

        // Scroll to the bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Send the message to the backend via fetch
        sendToBackend(userMessage, chatContainer);
    }
}

// Function to send the message to the backend
function sendToBackend(userMessage, chatContainer) {
    fetch('/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userMessage })
    })
    .then(response => response.json())
    .then(data => handleResponse(data, chatContainer))
    .catch(error => {
        console.error('Error:', error);
        displayBotMessage("Une erreur est survenue. Veuillez réessayer.", chatContainer);
    });
}

// Function to display the user's message
function displayUserMessage(userMessage, chatContainer) {
    const userBubble = document.createElement("div");
    userBubble.className = "message user";
    userBubble.innerHTML = `<div class="bubble">${userMessage}</div>`;
    chatContainer.appendChild(userBubble);
}

function displayBotMessage(botMessage, chatContainer) {
    const botBubble = document.createElement("div");
    const profilePic = `<div class="profile-pic">
                            <img src="../static/img/logo/logo0.png" alt="Bot Profile" class="bot-profile">
                        </div>`;
    botBubble.className = "message bot";
    botBubble.innerHTML = `${profilePic}<div class="bubble"></div>`;
    chatContainer.appendChild(botBubble);

    const bubble = botBubble.querySelector(".bubble");

    // Diviser le message par la balise <table>
    const parts = botMessage.split("<table>");
    const firstPart = parts[0]; // Texte avant la table (peut contenir du HTML)
    const secondPart = parts[1] ? `<table>${parts[1]}` : null; // Table si elle existe

    let tempContainer = document.createElement("div");
    tempContainer.innerHTML = firstPart; // Charger le HTML de la première partie
    const childNodes = Array.from(tempContainer.childNodes); // Obtenir les nœuds enfants

    let nodeIndex = 0;
    let charIndex = 0;

    function displayFirstPart() {
        const chatContainer = document.getElementById("chat-container");
        chatContainer.scrollTop = chatContainer.scrollHeight;
        if (nodeIndex < childNodes.length) {
            const currentNode = childNodes[nodeIndex];
            if (currentNode.nodeType === Node.TEXT_NODE) {
                // Si le nœud est un texte, afficher progressivement
                if (charIndex < currentNode.textContent.length) {
                    bubble.innerHTML += currentNode.textContent[charIndex];
                    charIndex++;
                    setTimeout(displayFirstPart, 1); // Intervalle entre les lettres
                } else {
                    // Une fois le texte terminé, passer au nœud suivant
                    nodeIndex++;
                    charIndex = 0;
                    displayFirstPart();
                }
            } else {
                // Si le nœud est une balise HTML, l'ajouter directement
                bubble.innerHTML += currentNode.outerHTML;
                nodeIndex++;
                displayFirstPart();
            }
        } else {
            // Une fois la première partie terminée, afficher la table si elle existe
            if (secondPart) {
                bubble.innerHTML += secondPart;
            }
            chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom
        }
    }

    displayFirstPart();

    // Vérifie si le message contient une table avec des commandes
    if (botMessage.includes("Votre texte est traité avec succès")) {
        const dashboardButton = document.querySelector(".dash_btn");
        if (dashboardButton) {
            dashboardButton.classList.remove("dash_btn");
            dashboardButton.classList.add("dash_btn_act");
        }

        // Sélectionne l'élément avec l'ID "dash_a"
        const dashElement = document.getElementById("dash_a");
        if (dashElement) {
            dashElement.href = "dashboard";
            dashElement.target = "_blank";
            dashElement.style.cursor = "pointer";
        }
    }
}

// Handle the response from the backend
function handleResponse(data, chatContainer) {
    if (data.status === 'success') {
        displayBotMessage(data.processed_input, chatContainer);
    } else {
        displayBotMessage("Erreur dans le traitement de l'input.", chatContainer);
    }
}

// Event listener for the 'Enter' key to send the message
function checkEnter(event) {
    if (event.keyCode === 13) { // Check if the key is "Enter"
        sendMessage();
        event.preventDefault(); // Prevent default action (e.g., form submission)
    } else if (event.key === "Tab" && suggestionDiv.textContent) { // "Tab"
        event.preventDefault();
        userInput.value = suggestionDiv.textContent.replace("# Tapez Tab pour compléter", "");
        suggestionDiv.textContent = ""; // Efface la suggestion après complétion
      }
}
////////////////////////////////////////////
// SEND IMAGE
////////////////////////////////////////////
function sendImage() {
    const imageInput = document.getElementById("image-input");
    imageInput.click();  // Déclencher l'input de fichier
}

function previewImage(event) {
    const inputContainer = document.querySelector(".input-container");
    inputContainer.classList.remove("input-container-center"); // Retirer la classe de centrage
    inputContainer.classList.add("input-container-bottom");   // Ajouter la classe pour le bas

    // Sélectionne la div avec l'ID "logo-id"
    const logoDiv = document.getElementById("logo-id");

    // Vérifie si l'élément existe pour éviter les erreurs
    if (logoDiv) {
        logoDiv.style.display = "none"; // Masque la div
    }

    const file = event.target.files[0]; // Obtenir le fichier sélectionné
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const imageSrc = e.target.result; // Données base64 de l'image
            // Afficher l'image dans la fenêtre de chat côté utilisateur
            displayUserImageMessage(imageSrc);

            // Envoyer l'image au backend
            sendImageToBackend(imageSrc);
        };

        reader.readAsDataURL(file); // Lire le fichier image et le convertir en URL de données
    } else {
        alert("Veuillez choisir un fichier image.");
    }

    event.target.value = "";
}

// Fonction pour envoyer l'image au backend
function sendImageToBackend(imageSrc) {
    const chatContainer = document.getElementById("chat-container");
    fetch('/send_image/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_data: imageSrc })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Image envoyée avec succès');
            // Afficher un message du bot avec le texte OCR extrait
            displayBotMessage("Votre texte est : <br>" + data.processed_input, chatContainer);
            let texte = data.processed_input
            texte = texte.split("<table>")[0];
            localStorage.setItem("sharedData", texte);
        } else {
            console.log('Erreur lors de l\'envoi de l\'image');
            // Afficher un message d'erreur du bot
            displayBotMessage("Une erreur est survenue lors du traitement de l'image.", chatContainer);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        // Afficher un message d'erreur du bot
        displayBotMessage("Une erreur est survenue. Veuillez réessayer.", chatContainer);
    });
}

// Fonction pour afficher l'image dans la fenêtre de chat côté utilisateur
function displayUserImageMessage(imageSrc) {
    const chatContainer = document.getElementById("chat-container");
    const userBubble = document.createElement("div");
    userBubble.className = "message user";

    // Afficher l'image avec la classe pour limiter la taille à 40% de la largeur
    userBubble.innerHTML = `<div class="image-bubble"><img src="${imageSrc}" alt="Image" style="max-width: 80%; height: auto; border-radius: 10px; float: right;"></div>`;
    chatContainer.appendChild(userBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Faire défiler la fenêtre de chat
}

////////////////////////////////////////////

document.getElementById("exportPdfButton").addEventListener("click", function () {
    const dashboard = document.body;

    html2canvas(dashboard, {scale: 2, useCORS: true}).then(canvas => {
        const imgData = canvas.toDataURL("image/png");

        const imgWidth = canvas.width;
        const imgHeight = canvas.height;

        const pdf = new jspdf.jsPDF('p', 'px', [imgWidth, imgHeight]);

        pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);

        pdf.save("dashboard.pdf");
    });
});


////////////////////////////////////////////
function compterTexte(texte) {
            let mots = texte.trim().split(/\s+/).filter(word => word.length > 0).length;
            const phrases = texte.split(/[.!?]/).filter(sentence => sentence.trim().length > 0).length;

            document.getElementById("resultatMots").innerText = `${mots}`;
            document.getElementById("resultatPhrases").innerText = `${phrases}`;
            document.getElementById("resultatTextes").innerText = `${texte}`;
        }

function loadData(){
    const sharedData = localStorage.getItem("sharedData");
    compterTexte(sharedData)
}

