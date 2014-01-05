ko.bindingHandlers.elctrl = {
	init: function(element, valueAccessor, allBindings, viewModel, bindingContext){
        
        var stateValue = bindingContext.$data.state();
        if(stateValue === 1)
        {
			$(element).children("input").attr("checked", "");
        }
        $(element).children("input").change(bindingContext.$data.click);
        $(element).trigger("create");
        
       
	}
};

var sensor = function(data)
{
	var self = this;
	self.name = ko.observable(data.Name);
	self.temperature = ko.observable(data.Data[0].Temperature);
	self.humidity = ko.observable(data.Data[0].Humidity);
	self.time = ko.observable(data.Data[0].Time);
	self.value = ko.computed(function(){return self.name() + " " + self.temperature() + "C " + self.humidity() + "%";});
}	

var powerSwitch = function(id, data)
{
	var self = this;
	self.name = ko.observable(data.Name);
	self.state = ko.observable(data.State);
	self.id = ko.observable(id);
	self.value = ko.computed(function(){return self.name() + ": " + self.state();}, self);
	self.toggleState = ko.computed(function(){return self.state() === 0 ? 1 : 0;}, self);
	
	self.click = function(e){
		$.ajax({
			url: "/switches/" + self.id() + "/state",
			type: "POST",
			data: JSON.stringify({"state": self.toggleState()}),
			contentType: "application/json",
			success: function(data){console.log(data); self.state(data.State);}
		})
	};
}

var elctrlModelView = function()
{
	var self = this;
	
	self.sensors = ko.observableArray();
    self.switches = ko.observableArray();
   
    $.getJSON(
		"/switches",
		function(resp)
		{
			$.each(resp, function(key, value){
				console.log(value.Name);
				self.switches.push(new powerSwitch(key, value));
			});
		}
	);
    
	$.getJSON(
		"/sensors", 
		function(resp) 
		{				
			$.each(resp, function(key, value){
				self.sensors.push(new sensor(value));
			});
		} 
	);
	
	
}

ko.applyBindings(new elctrlModelView());
