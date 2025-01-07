table_css = f"""<style>
                    table {{
                        border-collapse: collapse;
                        width: auto;
                        margin: 10px auto;
                        float: left;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #f4f4f4;
                        font-weight: bold;
                    }}
                    h1 {{
                        margin-top: -7px;
                    }}
                </style>"""

def menu():
    global table_css
    output_res = f"""<h1>Tableau des commandes</h1>
                    <table>
                        <thead>
                            <tr><th>Commande</th> <th>Fonction</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>/menu</td>                          <td>Afficher le menu</td></tr>
                            <tr><td>/texte votre texte</td>             <td>Ajouter le texte à traiter</td></tr>
                            <tr><td>/verbe</td>                         <td>Afficher les informations sur les verbes</td></tr>
                            <tr><td>/sujet</td>                         <td>Afficher les informations sur les sujets</td></tr>
                            <tr><td>/champs_lexicaux</td>               <td>Afficher les informations sur les champs lexicaux</td></tr>
                            <tr><td>/adjectif</td>                      <td>Afficher les informations sur les adjectifs</td></tr>
                            <tr><td>/adverbe</td>                       <td>Afficher les informations sur les adverbes</td></tr>
                            <tr><td>/preposition</td>                   <td>Afficher les informations sur les prépositions</td></tr>
                            <tr><td>/conjonction</td>                   <td>Afficher les informations sur les conjonctions de coordinations</td></tr>
                            <tr><td>/determinant</td>                   <td>Afficher les informations sur les determinants</td></tr>
                            <tr><td>/complement</td>                    <td>Afficher les informations sur les compléments</td></tr>
                            <tr><td>/discours</td>                      <td>Afficher les informations sur les discours</td></tr>
                            <tr><td>/registre</td>                      <td>Afficher les informations sur les registres linguistiques</td></tr>
                            <tr><td>/type_phrase</td>                   <td>Afficher les informations sur les types de phrase</td></tr>
                            <tr><td>/figure_style</td>                  <td>Afficher les informations sur les figures de style</td></tr>
                        </tbody>
                    </table>
                    """
    return output_res + table_css

def bilan(output_json):
    global table_css
    output_res = f"""<h1>Tableau du bilan</h1>
                    <table>
                        <thead>
                            <tr><th>Type</th> <th>Total</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Sujets</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Sujets", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Verbes</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Verbes", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Champs Lexicaux</td>
                                <td>{len(output_json.get("output", {}).get("Grammaire", {}).get("Champs Lexicaux", [])) if "Champs Lexicaux" in output_json.get("output", {}).get("Grammaire", {}) else "Introuvable"}</td>
                            </tr>
                            <tr><td>Adjectifs</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Adjectifs", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Adverbes</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Adverbes", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Prépositions</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Prépositions", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Conjonctions de coordination</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Conjonctions de coordination", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Déterminants</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Déterminants", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Compléments</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Compléments", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Types de discours</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Types de discours", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Figures de style</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Figures de style", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Registres linguistiques</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Registres linguistiques", {}).get("Total", "Introuvable")}</td>
                            </tr>
                            <tr><td>Type de phrases</td>
                                <td>{output_json.get("output", {}).get("Grammaire", {}).get("Type de phrases", {}).get("Total", "Introuvable")}</td>
                            </tr>
                        </tbody>
                    </table>
                    """

    return output_res + table_css

def sujet(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Sujets", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Sujets"]["Details"]
        output_res_sujt = ""
        for key, value in details.items():
            output_res_sujt += f"<tr><td>{key}</td><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des sujets</h1>
                        <table>
                            <thead>
                                <tr><th>Sujet</th> <th>Nombre d'occurrence</th></tr>
                            </thead>
                            <tbody>
                                {output_res_sujt}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de sujet!"

