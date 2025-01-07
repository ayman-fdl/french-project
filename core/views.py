from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from groq import Groq
import base64
from io import BytesIO
from PIL import Image

import ocr
import resultat
import correction
import claude

import utils

# Use settings to get API key
api_key = settings.API_KEY

check = 0
output_json = ""
# output_json = {
#               "output": {
#                 "Grammaire": {
#                   "Sujets": {
#                     "Total": 15,
#                     "Details": {
#                       "un vieil homme": 1,
#                       "il": 7,
#                       "son télescope": 1,
#                       "une lumière étrange": 1,
#                       "cette idée": 1,
#                       "les étoiles": 1,
#                       "son chat noir": 1,
#                       "le ciel": 1,
#                       "l'attente": 1
#                     }
#                   },
#                   "Verbes": {
#                     "Total": 22,
#                     "Par Temps": {
#                       "Imparfait": {
#                         "Total": 6,
#                         "Verbes": [
#                           {"Forme Conjuguee": "observait", "Infinitif": "observer", "Voix": "active"},
#                           {"Forme Conjuguee": "s'efforçait", "Infinitif": "s'efforcer", "Voix": "active"},
#                           {"Forme Conjuguee": "se demandait", "Infinitif": "se demander", "Voix": "active"},
#                           {"Forme Conjuguee": "dormait", "Infinitif": "dormir", "Voix": "active"},
#                           {"Forme Conjuguee": "faisait", "Infinitif": "faire", "Voix": "active"},
#                           {"Forme Conjuguee": "l'enflammait", "Infinitif": "enflammer", "Voix": "active"}
#                         ]
#                       },
#                       "Passé composé": {
#                         "Total": 2,
#                         "Verbes": [
#                           {"Forme Conjuguee": "avait été acheté", "Infinitif": "acheter", "Voix": "passive"},
#                           {"Forme Conjuguee": "n'avait rien trouvé", "Infinitif": "trouver", "Voix": "active"}
#                         ]
#                       },
#                       "Passé simple": {
#                         "Total": 4,
#                         "Verbes": [
#                           {"Forme Conjuguee": "apparut", "Infinitif": "apparaître", "Voix": "active"},
#                           {"Forme Conjuguee": "nota", "Infinitif": "noter", "Voix": "active"},
#                           {"Forme Conjuguee": "sembla", "Infinitif": "sembler", "Voix": "active"},
#                           {"Forme Conjuguee": "décida", "Infinitif": "décider", "Voix": "active"}
#                         ]
#                       },
#                       "Présent": {
#                         "Total": 2,
#                         "Verbes": [
#                           {"Forme Conjuguee": "reste", "Infinitif": "rester", "Voix": "active"},
#                           {"Forme Conjuguee": "continuaient", "Infinitif": "continuer", "Voix": "active"}
#                         ]
#                       }
#                     },
#                     "Par mode": {
#                       "Indicatif": {
#                         "Total": 14
#                       },
#                       "Infinitif": {
#                         "Total": 4
#                       }
#                     }
#                   },
#                   "Champs Lexicaux": {
#                     "Astronomie": {
#                       "Total": 7,
#                       "Details": ["étoiles", "télescope", "univers", "cosmos", "lumière", "ciel", "découvertes"]
#                     },
#                     "Temps": {
#                       "Total": 6,
#                       "Details": ["chaque soir", "hier", "ce soir-là", "soudainement", "lendemain matin", "attente"]
#                     },
#                     "Émotions": {
#                       "Total": 4,
#                       "Details": ["fascination", "joie enfantine", "excitation", "espoir"]
#                     }
#                   },
#                   "Adjectifs": {
#                     "Total": 12,
#                     "Details": ["petit", "verdoyante", "vieil", "scintillantes", "bancale", "infini", "vaste", "étrange", "extraordinaire", "enfantine", "usée", "noir"]
#                   },
#                   "Adverbes": {
#                     "Total": 4,
#                     "Details": {
#                       "délicatement": 1,
#                       "soudainement": 1,
#                       "soigneusement": 1,
#                       "profondément": 1
#                     }
#                   },
#                   "Prépositions": {
#                     "Total": 8,
#                     "Details": {
#                       "sur": 2,
#                       "dans": 2,
#                       "avec": 1,
#                       "à": 2,
#                       "de": 1
#                     }
#                   },
#                   "Conjonctions de coordination": {
#                     "Total": 4,
#                     "Details": {
#                       "mais": 2,
#                       "car": 1,
#                       "et": 1
#                     }
#                   },
#                   "Déterminants": {
#                     "Total": 18,
#                     "Par type": {
#                       "Définis": {
#                         "Total": 7,
#                         "Details": {
#                           "le": 2,
#                           "les": 2,
#                           "la": 2,
#                           "l'": 1
#                         }
#                       },
#                       "Indéfinis": {
#                         "Total": 4,
#                         "Details": {
#                           "un": 3,
#                           "une": 1
#                         }
#                       },
#                       "Possessifs": {
#                         "Total": 4,
#                         "Details": {
#                           "son": 3,
#                           "sa": 1
#                         }
#                       },
#                       "Démonstratifs": {
#                         "Total": 2,
#                         "Details": {
#                           "ce": 2
#                         }
#                       }
#                     }
#                   },
#                   "Compléments": {
#                     "Total": 15,
#                     "Par type": {
#                       "CCL": {
#                         "Total": 4,
#                         "Details": [
#                           "sur une colline verdoyante",
#                           "sur une table bancale",
#                           "dans le ciel",
#                           "à côté de lui"
#                         ]
#                       },
#                       "CCT": {
#                         "Total": 4,
#                         "Details": [
#                           "chaque soir",
#                           "hier",
#                           "ce soir-là",
#                           "le lendemain matin"
#                         ]
#                       },
#                       "CCM": {
#                         "Total": 3,
#                         "Details": [
#                           "avec fascination",
#                           "délicatement",
#                           "soigneusement"
#                         ]
#                       },
#                       "COD": {
#                         "Total": 4,
#                         "Details": [
#                           "les étoiles scintillantes",
#                           "l'univers infini",
#                           "ses observations",
#                           "l'espoir"
#                         ]
#                       }
#                     }
#                   },
#                   "Types de discours": {
#                     "Total": 3,
#                     "Details": ["Narratif", "Descriptif", "Dialogué"]
#                   },
#                   "Figures de style": {
#                     "Total": 3,
#                     "Par type": {
#                       "Personnification": {
#                         "Total": 1,
#                         "Details": ["les étoiles continuaient de briller, indifférentes à sa passion"]
#                       },
#                       "Métaphore": {
#                         "Total": 1,
#                         "Details": ["sembla éteindre l'espoir"]
#                       },
#                       "Hyperbole": {
#                         "Total": 1,
#                         "Details": ["l'univers infini"]
#                       }
#                     }
#                   },
#                   "Registres linguistiques": {
#                     "Total": 2,
#                     "Details": ["Soutenu", "Courant"]
#                   },
#                   "Type de phrases": {
#                     "Total": 12,
#                     "Par forme": {
#                       "Phrases positives": {
#                         "Total": 9
#                       },
#                       "Phrases négatives": {
#                         "Total": 1
#                       },
#                       "Phrases interrogatives": {
#                         "Total": 2
#                       }
#                     },
#                     "Par structure": {
#                       "Phrases nominales": {
#                         "Total": 0
#                       },
#                       "Phrases verbales": {
#                         "Total": 12
#                       }
#                     },
#                     "Par voix": {
#                       "Passive": {
#                         "Total": 1
#                       },
#                       "Active": {
#                         "Total": 13
#                       }
#                     },
#                     "Par complexité": {
#                       "Phrases simples": {
#                         "Total": 5
#                       },
#                       "Phrases complexes": {
#                         "Total": 7,
#                         "Details": {
#                           "Coordination": 3,
#                           "Juxtaposition": 2,
#                           "Subordination": 2
#                         }
#                       }
#                     }
#                   }
#                 }
#               }
#             }

