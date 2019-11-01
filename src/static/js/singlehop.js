//loading
function loading(){
    $("#loading").show();
    $(".form-section").hide();
}

//find available edges based on input class (e.g. gene) and output class
function findEdges(input_cls, output_cls) {
    var promise = $.ajax({
        type:"GET",
        url: "http://localhost:8855/api/v1/find_edge",
        data: {input_cls: input_cls, output_cls: output_cls},
        datatype: "json"
        });
    return promise;
};

//Retrieve edges and populate them as options in select
function populateEdges(input_cls, output_cls) {
    if (input_cls) {
        findEdges(input_cls=input_cls, output_cls=null).done(function(jsonResponse){
            $("#edge1").empty();
            $('#edge1').multipleSelect('enable');
            var edges = jsonResponse.edges;
            edges.forEach(function(_edge) {
                $("#edge1").append(new Option(_edge, _edge))
            });
            $('select').multipleSelect({
                enable: true,
                multiple: true,
                width: 475,
                multipleWidth: 400,
                dropWidth: 475
            });
        });
    } else if (output_cls) {
        findEdges(input_cls=output_cls, output_cls=null).done(function(jsonResponse){
            $("#edge2").empty();
            $('#edge2').multipleSelect('enable');
            var edges = jsonResponse.edges;
            edges.forEach(function(_edge) {
                $("#edge2").append(new Option(_edge, _edge))
            });
            $('select').multipleSelect({
                enable: true,
                multiple: true,
                width: 475,
                multipleWidth: 400,
                dropWidth: 475
            });
        });
    }

};

$(document).ready(function(){
    var options = {
        url: function(phrase) {
            return "http://localhost:8855/api/v1/hint?q=" + phrase;
        },

        template: {
            type: "description",
            fields: {
                description: "display"
            }
        },
        placeholder: "Type your input here!",

        getValue: "display",

        list: {
            maxNumberOfElements: 20,
            onClickEvent: function() {
                var value = $("#autocomplete-input").getSelectedItemData();
                $("#input_cls").val(value.primary.cls);
                $("#input_id").val(value.primary.identifier);
                $("#input_val").val(value.primary.value);
                populateEdges(input_cls=value.type,output_cls=null);
            }
        },

        categories: [
            {   //Category fruits
                listLocation: "Gene",
                header: "-- GENES --",
                getValue: "symbol"

            }, 
            {   //Category vegetables
                listLocation: "DiseaseOrPhenotypicFeature",
                header: "-- DISEASE --",
                getValue: "mondo"
            },
            {   //Category vegetables
                listLocation: "SequenceVariant",
                header: "-- VARIANT --",
                getValue: "hgvs"
            },
            {   //Category vegetables
                listLocation: "ChemicalSubstance",
                header: "-- CHEMICAL --",
                getValue: "name"
            }
        ]

    };
    // initiate the input autocomplete box
    $("#autocomplete-input").easyAutocomplete(options);
    options['placeholder'] = "Type your output here";
    options['list']['onClickEvent'] = function() {
        var value = $("#autocomplete-output").getSelectedItemData();
        $("#output_cls").val(value.primary.cls);
        $("#output_id").val(value.primary.identifier);
        $("#output_val").val(value.primary.value);
        populateEdges(input_cls=null, output_cls=value.type);
    };
    // initiate the output autocomplete box
    $("#autocomplete-output").easyAutocomplete(options);
    $('#edge1').change(function() {
        $("#edge1_label").val($('#edge1').multipleSelect('getSelects', 'text'));
    });
    $('#edge2').change(function() {
        $("#edge2_label").val($('#edge2').multipleSelect('getSelects', 'text'));
    });
    $('select').multipleSelect({
        enable: true,
        multiple: true,
        width: 470,
        multipleWidth: 400,
        dropWidth: 470
    });
});