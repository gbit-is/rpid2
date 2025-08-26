  //let output = document.getElementById("output");
//let steamdeck_icon_img = document.getElementById("steamdeck_icon")

//const apiPort = 9000;  // or whatever your API runs on

function send_gamepad(data){
    let apiPath = '/drive';
    let url = `http://${window.location.hostname}:${apiPort}${apiPath}`;
        fetch(url, {
                method: "POST",
        	body: data
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


 let prevState = {};

    function gameLoop() {
      let gamepads = navigator.getGamepads();

      if (gamepads[0]) {
        let gp = gamepads[0];



	change_occured = false;
	var key_dict = {};
	var buttons = {}
	var axis_dict = { }
        gp.buttons.forEach((btn, i) => {
          let pressed = btn.pressed;
	  buttons[i] = pressed;
          if (prevState[`b${i}`] !== pressed) {
	    change_occured = true;
            prevState[`b${i}`] = pressed;
          }
        });
	key_dict["buttons"] = buttons;

        // --- Axes (sticks) ---
        gp.axes.forEach((axis, i) => {
          let value = axis.toFixed(2);
	  //console.log(axis,i)	 
	  axis_dict[i] = value;
          if (prevState[`a${i}`] !== value) {
	    change_occured = true;
            prevState[`a${i}`] = value;
	    //console.log(value, i )
          }
        });
	key_dict["axis"] = axis_dict;
	if (change_occured) {
		dict_json = JSON.stringify(key_dict);
		//console.log(dict_json)
		console.log(key_dict)
		send_gamepad(dict_json)
	}
	
      }

      requestAnimationFrame(gameLoop);
    }

    window.addEventListener("gamepadconnected", (e) => {
      console.log("Gamepad connected:", e.gamepad);
      let steamdeck_icon_img = document.getElementById("steamdeck_icon")
      steamdeck_icon_img.src="/img/steamdeck_green.svg"
      requestAnimationFrame(gameLoop);
      
    });

    window.addEventListener("gamepaddisconnected", (e) => {
      let steamdeck_icon_img = document.getElementById("steamdeck_icon")
      steamdeck_icon_img.src="/img/steamdeck_red.svg"
      console.log("Gamepad disconnected:", e.gamepad);
    });

    
