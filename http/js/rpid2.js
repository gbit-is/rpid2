const apiPort = 9000;  // or whatever your API runs on

async function list_sounds() {
    let apiPath = '/audio/list';
    let url = `http://${window.location.hostname}:${apiPort}${apiPath}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API error:', error);
    }

}

async function get_params() {
    let apiPath = '/config/list';
    let url = `http://${window.location.hostname}:${apiPort}${apiPath}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API error:', error);
    }
}


async function generate_controls(debug) {

    let data;

    if (debug) {
    	let raw_data = '{"audio.enabled":{"value":true,"type":"bool","http_type":"toggle","http_extra":null},"audio.volume.main":{"value":80,"type":"int","http_type":"slider","http_extra":"0-100"},"audio.volume.generated":{"value":53,"type":"int","http_type":"slider","http_extra":"0-100"},"audio.volume.manual":{"value":60,"type":"int","http_type":"slider","http_extra":"0-100"},"audio.loop.interval.low":{"value":11,"type":"int","http_type":"numsel","http_extra":"1-9999"},"audio.loop.interval.high":{"value":30,"type":"int","http_type":"numsel","http_extra":"1-9999"},"audio.loop.length.low":{"value":3,"type":"int","http_type":"numsel","http_extra":"1-9999"},"audio.loop.length.high":{"value":10,"type":"int","http_type":"numsel","http_extra":"10-999"},"audio.loop.enabled":{"value":true,"type":"bool","http_type":"toggle","http_extra":null}}'
	data = JSON.parse(raw_data)

    }
    else {
    	data = await get_params();
    }



    for (const [key, value] of Object.entries(data)) {
	if ( value["http_type"] == "toggle" ) {
		generate_toggle(key,value);
	}
	else if ( value["http_type"] == "slider" ) {
		generate_slider(key,value);

	}
	else if ( value["http_type"] == "numsel" ) {
		generate_number_input(key,value)

	}
    }

}



async function generate_soundboard(debug) {

	let data;

	if (debug) {
		raw_data = '{"base":["GENERATE","RANDOM","STOP"],"songs":["CANTINA","DUEL_FATES","EMPEROR","THEME"],"speak":["LEIA_MSG"],"sounds":["ALARM_1","ALARM_2","ALARM_3","ALARM_4","ANNOYED","BLEEP_1","BLEEP_2","BLEEP_3","CHORTLE","LONG_BLEEP_1","LONG_DOO","MISC_1","MISC_2","MISC_3","MISC_4","MISC_5","MISC_6","MISC_7","MISC_8","OOH_1","OOH_2","OOH_3","OOH_4","OOH_5","OOH_6","PATROL","SCREAM","SENT_1","SENT_10","SENT_11","SENT_12","SENT_13","SENT_14","SENT_15","SENT_16","SENT_17","SENT_18","SENT_19","SENT_2","SENT_3","SENT_4","SENT_5","SENT_6","SENT_7","SENT_8","SENT_9","SHORT-CIRCUIT","WHISTLE"]}'
		data = data = JSON.parse(raw_data)
	}
	else {
		data = await list_sounds();
	}

	console.log(data)	

	const buttonContainer = document.getElementById("button-container");

	for (const [key, value] of Object.entries(data)) {

		
		const category = document.createElement("div");

		let row_div = document.createElement("div")
		row_div.className = "row g-2"
		const title = document.createElement("span")
	
		title.textContent = key
		title.classList.add("title_text")
		category.appendChild(title)

		var br = document.createElement("br");
		category.appendChild(br)

		let col_count = 1;
		let col_max = 4;

		for ( const [ num, name ] of  Object.entries(value) ) {

			const col = document.createElement("div");
			//col.className = "col-6 col-sm-4 col-md-3"; 
			col.className = "col-sm-3"; 
			const btn = document.createElement("button");
			btn.className = "btn btn-primary w-100";
			btn.textContent = name;
			btn.id = name;
			btn.addEventListener("click", play_sound)
			col.appendChild(btn);
			//buttonContainer.appendChild(col);
			//category.appendChild(col);
			row_div.appendChild(col);
			col_count++;
			console.log(col_count)
			if ( col_count == col_max ){
				category.appendChild(row_div)
				row_div = document.createElement("div")
				row_div.className = "row g-2"
				col_count = 0
			}
		}
		category.appendChild(row_div)
		buttonContainer.appendChild(category)
		var br = document.createElement("br");
		buttonContainer.appendChild(br)
	}
}


