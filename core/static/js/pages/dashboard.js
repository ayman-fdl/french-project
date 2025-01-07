const COLORS = {
	primary: '#435ebe',
	secondary: '#00ab57',
	accent: '#ff4560',
	orange: '#fd7e14',
	scrollbarThumb: '#4f46e5',
	lightGreen: '#28a745',
	yellow: '#ffc107',
	teal: '#20c997',
	pink: '#e83e8c'
	// background: '#f2f7ff',
};

// Function to generate a list of colors dynamically
const generateColors = (numColors) => {
	const colorValues = Object.values(COLORS);
	const colors = [];
	for (let i = 0; i < numColors; i++) {
		colors.push(colorValues[i % colorValues.length]);
	}
	return colors;
};

let jsonData = null;

const createPlotContainer = (id, colClass) => {
	const container = document.createElement('div');
	container.className = colClass;
	const plotDiv = document.createElement('div');
	plotDiv.id = id;
	container.appendChild(plotDiv);
	return container;
};

document.addEventListener("DOMContentLoaded", async () => {
	try {
		const response = await fetch('/api/result/');
		const jsonData = await response.json();

		const components = ["Sujets", "Verbes", "Adjectifs", "Adverbes", "Prépositions", "Conjonctions", "Déterminants", "Compléments"];
		const componentsTotals = components.map(component => {
			if (component === "Conjonctions") {
				return jsonData.output.Grammaire["Conjonctions de coordination"]?.Total || 0;
			}
			return jsonData.output.Grammaire[component]?.Total || 0;
		});
		if (componentsTotals.some(total => total > 0)) {
			renderCompsBarPlot(components, componentsTotals);
		}

		const grammairePlotsContainer = document.getElementById('grammairePlotsContainer');

		const sujets = jsonData.output.Grammaire.Sujets?.Details;
		if (sujets) {
			const sujetKeys = Object.keys(sujets);
			const sujetValues = Object.values(sujets);
			const container = createPlotContainer('sujetBar', 'col-md-4');
			grammairePlotsContainer.appendChild(container);
			renderSujetBarPlot(sujetKeys, sujetValues);
			console.log(sujetKeys);
		}

		const complements = jsonData.output.Grammaire.Compléments?.["Par type"];
		if (complements) {
			const complementKeys = Object.keys(complements);
			const complementTotals = complementKeys.map(complement => complements[complement].Total);
			const container = createPlotContainer('complementDonut', 'col-md-4');
			grammairePlotsContainer.appendChild(container);
			renderComplementDonutChart(complementKeys, complementTotals);
		}

		const prepositions = jsonData.output.Grammaire['Prépositions']?.Details;
		if (prepositions) {
			const prepositionKeys = Object.keys(prepositions);
			const prepositionValues = Object.values(prepositions);
			const container = createPlotContainer('prepositionBar', 'col-md-4');
			grammairePlotsContainer.appendChild(container);
			renderPrepositionBarPlot(prepositionKeys, prepositionValues);
		}

		const conjunctions = jsonData.output.Grammaire["Conjonctions de coordination"]?.Details;
		if (conjunctions) {
			const conjunctionKeys = Object.keys(conjunctions);
			const conjunctionValues = Object.values(conjunctions);
			const container = createPlotContainer('conjonctionBar', 'col-md-4');
			grammairePlotsContainer.appendChild(container);
			renderConjonctionBarPlot(conjunctionKeys, conjunctionValues);
		}

		const determiners = jsonData.output.Grammaire.Déterminants?.["Par type"];
		if (determiners) {
			const container = createPlotContainer('determinantTreemap', 'col-md-4');
			grammairePlotsContainer.appendChild(container);
			renderDeterminantTreemap(determiners);
		}

		const verbes_temps = jsonData.output.Grammaire.Verbes?.["Par Temps"];
		if (verbes_temps) {
			renderVerbTensePieChart(verbes_temps);
		}

		const verbes_modes = jsonData.output.Grammaire.Verbes?.["Par mode"];
		if (verbes_modes) {
			renderVerbModeBarChart(verbes_modes);
		}

		const phrasesPlotsContainer = document.getElementById('phrasesPlots');
		let plotCount = 0;

		const phraseTypesForme = jsonData.output.Grammaire["Type de phrases"]?.["Par forme"];
		if (phraseTypesForme) {
			plotCount++;
		}

		const phraseTypesStructure = jsonData.output.Grammaire["Type de phrases"]?.["Par structure"];
		if (phraseTypesStructure) {
			plotCount++;
		}

		const phraseTypesComplexite = jsonData.output.Grammaire["Type de phrases"]?.["Par complexité"];
		if (phraseTypesComplexite) {
			plotCount++;
		}

		const colClass = plotCount === 1 ? 'col-12' : plotCount === 2 ? 'col-md-6' : 'col-md-4';

		if (phraseTypesForme) {
			const container = createPlotContainer('phraseTypeFormeBar', colClass);
			phrasesPlotsContainer.appendChild(container);
			renderPhraseTypeBarChart(phraseTypesForme, 'phraseTypeFormeBar', 'Répartition des Types de Phrases (Par forme)');
		}

		if (phraseTypesStructure) {
			const container = createPlotContainer('phraseTypeStructureDonut', colClass);
			phrasesPlotsContainer.appendChild(container);
			renderPhraseTypeDonutChart(phraseTypesStructure, 'phraseTypeStructureDonut', 'Répartition des Types de Phrases (Par structure)');
		}

		if (phraseTypesComplexite) {
			const container = createPlotContainer('phraseTypeComplexitePie', colClass);
			phrasesPlotsContainer.appendChild(container);
			renderPhraseTypeComplexitePieChart(phraseTypesComplexite);
		}

		const typesDeDiscours = jsonData.output.Grammaire["Types de discours"]?.Details;
		if (typesDeDiscours) {
			renderTypesDeDiscours(typesDeDiscours);
		}

		const registresLinguistiques = jsonData.output.Grammaire["Registres linguistiques"]?.Details;
		if (registresLinguistiques) {
			renderRegistresLinguistiques(registresLinguistiques);
		}

		const figuresDeStyle = jsonData.output.Grammaire["Figures de style"]?.["Par type"];
		if (figuresDeStyle) {
			renderFiguresDeStyleDonutChart(figuresDeStyle);
		}

		let lexicalCategories = jsonData.output.Grammaire["Champs Lexicaux"];

		// Nettoyage si nécessaire
		if (typeof lexicalCategories !== "object" || lexicalCategories === null) {
		  console.error("Les champs lexicaux ne sont pas un objet standard !");
		} else {
		  lexicalCategories = Object.assign({}, lexicalCategories);
		}

		// Extraire les catégories et totaux
		const lexicalKeys = Object.keys(lexicalCategories).map(key => key.trim());
		const lexicalTotals = lexicalKeys.map(category => {
		  const total = lexicalCategories[category]?.Total;
		  return typeof total === "number" ? total : 0;
		});

		// Rendu du graphique
		renderLexicalFieldBarChart(lexicalKeys, lexicalTotals);



		//console.log(lexicalCategories, verbes_temps, verbes_modes, phraseTypesForme, phraseTypesStructure, phraseTypesComplexite, typesDeDiscours, registresLinguistiques, figuresDeStyle);

	} catch (error) {
		console.error('Erreur lors du chargement des données JSON:', error);
	}
});