# Refactor Groq API call into a helper function for cleaner code
def get_groq_response(user_input):
    """Helper function to handle the Groq API call."""
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="llama3-groq-70b-8192-tool-use-preview",
            temperature=0.3,
            max_tokens=1024
        )
        # Return only the message content from the response
        return chat_completion.choices[0].message.content, None
    except Exception as e:
        # Catch any error and return it along with a None response
        return None, str(e)

@csrf_exempt
def result_json_view(request):
    global output_json
    return JsonResponse(output_json)

# View for rendering the index page
def index(request):
    return render(request, 'chatbot.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# View to handle user input and respond with Groq's API output
@csrf_exempt
def handle_input(request):
    output_res = "ERREUR !!"
    global check
    global output_json
    # output_string = """{
    #                       "output": {
    #                         "Grammaire": {
    #                           "Sujets": {
    #                             "Total": 15,
    #                             "Details": {
    #                               "un vieil homme": 1,
    #                               "il": 7,
    #                               "son télescope": 1,
    #                               "une lumière étrange": 1,
    #                               "cette idée": 1,
    #                               "les étoiles": 1,
    #                               "son chat noir": 1,
    #                               "le ciel": 1,
    #                               "l'attente": 1
    #                             }
    #                           },
    #                           "Verbes": {
    #                             "Total": 22,
    #                             "Par Temps": {
    #                               "Imparfait": {
    #                                 "Total": 6,
    #                                 "Verbes": [
    #                                   {"Forme Conjuguee": "observait", "Infinitif": "observer", "Voix": "active"},
    #                                   {"Forme Conjuguee": "s'efforçait", "Infinitif": "s'efforcer", "Voix": "active"},
    #                                   {"Forme Conjuguee": "se demandait", "Infinitif": "se demander", "Voix": "active"},
    #                                   {"Forme Conjuguee": "dormait", "Infinitif": "dormir", "Voix": "active"},
    #                                   {"Forme Conjuguee": "faisait", "Infinitif": "faire", "Voix": "active"},
    #                                   {"Forme Conjuguee": "l'enflammait", "Infinitif": "enflammer", "Voix": "active"}
    #                                 ]
    #                               },
    #                               "Passé composé": {
    #                                 "Total": 2,
    #                                 "Verbes": [
    #                                   {"Forme Conjuguee": "avait été acheté", "Infinitif": "acheter", "Voix": "passive"},
    #                                   {"Forme Conjuguee": "n'avait rien trouvé", "Infinitif": "trouver", "Voix": "active"}
    #                                 ]
    #                               },
    #                               "Passé simple": {
    #                                 "Total": 4,
    #                                 "Verbes": [
    #                                   {"Forme Conjuguee": "apparut", "Infinitif": "apparaître", "Voix": "active"},
    #                                   {"Forme Conjuguee": "nota", "Infinitif": "noter", "Voix": "active"},
    #                                   {"Forme Conjuguee": "sembla", "Infinitif": "sembler", "Voix": "active"},
    #                                   {"Forme Conjuguee": "décida", "Infinitif": "décider", "Voix": "active"}
    #                                 ]
    #                               },
    #                               "Présent": {
    #                                 "Total": 2,
    #                                 "Verbes": [
    #                                   {"Forme Conjuguee": "reste", "Infinitif": "rester", "Voix": "active"},
    #                                   {"Forme Conjuguee": "continuaient", "Infinitif": "continuer", "Voix": "active"}
    #                                 ]
    #                               }
    #                             },
    #                             "Par mode": {
    #                               "Indicatif": {
    #                                 "Total": 14
    #                               },
    #                               "Infinitif": {
    #                                 "Total": 4
    #                               }
    #                             }
    #                           },
    #                           "Champs Lexicaux": {
    #                             "Astronomie": {
    #                               "Total": 7,
    #                               "Details": ["étoiles", "télescope", "univers", "cosmos", "lumière", "ciel", "découvertes"]
    #                             },
    #                             "Temps": {
    #                               "Total": 6,
    #                               "Details": ["chaque soir", "hier", "ce soir-là", "soudainement", "lendemain matin", "attente"]
    #                             },
    #                             "Émotions": {
    #                               "Total": 4,
    #                               "Details": ["fascination", "joie enfantine", "excitation", "espoir"]
    #                             }
    #                           },
    #                           "Adjectifs": {
    #                             "Total": 12,
    #                             "Details": ["petit", "verdoyante", "vieil", "scintillantes", "bancale", "infini", "vaste", "étrange", "extraordinaire", "enfantine", "usée", "noir"]
    #                           },
    #                           "Adverbes": {
    #                             "Total": 4,
    #                             "Details": {
    #                               "délicatement": 1,
    #                               "soudainement": 1,
    #                               "soigneusement": 1,
    #                               "profondément": 1
    #                             }
    #                           },
    #                           "Prépositions": {
    #                             "Total": 8,
    #                             "Details": {
    #                               "sur": 2,
    #                               "dans": 2,
    #                               "avec": 1,
    #                               "à": 2,
    #                               "de": 1
    #                             }
    #                           },
    #                           "Conjonctions de coordination": {
    #                             "Total": 4,
    #                             "Details": {
    #                               "mais": 2,
    #                               "car": 1,
    #                               "et": 1
    #                             }
    #                           },
    #                           "Déterminants": {
    #                             "Total": 18,
    #                             "Par type": {
    #                               "Définis": {
    #                                 "Total": 7,
    #                                 "Details": {
    #                                   "le": 2,
    #                                   "les": 2,
    #                                   "la": 2,
    #                                   "l'": 1
    #                                 }
    #                               },
    #                               "Indéfinis": {
    #                                 "Total": 4,
    #                                 "Details": {
    #                                   "un": 3,
    #                                   "une": 1
    #                                 }
    #                               },
    #                               "Possessifs": {
    #                                 "Total": 4,
    #                                 "Details": {
    #                                   "son": 3,
    #                                   "sa": 1
    #                                 }
    #                               },
    #                               "Démonstratifs": {
    #                                 "Total": 2,
    #                                 "Details": {
    #                                   "ce": 2
    #                                 }
    #                               }
    #                             }
    #                           },
    #                           "Compléments": {
    #                             "Total": 15,
    #                             "Par type": {
    #                               "CCL": {
    #                                 "Total": 4,
    #                                 "Details": [
    #                                   "sur une colline verdoyante",
    #                                   "sur une table bancale",
    #                                   "dans le ciel",
    #                                   "à côté de lui"
    #                                 ]
    #                               },
    #                               "CCT": {
    #                                 "Total": 4,
    #                                 "Details": [
    #                                   "chaque soir",
    #                                   "hier",
    #                                   "ce soir-là",
    #                                   "le lendemain matin"
    #                                 ]
    #                               },
    #                               "CCM": {
    #                                 "Total": 3,
    #                                 "Details": [
    #                                   "avec fascination",
    #                                   "délicatement",
    #                                   "soigneusement"
    #                                 ]
    #                               },
    #                               "COD": {
    #                                 "Total": 4,
    #                                 "Details": [
    #                                   "les étoiles scintillantes",
    #                                   "l'univers infini",
    #                                   "ses observations",
    #                                   "l'espoir"
    #                                 ]
    #                               }
    #                             }
    #                           },
    #                           "Types de discours": {
    #                             "Total": 3,
    #                             "Details": ["Narratif", "Descriptif", "Dialogué"]
    #                           },
    #                           "Figures de style": {
    #                             "Total": 3,
    #                             "Par type": {
    #                               "Personnification": {
    #                                 "Total": 1,
    #                                 "Details": ["les étoiles continuaient de briller, indifférentes à sa passion"]
    #                               },
    #                               "Métaphore": {
    #                                 "Total": 1,
    #                                 "Details": ["sembla éteindre l'espoir"]
    #                               },
    #                               "Hyperbole": {
    #                                 "Total": 1,
    #                                 "Details": ["l'univers infini"]
    #                               }
    #                             }
    #                           },
    #                           "Registres linguistiques": {
    #                             "Total": 2,
    #                             "Details": ["Soutenu", "Courant"]
    #                           },
    #                           "Type de phrases": {
    #                             "Total": 12,
    #                             "Par forme": {
    #                               "Phrases positives": {
    #                                 "Total": 9
    #                               },
    #                               "Phrases négatives": {
    #                                 "Total": 1
    #                               },
    #                               "Phrases interrogatives": {
    #                                 "Total": 2
    #                               }
    #                             },
    #                             "Par structure": {
    #                               "Phrases nominales": {
    #                                 "Total": 0
    #                               },
    #                               "Phrases verbales": {
    #                                 "Total": 12
    #                               }
    #                             },
    #                             "Par voix": {
    #                               "Passive": {
    #                                 "Total": 1
    #                               },
    #                               "Active": {
    #                                 "Total": 13
    #                               }
    #                             },
    #                             "Par complexité": {
    #                               "Phrases simples": {
    #                                 "Total": 5
    #                               },
    #                               "Phrases complexes": {
    #                                 "Total": 7,
    #                                 "Details": {
    #                                   "Coordination": 3,
    #                                   "Juxtaposition": 2,
    #                                   "Subordination": 2
    #                                 }
    #                               }
    #                             }
    #                           }
    #                         }
    #                       }
    #                     }"""
    if request.method == 'POST':
        try:
            code = ["/menu", "/texte", "/bilan", "/verbe", "/sujet", "/champs_lexicaux", "/adjectif", "/adverbe", "/preposition", "/conjonction", "/determinant", "/complement", "/discours", "/registre", "/type_phrase", "/figure_style"]

            data = json.loads(request.body)
            user_input = data.get('user_input', '').strip()

            if utils.token_count(user_input) > 1500:
                return JsonResponse({'status': 'success', 'processed_input': 'Texte trop long!!<br>Veuillez donner un texte plus court.'})

            splited_user_input = user_input.split()

            if splited_user_input[0] not in code and utils.sim_find(splited_user_input[0], code):
                splited_user_input[0] = utils.sim_find(splited_user_input[0], code)

            if splited_user_input[0] in code and check == 0 and len(splited_user_input) == 1:
                output_res = "Pas de texte à traiter !!"

            if splited_user_input[0] in code:
                if splited_user_input[0] == "/menu":
                    output_res = resultat.menu()
                if splited_user_input[0] == "/texte" and len(splited_user_input) > 1:
                    check = 1
                    user_input = user_input.replace("/texte ", "")
                    corrected_text = correction.Correction(user_input)
                    if corrected_text is None:
                        output_res = "Votre texte n'est pas valide!!"
                    else:
                        if corrected_text != user_input:
                            output_res = "Votre texte après correction:<br>" + corrected_text + "<br><br>Votre texte est traité avec succès !!<br>Veuillez choisir une commande pour plus de détails.<br><br><br>"
                        else:
                            output_res = "Votre texte est traité avec succès !!<br>Veuillez choisir une commande pour plus de détails.<br><br><br>"
                        output_res += resultat.menu()
                        output_json = claude.get_results(corrected_text)
                elif splited_user_input[0] == "/bilan" and check == 1:
                    output_res = resultat.bilan(output_json)
                elif splited_user_input[0] == "/sujet" and check == 1:
                    output_res = resultat.sujet(output_json)
                elif splited_user_input[0] == "/verbe" and check == 1:
                    output_res = resultat.verbe(output_json)
                elif splited_user_input[0] == "/champs_lexicaux" and check == 1:
                    output_res = resultat.champs_lexicaux(output_json)
                elif splited_user_input[0] == "/adjectif" and check == 1:
                    output_res = resultat.adjectif(output_json)
                elif splited_user_input[0] == "/adverbe" and check == 1:
                    output_res = resultat.adverbe(output_json)
                elif splited_user_input[0] == "/preposition" and check == 1:
                    output_res = resultat.preposition(output_json)
                elif splited_user_input[0] == "/conjonction" and check == 1:
                    output_res = resultat.conjonction(output_json)
                elif splited_user_input[0] == "/determinant" and check == 1:
                    output_res = resultat.determinant(output_json)
                elif splited_user_input[0] == "/complement" and check == 1:
                    output_res = resultat.complement(output_json)
                elif splited_user_input[0] == "/discours" and check == 1:
                    output_res = resultat.discours(output_json)
                elif splited_user_input[0] == "/figure_style" and check == 1:
                    output_res = resultat.figure_style(output_json)
                elif splited_user_input[0] == "/registre" and check == 1:
                    output_res = resultat.registre(output_json)
                elif splited_user_input[0] == "/type_phrase" and check == 1:
                    output_res = resultat.type_phrase(output_json)
            else:
                output_res = "Commande invalide"

            if not user_input:
                return JsonResponse({'status': 'error', 'message': 'Input is empty'}, status=400)

            # Call the helper function for Groq API response
            output, error = get_groq_response(user_input)

            if error:
                # If there was an error, return the error message in the response
                return JsonResponse({'status': 'error', 'message': f"API error: {error}"}, status=500)

            # Return the processed input from Groq's API
            return JsonResponse({'status': 'success', 'processed_input': output_res})
            # return JsonResponse({'status': 'success', 'processed_input': output})

        except json.JSONDecodeError:
            # Handle JSON parsing errors gracefully
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # General exception handler for any other errors
            return JsonResponse({'status': 'error', 'message': f"Unexpected error: {str(e)}"}, status=500)

@csrf_exempt
def send_image(request):
    global check
    global output_json
    texte = "Impossible d'extraire le texte deuis cette image !!"
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image_data')

            if image_data:
                _, encoded = image_data.split(",", 1)

                img_data = base64.b64decode(encoded)
                image = Image.open(BytesIO(img_data))

                image_path = 'media/uploads/img.png'
                image.save(image_path)

                texte = ocr.perform_ocr(image_path)
                input_texte = texte
                texte = texte.replace('\n', '<br>')

                texte +=  "<br><br>Votre texte est traité avec succès !!<br>Veuillez choisir une commande pour plus de détails.<br><br><br>" + resultat.menu()
                output_json = claude.get_results(input_texte)

                check = 1

            return JsonResponse({'status': 'success', 'processed_input': texte})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur : {str(e)}'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})