function play_sound(event) {
	let sound_id = event.target.id
	let message = "play:" + sound_id
	send_mqtt("my/audio/server",message)

}

function send_mqtt(topic_raw,message) {


        let topic = topic_raw.trim().replace(/\//g, "_");
        let url = `http://${window.location.hostname}:${apiPort}/mqtt/post/${topic}`;
	
	value = message

	//return

        fetch(url, {
                method: "POST",
        body: message
        })
        .then(response => {
        if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
        }
                return response.json(); // or response.text() if you're not expecting JSON
        })
        .then(data => {
                console.log("Response received:", data);
        })
                .catch(error => {
        console.error("Error during fetch:", error);
        });


}



function update_value(parameter, value) {

	let param_url = parameter.trim().replace(/\./g, "/");
	let url = `http://${window.location.hostname}:${apiPort}/config/set/${param_url}`;
	
	fetch(url, {
  		method: "POST",
  		headers: {
    		"Content-Type": "application/json"
  	},
  	body: JSON.stringify({ value: value })
	})
	.then(response => {
  	if (!response.ok) {
    		throw new Error(`HTTP error! status: ${response.status}`);
  	}
  		return response.json(); // or response.text() if you're not expecting JSON
	})
	.then(data => {
  		console.log("Response received:", data);
	})
		.catch(error => {
  	console.error("Error during fetch:", error);
	});	


}

function click_toggle_switch(event) {

	toggle_id = event.target.id
	toggle_value = document.getElementById(toggle_id).checked
	update_value(toggle_id,toggle_value)

}

function change_numeric(event) {
	numeric_id = event.target.id
	numeric_value = event.target.value
	update_value(numeric_id,numeric_value)
}

function change_slider(event) {
        numeric_id = event.target.id
        numeric_value = event.target.value
        update_value(numeric_id,numeric_value)
	num_box = document.getElementById(numeric_id + "_num")	
	num_box.textContent = numeric_value

}

function generate_toggle(toggle_key,toggle_value) {


	const toggle_parent_div = document.getElementById("params_toggle");

	const toggle_div = document.createElement("div");
	
	const toggle_name_div =  document.createElement("div");
	toggle_name_div.style.display = "table-cell";
	
	//toggle_name_div.style.width = "10%";



	let toggle_name_span = document.createElement("span")
	toggle_name_span.textContent = toggle_key
	toggle_name_span.classList.add("title_text")

	const toggle_switch_div =  document.createElement("div");
        toggle_switch_div.style.display = "table-cell";
        toggle_switch_div.style.width = "10%";

	let toggle_label = document.createElement("label")
	toggle_label.className = "switch"

	let toggle_switch = document.createElement("input")
	toggle_switch.type = "checkbox"
	toggle_switch.checked = toggle_value["value"]
	toggle_switch.id = toggle_key
	toggle_switch.addEventListener("change", click_toggle_switch);

	let toggle_span =  document.createElement("span");
	toggle_span.className = "slider";
	
	

	toggle_name_div.appendChild(toggle_name_span);
	toggle_div.appendChild(toggle_name_div)

	toggle_label.appendChild(toggle_switch)
	toggle_label.appendChild(toggle_span)
	
	toggle_switch_div.appendChild(toggle_label)
	//toggle_switch_div.appendChild(toggle_switch)
	//toggle_switch_div.appendChild(toggle_span)

	toggle_div.appendChild(toggle_switch_div)
	toggle_parent_div.appendChild(toggle_div)
	
	

}