const renderCompsBarPlot = (components, componentsTotals) => {
	const filteredComponents = components.map((component, index) => ({ component, total: componentsTotals[index] }))
		.filter(item => item.total > 0)
		.sort((a, b) => b.total - a.total);

	const options = {
		chart: { type: 'bar', height: 300 },
		series: [{ name: 'Les Composants', data: filteredComponents.map(item => item.total) }],
		// colors: '#435ebe',
		colors: [COLORS.primary],
		xaxis: { categories: filteredComponents.map(item => item.component) },
		dataLabels: { enabled: true },
		annotations: { position: 'back' },
		fill: { opacity: 1 }
	};
	new ApexCharts(document.getElementById("chart-analyse-composants"), options).render();
};

const renderSujetBarPlot = (sujets, occurrences) => {
	const sortedSujets = sujets.map((sujet, index) => ({ sujet, total: occurrences[index] }))
		.sort((a, b) => b.total - a.total);

	const options = {
		chart: { type: 'bar', height: 300 },
		series: [{ name: 'Sujet', data: sortedSujets.map(item => item.total) }],
		colors: [COLORS.primary],
		xaxis: { categories: sortedSujets.map(item => item.sujet) },
		dataLabels: { enabled: true },
		annotations: { position: 'back' },
		fill: { opacity: 1 },
		title: { text: 'Occurrences des sujets' },
		legend: { position: 'bottom' }
	};
	new ApexCharts(document.getElementById("sujetBar"), options).render();
};