def verbe(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Verbes", {}).get("Par Temps"):
        global table_css
        details = output_json["output"]["Grammaire"]["Verbes"]["Par Temps"]
        output_res_vrb = ""
        for key, value in details.items():
            for i in range(value["Total"]):
                if i == 0:
                    output_res_vrb += f"""<tr><td rowspan=\"{value["Total"]}\"><b>{key}</b></td>
                                                                    <td>{value["Verbes"][i]["Forme Conjuguee"]}</td><td>{value["Verbes"][i]["Infinitif"]}</td><td>{value["Verbes"][i]["Voix"]}</td></tr>"""
                else:
                    output_res_vrb += f"<tr><td>{value["Verbes"][i]["Forme Conjuguee"]}</td><td>{value["Verbes"][i]["Infinitif"]}</td><td>{value["Verbes"][i]["Voix"]}</td></tr>"

        output_res = f"""<h1>Tableau des verbes</h1>
                        <table>
                            <thead>
                                <tr><th>Temps</th> <th>Forme Conjuguée</th> <th>Infinitif</th> <th>Voix</th></tr>
                            </thead>
                            <tbody>
                                {output_res_vrb}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    return "Ce texte ne contient pas de verbe!"

def champs_lexicaux(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Champs Lexicaux"):
        global table_css
        details = output_json["output"]["Grammaire"]["Champs Lexicaux"]
        output_res_chmlx = ""
        for key, value in details.items():
            for i in range(value["Total"]):
                if i == 0:
                    output_res_chmlx += f"<tr><td rowspan=\"{value["Total"]}\"><b>{key}</b></td><td>{value["Details"][i]}</td></tr>"
                else:
                    output_res_chmlx += f"<tr><td>{value["Details"][i]}</td></tr>"

        output_res = f"""<h1>Tableau des champs lexicaux</h1>
                        <table>
                            <thead>
                                <tr><th>Nom du Champs Lexical</th> <th>Vocabulaires</th></tr>
                            </thead>
                            <tbody>
                                {output_res_chmlx}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de champs lexicaux!"

def adjectif(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Adjectifs", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Adjectifs"]["Details"]
        output_res_adj = ""
        for value in details:
            output_res_adj += f"<tr><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des adjectifs</h1>
                        <table>
                            <thead>
                                <tr><th>Adjectifs</th></tr>
                            </thead>
                            <tbody>
                                {output_res_adj}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas d'adjectif!"

def adverbe(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Adverbes", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Adverbes"]["Details"]
        output_res_adv = ""
        for value in details:
            output_res_adv += f"<tr><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des adverbes</h1>
                        <table>
                                <thead>
                                    <tr><th>Adverbes</th></tr>
                                </thead>
                                <tbody>
                                    {output_res_adv}
                                </tbody>
                            </table>
                            """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas d'adverbe!"

def preposition(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Prépositions", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Prépositions"]["Details"]
        output_res_prepo = ""
        for key, value in details.items():
            output_res_prepo += f"<tr><td>{key}</td><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des prépositions</h1>
                        <table>
                            <thead>
                                <tr><th>Préposition</th> <th>Nombre d'occurrence</th></tr>
                            </thead>
                            <tbody>
                                {output_res_prepo}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de préposition!"

def conjonction(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Conjonctions de coordination", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Conjonctions de coordination"]["Details"]
        output_res_conj_coor = ""
        for key, value in details.items():
            output_res_conj_coor += f"<tr><td>{key}</td><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des conjonction de coordination</h1>
                        <table>
                            <thead>
                                <tr><th>Conjonctions de coordination"</th> <th>Nombre d'occurrence</th></tr>
                            </thead>
                            <tbody>
                                {output_res_conj_coor}
                            </tbody>
                        </table>
                            """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de conjonctions de coordination!"

def determinant(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Déterminants", {}).get("Par type"):
        global table_css
        details = output_json["output"]["Grammaire"]["Déterminants"]["Par type"]
        output_res_det = ""
        for key, value in details.items():
            i = 0
            for k, v in value["Details"].items():
                if i == 0:
                    output_res_det += f"""<tr><td rowspan=\"{len(value["Details"])}\"><b>{key}</b></td>
                                                                <td>{k}</td><td>{v}</td></tr>"""
                    i = 1
                else:
                    output_res_det += f"<tr><td>{k}</td><td>{v}</td></tr>"

        output_res = f"""<h1>Tableau des déterminants</h1>
                        <table>
                            <thead>
                                <tr><th>Type de Déterminant</th> <th>Déterminant</th> <th>Nombre d'occurrence</th></tr>
                            </thead>
                            <tbody>
                                {output_res_det}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de déterminant!"

def complement(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Compléments", {}).get("Par type"):
        global table_css
        details = output_json["output"]["Grammaire"]["Compléments"]["Par type"]
        output_res_comp = ""
        for key, value in details.items():
            for i in range(value["Total"]):
                if i == 0:
                    output_res_comp += f"<tr><td rowspan=\"{value["Total"]}\"><b>{key}</b></td><td>{value["Details"][i]}</td></tr>"
                else:
                    output_res_comp += f"<tr><td>{value["Details"][i]}</td></tr>"

        output_res = f"""<h1>Tableau des compléments</h1>
                        <table>
                            <thead>
                                <tr><th>Type de Complément</th> <th>Complément</th></tr>
                            </thead>
                            <tbody>
                                {output_res_comp}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de complément!"

def discours(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Types de discours", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Types de discours"]["Details"]
        output_res_dsc = ""
        for value in details:
            output_res_dsc += f"<tr><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des discours</h1>
                        <table>
                            <thead>
                                <tr><th>Types de discours</th></tr>
                            </thead>
                            <tbody>
                                {output_res_dsc}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de discours!"

def figure_style(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Figures de style", {}).get("Par type"):
        global table_css
        details = output_json["output"]["Grammaire"]["Figures de style"]["Par type"]
        output_res_fig_sty = ""
        for key, value in details.items():
            for i in range(value["Total"]):
                if i == 0:
                    output_res_fig_sty += f"<tr><td rowspan=\"{value["Total"]}\"><b>{key}</b></td><td>{value["Details"][i]}</td></tr>"
                else:
                    output_res_fig_sty += f"<tr><td>{value["Details"][i]}</td></tr>"

        output_res = f"""<h1>Tableau des figures de style</h1>
                        <table>
                            <thead>
                                <tr><th>Figure de style</th> <th>Phrase</th></tr>
                            </thead>
                            <tbody>
                                {output_res_fig_sty}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de figure de style!"

def registre(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Registres linguistiques", {}).get("Details"):
        global table_css
        details = output_json["output"]["Grammaire"]["Registres linguistiques"]["Details"]
        output_res_reg_ling = ""
        for value in details:
            output_res_reg_ling += f"<tr><td>{value}</td></tr>"

        output_res = f"""<h1>Tableau des registres linguistiques</h1>
                        <table>
                            <thead>
                                <tr><th>Registres linguistiques</th></tr>
                            </thead>
                            <tbody>
                                {output_res_reg_ling}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de registre linguistique!"

def type_phrase(output_json):
    if output_json.get("output", {}).get("Grammaire", {}).get("Type de phrases"):
        global table_css
        details = output_json["output"]["Grammaire"]["Type de phrases"]
        output_res_tp_phr = ""
        for key, value in details.items():
            if key != "Total":
                i = 0
                for k, v in value.items():
                    if i == 0:
                        i = 1
                        if key != "Par complexité":
                            output_res_tp_phr += f"<tr><td rowspan=\"{len(value.items())}\"><b>{key}</b></td><td>{k}</td><td colspan=\"2\">{v["Total"]}</td></tr>"
                        else:
                            t = len(value.items())
                            for k_, v_ in value.items():
                                if k_ == "Phrases complexes":
                                    t = len(value.items()) + len(v_["Details"]) - 1
                            output_res_tp_phr += f"<tr><td rowspan=\"{t}\"><b>{key}</b></td><td>{k}</td><td colspan=\"2\">{v["Total"]}</td></tr>"
                    else:
                        if k != "Phrases complexes":
                            output_res_tp_phr += f"<tr><td>{k}</td><td colspan=\"2\">{v["Total"]}</td></tr>"
                        else:
                            j = 0
                            for ky, val in v["Details"].items():
                                if j == 0:
                                    j = 1
                                    output_res_tp_phr += f"<tr><td rowspan=\"{len(v["Details"])}\">{k}</td><td>{ky}</td><td>{val}</td></tr>"
                                else:
                                    output_res_tp_phr += f"<tr><td>{ky}</td><td>{val}</td></tr>"

        output_res = f"""<h1>Tableau des types de phrase</h1>
                        <table>
                            <thead>
                                <tr><th>Type de Phrase</th> <th>Phrase</th> <th colspan=\"2\">Nombre d'occurrence</th></tr>
                            </thead>
                            <tbody>
                                {output_res_tp_phr}
                            </tbody>
                        </table>
                        """
        return output_res + table_css
    else:
        return "Ce texte ne contient pas de type de phrase!"