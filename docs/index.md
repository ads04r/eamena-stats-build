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

const maindata = Inputs.table(role_sel.filter((d) => d.year === year_sel).map((d) => d.countries).flat().filter((d) => d.sites.role_year > 0), {
	columns: ['label', 'sites', 'grids'],
	header: {'label': 'Country', 'sites': 'Sites uploaded/ammended', 'grids': 'Grid squares covered'},
	format: {
		'sites': (x) => htl.html`<strong>${ x.role_year }</strong>&nbsp;<a href="${ filename('sites', role_sel.filter((y) => y.year === year_sel).flat()[0], year_sel, '') }">View all</a>`,
		'grids': (x) => htl.html`<strong>${ x.role_year }</strong>&nbsp;<a href="${ filename('grids', role_sel.filter((y) => y.year === year_sel).flat()[0], year_sel, '') }">View all</a>`
	},
	sort: 'label'});

```

<div class="card"> ${ view(maindata) } </div>

<div class="card"> ${ maindata } </div>
