// Function to send a message
function sendMessage() {
    const input = document.getElementById("user-input");
    const chatContainer = document.getElementById("chat-container");
    const userMessage = input.value.trim();

    if (userMessage) {
        let texte = userMessage.replace(/\/texte\s/g, "");
        localStorage.setItem("sharedData", texte);
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

// Function to display the bot's response
function displayBotMessage(botMessage, chatContainer) {
    const botBubble = document.createElement("div");
    botBubble.className = "message bot";
    botBubble.innerHTML = `<div class="bubble">${botMessage}</div>`;
    chatContainer.appendChild(botBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom
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


// document.getElementById("resultatMots").innerText = userMessage;
// document.getElementById("resultatPhrases").innerText = "Nombre de phrases :";