function generate_slider(slider_key,slider_value) {
	const slider_parent_div = document.getElementById("params_slider");

        const slider_row = document.createElement("div");

        const slider_name_div =  document.createElement("div");
	const slider_name_span = document.createElement("span");

	const slider_number_div =  document.createElement("div");
	const slider_number_span = document.createElement("span");


	slider_name_div.style.display = "table-cell";
        slider_name_div.style.width = "10%";
	slider_name_span.textContent = slider_key;
	slider_name_span.classList.add("title_text")

        slider_number_div.style.display = "table-cell";
        slider_number_div.style.width = "10%";
        slider_number_span.textContent = slider_value["value"]
	slider_number_span.id = slider_key + "_num";
	slider_number_span.classList.add("title_text")

	var slider_div = document.createElement("div");
	slider_div.style.display = "table-cell";
        slider_div.style.width = "90%";
	var slider = document.createElement("input");


	let [min_val, max_val] = slider_value["http_extra"].split("-").map(Number);


	slider.id = slider_key;
        slider.type = "range";
        slider.min = min_val;
        slider.max = max_val;
        slider.value = slider_value["value"];
        slider.classList.add("sslider");
        slider.step = 1;

	//slider.addEventListener('change',change_numeric)
	slider.addEventListener('change',change_slider)

	slider_name_div.display = "table-row";

	slider_name_div.appendChild(slider_name_span)
	slider_div.appendChild(slider)

	slider_row.appendChild(slider_name_div)
	slider_row.appendChild(slider_div)
	
	slider_number_div.appendChild(slider_number_span)
	slider_row.appendChild(slider_number_div)

	slider_parent_div.appendChild(slider_row)

}

function generate_number_input(input_key, input_value) {
    const parent = document.getElementById("params_slider");

    // Row container
    const row = document.createElement("div");
    row.style.display = "table-row";

    // Name cell
    const nameCell = document.createElement("div");
    nameCell.style.display = "table-cell";
    nameCell.style.width = "10%";

    const nameSpan = document.createElement("span");
    nameSpan.textContent = input_key;
    nameSpan.classList.add("title_text")
    nameCell.appendChild(nameSpan);

    // Control cell
    const controlCell = document.createElement("div");
    controlCell.style.display = "table-cell";
    controlCell.style.width = "90%";
    controlCell.style.display = "flex";
    controlCell.style.alignItems = "center";
    controlCell.style.gap = "5px";

    // Create - button
    const minusBtn = document.createElement("button");
    minusBtn.textContent = "−";
    minusBtn.classList.add("num_but")

    // Create input field
    const inputField = document.createElement("input");
    inputField.type = "number";
    inputField.id = input_key;
    inputField.value = input_value["value"];
    inputField.step = 1;
    inputField.min = 1; // Just ensure > 0
    inputField.classList.add("number_input_class");
    inputField.style.width = "60px";

    // Create + button
    const plusBtn = document.createElement("button");
    plusBtn.textContent = "+";
    plusBtn.classList.add("num_but")

    // Event listeners
    minusBtn.addEventListener("click", () => {
        let val = parseInt(inputField.value, 10) || 1;
        if (val > 1) {
            inputField.value = val - 1;
            inputField.dispatchEvent(new Event("change"));
        }
    });

    plusBtn.addEventListener("click", () => {
        let val = parseInt(inputField.value, 10) || 1;
        inputField.value = val + 1;
        inputField.dispatchEvent(new Event("change"));
    });

    inputField.addEventListener("change", change_numeric);

    // Append
    controlCell.appendChild(minusBtn);
    controlCell.appendChild(inputField);
    controlCell.appendChild(plusBtn);

    row.appendChild(nameCell);
    row.appendChild(controlCell);
    parent.appendChild(row);
}

const params = new URLSearchParams(window.location.search);
const debug = params.has("debug");

if (debug) {
	document.addEventListener("DOMContentLoaded", async () => {

	generate_controls(debug)
	generate_soundboard(debug)

	});
}
else {
	generate_controls(debug)
	generate_soundboard(debug)
}
