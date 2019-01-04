function mapRaw(raw, html_anchor){
    html_anchor.innerHTML += "<div>" + raw + "</div><br>";
}

/**
 * Very inefficient, as we keep trying to find the properties
 **/
function mapJson(obj, html_anchor, path = []){

    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            if(isPrimitive(obj[key])){

                if(isNaN(obj[key])){
                    if(sensitive){
                        // Cancel graph
                    } else {
                        // Skip value
                    }
                }

                //path.push(key);
                let var_path = "";
                let var_id = "";
                for(let p in path){
                    var_path += "["+path[p]+"]";

                    if(var_id.length > 0) var_id += ",";
                    var_id += path[p]
                }
                //console.log(var_path + " = " + obj[key]);
                let html_id = var_id;
                if(html_id.length > 0){
                    html_id += ",";
                }
                html_id += key;


                let html_entry = var_path + "<button id='" + html_id + "' onclick=setupChart('" + html_id + "') >" + key + " (" + obj[key] + ")" + "</button><br>";

                html_anchor.innerHTML += "<span class='app_entry'>" + html_entry + "</span>";
            } else {
                let new_path = path.slice();
                new_path.push(key);
                mapJson(obj[key], html_anchor, new_path);
            }
        }
    }
}

function refresh() {
    let container = document.getElementById("entries_container");
    container.innerHTML = "";

    let selection = document.querySelector('input[name="data_representation"]:checked').value;

    switch (selection) {
        case "JSON":
            for(let entry in entries){
                try{
                    mapJson(JSON.parse(entries[entry]), container);
                } catch (e) {
                    console.log("Unable to parse json:" + entries[entry])
                }
            }
            break;
        case "RAW":
            for(let entry in entries){
                mapRaw(entries[entry], container);
            }
    }
}


function setupChart(varPath){

    // entries data

    window.onresize = function (){
        setupChart(varPath);
    };
    let svgWidth = window.innerWidth;
    let svgHeight = 300;

    // Remove existing
    let svg_cont = document.getElementById("graph_container");
    // Add new
    if(svg_cont.firstChild) { svg_cont.removeChild(svg_cont.firstChild); }

    let new_svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    //new_svg.className = ""
    svg_cont.appendChild(new_svg);

    let svg = d3.select('svg')
    //.attr("width", svgWidth)
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .attr("class", "bar-chart");

    //let dataset = [80, 100, 56, 120, 180, 30, 40, 120, 160];
    let pathEntries = varPath.split(",");
    let vals = getObjVals(pathEntries, entries);
    let dataset = scaleData(svgHeight, vals);

    let barPadding = 5;
    let barWidth = (svgWidth / dataset.length);

    document.getElementById("meta_data").innerText = "Max val: " + Math.max(...vals) + ", Min val: " + Math.min(...vals);

    svg.selectAll("rect")
        .data(dataset)
        .enter()
        .append("rect")
        .attr("y", function(d) {
            return svgHeight - d
        })
        .attr("height", function(d) {
            return d;
        })
        .attr("width", barWidth - barPadding)
        .attr("transform", function (d, i) {
             let translate = [barWidth * i, 0];
             return "translate("+ translate +")";
        });
}

/*
function saveAppState(name_app, name_prop, path, onComplete){
    // TODO THIS: Copy paste from: https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/send
    let xhr = new XMLHttpRequest();
    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.open("POST", '/server', true);

    xhr.onreadystatechange = function() {//Call a function when the state changes.
        if(this.readyState == XMLHttpRequest.DONE) {
            // Request finished. Do processing here.
            onComplete(this.status);
        }
    };

    xhr.send("app=" + name_app + "&prop=" + name_prop + "&path=" + path);
}
*/