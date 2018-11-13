/**
 * Good idea! https://stackoverflow.com/a/31538091
 * @param test
 * @returns {boolean}
 */
function isPrimitive(test) {
    return (test !== Object(test));
}

 /**
 * Takes the variable path to property and retrieves the value from that path of every object in the dataArr
 * @param varPath
 * @param dataArr
 */
function getObjVals(varPath, dataArr){
    let attrEntries = [];

    let eval_path = "";
    for(let i in varPath){
        eval_path += '[\'' + varPath[i] + '\']';
    }

    for(let i in dataArr){
        let entry = JSON.parse(dataArr[i]);

        let data = eval("entry"+eval_path);

        if(data != null){
            attrEntries.push(data);
        } else {
            console.log("null data found");
        }
    }
    return attrEntries;
}

function scaleData(graph_height, data){
    let max = Math.max(...data);

    return data.map(val => graph_height / max * val )
}