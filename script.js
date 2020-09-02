//CHART
var currency_dict = {
	"BTC": "Bitcoin",
	"ETH": "Etherum",
	"BCH": "Bitcoin Cash"
}

function UserAction() {
	var days = document.getElementById("chartForm").value;
	var currency = document.getElementById("currency").value;
	fetch('https://min-api.cryptocompare.com/data/histoday?fsym='+currency+'&tsym=USD&limit='+days)
		.then(function (response) {
			return response.text();
		})
		.then(function (text) {
			//console.log(text)
			let series = csvToSeries(text);
			renderChart(series);
		})
		.catch(function (error) {
			//Something went wrong
			console.log(error);
		});

	function csvToSeries(text) {
		const lifeExp = 'average_life_expectancy';
		//let dataAsJson = JSC.csv2Json(text);
		let high = [], low = [];
		data = JSON.parse(text)["Data"];
		for (i = 0; i < data.length; i++) {
			
			let timeVar = new Date(data[i].time * 1000);
			//console.log(typeof timeVar.getMonth());
			let month = timeVar.getMonth() + 1
			let day = timeVar.getDate()
			let fullYear = timeVar.getFullYear()
			timeVar = day + "/" + month + "/" + fullYear;
			high.push({x: timeVar, y: data[i].high});
			low.push({x: timeVar, y: data[i].low});
		}
		return [
			{name: 'High', points: high},
			{name: 'Low', points: low},
		];
	}

	function renderChart(series) {
		JSC.Chart('chartDiv', {
			title_label_text: 'Daily '+currency_dict[currency]+' prices',
			annotations: [{
				label_text: 'Source: Cryptocompare',
				position: 'bottom left'
			}],
			legend_visible: false,
			xAxis_crosshair_enabled: true,
			defaultSeries_firstPoint_label_text: '<b>%seriesName</b>',
			defaultPoint_tooltip: '%seriesName <b>%yValue</b> years',
			series: series
		});
	}
}