const renderPrepositionBarPlot = (prepositions, occurrences) => {
	const sortedPrepositions = prepositions.map((preposition, index) => ({ preposition, total: occurrences[index] }))
		.sort((a, b) => b.total - a.total);

	const options = {
		chart: { type: 'bar', height: 300 },
		series: [{ name: 'Preposition', data: sortedPrepositions.map(item => item.total) }],
		colors: [COLORS.primary],
		xaxis: { categories: sortedPrepositions.map(item => item.preposition) },
		yaxis: { labels: { formatter: function (val) { return Math.floor(val) } } },
		dataLabels: { enabled: true },
		annotations: { position: 'back' },
		fill: { opacity: 1 },
		title: { text: 'Occurrences des Prepositions' },
		legend: { position: 'bottom' }
	};
	new ApexCharts(document.getElementById("prepositionBar"), options).render();
};

const renderConjonctionBarPlot = (conjonctions, occurrences) => {
	const sortedConjunctions = conjonctions.map((conjunction, index) => ({ conjunction, total: occurrences[index] }))
		.sort((a, b) => b.total - a.total);

	const options = {
		chart: { type: 'bar', height: 300 },
		series: [{ name: 'Conjonction', data: sortedConjunctions.map(item => item.total) }],
		colors: [COLORS.primary],
		xaxis: { categories: sortedConjunctions.map(item => item.conjunction) },
		yaxis: { labels: { formatter: function (val) { return Math.floor(val) } } },
		dataLabels: { enabled: true },
		annotations: { position: 'back' },
		fill: { opacity: 1 },
		title: { text: 'Occurrences des Conjonctions' },
		legend: { position: 'bottom' }
	};
	new ApexCharts(document.getElementById("conjonctionBar"), options).render();
};

const renderComplementDonutChart = (complements, occurrences) => {
	const options = {
		chart: { type: 'donut', height: 300 },
		series: occurrences,
		labels: complements,
		colors: generateColors(complements.length),
		title: { text: 'Répartition des compléments', align: 'center' },
		legend: { position: 'bottom' }
	};
	new ApexCharts(document.getElementById("complementDonut"), options).render();
};

const renderDeterminantTreemap = (determiners) => {
	const labels = ["Les Déterminants"];
	const parents = [""];
	const values = [0]; // Initial value for the main parent node
	const texts = ["Total: 0"];

	for (const type in determiners) {
		if (determiners.hasOwnProperty(type)) {
			const typeData = determiners[type];
			labels.push(type);
			parents.push("Les Déterminants");
			values.push(typeData.Total);
			texts.push(`Total: ${typeData.Total}`);

			for (const detail in typeData.Details) {
				if (typeData.Details.hasOwnProperty(detail)) {
					labels.push(detail);
					parents.push(type);
					values.push(typeData.Details[detail]);
					texts.push(`Count: ${typeData.Details[detail]}`);
				}
			}
		}
	}

	const data = [{
		type: "treemap",
		labels: labels,
		parents: parents,
		values: values,
		textinfo: "label+text",
		hoverinfo: "label+text",
		text: texts,
		hovertext: texts,
		outsidetextfont: { size: 20, color: COLORS.primary },
		pathbar: { visible: true }
	}];

	const layout = {
		title: "Répartition des Déterminants",
		margin: { t: 35, l: 10, r: 10, b: 10 },
		treemapcolorway: generateColors(labels.length),
		autosize: true, // Ensure the plot takes up the full size of its container
		font: {
			family: 'Nunito, sans-serif',
			size: 14,
			color: '#333'
		},
		plot_bgcolor: 'transparent'
	};

	Plotly.newPlot('determinantTreemap', data, layout);
};

const renderVerbTensePieChart = (verbes_temps) => {
	const tenses = Object.keys(verbes_temps);
	const occurrences = tenses.map(tense => verbes_temps[tense].Total);
	const options = {
		chart: { type: 'pie', height: 300 },
		series: occurrences,
		labels: tenses,
		colors: generateColors(tenses.length),
		legend: { position: 'bottom' },
		responsive: [{ breakpoint: 600, options: { chart: { height: 250 } } }],
		title: { text: 'Répartition des Temps de Verbes' }
	};
	new ApexCharts(document.getElementById("verbTensePie"), options).render();
};

