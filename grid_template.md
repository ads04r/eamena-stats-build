---
toc: false
---
# %%%

```js

const grid_data = await FileAttachment("data/grids/%%%.json").json();

function summarise_tiles(item)
{
	console.log(item);

	var intret = {};
	var ret = [];
	for(var i=0; i < item.length; i++)
	{
		for(var j=0; j < item[i].Tiles.length; j++)
		{
			const kv = item[i].Tiles[j];
			const k = kv[0];
			const v = parseInt(kv[1]);
			if(!(k in intret)) { intret[k] = 0; }
			intret[k] = intret[k] + v;
		}
	}
	console.log(intret);
	for (const [key, value] of Object.entries(intret))
	{
		ret.push({'label': key, 'records': value})
	}
	return ret;
}

function summarise_damage(item)
{
	console.log(item);

	var intret = {};
	var ret = [];
	for(var i=0; i < item.length; i++)
	{
		for(var j=0; j < item[i].Disturbances.length; j++)
		{
			const k = item[i].Disturbances[j];
			const v = 1;
			if(!(k in intret)) { intret[k] = 0; }
			intret[k] = intret[k] + v;
		}
	}
	console.log(intret);
	for (const [key, value] of Object.entries(intret))
	{
		ret.push({'label': key, 'records': value})
	}
	return ret;
}

function role_expand(role)
{
	if(role.constructor.name == "Array")
	{
		var ret = Array();
		for(var i = 0; i < role.length; i++)
		{
			ret.push(role[i].label);
		}
		return ret.join(', ');
	}
	return role.label;
}

const site_sel = view(Inputs.table(grid_data['sites'], {
        columns: ['Label', 'Role', 'Date', 'Tiles', 'ID'],
        header: {'Label': 'EAMENA ID', 'Date': 'Assessment Date(s)', 'Tiles': 'Assessments', 'ID': ''},
        format: {
                'ID': (x) => htl.html`<a href="https://database.eamena.org/report/${ x }">EAMENA Link</a>`,
                'Role': (x) => htl.html`${ role_expand(x) }`,
		'Tiles': (x) => htl.html`${ x.length }`,
        },
  }));

```
  <h2>Grid Completeness</h2>

  <div class="card">${
    resize((width) => Plot.plot({
        label: "Resource Instance Components",
        marginLeft: 250,
        marginRight: 30,
        width: width,
        x: { axis: null },
        y: { axis: null },
        marks: [
                Plot.barX(summarise_tiles(site_sel), {
                        x: "records",
                        y: "label",
                        color: { legend: false },
                        fill: "label"
                }),
                Plot.text(summarise_tiles(site_sel), {
                        text: d => `${ d.records }`,
                        x: "records",
                        y: "label",
                        textAnchor: "start",
                        dx: 3,
                        fill: "white"
                }),
                Plot.text(summarise_tiles(site_sel), {
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

  <h2>Disturbance Causes</h2>

  <div class="card">${
    resize((width) => Plot.plot({
        label: "Disturbance Causes",
        marginLeft: 250,
        marginRight: 30,
        width: width,
        x: { axis: null },
        y: { axis: null },
        marks: [
                Plot.barX(summarise_damage(site_sel), {
                        x: "records",
                        y: "label",
                        color: { legend: false },
                        fill: "label"
                }),
                Plot.text(summarise_damage(site_sel), {
                        text: d => `${ d.records }`,
                        x: "records",
                        y: "label",
                        textAnchor: "start",
                        dx: 3,
                        fill: "white"
                }),
                Plot.text(summarise_damage(site_sel), {
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
