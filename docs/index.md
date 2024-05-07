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

function role_values(data)
{
	var ret = [];
	for(let k in data)
	{
		ret.push(data[k]);
	}
	return ret;
}

const roles = role_values(await FileAttachment("data/roles.json").json());
const role_sel = view(
	Inputs.select(roles, {
		label: "Roles",
		format: (i) => i.label,
		valueof: (i) => i.reports
	})
);
```