const renderVerbModeBarChart = (verbes_modes) => {
	const modes = Object.keys(verbes_modes);
	const occurrences = modes.map(mode => verbes_modes[mode].Total)
	const sortedModes = modes.map((mode, index) => ({ mode, total: occurrences[index] }))
		.sort((a, b) => b.total - a.total);

	const options = {
		chart: { type: 'bar', height: 300 },
		series: [{ name: 'Modes de Verbes', data: sortedModes.map(item => item.total) }],
		colors: [COLORS.primary],
		xaxis: { categories: sortedModes.map(item => item.mode), position: 'back' },
		yaxis: { labels: { formatter: function (val) { return Math.floor(val) } } },
		fill: { opacity: 1 },
		title: { text: 'Occurrences des Modes de Verbes' }
	};
	new ApexCharts(document.getElementById("verbModeBar"), options).render();
};

const renderPhraseTypeBarChart = (phraseTypes) => {
	const types = Object.keys(phraseTypes);
	const occurrences = types.map(type => phraseTypes[type].Total);

	const sortedTypes = types.map((type, index) => ({ type, total: occurrences[index] }))
		.sort((a, b) => b.total - a.total);

	const options = {
		chart: { type: 'bar', height: 300 },
		series: [{ name: 'Occurrences', data: sortedTypes.map(item => item.total) }],
		colors: generateColors(types.length),
		xaxis: { categories: sortedTypes.map(item => item.type), position: 'back' },
		yaxis: { labels: { formatter: function (val) { return Math.floor(val) } } },
		title: { text: "Par Forme" }
	};
	new ApexCharts(document.getElementById("phraseTypeFormeBar"), options).render();
};

const renderPhraseTypeDonutChart = (phraseTypes) => {
	const types = Object.keys(phraseTypes);
	const occurrences = types.map(type => phraseTypes[type].Total);

	const options = {
		chart: { type: 'donut', height: 300 },
		series: occurrences,
		labels: types,
		colors: generateColors(types.length),
		legend: { position: 'bottom' },
		title: { text: "Par Structure" }
	};
	new ApexCharts(document.getElementById("phraseTypeStructureDonut"), options).render();
};

const renderPhraseTypeComplexitePieChart = (phraseTypes) => {
	const types = Object.keys(phraseTypes);
	const occurrences = types.map(type => phraseTypes[type].Total);

	const options = {
		chart: { type: 'pie', height: 300 },
		series: occurrences,
		labels: types,
		colors: generateColors(types.length),
		legend: { position: 'bottom' },
		title: { text: "Par complexité" }
	};
	new ApexCharts(document.getElementById("phraseTypeComplexitePie"), options).render();
};

const renderFiguresDeStyleDonutChart = (figuresDeStyle) => {
	const types = Object.keys(figuresDeStyle);
	const occurrences = types.map(type => figuresDeStyle[type].Total);

	const options = {
		chart: { type: 'donut', height: 300 },
		series: occurrences,
		labels: types,
		colors: generateColors(types.length),
		title: { text: "Répartition des Figures de Style" }
	};
	new ApexCharts(document.getElementById("figuresDeStyleDonut"), options).render();
};

const renderLexicalFieldBarChart = (categories, totals) => {
  const options = {
    chart: { type: 'bar', height: 350 },
    series: [{ name: 'Total des Champs Lexicaux', data: totals }],
    colors: [COLORS.primary], // Couleur personnalisée
    xaxis: {
      categories: categories, // Les totaux sur l'axe horizontal (en mode horizontal)
      position: 'bottom'
    },
    yaxis: {
      categories: categories, // Les noms des catégories sur l'axe vertical
      labels: { formatter: function (val) { return val; } }
    },
    title: { text: 'Total des Champs Lexicaux', align: 'center' },
    plotOptions: {
      bar: {
        horizontal: true,
        borderRadius: 5
      }
    },
    responsive: [{ breakpoint: 600, options: { chart: { height: 250 } } }]
  };

  // Sélection de l'élément et rendu
  const chartElement = document.querySelector("#lexicalBarChart");
  if (!chartElement) {
    console.error("Élément DOM avec l'ID 'lexicalBarChart' introuvable !");
    return;
  }
  new ApexCharts(chartElement, options).render();
};


const renderTypesDeDiscours = (typesDeDiscours) => {
	const listElement = document.getElementById("typesDeDiscoursList");
	typesDeDiscours.forEach(discours => {
		const listItem = document.createElement("li");
		listItem.textContent = discours;
		listElement.appendChild(listItem);
	});
};

const renderRegistresLinguistiques = (registresLinguistiques) => {
	const listElement = document.getElementById("registresLinguistiquesList");
	registresLinguistiques.forEach(registre => {
		const listItem = document.createElement("li");
		listItem.textContent = registre;
		listElement.appendChild(listItem);
	});
};

