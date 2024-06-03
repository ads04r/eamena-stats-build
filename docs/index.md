---
toc: false
---

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

.nocheckbox td:nth-child(1), .nocheckbox th:nth-child(1) {
  display: none;
}
.nocheckbox td:nth-child(2), .nocheckbox th:nth-child(2) {
  padding-left: 0px;
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>

<div class="hero">
  <h1>EAMENA Stats</h1>
  <h2>Statistics on the data quality and completeness of the EAMENA database.</h2>
</div>

  <div class="card">${
    resize((width) => Plot.plot({
	label: "Overall record count",
	marginLeft: 250,
	marginRight: 30,
	width: width,
	x: { axis: null },
	y: { axis: null },
	marks: [
		Plot.barX(roles, {
			x: "records",
			y: "label",
			color: { legend: false },
			fill: "label",
			sort: { y: "x", reverse: true, limit: 10 }
		}),
		Plot.text(roles, {
			text: d => `${Math.floor(d.records / 1000)} K`,
			x: "records",
			y: "label",
			textAnchor: "start",
			dx: 3,
			fill: "white"
		}),
		Plot.text(roles, {
			text: d => d.label,
			textAnchor: "end",
			x: 0,
			y: "label",
			dx: -3,
			fill: "white"
		})
	]
    }))
  }</div>

```js

const years = await FileAttachment("data/years.json").json();
const roles = await FileAttachment("data/combine.json").json();
const countries = await FileAttachment("data/countries.json").json();
const grid_data = FileAttachment("data/grid_data.json").json();
const role_sel = view(
	Inputs.select(roles, {
		label: "Role",
		format: (i) => i.label,
		valueof: (i) => i.reports
	})
);
const year_sel = view(
	Inputs.select(years, {
		label: "Year"
	})
);

```

<div class="grid grid-cols-3">
  <div class="card">
	<p> Total sites </p>
	<h2> ${ role_sel.filter((d) => d.year === year_sel).flat()[0].role_year_total } </h2>
  </div>
  <div class="card">
	<p> Total grid squares </p>
	<h2> ${ role_sel.filter((d) => d.year === year_sel).flat()[0].grid_role_year } </h2>
  </div>
  <div class="card">
	<p> Bulk uploads </p>
	<h2> ${ role_sel.filter((d) => d.year === year_sel).flat()[0].role_year_bulk } </h2>
  </div>
</div>

```js

function filename(type, role, year, row)
{
	return role['role']['id'] + '_' + type + '_' + year + '.html';
}

function selected_grids(table)
{
	var id = '';
	var data = {}
	var ret = []

	for(var i = 0; i < table.length; i++)
	{
		id = table[i].id;
		var temp_data = role_sel.filter((d) => d.year === year_sel)[0]['country_role_year'][id]['grids'];
 		for(var j = 0; j < temp_data.length; j++)
		{
			var grid = temp_data[j];
			if(!(grid in data)) { data[grid] = {'label': grid, 'countries': []}; }
			data[grid]['countries'].push(countries[id]);
		}
	}
	for(var key in data) { ret.push(data[key]); }
	return ret;
}

function selected_sites(table)
{
	var ret = []

	var id = role_sel.filter((d) => d.year === year_sel);
	var role_id = id[0].role.id;
	var year = id[0].year;
	for(var i = 0; i < table.length; i++)
	{
		for (var j = 0; j < grid_data[table[i]['label']].length; j++)
		{
			var item = grid_data[table[i]['label']][j];
			var id = item['ID'];
			var label = item['Label'];
			var role = item['Role'];
			console.log(role);
			
//			if(role.id == role_id)
//			{
//				ret.push(item);
//			}
		}
	}
	return ret
}

const maindata_sel = view(Inputs.table(role_sel.filter((d) => d.year === year_sel).map((d) => d.countries).flat().filter((d) => d.sites.role_year > 0), {
	columns: ['label', 'sites', 'grids'],
	header: {'label': 'Country', 'sites': 'Sites uploaded/ammended', 'grids': 'Grid squares covered'},
	format: {
		'sites': (x) => htl.html`<strong>${ x.role_year }</strong>&nbsp;<a href="${ filename('sites', role_sel.filter((y) => y.year === year_sel).flat()[0], year_sel, '') }"></a>`,
		'grids': (x) => htl.html`<strong>${ x.role_year }</strong>&nbsp;<a href="${ filename('grids', role_sel.filter((y) => y.year === year_sel).flat()[0], year_sel, '') }"></a>`
	},
	sort: 'label'}));

```
<div class="grid grid-cols-2">
<div class="card">

```js

const grid_sel = view(Inputs.table(selected_grids(maindata_sel), {
	columns: ['label', 'countries'],
	header: {'label': 'Grid square', 'countries': 'Country / Countries'},
	format: {
		'label': (x) => htl.html`<strong>${ x }</strong>`,
	},
  }));

```

</div>
<div class="card">

```js

const site_sel = view(Inputs.table(selected_sites(grid_sel), {
	columns: ['Label', 'Date', 'ID'],
	header: {'Label': 'EAMENA ID', 'ID': ''},
	format: {
		'ID': (x) => htl.html`<a href="https://database.eamena.org/report/${ x }">EAMENA Link</a>`,
	},
  }));

```

</div>
</div>
