(function() {
    'use strict';
    console.log('hello');

    // Load JSON data
    const equipfile = document.getElementById('equipments');
    const propfile = document.getElementById('properties');
    function loadJSON(input) {
        let promise = new Promise(function(resolve, reject) {
            let reader = new FileReader();
            reader.readAsText(input.files[0]);
            reader.onload = (e) => resolve(JSON.parse(e.target.result));
            reader.onerror = (e) => reject(
                new Error('Error while loading the file'));
        });
        return promise;
    }

    // Load button
    const form = document.getElementById('data');
    form.onsubmit = function() {
        // application code
        let data = {};
        Promise.all([
            loadJSON(equipfile),
            loadJSON(propfile),
        ]).then((d) => {
            data.equipments = d[0];
            data.properties = d[1];
            console.log(data);
            main(data);
        });
        return false;
    };

    function main(data) {
        // Check the loaded JSON
        if (!validateEquipmentsJson(data.equipments)
            || !validatePropertiesJson(data.properties)) {
            console.log('Error: invalid JSON');
            return;
        }

        const itemlist = document.getElementById('itemlist');
        // Add header
        let title = document.createElement('h2');
        title.appendChild(document.createTextNode('一覧'));
        itemlist.appendChild(title);

        // Add filter input
        let filterInput = document.createElement('input');
        filterInput.type = 'text';
        filterInput.placeholder = 'Filter (e.g., 炎ダメージ)';
        itemlist.appendChild(filterInput);

        // Add table
        let table = document.createElement('table');

        // Add table header
        let thead = document.createElement('thead');
        let headerRow = document.createElement('tr');
        headerRow.appendChild(makeCell('アイテム名'));
        headerRow.appendChild(makeCell('レア'));
        for (let i=1; i<=6; i++) {
            headerRow.appendChild(makeCell('プロパティ'+i));
            //, {'colspan': '3'}));
            headerRow.appendChild(makeCell('最小'));
            headerRow.appendChild(makeCell('最大'));
        }
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Add table body
        let tableBody = document.createElement('tbody');
        for (let itemId in data.equipments) {
            let row = document.createElement('tr');
            const item = data.equipments[itemId];

            // Add item name cell
            row.appendChild(makeCell(item['equipment_name']));
            // Add rarity
            row.appendChild(makeCell(item['equipment_rarity']));
            // TODO カテゴリを表示したい
            // Add property data
            for (let i=1; i<=item['property_count']; i++) {
                let propId = item['equipment_property_id_' + i];
                let min_value = item['equipment_property_value_min_' + i];
                let max_value = item['equipment_property_value_max_' + i];
                if (min_value == 0) {
                    min_value = '';
                }
                if (max_value == 0) {
                    max_value = '';
                }
                let propname = findPropertyName(data.properties, propId);

                row.appendChild(makeCell(propname));
                row.appendChild(makeCell(min_value));
                row.appendChild(makeCell(max_value));
            }
            tableBody.appendChild(row);
        }
        table.appendChild(tableBody);
        itemlist.appendChild(table);

        // Add filter function
        TableFilter(table, filterInput);
    };

    // Data validation
    function validateEquipmentsJson(json) {
        if (!('id10100101' in json)) {
            return false;
        }
        return true;
    };
    function validatePropertiesJson(json) {
        if (!('id101' in json)) {
            return false;
        }
        return true;
    };

    // Helper
    function makeCell(text, attr={}) {
        let cell = document.createElement('td');
        for (let key in attr) {
            cell.setAttribute(key, attr[key]);
        }
        let node = document.createTextNode(text);
        cell.appendChild(node);
        return cell;
    }
    function findPropertyName(propJson, propId) {
        if (propId == 0) {
            return 'ランダムプロパティ';
        }
        else {
            return propJson['id' + propId]['equipment_property_name'];
        }
    }

    // Table filter
    // TODO: マッチしたセルを色つき表示
    // 行ごとにフィルタ
    function TableFilter(table, input) {
        input.oninput = function(e) {
            const filterValues = input.value.match(/\S+/g) || [];
            console.log('filter values:', filterValues);

            const tbodies = table.tBodies;
            for (let tbody of tbodies) {
                const rows = tbody.getElementsByTagName('tr');
                for (let tr of rows) {
                    if (filterRow(tr, filterValues)) {
                        // keep
                        tr.style.display = 'table-row';
                    }
                    else {
                        tr.style.display = 'none';
                    }
                }
            }
        };
    };
    function filterRow(row, filterValues) {
        // キーワードなしはフィルタなし
        if (!filterValues) {
            return true;
        }

        let found = new Set();
        for (let td of row.getElementsByTagName('td')) {
            let text = td.textContent || td.innerText;
            for (let value of filterValues) {
                if (text.indexOf(value) > -1) {
                    found.add(value);
                }
            }
        }
        if (found.size == filterValues.length) {
            // keep
            return true;
        }
        else {
            return false;
        }
    }
}());
