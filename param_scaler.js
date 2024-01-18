// Scale a list of normalised values (0. 1.) to a desired range
// Right inlet a scale map: <index number (1-based)> <new min> <new max>. It is possible to scale multiple values at once
// Left inlet incoming list to be scaled

inlets = 2;
outlets = 1;

setinletassist(1, "list of values to be scaled: index, new min, new max");
setinletassist(0, "params' list");

setoutletassist(0, "params' list scaled");


var scaleMap = [];
var paramValues = [];

function scaleValue(value, oldMin, oldMax, newMin, newMax) {
	var scaledValue = ((value - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin;
	//post("Scaling value: " + value + " to: " + scaledValue + "\n");
	return scaledValue
}


function scaleArray(paramValues, scaleMap) {
	var scaleObject = {};
	
	for (var i = 0; i < scaleMap.length; i += 3) {
		var index = scaleMap[i] - 1;
		var new_min = scaleMap[i + 1];
		var new_max = scaleMap[i + 2];
		scaleObject[index] = { min_: new_min, max_: new_max };
	}
	
	for (var i = 0; i < paramValues.length; i++) {
		if (scaleObject.hasOwnProperty(i)) {
			var value = paramValues[i];
			var scale = scaleObject[i];
			paramValues[i] = scaleValue(value, 0.0, 1.0, scale.min_, scale.max_);
		}
	}
	outlet(0, paramValues);
	scaleMap.length = paramValues.length = 0;
}


function list() {
	if(inlet==1) scaleMap = arrayfromargs(arguments);
	if(inlet==0) paramValues = arrayfromargs(arguments);
	
	if(scaleMap && scaleMap.length > 0 && scaleMap.length % 3 === 0 && paramValues && paramValues.length > 0) {
		scaleArray(paramValues, scaleMap);
	} else {
		outlet(0, paramValues);
		paramValues.length = 0;
	}
}