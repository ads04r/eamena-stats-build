---
toc: false
---

# Errors in the Database

```js

const errors = await FileAttachment("data/errors.csv").csv();

const maindata_sel = view(Inputs.table(errors, {
	columns: ['eamena_id', 'grid_square', 'country', 'name', 'role', 'problems'],
	header: {'eamena_id': 'EAMENA ID', 'grid_square': 'Grid square', 'country': 'Country', 'name': 'Researcher name', 'role': 'Researcher role', 'problems': 'Issues'},
	format: {
                'eamena_id': (x) => htl.html`<strong><a href="https://database.eamena.org/report/${ errors.filter((d) => d.eamena_id === x)[0].arches_id }">${ x }</a></strong>`,
		'grid_square': (x) => htl.html`<strong>${ x }</strong> <a href="${ x }.html">Detail</a>`,
		'problems': (x) => htl.html`<small>${ JSON.parse(x).join(', ') }</small>`
	}
}));

```
